from typing import List, Dict
from flask import Flask, request, Response
import mysql.connector
import json
from model import *

app = Flask(__name__)
@app.route('/exams', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['exam'] != '' and 'exam' in request.form:
            result = insert_exam(request.form['exam'])
            if result['error'] == '':
                return Response(result['msg'], status=result["status"])
            else:
                return Response(result['error'], status=result["status"])
        else:
            return Response("Please enter the required fields", status=400)
    else:
        return Response(json.dumps({'exams': exams_list()}), status=200)


@app.route('/subCategory', methods=['GET', 'POST'])
def subCategory():
    if request.method == 'POST':
        if 'exam' in request.form and 'subcategory' in request.form and request.form['exam'] != '' and request.form['subcategory'] != '':
            if 'subject' not in request.form:
                subject = ''
            else:
                subject = request.form['subject']
            if 'topic' not in request.form:
                topic = ''
            else:
                topic = request.form['topic']
            result = insert_subcategory(request.form['exam'], request.form[
                                        'subcategory'], subject, topic)
            if result['error'] == '':
                return Response(result['msg'], status=result['status'])
            else:
                return Response(result['error'], status=result['status'])
        else:
            return Response("Please fill required fields!", status=400)
    else:
        return Response(json.dumps({'result': all_details()}), status=200)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
