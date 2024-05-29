
<div align="center">
  <img src="docs/source/_static/logo.png" alt="Yipao Logo" width="200"/>
</div>


Yipao is a cutting-edge Python library that enables AI-driven interactions with SQL databases. It specializes in facilitating dynamic SQL query generation and execution, particularly for large databases with numerous tables. Integrated with ChromaDB, Google Generative AI, Vertex AI, and Qdrant, Yipao is a powerful tool for developers looking to leverage machine learning models and vector storage solutions.

## Why Yipao?

Yipao is designed to simplify complex SQL query operations and enhance the interaction between large-scale database systems and AI technologies. It allows developers to:
- Generate and execute SQL queries dynamically using natural language.
- Integrate seamlessly with leading AI platforms and vector databases.
- Improve database querying efficiency and accuracy through AI-driven insights.

## Installation

To install Yipao, you can use pip:

```bash
pip install yipao
```

## Quick Start

Here's a quick example to get you started with **Yipao**:

```python
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

agent.document_database()

prompt = f"Cual es el top 10 de mis productos mas vendidos?, pista usa las siguientes tablas: phppos_items y phppos_sales_items"

res = agent.invoke(prompt)

# tus productos mas vendidos son tales
```
