import csv
import os
import pyodbc
# Path to the CSV file
csv_file = './ans.csv'

# Open the CSV file
connection_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:rc-cloud-server.database.windows.net,1433;Database=RC_cloud_database;UID=Saket;PWD=RC@12345678;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30'


def get_conn():
    conn = pyodbc.connect(connection_string)
    return conn
conn = get_conn()

def upload_row(paper_no,student_id,question_no,answer):
    
    cursor.execute(
            f"INSERT INTO test4 (paper_no, student_id,question_no,answer) VALUES (?, ?, ?, ?)",
            paper_no,
            student_id,
            question_no,
            answer,
    )



with open(csv_file, 'r') as file:
    # Create a CSV reader object
    reader = csv.DictReader(file)
    cursor = conn.cursor()
    # Iterate over each row in the CSV file
    for row in reader:
        # Print the values of each column in the row
        print(row)
        print(row['Paper_no'], row['Student_id'], row['question_number'], row['answer'])
        #upload_row(10001, 1, 1, "testing")
        upload_row(row['Paper_no'], row['Student_id'], row['question_number'], row['answer'])
    conn.commit()  