from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session

app = Flask(__name__, static_url_path='/static')


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