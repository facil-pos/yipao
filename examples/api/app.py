import os
# import ssl
from fastapi import FastAPI
from pydantic import BaseModel
import vertexai.preview.generative_models as generative_models
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

app = FastAPI(
        title="Simple Inference API",
        version="1.0.0",
        description="This is the OpenAPI specification of a service to query a sql database using natural language. Its purpose is to illustrate how to declare your REST API as an OpenAPI tool."
)
app.openapi_version = "3.0.0"

#----------------
# SSL
#----------------

#ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
#ssl_context.load_cert_chain('./examples/api/server.crt', keyfile='./examples/api/server.key')

# --------------
# APP
# --------------

@app.get("/ping")
def root():
    return {"Hello": "World"}


class QueryModel(BaseModel):
    Item: str = Field(..., description="Name Item")
    q: str

class InitializeModel(BaseModel):
    Item: str = Field(..., description="Name Item")


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


@app.post("/init_item", summary="Initializes by the item")
def initialize_qdrant(data: InitializeModel):

    try:
        connection = parse_sql_url(data.Item)

        qdrant.initialize(connection["database"])

        mysql = connect_sql(connection)

        agent = yp.Agent(llm=chat, 
                            database=mysql, 
                            vectorstore=qdrant,
                            name_collection=connection["database"])
        print('Entrenan documento', agent)
        result = agent.document_database(force_update=True)
        print('Documentos Entrenados', result)

        return {"message": "Qdrant initialized", "payload": connection["database"]}
    except Exception as e:
        print('error',e)
        return{
            "error": 'Error'
        }


@app.post("/inference", summary="Executes a natural language query. Needs Item and 'q' is the query to be performed.")
def query_inference(data: QueryModel):

    connection = parse_sql_url(data.Item)

    mysql = connect_sql(connection)

    agent = yp.Agent(llm=chat, 
                        database=mysql, 
                        vectorstore=qdrant,
                        name_collection=connection["database"])

    try:
        res, _, _, sql_query = agent.invoke(data.q, debug=True, iterations=6)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query execution failed: {str(e)}")
    
    return {"q": data.q, "res": res, "sql_query_generated": sql_query}
