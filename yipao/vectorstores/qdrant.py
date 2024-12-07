from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from typing import List, Optional
import openai
import os

class QdrantDB:
    """
    Class for interacting with Qdrant using OpenAI embeddings.
    """
    def __init__(
        self, 
        connection_str: str, 
        api_key: Optional[str] = None, 
        collection_name: str = 'ddl',
        embedding_model: str = "text-embedding-3-small"
    ):
        """
        Initialize the Qdrant client with OpenAI embeddings.

        Args:
            connection_str (str): Can be ":memory:", "/path/to/db" or "http://host:port"
            api_key (str, optional): The API key for Qdrant
            collection_name (str): Name of the collection to use
            embedding_model (str): OpenAI embedding model to use
        """
        self.client = QdrantClient(connection_str, api_key=api_key)
        self.collection_name = collection_name
        self.embedding_model = embedding_model
        
        # Initialize OpenAI client
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.openai_client = openai.Client(api_key=openai_api_key)
        
        self.initialize_collection()

    def initialize_collection(self):
        """Initialize the Qdrant collection if it doesn't exist."""
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=1536,  # Dimension for text-embedding-3-small
                    distance=Distance.COSINE
                )
            )
            print(f"Created new collection: {self.collection_name}")

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Get OpenAI embeddings for a list of texts.
        
        Args:
            texts (List[str]): List of texts to embed
            
        Returns:
            List[List[float]]: List of embedding vectors
        """
        if not texts:
            return []
        
        print(f"Getting embeddings for {texts}")
            
        result = self.openai_client.embeddings.create(
            input=texts,
            model=self.embedding_model
        )
        
        print(f"Embeddings retrieved: {result}")
        
        return [data.embedding for data in result.data]

    def add_ddl(self, ddl: str) -> int:
        """
        Add a single DDL statement to the collection.
        
        Args:
            ddl (str): The DDL statement to add
            
        Returns:
            int: ID of the added point
        """
        embeddings = self.get_embeddings([ddl])
        if not embeddings:
            raise ValueError("Failed to generate embedding for DDL")
            
        point = PointStruct(
            id=self.client.count(self.collection_name).count,  # Auto-increment ID
            vector=embeddings[0],
            payload={"text": ddl}
        )
        
        operation_info = self.client.upsert(
            collection_name=self.collection_name,
            points=[point]
        )
        
        if operation_info.status != "completed":
            raise RuntimeError(f"Failed to add DDL: {operation_info.status}")
            
        return point.id

    def add_ddls(self, ddls: List[str], collection_name: str | None = None) -> List[int]:
        """
        Add multiple DDL statements to the collection.
        
        Args:
            ddls (List[str]): List of DDL statements to add
            
        Returns:
            List[int]: List of added point IDs
        """
        if collection_name is None:
            collection_name = self.collection_name
        
        embeddings = self.get_embeddings(ddls)
        print(f"Embeddings generated: {embeddings}")
        if not embeddings:
            raise ValueError("Failed to generate embeddings for DDLs")
            
        start_id = self.client.count(self.collection_name).count
        points = [
            PointStruct(
                id=start_id + idx,
                vector=embedding,
                payload={"text": ddl}
            )
            for idx, (embedding, ddl) in enumerate(zip(embeddings, ddls))
        ]
        
        operation_info = self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        
        if operation_info.status != "completed":
            raise RuntimeError(f"Failed to add DDLs: {operation_info.status}")
            
        return [point.id for point in points]

    def query(self, query_text: str, n_results: int = 5, collection_name: str | None = None) -> List[dict]:
        """
        Query the collection using semantic search.
        
        Args:
            query_text (str): Text to search for
            n_results (int): Number of results to return
            
        Returns:
            List[dict]: List of results with payload and score
        """
        if collection_name is None:
            collection_name = self.collection_name
        
        embeddings = self.get_embeddings([query_text])
        if not embeddings:
            raise ValueError("Failed to generate embedding for query")
            
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=embeddings[0],
            limit=n_results
        )
        
        return [result.payload["text"] for result in results]

    def check_documents(self, collection_name: str | None = None) -> bool:
        """
        Check if the collection has any documents.
        
        Returns:
            bool: True if collection has documents, False otherwise
        """
        
        if collection_name is None:
            collection_name = self.collection_name
        
        return self.client.count(self.collection_name).count > 0