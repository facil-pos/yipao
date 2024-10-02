import pymysql
from pymysql.connections import Connection
from typing import Optional
import pandas as pd
from ..utils.constants import DESCRIBE_TABLE_QUERY, RELATIONS_TABLE_QUERY, DESCRIBE_DATABASE_QUERY
import ast


class MySql:
    """
    Class to handle interactions with a MySQL database.
    Manages connections and performs database operations securely and efficiently.
    """

    def __init__(self, host: str, user: str, password: str, database: str, port: int = 3306):
        """
        Initializes the MySQLDatabase instance with connection parameters.

        Args:
        host (str): Hostname of the MySQL server.
        user (str): Username to connect to the database.
        password (str): Password for the database user.
        database (str): Name of the database to connect to.
        port (int, optional): Port number on which the MySQL server is listening. Defaults to 3306.
        """
        self.connection: Optional[Connection] = None
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.dialect = 'mariadb'

        self.connect()


    def connect(self):
        """
        Creates a connection to the MySQL database using the instance's configuration.
        
        Raises:
        pymysql.MySQLError: If an error occurs during connection.
        """
        try:
            print(f"Connecting to MySQL DB... {self.host, self.user, self.password, self.database, self.port}")
            self.connection = pymysql.connect(host=self.host, user=self.user, password=self.password,
                                              db=self.database, port=self.port)
            print("Connection to MySQL DB successful")
        except pymysql.MySQLError as e:
            print(f"Failed to connect to MySQL: {e}")
            raise


    def close(self):
        """
        Closes the connection to the MySQL database.
        
        Raises:
        Exception: If an error occurs while closing the connection.
        """
        if self.connection:
            try:
                self.connection.close()
                print("MySQL connection closed")
            except Exception as e:
                print(f"Failed to close the connection: {e}")
                raise


    def describe_ddl(self, table: str) -> str:
        """
        Describes the Data Definition Language (DDL) structure and relationships of a given table.
        """
        try:
            description_query = DESCRIBE_TABLE_QUERY.format(table)
            # Using pandas to execute SQL query and return results in DataFrame
            description_df = pd.read_sql(description_query, self.connection)
            description = f"Description of the table {table}:\n{description_df.to_string()}"

            relations_query = RELATIONS_TABLE_QUERY.format(database=self.database, table=table)
            relations_df = pd.read_sql(relations_query, self.connection)
            relations = f"Relationships of the table {table}:\n{relations_df.to_string()}"

            return description + "\n" + relations

        except Exception as e:
            return f"Error describing the table: {e}"
        

    def describe_database(self,database):
        """
        Describes the Data Definition Language (DDL) structure and relationships of all tables.

        Returns:
            List[str]: List of descriptions for each table in the database.

        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(DESCRIBE_DATABASE_QUERY.format(database, database))
            res = cursor.fetchall()

            resultados = res #ast.literal_eval(res)
            tablas = {}

            for fila in resultados:
                nombre_tabla = fila[0]
                campo = fila[1]
                tipo = fila[2]
                if len(fila) > 5:  # Hay una relación definida
                    relacion = (fila[4], fila[5])
                else:
                    relacion = None

                if nombre_tabla not in tablas:
                    tablas[nombre_tabla] = {
                        'campos': {},
                        'relaciones': []
                    }
                
                if campo not in tablas[nombre_tabla]['campos']:
                    tablas[nombre_tabla]['campos'][campo] = tipo

                if relacion and relacion not in tablas[nombre_tabla]['relaciones']:
                    tablas[nombre_tabla]['relaciones'].append(relacion)

            # Formatear la descripción para cada tabla
            descripciones = []

            for nombre_tabla, info in tablas.items():
                descripcion_campos = ", ".join([f"{campo} ({tipo})" for campo, tipo in info['campos'].items()])
                if info['relaciones']:
                    descripcion_relaciones = ", ".join([f"{rel[0]} ({rel[1]})" for rel in info['relaciones']])
                else:
                    descripcion_relaciones = "ninguna"

                descripcion = f"Description of the table {nombre_tabla}:\n{descripcion_campos}, Relationships of the table:\n{descripcion_relaciones}"
                descripciones.append(descripcion)
                
            return descripciones


        except Exception as e:
            print(e)
            return f"Error describing the database"

    
    def execute_query(self, query: str, markdown: bool = False):
        """
        Executes a query on the MySQL database.

        Args:
        query (str): SQL query to be executed.

        Returns:
        str: Result of the query execution.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            res = cursor.fetchall()
            res = pd.DataFrame(res)
            if markdown:
                return res.to_markdown()
            return res
        except pymysql.MySQLError as sql_error:
            raise TypeError(f"SQL Error {sql_error.args[0]}: {sql_error.args[1]}")
        except Exception as e:
            raise TypeError(f"Error executing query: {e}") 