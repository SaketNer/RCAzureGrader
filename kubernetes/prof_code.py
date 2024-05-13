import pyodbc
import pandas as pd
from openai import OpenAI
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
import os

import pinecone
from pinecone import Pinecone

# Placeholder code
student_ans = pd.DataFrame(columns=['student_id', 'question_no', 'answer', 'marks', 'reason'])
ideal_ans = pd.DataFrame(columns=['question_no', 'answer'])
# Rest of the code
# paper_number = input("Please enter the paper number: ")
#paper_number = 1
connection_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:rc-cloud-server.database.windows.net,1433;Database=RC_cloud_database;UID=Saket;PWD=RC@12345678;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30'

pc = Pinecone(
    api_key="8f05e211-66e3-43fc-a2fe-ca6081ecf797"
)
embeddings = OpenAIEmbeddings(openai_api_key="sk-proj-W0lHK8EgUiZY0QxMtYc8T3BlbkFJFDOiSZnoED53RX4pf14N")
vectorstore = PineconeVectorStore(pinecone_api_key="8f05e211-66e3-43fc-a2fe-ca6081ecf797",index_name='azure-openai', embedding=embeddings,namespace="ns2")

client = OpenAI(api_key="sk-proj-W0lHK8EgUiZY0QxMtYc8T3BlbkFJFDOiSZnoED53RX4pf14N")

def get_context(ideal_answer):
    query_summary = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are amazing at summarizing and finding key points in an answer. Write a summary of th text that will assist us to query a vector database accurately"},
            {"role": "user", "content":ideal_answer}
        ]
    )
    search_text = query_summary.choices[0].message.content
    context = vectorstore.similarity_search(search_text,k = 2)
    return context

def get_conn():
    conn = pyodbc.connect(connection_string)
    return conn

conn = get_conn()
print("conn done")

def get_ideal_ans(paper_no):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM final_ideal where paper_no = ?", paper_no)

        for row in cursor.fetchall():
            #print(row)
            ideal_ans.loc[len(ideal_ans.index)] = [row.question_no, row.answer ]
        print(ideal_ans)

def upload_marks(paper_no,student_id,quesntion_no,marks,reason):
    cursor = conn.cursor()
    print("uploading")
    cursor.execute("INSERT INTO final_marks (paper_no,student_id,question_no,marks,reason) VALUES (?,?,?,?,?)", (paper_no,student_id,quesntion_no,marks,reason))
    

def check_ans(ideal_answer, student_answer):
    context = get_context(ideal_answer)
    text = f"You are a highly experienced professor in the field of computer science, tasked with evaluating a student's answer to a descriptive question. Your goal is to provide a fair and accurate assessment of the student's response, based on the ideal answer and marking scheme provided. You may also refer to the context provided by the textbook, but please keep in mind that it may not always be accurate. The student's answer is as follows: {student_answer} The ideal answer is as follows: {ideal_answer} The context provided by the textbook is as follows: {context} The marking scheme is as follows: Total marks that can be awarded are 10. 2 marks are awarded for each point in the ideal answer. If a point is partially written, then award 1 mark for that point. If a point which is not mentioned in the ideal answer and context is written, then do not give marks for that point. Please provide a detailed explanation of how you arrived at your assessment, including the specific points in the student's answer that earned marks and any points that were not awarded. Your response should be in the following format: Marks: [number of marks awarded], Reasons: [detailed explanation of how marks were awarded].Ensure there is a comma imediately after the marks value."
    #print(text)
    client = OpenAI(api_key="sk-proj-W0lHK8EgUiZY0QxMtYc8T3BlbkFJFDOiSZnoED53RX4pf14N")

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a professor grading answer papers of college students. Strictly stick to the grading scheme and give marks based on the ideal answer and reference material. Do not use your own knowledge."},
            {"role": "user", "content":text}
        ],
        temperature= 0
    )
    print(completion.choices[0].message.content)
    split_text = completion.choices[0].message.content.split(',', 1)
    marks_split = split_text[0].split(' ')
    marks = marks_split[1]
    print("marks give are ", int(marks))
    print("reasons are ", split_text[1])
    return int(marks),split_text[1]

def get_student_ans(paper_no):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM final_student_ans where paper_no = ?", paper_no)

        for row in cursor.fetchall():
            #print(row)
            q_no = row.question_no
            prof_ans = ideal_ans.loc[ideal_ans['question_no']==q_no].iloc[0]['answer']
            marks,reason = check_ans(prof_ans, row.answer)
            upload_marks(paper_no,row.student_id,row.question_no,marks,reason)
            student_ans.loc[len(student_ans.index)] = [row.student_id,row.question_no, row.answer,marks,reason ]
            print("********start**********\n",prof_ans,'\n\n',row.answer,"\n******************\n")
        print(ideal_ans)
        conn.commit()

# get_ideal_ans(paper_number)
# get_student_ans(paper_number)
