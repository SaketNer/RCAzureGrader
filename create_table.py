import csv
import os
import pyodbc


connection_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:rc-cloud-server.database.windows.net,1433;Database=RC_cloud_database;UID=Saket;PWD=RC@12345678;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30'

def get_conn():
    conn = pyodbc.connect(connection_string)
    return conn
conn = get_conn()
cursor = conn.cursor()

cursor.execute(
            """
            CREATE TABLE test6 (
                ID int NOT NULL PRIMARY KEY IDENTITY,
                paper_no int,
                question_no int,
                answer varchar(2000),
            );
        """
        )

conn.commit()
    