import os
import pyodbc, struct
from azure import identity

from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

# connection_string = os.environ["AZURE_SQL_CONNECTIONSTRING"]
# print(connection_string)
import pyodbc

connection_string = os.environ["AZURE_SQL_CONNECTIONSTRING"]


# connection_string = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:rc-cloud-server.database.windows.net,1433;Database=RC_cloud_database;UID=Saket;PWD=RC@12345678;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30"
def get_conn():
    # credential = identity.DefaultAzureCredential(exclude_interactive_browser_credential=False)
    # token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
    # token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
    # SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h
    # conn = pyodbc.connect(connection_string, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})
    conn = pyodbc.connect(connection_string)
    return conn


conn = get_conn()
cursor = conn.cursor()

cursor.execute(
    """
                CREATE TABLE test3 (
                    Paper int NOT NULL PRIMARY KEY ,
                    Questionno int,
                    Answer varchar(2000)
                );
            """
)
cursor.execute(
    f"INSERT INTO test3 (Paper, Questionno,Answer) VALUES (?, ?, ?)",
    1,
    1,
    "what is your name?",
)
conn.commit()
