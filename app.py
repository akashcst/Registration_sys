from flask import Flask,render_template,redirect,url_for,request,jsonify
import os
import sqlite3
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired,Email,Length
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash , check_password_hash
from flask_login import LoginManager,login_required,UserMixin,current_user,logout_user,login_user

project_dir = os.path.dirname(os.path.abspath(__file__))


app = Flask(__name__)
app.config['SECRET_KEY']="THISISSECRET"
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///site.db"
db=SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

Bootstrap(app)

class User(UserMixin,db.Model):

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(15))
    email = db.Column(db.String(80),unique=True)
    password = db.Column(db.String(80))

    def __repr__(self):

        return f"User('{self.username}','{self.email}')"


@login_manager.user_loader

def load_user(user_id):
    return  User.query.get(int(user_id))








class LoginForm(FlaskForm):
    username=StringField('username',validators=[InputRequired(),Length(min=4,max=80)])
    password=PasswordField('password',validators=[InputRequired(), Length(min=4,max=80)])
    remember=BooleanField('remember me')


class RegistrationForm(FlaskForm):
    email=StringField('email',validators=[InputRequired(),Email(message="invalid"),Length(max=50)])
    username=StringField('username',validators=[InputRequired(),Length(min=4,max=80)])
    password=PasswordField('password',validators=[InputRequired(), Length(min=4,max=80)])





@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():

    form=LoginForm()
    if form.validate_on_submit():

        user=User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user,remember=True)
                return redirect(url_for('dashboard'))

        return "invalid user"



    return render_template('login.html',form=form)





@app.route('/signup',methods=['GET','POST'])
def signup():

    form = RegistrationForm()

    # email = request.form['email']
    # username = request.form['username']
    # password = request.form['password']
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method="sha256")
        new_user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        # if username and email and password:
        #     newName = username
        #     return jsonify({'name', newName})
        #
        # return jsonify({'error': "missing data"})
        return '<h1> new user has been created<h1>'
    return render_template('signup.html',form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html',username=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/process',methods=['POST'])
def process():
    # form=RegistrationForm()
    email=request.form['email']
    username=request.form['username']
    password=request.form['password']

    if username and email and password:
        newName=username[::-1]
        return jsonify ({'name', newName})
    return jsonify({'error':"missing data"})



if __name__ == '__main__':
    app.run(debug=True)
