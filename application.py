import os
import sys

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from classes import *
from uuid import uuid4

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database on heroku
engine = create_engine(os.getenv("DATABASE_URL"))

# make sure user sessions are seperated from another if happening at the same time
db = scoped_session(sessionmaker(bind=engine))



# Handler for Login of User
@app.route("/", methods=["GET","POST"])
def index():
    mainHeading = "Welcome to Bookuru!"

    # When user tries to login
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        session['username'] = username
        session['usernumber'] = uuid4()

        # check whether password and username can be found in the database
        if db.execute("SELECT * FROM users WHERE username = :username AND password = :password", {"username":username, "password":password}).rowcount == 0:
            mainHeading = "Username or Password not found. Please try again."
            loggedInUserTxt = ""
            return render_template("index.html", mainHeading = mainHeading, loggedInUserTxt = loggedInUserTxt)

        # welcome user, if password and username can be found
        else:
            username = username
            mainHeading = f"Welcome, {username}!"
            loggedInUserTxt = f"Logged in as: {username}"
            return render_template("index.html", mainHeading = mainHeading, loggedInUserTxt = loggedInUserTxt) 
    else:
        if session.get('username') == None: # user clicks home button / enters webpage without being logged in
            mainHeading = "Welcome to Bookuru! Please login."
            return render_template("index.html", mainHeading = mainHeading)
        else:
            mainHeading = f"Find your book" # user clicks home button / enters webpage while being logged in
            loggedInUserTxt = f"Logged in as: {session['username']}"
            return render_template("bookSearch.html", mainHeading = mainHeading, loggedInUserTxt = loggedInUserTxt)



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

# Log user out of this session
@app.route("/logout")
def logout():
    if session.get('username') is None:
        return redirect(url_for('index'))
    else:
        session.clear()
        mainHeading = "You are logged out, now. Do you wan to log in again?"
        return render_template('index.html', mainHeading = mainHeading)


# route to display the book details
@app.route("/bookList", methods=["GET", "POST"])
def bookList():
    loggedInUserTxt = f"Logged in as: {session['username']}"
    mainHeading = "Here are the detailed information about your book:"
    bookTitleInput = request.form.get("bookTitle")
    bookAuthorInput = request.form.get("bookAuthor")
    bookISBNInput = request.form.get("bookISBN")

    # --- implementiere hier Datenbankabfrage über Bücher --- #
    #       .............................................
    #       ............................................. 
    # ------------------------------------------------------- #

    # --- implementiere hier Visualisierung der Infos der gefundenen Bücher --- #
    #       .............................................
    #       ............................................. 
    # ------------------------------------------------------- #

    return render_template("bookList.html", mainHeading = mainHeading, loggedInUserTxt = loggedInUserTxt, bookTitle = bookTitleInput, bookAuthor = bookAuthorInput, bookISBN = bookISBNInput)

