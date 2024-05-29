class VectorStoreRetriever:
    """
    A class that retrieves related data definition language (DDL) statements from a vectorstore based on a query.

    Attributes:
        vectorstore: The vector store where DDLs are stored and queried.
        n_results (int): The number of query results to return.
    """

    def __init__(self, vectorstore, n_results, name_collection):
        """
        Initializes the VectorStoreRetriever with a specified vectorstore and the number of results to retrieve.

        Args:
            vectorstore: The vector store to use for retrieving DDLs.
            n_results (int): The number of results to return per query.
        """
        self.vectorstore = vectorstore
        self.n_results = n_results
        self.name_collection = name_collection

    def get_related_ddl(self, question: str) -> list:
        """
        Queries the vectorstore for related DDL statements based on the provided question.

        Args:
            question (str): The query string used to find related DDLs.

        Returns:
            list: A list of DDLs that are related to the query, up to the number of results specified.
        """
        return self.vectorstore.query(
            collection_name=self.name_collection,
            query_text=question,
            n_results=self.n_results,
        )