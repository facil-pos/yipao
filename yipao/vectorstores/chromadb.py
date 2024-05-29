import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import uuid
from typing import Dict 

class ChromaDB:
    """
    Class for interacting with ChromaDB, a database designed for handling and querying embedded documents.

    Attributes:
        client (PersistentClient or HttpClient): The database client for interacting with ChromaDB.
        ddl_collection (Collection): A collection for DDL (Data Definition Language) statements.
    """

    def __init__(self, cfg: Dict[str, int], **settings):
        """
        Initializes the ChromaDB client based on configuration.

        Args:
            cfg (Dict[str, int] or str): If string, it represents the file path to the database;
                                         if dictionary, it specifies configuration settings for HTTP connection.
            settings (dict): Additional settings for the ChromaDB client, passed to the Settings object.

        Raises:
            TypeError: If cfg is neither a dict nor a string.
        """
        if isinstance(cfg, str):
            self.client = chromadb.PersistentClient(path=cfg, settings=Settings(**settings))
        elif isinstance(cfg, Dict):
            self.client = chromadb.HttpClient(**cfg, settings=Settings(**settings))
        else:
            raise TypeError("Configuration must be either a path (str) or settings (dict).")

        #self.reset()
        embedding_function = embedding_functions.DefaultEmbeddingFunction()  # TODO: add custom embedding function
        self.ddl_collection = self.client.get_or_create_collection(name="ddl", embedding_function=embedding_function)


    def reset(self):
        """
        Resets the database client, clearing all stored data and configurations.
        """
        self.client.reset()


    def add_ddl(self, ddl: str):
        """
        Adds a DDL statement to the ChromaDB collection.

        Args:
            ddl (str): The DDL statement to be added.

        Returns:
            None but prints the UUID of the added DDL document.
        """
        id = str(uuid.uuid4())
        self.ddl_collection.add(documents=ddl, ids=id)
        print(f"Added DDL to ChromaDB with ID: {id}")


    def add_ddls(self, ddls: list):
        """
        Adds multiple DDL statements to the ChromaDB collection.

        Args:
            ddls (list of str): A list of DDL statements to be added.

        Returns:
            None
        """
        for ddl in ddls:
            self.add_ddl(ddl)


    def query(self, collection_name:str, query_text: str, n_results: int):
        """
        Queries the ChromaDB collection and retrieves documents based on the specified query texts.

        Args:
            query_texts (list of str): The texts to query in the database.
            n_results (int): The number of results to return per query.

        Returns:
            list: A list of documents that match the query criteria.
        """
        collection = self.client.get_collection(collection_name)
        return collection.query(query_texts=[query_text], n_results=n_results)['documents']
