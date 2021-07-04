from flask import Flask
from flask import session
from flask import request
from flask import redirect
from flask import render_template

from werkzeug.utils import secure_filename

from models import LoginForm
from models import User
from models import db

import os


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('user/login.html')


@app.route('/loginAction', methods=['GET', 'POST'])
def loginAction():
	
	if request.method == 'GET':
		return redirect('index.html')
	else:
		pass
			

@app.route('/register')
def join():
	return render_template('user/register.html')


@app.route('/registerAction', methods=['GET', 'POST'])
def register():
	
	if request.method == 'GET':
		return redirect('index.html')
	else:
		classOf = request.form['inputClassOf4']
		email = request.form['inputEmail4']
		username = request.form['inputUserName4']
		passwd = request.form['inputPassword4']

		if not(classOf and email and username and passwd):
			return '입력되지 않은 정보가 있습니다.'
		else:
			userInfo = User(classOf, email, username, passwd)
			userInfo.classOf = classOf
			userInfo.email = email
			userInfo.username = username
			userInfo.password = passwd

			db.session.add(userInfo)
			db.session.commit()

			return '회원가입 성공'

		return redirect('index.html')


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/fileUpload', methods = ['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		f = request.files['file']
		f.save('./uploads/' + secure_filename(f.filename))
		return render_template('check.html')
	else:
		return "Not"


basdir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basdir, 'db.sqlite')

app.config['MAX_CONTENT_LENGTH'] = 1024 * 100

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'jqiowejrojzxcovnklqnweiorjqwoijroi'

db.init_app(app)
db.app = app
db.create_all()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)