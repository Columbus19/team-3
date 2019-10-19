from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session, Response
from flask_pymongo import PyMongo
import os
from werkzeug.utils import secure_filename
import time
try:
    from keys import *
except:
    pass
try:
    from flask_sockets import Sockets
except:
    pass
import requests
import datetime
#import scanImage


app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'Cluster0'
app.config['MONGO_URI'] = 'mongodb+srv://Shinvalor:MxUagWGzWGG9l0cU@cluster0-z8nxe.mongodb.net/test?retryWrites=true&w=majority'

mongo = PyMongo(app)

sockets = Sockets(app)



emails = {
"jpmc.com": "JP Morgan & Chase",
"facebook.com": "Facebook",
"google.com": "Google",
"facebook.com": "Facebook",
}

SIGN_UP_MESSAGE = """
Thanks for signing up with INROADS, {0}!

You are now subscribed to our automated status messages."""

CLIENT_SUCCESS_PAGE = """
<div class="text-center">
    <!-- Button HTML (to Trigger Modal) -->
    <a href="#myModal" class="trigger-btn" id="openVal" data-toggle="modal"></a>
</div>

<!-- Modal HTML -->
<div id="myModal" class="modal show">
    <div class="modal-dialog modal-confirm">
        <div class="modal-content">
            <div class="modal-header">
                <div class="icon-box" style="background-color: {1}">
                    <i class="material-icons">&#xE876;</i>
                </div>              
                <h4 class="modal-title">Awesome!</h4>   
            </div>
            <div class="modal-body">
                <p class="text-center">{0}</p>
            </div>
            <div class="modal-footer">
                <button style="background: {1}" class="btn btn-success btn-block" data-dismiss="modal">OK</button>
            </div>
        </div>
    </div>
</div> 
"""

student_info = {
}

LOGINS = []

app.config["UPLOAD_FOLDER"] = "resumes"
PATH_TO_TEST_IMAGES_DIR = './images'

HISTORY = ["progress"]

@sockets.route('/echo')
def echo_socket(ws):
    prev = "AYYY"
    while True:
        #message = ws.receive()
        if HISTORY[-1] != prev:
            if HISTORY[-1] == "progress":
                message = "You application is currently in progress"
                ws.send(CLIENT_SUCCESS_PAGE.format(message, "#ffc107"))
            elif HISTORY[-1] == "approved":
                message = "Your application has been approved"
                ws.send(CLIENT_SUCCESS_PAGE.format(message, "#5cb85c"))
            prev = HISTORY[-1]
        time.sleep(.1)

@app.route("/upload")
def uploadFile():
    return render_template("resumeUpload.html")

@app.route("/change")
def change():
    if HISTORY[-1] != "approved":
        HISTORY[-1] = "approved"
    else:
        HISTORY[-1] = "progress"
    return HISTORY[-1]

# save the image as a picture
@app.route('/image', methods=['POST'])
def image():

    i = request.files['image']  # get the image
    f = ('%s.jpeg' % time.strftime("%Y%m%d-%H%M%S"))
    i.save('%s/%s' % (PATH_TO_TEST_IMAGES_DIR, f))
    scanImage.save_image('%s/%s' % (PATH_TO_TEST_IMAGES_DIR, f))
    return Response("%s saved" % f)

@app.route('/admin', methods=['GET'])
def admin():
    return render_template("admin.html")

# def modify_resume(resumeFile):

@app.route("/sendfile", methods=["POST"])
def send_file():
    fileob = request.files["file2upload"]
    filename = secure_filename(fileob.filename)
    save_path = "{}/{}".format(app.config["UPLOAD_FOLDER"], filename)
    fileob.save(save_path)

    # open and close to update the access time.
    with open(save_path, "r") as f:
        pass

    return "successful_upload"

@app.route("/filenames", methods=["GET"])
def get_filenames():
    filenames = os.listdir("resumes/")

    #modify_time_sort = lambda f: os.stat("uploads/{}".format(f)).st_atime

    def modify_time_sort(file_name):
        file_path = "resumes/{}".format(file_name)
        file_stats = os.stat(file_path)
        last_access_time = file_stats.st_atime
        return last_access_time

    filenames = sorted(filenames, key=modify_time_sort)
    return_dict = dict(filenames=filenames)
    return jsonify(return_dict)

@app.route('/', methods=['GET'])
def index():
	return render_template("index.html")

@app.route('/student', methods=['GET'])
def student():
	return render_template("student.html")

@app.route('/studentRegistration', methods=['GET'])
def studentRegistration():
	return render_template("student_register.html")

@app.route('/alumniRegistration', methods=['GET'])
def alumniRegistration():
	return render_template("client_login.html")

@app.route('/client_login', methods=['GET'])
def client_login_page():
    return render_template("client_login.html")

@app.route('/test', methods=['GET'])
def test():
	return "<h1>testing hey</h1>"

def send_text(body, number=8645674106):
    number = str(number)
    headers = {
        'Authorization': 'Bearer {}'.format(STD_KEY),
    }

    data = {
      'to': number,
      'body': body
    }

    response = requests.post('https://utils.api.stdlib.com/sms@1.0.11/', headers=headers, data=data)

@app.route('/login', methods=['GET'])
def login():
	return render_template("login.html")

@app.route('/submitPerson', methods=['GET'])
def submitPerson():
    send_text(SIGN_UP_MESSAGE.format(request.args.get("firstname")),request.args.get("phoneNumber")) 
    return redirect(url_for('con'))
    return jsonify(request.args)

@app.route('/contactmentor', methods=['GET'])
def contactmentor():
	return render_template("contact_mentor.html")

@app.route('/student_login', methods=['GET'])
def student_login():
	return render_template("student_login.html")

@app.route('/LDA', methods=['GET'])
def LDA():
    return render_template("LDA.html")

@app.route('/congrats', methods=['GET'])
def con():
	return render_template("congrats.html")

@app.route('/con', methods=['GET'])
def congrats():
	return render_template("congrats.html")

@app.route('/student_info', methods=["GET"])
def get_student_info():
    x = request.args.get('student', "")
    return jsonify(student_info[x])

@app.route('/clientDashboard', methods=['GET'])
def clientDashboard():
    recruiterCompany = request.args.get('user', "")
    if "@" in recruiterCompany:
        for k, v in emails.iteritems():
            if recruiterCompany.partition("@")[2].lower() == k.lower():
                recruiterCompany = v
    
    LOGINS.append(recruiterCompany)

    return render_template("clientDashboard.html", company=recruiterCompany)

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
	app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)

