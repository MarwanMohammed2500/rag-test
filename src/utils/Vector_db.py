import os
import logging
import asyncio
from typing import List
from dotenv import load_dotenv
from langchain.schema import Document
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load environment variables
_ = load_dotenv(override=True)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def create_index(index_name: str='non-profit-rag', vect_length: int = 768):
    """
    Creates a Pinecone index with the specified name and vector length.

    Args:
        index_name (str): The name of the index to create. Defaults to 'non-profit-rag'.
        vect_length (int): The length of the vectors in the index. Defaults to 768.

    Returns:
        None
    """
    pinecone = Pinecone(api_key=os.getenv('PINECONE_API_KEY', ""))  
    if index_name not in [index["name"] for index in pinecone.list_indexes()]:
        logger.info(f'Creating Index: {index_name}')
        pinecone.create_index(
            name=index_name,
            dimension=vect_length,
            metric='cosine',
            spec=ServerlessSpec(cloud='aws', region='us-east-1')
        )
        logger.info(f'Done Creating Index: {index_name}')

def add_documents_to_pinecone(index_name: str='non-profit-rag', vect_length: int=768, 
                              documents: List[Document]=None):
    """
    Adds a list of documents to a Pinecone index. If the index does not exist, it is created first.

    Args:
        index_name (str): The name of the index to add the documents to. Defaults to 'non-profit-rag'.
        vect_length (int): The length of the vectors in the index. Defaults to 768.
        documents (List[Document], optional): The list of documents to add to the index. Defaults to None.

    Returns:
        None
    """
    try:
        if not documents:
            logger.warning("⚠️ No valid documents found for processing.")
            return
        
        # Ensure an event loop exists in Streamlit's ScriptRunner thread
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            asyncio.set_event_loop(asyncio.new_event_loop())
        
        embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001",
                                                       google_api_key=os.getenv('GOOGLE_API_KEY', ""))
        
        # embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=os.getenv('OPENAI_API_KEY'))
        
        pinecone = Pinecone(api_key=os.getenv('PINECONE_API_KEY', ""))
        
        if index_name not in [index_info["name"] for index_info in pinecone.list_indexes()]:
            logger.warning(f"⚠️ Index '{index_name}' does not exist. Create the index first.")
            
            ## If you using Gemini
            create_index(index_name=index_name, vect_length=vect_length)
            logger.info("✅ Successfully created the index in Pinecone.")
            
            ## If you using OpenAI
            # create_index(index_name=index_name, vect_length=1536)
            # logger.info("✅ Successfully created the index in Pinecone.")

        vector_store = PineconeVectorStore(
            index_name=index_name,
            embedding=embedding_model,
            pinecone_api_key=os.getenv('PINECONE_API_KEY', "")
        )
        vector_store.add_documents(documents=documents)
        logger.info("✅ Successfully added new documents to Pinecone.")
    except Exception as e:
        logger.error("❌ An error occurred while adding new documents to Pinecone.", exc_info=True)
