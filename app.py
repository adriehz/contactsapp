from flask import Flask, render_template, request, redirect
import smtplib
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'
# Initialize the database
db = SQLAlchemy(app)

#Create db model
class Friends(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200),nullable=False)
	lastname = db.Column(db.String(200),nullable=False)
	email = db.Column(db.String(200),nullable=False)
	company = db.Column(db.String(200),nullable=True)
	phone = db.Column(db.String(10),nullable=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

#Create a function to return a string when we add something
def __repr__(self):
	return '<Name %r>' % self.id

subscribers = []

@app.route('/')
def index():
	title = "Contacts List"
	return render_template("index.html", title = title)


@app.route("/friends", methods=["POST","GET"])
def friends():
	title = "Contact List"

	if request.method == "POST":
		friend_name = request.form["name"]
		friend_lastname = request.form["lastname"]
		friend_email = request.form["email"]
		friend_company = request.form["company"]
		friend_phone = request.form["phone"]
		new_friend = Friends(name=friend_name, lastname=friend_lastname, email=friend_email, company=friend_company, phone=friend_phone)

		#Push to database
		try:
			db.session.add(new_friend)
			db.session.commit()
			return redirect('/friends')

		except:
			return "There was an error adding your friend...."

	else:
		friends = Friends.query.order_by(Friends.date_created)
		return render_template("friends.html", title=title, friends=friends)

@app.route("/update/<int:id>", methods=["POST","GET"])
def update(id):
	friend_to_update = Friends.query.get_or_404(id)

	if request.method == "POST":
		friend_to_update.name = request.form["name"]
		friend_to_update.lastname = request.form["lastname"]
		friend_to_update.email = request.form["email"]
		friend_to_update.company = request.form["company"]
		friend_to_update.phone = request.form["phone"]
		try:
			db.session.commit()
			return redirect('/friends')
		except:
			return "There was a problem updating your friend"

	else:
		return render_template("/update.html", friend_to_update=friend_to_update)

@app.route('/delete/<int:id>')
def delete(id): 
	friend_to_delete = Friends.query.get_or_404(id)

	try:
		db.session.delete(friend_to_delete)
		db.session.commit()
		return redirect('/friends')

	except:	
		return "There was a problem deleting that friend"










