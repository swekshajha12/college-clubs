from flask import Flask, render_template,flash,url_for,request,redirect
from contentmgmt import content
from databaseconnection import connections#,check,insert
from wtforms import Form,validators,StringField,PasswordField
#from checkredundantusers import check,insert
c,conn=connections()

def check(data):
	eml=data[1]
	if eml:
		c.execute("select email from user where email=:eml",{"eml":eml})
		x=c.fetchall()
		if len(x)>0:
			return 0
		del x
	if data[2]:
			
		uname=data[2]
		c.execute("select username from user where username=:uname",{"uname":uname})
		x=c.fetchall()
		if len(x)>0:
			return 0
		
	return 1
def insert(data):
	if check(data)==1:
		c.execute('insert into user values(?,?,?,?)',data)
		conn.commit()
		conn.close()
		return 1
	return 0			
#data=['aa','swechhajha12@gmail.com','abc','sdkd']
#print(insert(data))
app = Flask(__name__)
app.secret_key = 'some_secret'

cont=content()

class Registration_Form(Form):
	name = StringField('name', validators=[validators.input_required()])
	email = StringField('email', validators=[validators.input_required()])
	username = StringField('username', validators=[validators.input_required()])
	password = PasswordField('Password', validators=[validators.input_required()])
	
	
		

@app.route('/')
def hello_name():
   return render_template('p.html')

   
@app.route('/dashboard/')
def dashboard():
	flash('new')
	return render_template('/dashboard.htm/', content=cont)

	
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404_not_found.html')	 
@app.errorhandler(405)
def method_not_found(e):
	return render_template('405_not_found.html')	 

@app.route('/login/',methods =['GET','POST'])
def login_page():
	error=''
	try:
		if request.method=="POST":
			attempted_username=request.form['email']
			attempted_pwd=request.form['pwd']
			#print(attempted_username)
			#print(attempted_pwd)
			#flash(attempted_pwd)
			if attempted_username=='shaikkamran3@gmail.com'  and attempted_pwd=='kaamu':
				return redirect(url_for('dashboard'))
			else:
				error='invalid credentials'
		return render_template('/login1.html/',u=error)
	except Exception as e:
		return render_template('login.html',u=error)
@app.route('/register/',methods =['GET','POST'])
def register():
	try:
		if request.method=="POST":
			attempted_Fullname=request.form['Name']
			attempted_email=request.form['email']
			attempted_username=request.form['username']
			attempted_pwd=request.form['pwd']
			data=[attempted_Fullname,attempted_email,attempted_username,attempted_pwd]
			if insert(data)==1:
				flash('registered succesfully')
				return redirect(url_for('dashboard'))

			flash('email or username already exists')
			flash('please enter your credentials again')


			
		return render_template('/register.html/',u='done')
	except Exception as e:
		return(str(e))	
@app.route('/signup/',methods=['GET','POST'])	
def sign_up():
	try:
		form=Registration_Form(request.form)
		if request.method=='POST' and form.validate():
			#c,conn=connections()
		
			name=form.name.data
			email=form.email.data
			username=form.username.data
			password=form.password.data
			data=[name,email,username,password]
			if insert(data)==1:
				flash('registered succesfully')
				return redirect(url_for('dashboard'))

			flash('email or username already exists')
			flash('please enter your credentials again')
	


		return render_template('signup.html',form=form)
			
	except Exception as e:
		return(str(e))

				
if __name__ == '__main__':
   app.run(debug = True)
