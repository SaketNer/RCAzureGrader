import csv
import os
import pyodbc


connection_string = 'YOUR_SQL_CONNECTION_STRING'
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
    