.. yipao documentation master file, created by
   sphinx-quickstart on Thu May  2 06:39:24 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to yipao's documentation!
=================================

.. toctree::
   :maxdepth: 2
   :hidden:

   quickstart
   llm
   agent
   databases
   retrievers
   vectorstores

.. raw:: html

   <div align="center">
   <img src="https://github.com/facil-pos/yipao/blob/main/docs/source/_static/logo.png?raw=true" alt="Yipao Logo" width="200"/>
   </div>


Yipao is a cutting-edge Python library that enables AI-driven interactions with SQL databases. It specializes in facilitating dynamic SQL query generation and execution, particularly for large databases with numerous tables. Integrated with ChromaDB, Google Generative AI, Vertex AI, and Qdrant, Yipao is a powerful tool for developers looking to leverage machine learning models and vector storage solutions.

+++++++++++++++
Why Yipao? 🤔
+++++++++++++++

Yipao is designed to simplify complex SQL query operations and enhance the interaction between large-scale database systems and AI technologies. It allows developers to:
- Generate and execute SQL queries dynamically using natural language.
- Integrate seamlessly with leading AI platforms and vector databases.
- Improve database querying efficiency and accuracy through AI-driven insights.

+++++++++++++++
Integrations 🚀
+++++++++++++++


In the actual version we have implemented this vectorstores, chromadb_ and qdrant_ to store and retrieve vectors.

.. _chromadb: https://www.trychroma.com
.. _qdrant: https://qdrant.tech/

for the llm model we have implemented googlegenai_ and vertexai_

.. _googlegenai: https://cloud.google.com/ai/generative-ai?hl=en
.. _vertexai: https://cloud.google.com/vertex-ai?hl=en