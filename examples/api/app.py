import os
import ssl
from fastapi import FastAPI
from pydantic import BaseModel
from vertexai.generative_models import GenerativeModel, SafetySetting, Part
from pydantic import BaseModel, Field
from fastapi import HTTPException
import re
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

import yipao as yp
from yipao.databases import MySql
from yipao.vectorstores import QdrantDB
from yipao.LLM import VertexAiLLM

KEY_PATH='./credentials/gen-lang-client-0867205962-4a2d259770b4.json'
PROJECT_ID = "gen-lang-client-0867205962"
REGION = "us-central1"
MODEL = "gemini-1.5-flash-002"
CONFIG  = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}
SAFETY_SETTINGS = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
]
added_excel = True

app = FastAPI(
        title="Simple Inference API",
        version="1.0.0",
        description="This is the OpenAPI specification of a service to query a sql database using natural language. Its purpose is to illustrate how to declare your REST API as an OpenAPI tool."
)
app.openapi_version = "3.0.0"

#----------------
# SSL
#----------------

# ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# ssl_context.load_cert_chain('./credentials/server.crt', keyfile='./credentials/server.key')

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


def parse_sql_url(url):
    pattern = re.compile(r'(?P<user>.*?):(?P<password>.*?)(?=@)@(?P<host>.*?):(?P<port>\d+?)/(?P<database>.*)')
    match = pattern.match(url)
    if match:
        connection = match.groupdict()
        connection['port'] = int(connection['port'])
    else:
        print("URL format is incorrect")
    return connection


qdrant = QdrantDB(':memory:')
chat = VertexAiLLM(MODEL, KEY_PATH, PROJECT_ID, CONFIG, SAFETY_SETTINGS)

#--------------
# ROUTES
#--------------


@app.get("/init_item", summary="Initializes by the item")
def initialize_qdrant():
    global added_excel
    

    qdrant.initialize(os.getenv('DATABASE'))

    mysql = connect_sql()

    agent = yp.Agent(llm=chat, 
                        database=mysql, 
                        vectorstore=qdrant,
                        name_collection=os.getenv('DATABASE'))
    agent.document_database()

    if not added_excel:

        file_path = './static/Question, intention and response.xlsx'

        df = pd.read_excel(file_path)

        selected_columns = df[['question (english)', 'intent (english)', 'intermediate response (SQL QUERY)']]

        formatted_output = [
            f"\npregunta: {row['question (english)']}\nintencion: {row['intent (english)']}\nejemplo de query: {row['intermediate response (SQL QUERY)']}\n"
            for _, row in selected_columns.iterrows()
        ]

        qdrant.add_ddls(formatted_output, connection["database"])
        added_excel = True

    return {"message": "Qdrant initialized", "payload": data.Item}


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
