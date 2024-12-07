import os
# import ssl
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from vertexai.generative_models import SafetySetting
from pydantic import BaseModel, Field
from fastapi import HTTPException
import re
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

import yipao as yp
from yipao.databases import MySql
from yipao.vectorstores import QdrantDB
from yipao.LLM import GoogleGenAi

app = FastAPI(
        title="Simple Inference API",
        version="1.0.0",
        description="Esta es una demo en swagger ui de una api para realizar consultas sql a una base de datos por medio de lenguaje natural")
app.openapi_version = "3.0.0"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#----------------
# SSL
#----------------

# ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# ssl_context.load_cert_chain('./credentials/server.crt', keyfile='./credentials/server.key')

# --------------
# APP
# --------------

class QueryModel(BaseModel):
    query: str = Field(..., description='Pregunta del usuario')

def connect_sql():
    connection = {
        'host': os.getenv('HOST'),
        'user': os.getenv('USERDB'),
        'password': os.getenv('PASSWORD'),
        'database': os.getenv('DATABASE'),
        'port': int(os.getenv('PORT'))
    }

    try:
        mysql = MySql(**connection)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to MySQL: {str(e)}")

    return mysql

qdrant =  QdrantDB('http://localhost:6333', os.getenv('QDRANT_API_KEY'), collection_name=os.getenv('DATABASE'))
chat = GoogleGenAi(model="gemini-1.5-pro", api_key=os.getenv('APIKEYGEMINI'))

qdrant.initialize_collection()
mysql = connect_sql()
agent = yp.Agent(llm=chat, database=mysql, vectorstore=qdrant, name_collection=os.getenv('DATABASE'))

#--------------
# ROUTES
#--------------


@app.get("/test_yipao/health", summary="Healthcheck")
def health():
    return {"message": "Healthy"}

@app.post("/test_yipao/inference", summary="Ejecuta una consulta en lenguaje natural, devuelve el resultado de la consulta junto con la consulta creada")
def query_inference(data: QueryModel):

    try:
        res, sql_query = agent.invoke(data.query, debug=True, iterations=6)
        
        try:
            res = res.to_dict(orient="records")
        except Exception as e:
            print(f"Error converting result to dict: {e}")
            res = str(res)
        return {"q": data.query, "res": res, "sql_query_generated": sql_query}
    except Exception as e:
        print('Error en el query',e)
        raise HTTPException(status_code=401, detail=f"Query execution failed")
    
