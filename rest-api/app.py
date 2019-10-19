from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'Cluster0'
app.config['MONGO_URI'] = 'mongodb+srv://Shinvalor:MxUagWGzWGG9l0cU@cluster0-z8nxe.mongodb.net/test?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route('/')
def home():
    return "This is home"

@app.route('/application', methods=['GET'])
def get_all_applications():
    applications = mongo.db.applications 

    output = []

    for application in applications.find():
        output.append({'first_name': application['first_name'], 'last_name': application['last_name'], 'region': application['region'], 'candidate_type': application['candidate_type'], 'academic_year': application['academic_year'], 'major': application['major'], 'career_interest': application['career_interest'], 'gpa': application['gpa'], 'college_name': application['college_name'], 'phone_number': application['phone_number'], 'email': application['email']})

    return jsonify({'result' : output})

@app.route('/application', methods=['POST'])
def add_application():
    application = mongo.db.applications

    first_name = request.json['first_name']
    last_name = request.json['last_name']
    region = request.json['region']
    candidate_type = request.json['candidate_type']
    academic_year = request.json['academic_year']
    major = request.json['major']
    career_interest = request.json['career_interest']
    gpa = request.json['gpa']
    college_name = request.json['college_name']
    phone_number = request.json['phone_number']
    email = request.json['email']

    application_id = application.insert({'first_name': first_name, 'last_name': last_name, "region": region,"candidate_type": candidate_type, "academic_year": academic_year, "major": major, "career_interest": career_interest, "gpa": gpa, "college_name": college_name, "phone_number": phone_number, "email": email})
    new_application = application.find_one({'_id' : application_id})

    return jsonify({'result' : "success"})

@app.route('/resume/<filename>', methods=['GET'])
def get_all_resumes(filename):
    return mongo.send_file(filename)

@app.route('/resume', methods=['POST'])
def add_resume():
    if 'resume' in request.files:
        resume = request.files['resume']
        mongo.save_file(resume.filename,resume)
    return "Done"


if __name__ == '__main__':
    app.run(debug=True)