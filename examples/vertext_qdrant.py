
import vertexai.preview.generative_models as generative_models

import os
from dotenv import load_dotenv
load_dotenv()

import yipao as yp
from yipao.databases import MySql
from yipao.vectorstores import QdrantDB
from yipao.LLM import VertexAiLLM

connection = {
    'host': os.getenv('HOST'),
    'user': os.getenv('USERDB'),
    'password': os.getenv('PASSWORD'),
    'database': os.getenv('DATABASE'),
    'port': int(os.getenv('PORT'))
}

KEY_PATH='./examples/credentials/gen-lang-client-0867205962-8353cd35557a.json'
PROJECT_ID = "gen-lang-client-0867205962"
REGION = "us-central1"
MODEL = "gemini-1.0-pro-002"

CONFIG = {
            "max_output_tokens": 1000,
            "temperature": 0.5,
            "top_p": 0.95,
            "top_k": 40
        }

SAFETY_SETTINGS = {
                    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                }


mysql = MySql(**connection)

qdrant = QdrantDB(':memory:', os.getenv('APIKEY_QDRANT'), name_collection='Daniel')

chat = VertexAiLLM(MODEL, KEY_PATH, PROJECT_ID, CONFIG, SAFETY_SETTINGS)

agent = yp.Agent(llm=chat, 
                 database=mysql, 
                 vectorstore=qdrant,
                 name_collection='Daniel')

agent.document_database()
                                                                                                                                                                                                                                                                                                                                                                                                                  
prompt = f"Cuales fueron mis ganancias totales del año 2023?"

res, input_tokens, output_tokens = agent.invoke(prompt, debug=True, iterations=6)
 
print(res)
print(chat.monitor())

