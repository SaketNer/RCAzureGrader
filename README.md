# Generative AI Grader

The application is an exam grader that uses OpenAI to grade student answer keys. The application can take student answers and professors ideal answers as input, query relevant paragraphs from textbooks and grade the answers from a scale of 0 to 10. We use Azure kubernetes to host our application giving us high scalability and availability. We also use Azure SQL database to store student answers, professor's answer key and student marks.

This project was done by Saket Nerurkar, Sharwin Neema, Ashmit Khandelwal, Yash Aditya and Hardav Raval as part of our "Modern Application Architectures for Cloud and Edge" under Krishnan Venkateswaran Sir.				


## Usage

- Kubernetes 
The kubernetes folder has the application code that is hosted on kubernetes. It can query the SQL database for student answers and professors answer key. It then sends the promt to OpenAI giving us a score and the reasoning for the score as output that is then stored in our SQL database.

- Prof_code
This folder has the code that the professor will run. It will call the kubernetes server which will then grade all the submissions for the exam paper that the professor has requested for and download the final marks of all the children.

- Other codes
Other codes were used in our experimental stage. Create_table.py is used to create tables in our SQL database. You can also create them from the Azure portal. Upload_answers.py is used to upload answers to the sql database.


