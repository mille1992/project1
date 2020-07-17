import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

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

@app.route("/")
def index():
    mainHeading = "Welcome to Bookuru!"
    username = "defaultUser"

    if username == "defaultUser":
        loggedInUserTxt = "Not logged in yet"
    else:
        loggedInUserTxt = f"Logged in as: {username}"
    return render_template("index.html", mainHeading = mainHeading, loggedInUserTxt = loggedInUserTxt)

@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
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

    # ----- check whether username and password are part of the db -----
    # ...
    # -------------

    if username == "defaultUser":
        loggedInUserTxt = "Not logged in yet"
    else:
        loggedInUserTxt = f"Logged in as: {username}"

    return render_template("login.html", mainHeading = mainHeading, username = username, password = password, loggedInUserTxt = loggedInUserTxt)

@app.route("/bookSearch")
def bookSearch():
    mainHeading = "Look up your next book"
    return render_template("bookSearch.html", mainHeading = mainHeading)