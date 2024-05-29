
import os
from dotenv import load_dotenv
load_dotenv()

import yipao as yp
from yipao.databases import MySql
from yipao.vectorstores import ChromaDB
from yipao.LLM import GoogleGenAi

connection = {
    'host': os.getenv('HOST'),
    'user': os.getenv('USERDB'),
    'password': os.getenv('PASSWORD'),
    'database': os.getenv('DATABASE'),
    'port': int(os.getenv('PORT'))
}

mysql = MySql(**connection)

chroma = ChromaDB(path='vectorstore', allow_reset=True)

gemini = GoogleGenAi(model='gemini-pro', api_key=os.getenv('APIKEYGEMINI'))

agent = yp.Agent(llm=gemini, 
                 database=mysql, 
                 vectorstore=chroma)

# agent.document_database()

prompt = f"Cual es el top 10 de mis productos mas vendidos?, pista usa las siguientes tablas: phppos_items y phppos_sales_items"

res = agent.invoke(prompt)

print(res)

