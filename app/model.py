import mysql.connector
import json

config = {
    'user': 'root',
    'password': 'root',
    'host': 'db',
    'port': '3306',
    'database': 'exams'
}
connection = mysql.connector.connect(**config)
cursor = connection.cursor()

def exams_list():   
    cursor.execute('SELECT * FROM ExamDetails')
    results = [{id: name} for (id, name) in cursor]
    return results

def insert_exam(exam):
    msg = ''
    error = ''
    status = ''
    try:
        cursor.execute("SELECT * FROM ExamDetails Where name = '{0}'".format(exam))
        result = cursor.fetchone() 
        if result == None: 
            cursor.execute("INSERT INTO ExamDetails (name) VALUES  ('{0}')".format(exam))
            connection.commit()
            msg = 'You have successfully created exam!'
            status = 201
        else:
            error = 'Exam already present'
            status = 400
    except:
        error = "some error occured while adding to db"
        status = 500
    output = {"msg": msg,"error":error, "status":status}
    return output

def insert_subcategory(exam, subcategory, subject, topic):
    msg = ''
    error = ''
    status = ''
    output = {"msg": msg,"error":error, 'status':status}
    try: 
        if subject == '' and topic != '':
            output['error'] = "Please enter required details"
            output["status"] = 400
            return output
        cursor.execute("SELECT * FROM ExamDetails Where name = '{0}'".format(exam))
        result = cursor.fetchone()
        if  result == None:
            cursor.execute("INSERT INTO ExamDetails (name) VALUES  ('{0}')".format(exam))
            connection.commit()
            cursor.execute("SELECT * FROM ExamDetails Where name = '{0}'".format(exam))
            result = cursor.fetchone()
        exam_id = result[0]
        cursor.execute("SELECT * FROM ExamCategoryDetails Where name = '{0}' and exam_id = '{1}'".format(subcategory, exam_id))
        result = cursor.fetchone()
        if result == None:
            cursor.execute("INSERT INTO ExamCategoryDetails (name,exam_id) VALUES  ('{0}',{1})".format(subcategory, exam_id))
            connection.commit()
        if result != None and subject == '' and topic == '':
                error = "Already Present"
                output["error"] = error
                output["status"] = 400
                return output
        if subject != '':
            cursor.execute("SELECT * FROM ExamCategoryDetails Where name = '{0}' and exam_id = '{1}'".format(subcategory, exam_id))
            result = cursor.fetchone()
            exam_category_id = result[0]
            cursor.execute("SELECT * FROM SubjectDetails Where name = '{0}' and exam_category_id = '{1}'".format(subject, exam_category_id))
            result1 = cursor.fetchone()
            if result1 == None:
                cursor.execute("INSERT INTO SubjectDetails (name,exam_category_id) VALUES  ('{0}',{1})".format(subject, exam_category_id))
                connection.commit()
            if result1 != None and topic == '':
                error = "Already Present"
                output["error"] = error
                output["status"] = 400
                return output
        if topic != '':
            cursor.execute("SELECT * FROM SubjectDetails Where name = '{0}' and exam_category_id = '{1}'".format(subject, exam_category_id))
            result = cursor.fetchone()
            sub_id = result[0]
            cursor.execute("SELECT * FROM TopicDetails Where name = '{0}' and sub_id = '{1}'".format(topic, sub_id))
            result1 = cursor.fetchone()
            if result1 == None:
                cursor.execute("INSERT INTO TopicDetails (name,sub_id) VALUES  ('{0}',{1})".format(topic, sub_id))
                connection.commit()
            else:
                error = "Already Present"
                output["error"] = error
                output["status"] = 400
                return output
        output["status"] = 201
        output['msg'] = "Successfully created"
    except:
        output["status"] = 500
        output["error"] = "some error occured while adding to db"
    return output

def all_details():
    cursor.execute('''SELECT ExamDetails.name as exam_name, ExamCategoryDetails.name as sub_category, SubjectDetails.name as subject, TopicDetails.name as topic FROM ExamDetails 
LEFT JOIN ExamCategoryDetails ON ExamDetails.id = ExamCategoryDetails.exam_id 
LEFT JOIN SubjectDetails ON ExamCategoryDetails.id = SubjectDetails.exam_category_id
LEFT JOIN TopicDetails ON SubjectDetails.id = TopicDetails.sub_id''')
    results = [{"exam": exam_name, "sub_category":sub_category, "subject":subject , "topic":topic} for (exam_name, sub_category, subject, topic) in cursor]
    return results
