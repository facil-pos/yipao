import os
from dotenv import load_dotenv
load_dotenv()

import yipao as yp
from yipao.databases import MySql
from yipao.vectorstores import QdrantDB
from yipao.LLM import GoogleGenAi

connection = {
    'host': os.getenv('HOST'),
    'user': os.getenv('USERDB'),
    'password': os.getenv('PASSWORD'),
    'database': os.getenv('DATABASE'),
    'port': int(os.getenv('PORT'))
}

mysql = MySql(**connection)

qdrant =  QdrantDB(':memory:')

gemini = GoogleGenAi(model='gemini-pro', api_key=os.getenv('APIKEYGEMINI'))

agent = yp.Agent(llm=gemini, 
                 database=mysql, 
                 vectorstore=qdrant)

agent.document_database()

prompt = f"What is my best selling product?"

res = agent.invoke(prompt)

print(res)