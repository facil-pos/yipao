from abc import ABC, abstractmethod
from .prompts import SQL_PROMPT, FINAL_RESPONSE_PROMPT

class PromptBuilder():
    """
    Abstract base class for building prompts used in SQL query generation.

    This class provides a framework for constructing SQL and response prompts,
    ensuring that all concrete implementations provide consistent behavior
    for filling out the necessary details.
    """
    def __init__(self):
        pass


    @abstractmethod
    def fill_sql_prompt(self, question, dialect_name, table_names, history):
        """
        Abstract method to fill an SQL prompt template with necessary details.

        Args:
            question (str): The natural language question to be translated into SQL.
            dialect_name (str): The SQL dialect to use (e.g., 'MySQL', 'PostgreSQL').
            table_names (list of str): List of table names to be included in the prompt.
            history (str): Previous SQL queries and responses to maintain context.

        Returns:
            str: A formatted SQL prompt filled with the provided details.
        """
        ddls = "\n\n".join(table_names)
        return SQL_PROMPT.format(question=question, dialect_name=dialect_name, table_names=ddls, history=history)
