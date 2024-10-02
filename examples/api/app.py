import os
# import ssl
from fastapi import FastAPI, Body
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from pydantic import BaseModel, Field
from fastapi import HTTPException
import re
from dotenv import load_dotenv
load_dotenv()

import yipao as yp
from yipao.databases import MySql
from yipao.vectorstores import QdrantDB
from yipao.LLM import GoogleGenAi

KEY = "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"
MODEL = "llama-3.1-8b-instant"
CONFIG = 0.3

origins = [
    "http://127.0.0.1:4200",
    "*"
]

app = FastAPI(
        title="Simple Inference API",
        version="1.0.0",
        description="Esta es una demo en swagger ui de una api para realizar consultas sql a una base de datos por medio de lenguaje natural"
)
app.openapi_version = "3.0.0"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#----------------
# SSL
#----------------

#ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
#ssl_context.load_cert_chain('./examples/api/server.crt', keyfile='./examples/api/server.key')

# --------------
# APP
# --------------

@app.get("/ping", summary="Ping de validacion")
def root():
    return {"Hello": "World"}


class QueryModel(BaseModel):
    Item: str = Field(...,  examples=["root:123456@127.0.0.1:3306/messagehistoryrag"], description="Url database")
    q: str = Field(..., description='Pregunta del usuario')

class InitializeModel(BaseModel):
    Item: str = Field(
        ..., 
        examples=["root:123456@127.0.0.1:3306/messagehistoryrag"], 
        description="Url database")

    class Config:
            schema_extra = {
                "example": {
                    "Item": "root:123456@127.0.0.1:3306/messagehistoryrag"
                }
            }


def connect_sql(db):
    try:
        mysql = MySql(**db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to MySQL: {str(e)}")

    return mysql


def parse_sql_url(url):
    pattern = re.compile(r'(?P<user>.*?):(?P<password>.*?)(?=@)@(?P<host>.*?):(?P<port>\d+?)/(?P<database>.*)')
    match = pattern.match(url)
    if match:
        connection = match.groupdict()
        connection['port'] = int(connection['port'])
    else:
        print("URL format is incorrect")
    return connection


qdrant = QdrantDB("http://localhost:6333", os.getenv('APIKEY_QDRANT'))
chat = GoogleGenAi("gemini-1.5-flash","AIzaSyB0a2toqWMPKbqM5jojx1RFTT1PhT-T7zY",temperature=0.2)

#--------------
# ROUTES
#--------------


@app.post("/init_item", summary="Inicializa la conexion a la base de datos SQL usando la url en base root:123456@127.0.0.1:3306/namedatabase")
def initialize_qdrant(data: Annotated[InitializeModel, Body(
    examples = [
        {
            "Item": "root:123456@127.0.0.1:3306/messagehistoryrag"
        }
    ]
)]):

    try:
        connection = parse_sql_url(data.Item)

        qdrant.initialize(connection["database"])

        mysql = connect_sql(connection)

        agent = yp.Agent(llm=chat, 
                            database=mysql, 
                            vectorstore=qdrant,
                            name_collection=connection["database"])

        agent.document_database(connection["database"])

        return {"message": "Qdrant initialized", "payload": connection["database"]}
    except Exception as e:
        print('error',e)
        raise HTTPException(status_code=401, detail="No fue posible conectar a la db")

@app.post("/inference", summary="Ejecuta una consulta en lenguaje natural, devuelve el resultado de la consulta junto con la consulta creada")
def query_inference(data: QueryModel):

    connection = parse_sql_url(data.Item)

    mysql = connect_sql(connection)

    agent = yp.Agent(llm=chat, 
                        database=mysql, 
                        vectorstore=qdrant,
                        name_collection=connection["database"])

    try:
        res, _, _, sql_query = agent.invoke(data.q, debug=True, iterations=6)

        res =  res.to_dict(orient="records")

        return {"q": data.q, "res": res, "sql_query_generated": sql_query}
    except Exception as e:
        print('Error en el query',e)
        raise HTTPException(status_code=401, detail=f"Query execution failed")
    
