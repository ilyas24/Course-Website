from flask import Flask, session, redirect, url_for, escape, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask import flash

app=Flask(__name__)
app.secret_key='34Wksdk45223Wkdio9gb38'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assignment3.db'

db = SQLAlchemy(app)


@app.route('/')
def index():
	# check if user is logged in already
	if 'username' in session:
		# determine if it's a student user
		if student_loggedin(session['username']):
			return render_template('studentindex.html',
				uname=session['username'])
		# it must be an instructor
		else:
			return render_template('instructorindex.html', 
				uname=session['username'])
	# user is not logged in
	else:
		# go to login page (redirect)
		return redirect(url_for('login'))



# helper method to check if student is still logged in
def student_loggedin(uname):
	# get everything from student table
	query = """
				SELECT *
				FROM studentusers"""
	
	# resulting table
	table = db.engine.execute(text(query))

	# check if username is that of student
	for element in table:
		# if username exist in table, return true
		if element['username']==uname:
			return True

	return False



@app.route('/login')
def login():

	return render_template('login_register.html')


@app.route('/loginattempt', methods=['GET','POST'])
def loginAttempt():
	# if request was made through HTTP Post
	if request.method=='POST':

		# user didn't specify	
		if request.form.get('accounttype') is None:
			flash ("Choose account type to login!")
			return redirect(url_for('login'))
		# check if it's a student user to call studentlogin method
		elif request.form['accounttype']=="student":
			return studentlogin()
		# check if it's a instructor user to call instructorlogin method
		elif request.form['accounttype']=="instructor":
			return instructorlogin()
		
	else:
		return login()


@app.route('/registerattempt',methods=['GET','POST'])
def registerAttempt():
	# if request was made through HTTP Post
	if request.method=='POST':

		# user didn't specify	
		if request.form.get('accounttype') is None:
			flash ("Choose account type to register!")
			return redirect(url_for('login'))
		# check if it's a student user to call studentlogin method
		elif request.form['accounttype']=="student":
			return registerStudent()
		# check if it's a instructor user to call instructorlogin method
		elif request.form['accounttype']=="instructor":
			return registerInstructor()
		
	else:
		return redirect(url_for('studentlogin'))



# helper method for registering student 
def registerStudent():
	
	# check if user didn't add text in any field
	if (request.form['ID']=='' or request.form['username']=='' or
    request.form['password']==''):
		flash ("You must enter in all fields!")
		return redirect(url_for('login'))
	else:
		# obtain all entered info
		student_id = request.form['ID']
		uname = request.form['username']
		pword = request.form['password']
		
		# use helper method to check for existing users with same id
		# for both students and instructors
		if checkStudent_id(student_id) or checkInstructor_id(student_id):
			# show warning on login page
			flash ("ID already exists")
			return redirect(url_for('login'))

		# helper method to check for same usernames
		elif checkStudent_username(uname) or checkInstructor_username(uname):
			# show warning on login page
			flash ("Username already exists")
			return redirect(url_for('login'))

		else:
			# insert values into table
			insert_info = """
							INSERT INTO studentusers
							VALUES ('{}','{}','{}')""".format(student_id, 
								uname, pword)

			# insert new info into table
			db.engine.execute(text(insert_info))
			# automatically log user in
			return studentlogin()



# helper method for registering instructor
def registerInstructor():
	
	# check if user didn't add text in any field
	if (request.form['ID']=='' or request.form['username']=='' or
    request.form['password']==''):
		flash ("You must enter in all fields!")
		return redirect(url_for('login'))
	else:
		# obtain all entered info
		instructor_id = request.form['ID']
		uname = request.form['username']
		pword = request.form['password']
		
		# use helper method to check for existing users with same id
		# for both instructors and students
		if (checkInstructor_id(instructor_id) or 
			checkStudent_id(instructor_id)):
			# show warning on login page
			flash ("ID already exists")
			return redirect(url_for('login'))

		# helper method to check for same usernames for both instructors
		# and students
		elif checkInstructor_username(uname) or checkStudent_username(uname):
			# show warning on login page
			flash ("Username already exists")
			return redirect(url_for('login'))

		else:
			# insert values into table
			insert_info = """
							INSERT INTO instructors
							VALUES ('{}','{}','{}')""".format(instructor_id, 
								uname, pword)

			# insert new info into table
			db.engine.execute(text(insert_info))
			# automatically log user in
			return instructorlogin()


# helper method to check for pre-existing id's
def checkInstructor_id(user_id):
	# select everything from instructors table
	query = """
			SELECT *
			FROM instructors
			"""
	# this is the resulting table from query
	table = db.engine.execute(text(query))
	# loop through each row to check for existing id's
	for element in table:
		if element['id']==user_id:
			# then user exists
			return True

	# then there is no existing users with same id
	return False


# helper method to check for pre-existing usernames
def checkInstructor_username(uname):
	# select everything from instructor table
	query = """
			SELECT *
			FROM instructors
			"""
	# this is the resulting table from query
	table = db.engine.execute(text(query))
	# loop through each row to check for existing usernames
	for element in table:
		if element['username']==uname:
			# then user exists
			return True

	# then there is no existing users with same username
	return False


						
# helper method to check for pre-existing id's
def checkStudent_id(user_id):
	# select everything from studentusers table
	query = """
			SELECT *
			FROM studentusers
			"""
	# this is the resulting table from query
	table = db.engine.execute(text(query))
	# loop through each row to check for existing id's
	for element in table:
		if element['id']==user_id:
			# then user exists
			return True

	# then there is no existing users with same id
	return False


# helper method to check for pre-existing usernames
def checkStudent_username(uname):
	# select everything from studentusers table
	query = """
			SELECT *
			FROM studentusers
			"""
	# this is the resulting table from query
	table = db.engine.execute(text(query))
	# loop through each row to check for existing usernames
	for element in table:
		if element['username']==uname:
			# then user exists
			return True

	# then there is no existing users with same username
	return False

# helper method to make sure user has same id and username
def checkall(uname, user_id):
	# select everything from instructor table
	query = """
			SELECT *
			FROM instructors
			"""
	# this is the resulting table from query
	table = db.engine.execute(text(query))

	# loop through each row to check for existing usernames
	for element in table:
		if element['username']==uname and element['id']==user_id:
			# then user exists
			return True

	# then there is no existing users with same username
	return False

@app.route('/studentlogin',methods=['GET','POST'])
def studentlogin():
	# if request was made through HTTP Post
	if request.method=='POST':
		# get info from all student users
		query = """
			SELECT *
			FROM studentusers
			"""
		# resulting table
		table = db.engine.execute(text(query))
		# go through each row in table
		for element in table:
			# check if username is same as what user inputted
			if element['username']==request.form['username']:
				# check if password is same as what user inputted
				if element['password']==request.form['password']:
					session['username']=request.form['username']
	
					return render_template('studentindex.html',
						uname=session['username'])
		# included incorrect username or password then
		flash("Incorrect UserName/Password")
		return redirect(url_for('login'))

	# check if user is already logged in
	elif 'username' in session:
			# go to homepage
			return render_template('studentindex.html',
				uname=session['username'])

	# user is not logged, so redirect user to login page
	else:
		return redirect(url_for('login'))



@app.route('/instructorlogin',methods=['GET','POST'])
def instructorlogin():
	# if request was made through HTTP Post
	if request.method=='POST':
		# get all info from instructors table
		query = """
			SELECT *
			FROM instructors
			"""
		# resulting table
		table = db.engine.execute(text(query))
		# go through each row in table
		for element in table:
			# check for matching usernames from user input
			if element['username']==request.form['username']:
				# check for matching passwords
				if element['password']==request.form['password']:
					session['username']=request.form['username']
					
					return render_template('instructorindex.html',
						uname=session['username'])
		
		# included incorrect username or password then
		flash("Incorrect UserName/Password")
		return redirect(url_for('login'))

	# check if user is already logged in
	elif 'username' in session:
		# go to home page
		return render_template('studentindex.html',uname=session['username'])

	# user must've logged out, so redirect user to login page
	else:
		return redirect(url_for('login'))


@app.route('/logout')
def logout():
	# log user out
	session.pop('username', None)
	return redirect(url_for('login'))


@app.route('/lecture')
def lecture():
	# check if user is still logged in
	if 'username' in session:
		return render_template('lecture.html')
	# user is not logged in, redirect them to login
	else:
		return redirect(url_for('login'))


@app.route('/coursework')
def coursework():
	# check if user is still logged in
	if 'username' in session:
		return render_template('coursework.html')
	# user is not logged in, redirect them to login
	else:
		return redirect(url_for('login'))


@app.route('/yourmarks')
def yourmarks():
	# check if user is still logged in
	if 'username' in session:
		# get info from marks table where student's name match
		query = """
					SELECT *
					FROM marks
					where studentname='{}'""".format(session['username'])
		# resulting table
		outcome = db.engine.execute(text(query))
		return render_template('yourmarks.html',table=outcome)
	# user is not logged in, so redirect user to login
	else:
		return redirect(url_for('login'))


@app.route('/coursefeedback')
def coursefeedback():
	# check if user is still logged in
	if 'username' in session:
		# get all info from instructors table
		query = """
					SELECT *
					FROM instructors"""
		# resulting table
		outcome = db.engine.execute(text(query))
		return render_template('coursefeedback.html',table=outcome)
	# user is not logged in, so redirect user to login
	else:
		return redirect(url_for('login'))


@app.route('/updatefeedback',methods=['GET','POST'])
def updatefeedback():
	try:
		# check if user is still logged in
		if 'username' in session:
			# obtaining info from feedback form
			instr_options = request.form["instr_options"]
			comment1 = request.form["feedback1"]
			comment2 = request.form["feedback2"]
			comment3 = request.form["feedback3"]
			comment4 = request.form["feedback4"]
			comment5 = request.form["feedback5"]

			# inserting entered info into database
			query = """
						INSERT INTO feedback
						VALUES ('{}','{}','{}','{}','{}','{}')""".format(
							instr_options, comment1, comment2, comment3,
							 comment4, comment5)

			# insert into feedback table
			db.engine.execute(text(query))
			# stay on same page
			return redirect(url_for('coursefeedback'))

		# user is not logged in, so redirect user to login
		else:
			return redirect(url_for('login'))

	# anything that goes wrong
	except:
		flash ("Something went wrong! Try again")
		return redirect(url_for('coursefeedback'))


@app.route('/observefeedback',methods=['GET','POST'])
def observefeedback():
	# make sure user is still logged in
	if 'username' in session:
		# obtain inputted info
		uname = request.form['username']
		user_id = request.form['id']
		# check if user has matching id and username
		if not(checkall(uname, user_id)):
			flash ("Username and id don't match!")
			return redirect(url_for('requestfeedback'))

		# check if it's the right id
		elif not(checkInstructor_id(user_id)):
			flash ("wrong id!")
			return redirect(url_for('requestfeedback'))
		# just to make sure user inputted same username 
		# thats also is in session, so this is same user 
		elif uname != session['username']:
			flash ("wrong username!")
			return redirect(url_for('requestfeedback'))
		# this is the right user info
		else:
			query =  """
						SELECT *
						FROM feedback
						where id='{}'""".format(user_id)
			
			result =  db.engine.execute(text(query))
			return render_template('viewfeedback.html', table=result)


	# user is not logged in, so redirect user to login
	else:
		return redirect(url_for('login'))




@app.route('/requestfeedback')
def requestfeedback():
	# make sure user is still logged in
	if 'username' in session:
		return render_template('requestfeedback.html')
	# user is not logged in, so redirect user to login
	else:
		return redirect(url_for('login'))


@app.route('/marks')
def marks():
	# check if user is still logged in
	if 'username' in session:
		# get all info from marks table
		query = """
					SELECT *
					FROM marks"""
		# resulting table
		outcome = db.engine.execute(text(query))
		return render_template('studentmarks.html',table=outcome)
	# user is not logged in, so redirect user to login
	else:
		return redirect(url_for('login'))
	

@app.route('/editgrade',methods=['GET', 'POST'])
def editGrade():
	# check is user is still logged in
	if 'username' in session:
		# if request was made through HTTP Post
		if request.method=='POST':
			# obtain all chosen info
			quiz1Grade=request.form['quiz1']
			quiz2Grade=request.form['quiz2']
			quiz3Grade=request.form['quiz3']
			quiz4Grade=request.form['quiz4']
			assignment1Grade=request.form['assignment1']
			assignment2Grade=request.form['assignment2']
			assignment3Grade=request.form['assignment3']
			labsGrade=request.form['labs']
			midtermExamGrade=request.form['midtermexam']
			finalExamGrade=request.form['finalexam']
			username=request.form['username']
			# update marks table with new information
			updateGrades="""UPDATE marks
				   SET quiz1 = '{}', quiz2 = '{}', quiz3 = '{}', quiz4 = '{}',
				    assignment1 = '{}', assignment2 = '{}', assignment3 = '{}',
				    labs = '{}', midtermexam = '{}', finalexam = '{}'  
				   WHERE studentname = '{}'""".format(quiz1Grade, quiz2Grade,
				    quiz3Grade, quiz4Grade, assignment1Grade, 
				    assignment2Grade, assignment3Grade, labsGrade,
				     midtermExamGrade, finalExamGrade, username);
			# execute query
			db.engine.execute(text(updateGrades))
			# stay on same page
			return redirect(url_for('marks'))

	# user is not logged in, so redirect user to login
	else:
		return redirect(url_for('login'))



@app.route('/remarkrequest',methods=['GET','POST'])
def remarkRequest():
	# check if user is still loggen in
	if 'username' in session:
		# get what user selected as assessment option
		a_option = request.form["assessment"]
		# obtain student username
		username = session['username']
		# obtain the request that student submitted
		re_request = request.form['request']
		# insert new info into table
		query = """
					INSERT INTO remarkrequests
					VALUES ('{}','{}','{}')""".format(username, a_option,
						re_request)

		db.engine.execute(text(query))
		return redirect(url_for('yourmarks'))

	# user is not logged in, so redirect user to login
	else:
		return redirect(url_for('login'))
	


@app.route('/viewrequest')
def viewRequest():
	# check if user is still logged in
	if 'username' in session:
		# get all info from remarkrequests table
		query =  """
					SELECT *
					FROM remarkrequests"""
		# resulting table
		outcome =  db.engine.execute(text(query))
		return render_template('requests.html', table=outcome)
	
	# user is not logged in, so redirect user to login
	else:
		return redirect(url_for('login'))
			

@app.route('/courseteam')
def courseteam():
	# check if user is still logged in
	if 'username' in session:
		return render_template('courseteam.html')
	# user is not logged in, redirect them to login
	else:
		return redirect(url_for('login'))


@app.route('/resources')
def resources():
	# check if user is still logged in
	if 'username' in session:
		return render_template('resources.html')
	# user is not logged in, redirect them to login
	else:
		return redirect(url_for('login'))


@app.route('/news')
def news():
	# check if user is still logged in
	if 'username' in session:
		return render_template('news.html')
	# user is not logged in, redirect them to login
	else:
		return redirect(url_for('login'))


@app.route('/calendar')
def calendar():
	# check if user is still logged in
	if 'username' in session:
		return render_template('calendar.html')
	# user is not logged in, redirect them to login
	else:
		return redirect(url_for('login'))



if __name__ == "__main__":
	 app.run(debug=True,host='0.0.0.0')
	 