from ..retrievers import VectorStoreRetriever
from ..prompts import PromptBuilder
from ..utils import extract_json
from ..LLM import CustomLLM

class Agent:
    """
    Agent class for managing interactions between language models and SQL databases.
    It uses Retrieval-Augmented Generation to construct and execute SQL queries based
    on natural language input.

    Attributes:
        llm (CustomLLM): A language model for generating SQL queries.
        database: The database object to execute SQL queries.
        vectorstore: The storage for vector embeddings of SQL statements.
        retriever (VectorStoreRetriever): A retriever for related data definitions.
        promptBuilder (PromptBuilder): A builder for creating SQL prompts.
        history (str): A record of executed SQL queries.
    """


    def __init__(self, llm: CustomLLM, database, vectorstore, name_collection):
        """
        Initializes the Agent with a language model, database, and vector store.

        Args:
            llm (CustomLLM): The language model used to generate SQL queries.
            database: The database interface to execute SQL queries.
            vectorstore: The vector store interface for saving SQL statement embeddings.
        """
        self.llm = llm
        self.history = '' 
        self.database = database
        self.vectorstore = vectorstore
        self.name_collection = name_collection
        self.retriever = VectorStoreRetriever(vectorstore, 5, name_collection)
        self.promptBuilder = PromptBuilder()


    def document_database(self, force_update=False):
        """
        Documents the database by extracting table descriptions and saving them into the vector store.
        """
        if not self.vectorstore.check_documents(self.name_collection) or force_update:
            table_description = self.database.describe_database()
            self.vectorstore.add_ddls(table_description, self.name_collection)
        else:
            print("Database already documented - skipping.")


    def execute_sql(self, sql_query):
        """
        Executes an SQL query on the database.

        Args:
            sql_query (str): The SQL query to execute.

        Returns:
            tuple: A tuple containing the result of the query and a status code (1 for success, 0 for failure).
        """
        try:
            res = self.database.execute_query(sql_query)
            return res, 1
        except Exception as e:
            print('Error executing query')
            return f"Error executing query: {e}", 0


    def invoke(self, question, iterations=1, debug=False):
        """
        Processes a natural language question to generate and execute SQL queries over multiple iterations.

        Args:
            question (str): The natural language question to be processed.
            iterations (int): The number of iterations to attempt query generation and execution.

        Returns:
            tuple: The final query result and token counts (input tokens, output tokens) for all iterations.
        """
        intokens, outokens = 0, 0

        for _ in range(iterations):
            related_ddl = self.retriever.get_related_ddl(question)
            if debug: print(f"related_ddl: {related_ddl}")

            prompt_sql_generation = self.promptBuilder.fill_sql_prompt(question, self.database.dialect, related_ddl[0], history=self.history)
            response, new_intokens, new_outokens = self.llm.invoke(prompt_sql_generation)
            intokens += new_intokens
            outokens += new_outokens
            sql_query = extract_json(response)['sql_query']
            if debug: print(f"sql generated: {sql_query}")
            
            result, status = self.execute_sql(sql_query)
            if debug: print(f"result: {result}")
            if status: break
            
            self.history += f"{sql_query} {result}\n"

        return result, intokens, outokens, sql_query
