
<div align="center">
  <img src="https://github.com/facil-pos/yipao/blob/main/docs/source/_static/logo.png?raw=true" alt="Yipao Logo" width="200"/>

| [![GitHub](https://img.shields.io/badge/GitHub-yipao-blue?logo=github)](https://github.com/facil-pos/yipao) | [![PyPI](https://img.shields.io/pypi/v/yipao?logo=pypi)](https://pypi.org/project/yipao/) | [![Documentation](https://img.shields.io/badge/Documentation-yipao-blue?logo=read-the-docs)](https://facil-pos.github.io/yipao/) |

</div>


Yipao is a cutting-edge Python library that enables AI-driven interactions with SQL databases. It specializes in facilitating dynamic SQL query generation and execution, particularly for large databases with numerous tables. Integrated with ChromaDB, Google Generative AI, Vertex AI, and Qdrant, Yipao is a powerful tool for developers looking to leverage machine learning models and vector storage solutions.

## Why Yipao? 🤔

Yipao is designed to simplify complex SQL query operations and enhance the interaction between large-scale database systems and AI technologies. It allows developers to:
- Generate and execute SQL queries dynamically using natural language.
- Integrate seamlessly with leading AI platforms and vector databases.
- Improve database querying efficiency and accuracy through AI-driven insights.

## Installation 🛠️

To install Yipao, you can use pip:

```bash
pip install yipao
```

## Quick Start  🚀

Here's a quick example to get you started with **Yipao**:

```python
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
# your best products are...
```

# ROADMAP

- implement groq interface
- implement openai interface
- customdatabase interface
- sqlite integration, other sql dialects
- create tests
- add sql database as example
- RAG-graph based for better accuracy
   - neo4j integration
   - embedding store in graphs


# Contributing 👋

Want to help improve Yipao? Contributions are welcome! 🎉


