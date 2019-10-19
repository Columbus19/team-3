from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session, Response
from flask import Flask, request, redirect, jsonify
import os
from werkzeug.utils import secure_filename
import time
import scanImage


app = Flask(__name__, static_url_path='/static')




app.config["UPLOAD_FOLDER"] = "resumes"
PATH_TO_TEST_IMAGES_DIR = './images'

@app.route("/upload")
def uploadFile():
    return render_template("resumeUpload.html")

# save the image as a picture
@app.route('/image', methods=['POST'])
def image():

    i = request.files['image']  # get the image
    f = ('%s.jpeg' % time.strftime("%Y%m%d-%H%M%S"))
    i.save('%s/%s' % (PATH_TO_TEST_IMAGES_DIR, f))
    scanImage.save_image('%s/%s' % (PATH_TO_TEST_IMAGES_DIR, f))
    return Response("%s saved" % f)

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
	return "Student Registration"

@app.route('/alumniRegistration', methods=['GET'])
def alumniRegistration():
	return "alumni Registration"



@app.route('/test', methods=['GET'])
def test():
	return "<h1>testing hey</h1>"

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)

