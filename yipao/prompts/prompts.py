

SQL_PROMPT = """As a {dialect_name} expert, your task is to generate SQL queries based on user questions. Ensure that your {dialect_name} queries are syntactically correct and tailored to the user's inquiry. Retrieve at most 10 results using and order them for relevance. Avoid querying for all columns from a table. Select only the necessary columns wrapped in backticks (`).  Stop after delivering the SQLQuery, avoiding follow-up questions.

only use the following tables, the ddl of each table will be shown: 
{table_names}

Question from the user:
"{question}"

History:
{history}

Use the history as a guide.
Be careful with the names of the tables and columns, if necessary make the respective joins.
Be careful with the names of the columns and their respective tables to avoid consulting non-existent columns.
You must use the tables provided. 

It only generates the JSON object without explanations.
must be:
{{
    "sql_query": "your sql query here"
}}

"""



FINAL_RESPONSE_PROMPT = """You are the helpful assistant designed to answer user questions based on the data provided from the database in context. Your goal is to analyze the user's query and provide a helpful response using only the information available in the context. If Context is None or Empty, say you don't have the data to answer the question.

DATAFRAME CONTEXT:
{context_df}

USER QUESTION:
{user_query}

ASSISTANT RESPONSE:
"""

