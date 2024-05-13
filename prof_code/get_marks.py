import pandas as pd
import pyodbc
import requests
import time
marks = pd.DataFrame(columns=['question_no', 'student_id','marks','reason'])


url = "http://4.188.92.216/?paper_no=2"  # Replace with your API endpoint URL

print("Processing your data on the server. Please wait...")
response = requests.get(url)

if response.status_code == 200:
    print(response)
else:
    print("API request failed with status code:", response.status_code)

print("Downloading Marks")

connection_string = 'YOUR_SQL_CONNECTION_STRING'
def get_conn():
    conn = pyodbc.connect(connection_string)
    return conn
print("Attempting Connection")
conn = get_conn()
print("connection done")

def get_student_marks(paper_no):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM final_marks where paper_no = ?", paper_no)

        for row in cursor.fetchall():
            #print(row)
            marks.loc[len(marks.index)] = [row.question_no, row.student_id, row.marks, row.reason ]
            
get_student_marks(1)
marks.to_csv('/Users/saket/devlopment/RCAzureGrader/prof_code/mark_reason.csv', index=False)


student_marks = marks.groupby('student_id')['marks'].sum().reset_index()
print(student_marks)

student_marks.to_csv('/Users/saket/devlopment/RCAzureGrader/prof_code/mark.csv', index=False)
