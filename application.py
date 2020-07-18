import os
import sys

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from classes import *

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database on hekoru
engine = create_engine(os.getenv("DATABASE_URL"))

# make sure user sessions are seperated from another if happening at the same time
db = scoped_session(sessionmaker(bind=engine))



# Handler for Login of User
@app.route("/", methods=["GET","POST"])
def index():
    mainHeading = "Welcome to Bookuru!"
    username = "defaultUser"

    # display text which user is logged in
    if username == "defaultUser":
        loggedInUserTxt = ""
    else:
        loggedInUserTxt = f"Logged in as: {username}"

    # When user tries to login
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # check whether password and username can be found in the database
        if db.execute("SELECT * FROM users WHERE username = :username AND password = :password", {"username":username, "password":password}).rowcount == 0:
            mainHeading = "Username or Password not found. Please try again."
            return render_template("index.html", mainHeading = mainHeading, loggedInUserTxt = loggedInUserTxt)
        # welcome user, if password and username can be found
        else:
            mainHeading = f"Welcome, {username}"
            loggedInUserTxt = f"Logged in as: {username}"
            return render_template("index.html", mainHeading = mainHeading, loggedInUserTxt = loggedInUserTxt) 
    # When user is not logged in yet or already logged in and accesses the home screen
    
    
    # !! not working properly yet. Sessions need to be included here !!
    else:
        if username ==  "defaultUser":
            return render_template("index.html", mainHeading = mainHeading, loggedInUserTxt = loggedInUserTxt)
        else:
            mainHeading = f"Welcome, {username}"
            loggedInUserTxt = f"Logged in as: {username}"
            return render_template("index.html", mainHeading = mainHeading, loggedInUserTxt = loggedInUserTxt) 




# Registration Process
@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        # get username and password from form on registration page
        username = request.form.get("username")
        password = request.form.get("password")
        print(f"password: {password}", file=sys.stderr)

        # create new user object and assign username and password to it
        user = User(username = username, password = password)

        # check if password and username were provided
        if password == "" or password is None or username == "" or username is None:
            mainHeading = f"Please enter a password and username"
            return render_template("registration.html", mainHeading = mainHeading)

        # check if username already exists
        if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount > 0:
            mainHeading = f"The username -> {username} <- is already taken, please choose a different username"
            return render_template("registration.html", mainHeading = mainHeading)

        # add new user to database
        user.add_userToDatabase(db)

        # display success message
        mainHeading = "Your Registration was successful"
        return render_template("index.html", mainHeading = mainHeading)
    else:
        mainHeading = "Please register here"
        return render_template("registration.html", mainHeading = mainHeading)





@app.route("/login", methods =["POST"])
def login():
    username = "defaultUser"

    username = request.form.get("username")
    password = request.form.get("password")
    mainHeading = f"Welcome,  {username} . Thanks for logging in!"

    if username == "defaultUser":
        loggedInUserTxt = "Not logged in yet"
    else:
        loggedInUserTxt = f"Logged in as: {username}"

    return render_template("login.html", mainHeading = mainHeading, username = username, password = password, loggedInUserTxt = loggedInUserTxt)

@app.route("/bookSearch")
def bookSearch():
    mainHeading = "Look up your next book"
    return render_template("bookSearch.html", mainHeading = mainHeading)