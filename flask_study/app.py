from flask import render_template
from flask import redirect
from flask import request
from flask import session
from flask import Flask

from werkzeug.utils import secure_filename

from models import Gallery
from models import Notice
from models import Refer
from models import User
from models import db

from hashlib import sha256
import shutil
import sys
import os


app = Flask(__name__)


@app.errorhandler(404)
def pageNotFound(error):
	return render_template('error/error404.html'), 404


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/admin')
def admin():
	try:
		data = User.query.filter_by(username=session['userid']).first()
		
		if data.admin:
			userArray = User.query.filter_by(accept=False).all()
			referArray = Refer.query.filter_by(hidden=1).all()
			noticeArray = Notice.query.filter_by(hidden=1).all()
			return render_template(
				'admin/admin.html',
				userArray=userArray,
				referArray=referArray,
				noticeArray=noticeArray
			)

		else:
			return '''
				<script>
					alert("You're not admin");
					history.back()
				</script>
			'''
			
	except Exception as e:
		print(sys.exc_info()[0])
		return render_template('user/login.html')


@app.route('/profile/<username>')
def profile(username):
	userInfo = User.query.filter_by(username=username).first()
	referArray = Refer.query.filter_by(username=username, hidden=1).all()
	galleryArray = Gallery.query.filter_by(username=username, hidden=1).all()

	if userInfo: # None
		return render_template(
			'page/profile.html', 
			userInfo=userInfo,
			referArray=referArray, 
			galleryArray=galleryArray
		)
	else:
		return render_template('error/error404.html')


@app.route('/myReferDelete/<idx>')
def myReferDelete(idx):
	data = Refer.query.filter_by(index=idx).first()

	data.hidden = 0

	return f'''
		<script>
			alert('글이 성공적으로 삭제 되었습니다.');
			location.href='/profile/{ data.username }';
		</script>
	'''


@app.route('/myImageDelete/<idx>')
def myImageDelete(idx):
	data = Gallery.query.filter_by(index=idx).first()

	data.hidden = 0

	return f'''
		<script>
			alert('이미지가 성공적으로 삭제 되었습니다.');
			location.href='/profile/{ data.username }';
		</script>
	'''


@app.route('/userInfoCheck/<idx>')
def  userInfoCheck(idx):
	data = User.query.filter_by(index=idx).first()

	return render_template('admin/userInfoCheck.html', userInfo=data)


@app.route('/userInfoAccept/<idx>')
def userInfoAccept(idx):
	data = User.query.filter_by(index=idx).first()
	data.accept = True

	return '''
		<script>
			location.href='/admin';
		</script>
	'''


@app.route('/logout')
def logout():
	try:
		if session['userid']:
			session.clear()
			return render_template('index.html')
		else:
			return render_template('index.html')
	except Exception as e:
		print(sys.exc_info()[0])
		return render_template('index.html')


@app.route('/login')
def login():
    return render_template('user/login.html')


@app.route('/loginAction', methods=['GET', 'POST'])
def loginAction():
	if request.method == 'GET':
		return redirect('index.html')
	else:
		email = request.form['inputEmail4']
		password = sha256(request.form['inputPassword4'].encode('utf-8')).hexdigest()
		try:
			data = User.query.filter_by(email=email, password=password).first()
			if data is not None:
				if data.accept:
					session['userid'] = data.username
					return '''
						<script>
							alert("Login Success");
							location.href='/';
						</script>
					'''
				else:
					return '''
						<script>
							alert("아직 계정 허용이 되지 않았습니다. 관리자에게 문의해 주세요!");
							location.href='/';
						</script>
					'''
			else:
				return render_template('user/login.html')
		except:
			return render_template('index.html')
			

@app.route('/register')
def register():
	return render_template('user/register.html')


@app.route('/registerAction', methods=['GET', 'POST'])
def registerAction():
	if request.method == 'GET':
		return redirect('index.html')
	else:
		classOf = request.form['inputClassOf4']
		email = request.form['inputEmail4']
		username = request.form['inputUserName4']
		password = request.form['inputPassword4']

		if not(classOf and email and username and password):
			return '''
				<script>
					alert('가입에 실패하였습니다!');
					history.back();
				</script>
			'''
		else:
			userInfo = User(classOf, email, username, password)
			userInfo.classOf = classOf
			userInfo.email = email
			userInfo.username = username
			userInfo.password = sha256(password.encode('utf-8')).hexdigest()

			db.session.add(userInfo)
			db.session.commit()

			return '''
				<script>
					location.href='/login';
				</script>
			'''


@app.route('/reference')
def reference():
	referArray = Refer.query.filter_by(hidden=1).all()
	return render_template('page/reference.html', referArray=referArray)


@app.route('/reference/<idx>/')
def referenceIdx(idx):
	referInfo = Refer.query.filter_by(index=idx).first()

	return render_template('page/referView.html', referInfo=referInfo)


@app.route('/referWrite')
def referWrite():
	return render_template('page/referWrite.html')


@app.route('/referWriteAction', methods=['GET', 'POST'])
def referWriteAction():
	if request.method == 'GET':
		return render_template('index.html')
	else:
		username = session['userid']
		subject = request.form['inputSubject4']
		content = request.form['inputContent4']
		fileName = ''
		fileHash = ''

		try:
			f = request.files['inputFile4']
			
			fileName = secure_filename(f.filename)
			
			f.save('./static/uploads/' + fileName)

			fp = open('./static/uploads/' + fileName, 'rb')
			data = fp.read()
			fp.close()
			
			fileHash = str(sha256(data).hexdigest()) + '.' + \
				fileName.split('.')[1]

			shutil.move('./static/uploads/' + fileName, \
				'./static/uploads/' + str(fileHash))

		except Exception as e: # No Attribute Error
			print(sys.exc_info()[0])

		if not(username and subject and content):
			return '''
				<script>
					alert('글 작성에 실패하였습니다!');
					history.back();
				</script>
			'''
		else:
			referInfo = Refer()
			referInfo.username =  username
			referInfo.subject = subject
			referInfo.content = content
			referInfo.fileName = fileName
			referInfo.fileHash = fileHash

			if not(username and subject and content):
				return '''
					<script>
						alert('글 작성에 실패하였습니다');
						history.back();
					</script>
				'''
			else:
				db.session.add(referInfo)
				db.session.commit()

				return '''
					<script>
						alert('글 작성 완료!!!');
						location.href='/reference'
					</script>
				'''


@app.route('/referDelete/<idx>')
def referDelete(idx):
	data = Refer.query.filter_by(index=idx).first()

	data.hidden = 0

	return '''
		<script>
			alert('글이 성공적으로 삭제 되었습니다.');
			location.href='/admin';
		</script>
	'''


@app.route('/notice')
def notice():
	noticeArray = Notice.query.filter_by(hidden=1).all()

	userInfo = ''

	try:
		username = session['userid']
		userInfo = User.query.filter_by(username=username).first()
	except Exception as e:
		print(sys.exc_info()[0])
		userInfo = ''

	return render_template('page/notice.html', noticeArray=noticeArray, userInfo=userInfo)


@app.route('/notice/<idx>/')
def noticeIdx(idx):
	noticeInfo = Notice.query.filter_by(index=idx).first()
	return render_template('page/noticeView.html', noticeInfo=noticeInfo)


@app.route('/noticeWrite')
def noticeWrite():
	userInfo = ''

	try:
		username = session['userid']
		userInfo = User.query.filter_by(username=username).first()

		if userInfo.admin:
			return render_template('page/noticeWrite.html')
		else:
			return '''
				<script>
					alert("공지사항은 어드민만 작성할 수 있습니다.");
					location.href='/';
				</script>
			'''
	except Exception as e:
		print(sys.exc_info()[0])
		return  '''
			<script>
				alert("로그인 먼저 해주세요");
				location.href='/login';
			</script>
		'''


@app.route('/noticeWriteAction', methods=['GET', 'POST'])
def noticeWriteAction():
	if request.method == 'GET':
		return render_template('index.html')
	else:
		username = session['userid']
		subject = request.form['inputSubject4']
		content = request.form['inputContent4']
		fileName = ''
		fileHash = ''

		try:
			f = request.files['inputFile4']
			
			fileName = secure_filename(f.filename)
			
			f.save('./static/uploads/' + fileName)

			fp = open('./static/uploads/' + fileName, 'rb')
			data = fp.read()
			fp.close()
			
			fileHash = str(sha256(data).hexdigest()) + '.' + \
				fileName.split('.')[1]

			shutil.move('./static/uploads/' + fileName, \
				'./static/uploads/' + str(fileHash))

		except Exception as e: # No Attribute Error
			print(sys.exc_info()[0])

		if not(username and subject and content):
			return '''
				<script>
					alert('글 작성에 실패하였습니다!');
					history.back();
				</script>
			'''

		else:
			noticeInfo = Notice()
			noticeInfo.username =  username
			noticeInfo.subject = subject
			noticeInfo.content = content
			noticeInfo.fileName = fileName
			noticeInfo.fileHash = fileHash

			db.session.add(noticeInfo)
			db.session.commit()

			return '''
				<script>
					alert('글 작성 완료!!!');
					location.href='/notice'
				</script>
			'''


@app.route('/noticeDelete/<idx>')
def noticeDelete(idx):
	data = Notice.query.filter_by(index=idx).first()

	data.hidden = 0

	return '''
		<script>
			alert('글이 성공적으로 삭제 되었습니다.');
			location.href='/admin';
		</script>
	'''


@app.route('/gallery')
def gallery():

	galleryArray = Gallery.query.filter_by(hidden=1).all()

	return render_template('page/gallery.html', galleryArray=galleryArray)


@app.route('/galleryWrite')
def galleryWrite():
	return render_template('page/galleryWrite.html')


@app.route('/galleryWriteAction', methods=['GET', 'POST'])
def galleryWriteAction():
	if request.method == 'GET':
		return render_template('index.html')
	else:
		username = session['userid']
		comment = request.form['inputComment4']
		fileName = ''
		fileHash = ''

		try:
			f = request.files['inputFile4']
			
			fileName = secure_filename(f.filename)
			
			f.save('./static/gallerys/' + fileName)

			fp = open('./static/gallerys/' + fileName, 'rb')
			data = fp.read()
			fp.close()
			
			fileHash = str(sha256(data).hexdigest()) + '.' + \
				fileName.split('.')[1]

			shutil.move('./static/gallerys/' + fileName, \
				'./static/gallerys/' + str(fileHash))

		except Exception as e: # No Attribute Error
			print(sys.exc_info()[0])

		if not(username and comment):
			return '''
				<script>
					alert('코멘트를 작성해 주세요!');
					history.back();
				</script>
			'''
		else:
			galleryInfo = Gallery()
			galleryInfo.username =  username
			galleryInfo.comment = comment
			galleryInfo.fileName = fileName
			galleryInfo.fileHash = fileHash

			db.session.add(galleryInfo)
			db.session.commit()

			return '''
				<script>
					alert('사진 작성 완료!!!');
					location.href='/gallery'
				</script>
			'''


basdir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basdir, 'db.sqlite')

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 100

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False	
app.config['SECRET_KEY'] = 'jqiowejrojzxcovnklqnweiorjqwoijroi'

db.init_app(app)
db.app = app
db.create_all()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
	