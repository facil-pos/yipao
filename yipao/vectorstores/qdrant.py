from qdrant_client import QdrantClient

class QdrantDB:
    """
    Class for interacting with Qdrant, a vector store designed for handling and querying embedded documents.


    """
    def __init__(self, cfg: str, api_key: str=None, embedding_model: str="sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initializes the Qdrant client based on configuration.

        Args:
            cfg (str): Can be ":memory:", "/path/to/db" or "http://host:port".
            api_key (str): The API key for the Qdrant client (default is None).

        Raises:
            TypeError: If cfg is not a string.
        """
        self.client = QdrantClient(cfg, api_key=api_key)
        self.client.set_model(embedding_model)
        print(f"Qdrant client initialized with Embedding-Model: {embedding_model}")

    
    def initialize(self, name_collection: str):
        """
        Initializes the Qdrant client.
        """   
        if not self.client.collection_exists(name_collection):
            self.client.create_collection(
                collection_name=name_collection,
                vectors_config = self.client.get_fastembed_vector_params()
            )
            

    def reset(self):
        """
        Resets the database client, clearing all stored data and configurations.
        """
        raise NotImplementedError("Reset is not supported in Qdrant.")


    def add_ddl(self, ddl: str, name_collection):
        """
        Adds a DDL statement to the Qdrant collection.

        Args:
            ddl (str): The DDL statement to be added.

        Returns:
            None but prints the UUID of the added DDL document.
        """
        id = self.client.add(
            collection_name=name_collection,
            documents=[ddl]
        )
        print(f"Added DDL to Qdrant with ID: {id[0]}")


    def add_ddls(self, ddls: list, name_collection: str):
        """
        Adds multiple DDL statements to the ChromaDB collection.

        Args:
            ddls (list of str): A list of DDL statements to be added.

        Returns:
            None
        """
        for ddl in ddls:
            self.add_ddl(ddl, name_collection)


    def check_documents(self, collection_name: str):
        """
        Checks if exist documents in a given collection.
        
        Args:
            collection_name (str): The name of the collection to check.

        Returns:
            bool: True if there are documents in the collection, False otherwise.
        """
        if not self.client.collection_exists(collection_name):
            raise ValueError(f"Collection {collection_name} does not exist.")
        return True if self.client.count(collection_name).count > 0 else False
    

    def query(self, collection_name:str, query_text: str, n_results: int):
        """
        Queries the Qdrant collection with the given query texts.

        Args:
            query_texts (list of str): A list of query texts.
            n_results (int): The number of results to return.

        Returns:
            List of dictionaries, each containing the ID and score of a result.
        """
        collection_name = collection_name if collection_name else self.name_collection
        results =  self.client.query(
            collection_name=collection_name,
            query_text=query_text,
            limit=n_results
        )

        return [ [doc.document] for doc in results ]