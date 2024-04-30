from prof_code import get_ideal_ans, get_student_ans

from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def process_answers():
    paper_no = request.args.get('paper_no')  # Get the 'paper_no' query parameter from the request

    if paper_no is None:
        return "Error: 'paper_no' parameter is missing."

    get_ideal_ans(paper_no)
    get_student_ans(paper_no)

    return f"Processing Finished."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
