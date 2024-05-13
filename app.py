# https://learn.microsoft.com/en-us/azure/azure-sql/database/azure-sql-python-quickstart?view=azuresql&tabs=mac-linux%2Csql-auth

import os
import pyodbc, struct
from azure import identity

from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel


class Person(BaseModel):
    first_name: str
    last_name: Union[str, None] = None


def get_conn():
    print(connection_string)
    conn = pyodbc.connect(connection_string)
    return conn


# current string
print(os.environ["AZURE_SQL_CONNECTIONSTRING"])
connection_string = os.environ["AZURE_SQL_CONNECTIONSTRING"]

conn = get_conn()
cursor = conn.cursor()
app = FastAPI()


@app.get("/")
def root():
    print("Root of Person API")
    try:
        conn = get_conn()
        cursor = conn.cursor()

        # Table should be created ahead of time in production app.
        cursor.execute(
            """
            CREATE TABLE Persons (
                ID int NOT NULL PRIMARY KEY IDENTITY,
                FirstName varchar(255),
                LastName varchar(255)
            );
        """
        )

        conn.commit()
    except Exception as e:
        # Table may already exist
        print(e)
    return "Person API"


@app.get("/all")
def get_persons():
    rows = []
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Persons")

        for row in cursor.fetchall():
            print(row.FirstName, row.LastName)
            rows.append(f"{row.ID}, {row.FirstName}, {row.LastName}")
    return rows


@app.get("/person/{person_id}")
def get_person(person_id: int):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Persons WHERE ID = ?", person_id)

        row = cursor.fetchone()
        return f"{row.ID}, {row.FirstName}, {row.LastName}"


@app.post("/person")
def create_person(item: Person):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO Persons (FirstName, LastName) VALUES (?, ?)",
            item.first_name,
            item.last_name,
        )
        conn.commit()

    return item
