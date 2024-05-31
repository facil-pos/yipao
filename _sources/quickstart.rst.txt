Quick Start Guide
=================

This guide will help you get started with Yipao, a library designed for seamless interaction between SQL databases and language models using Retrieval-Augmented Generation (RAG).

Installation
------------

To install Yipao, you will need Python 3.6 or later. You can install it using pip:

.. code-block:: bash

    pip install yipao

Ensure you have the necessary permissions to install the package or use a virtual environment.


and here is a basic example of how to use Yipao:

.. code-block:: python

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