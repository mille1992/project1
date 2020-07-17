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

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    mainHeading = "Welcome to Bookuru!"
    return render_template("index.html", mainHeading = mainHeading)

@app.route("/registration")
def registration():
    mainHeading = "Please register here"
    return render_template("registration.html", mainHeading = mainHeading)

@app.route("/bookSearch")
def bookSearch():
    mainHeading = "Look up your next book"
    return render_template("bookSearch.html", mainHeading = mainHeading)

@app.route("/login", methods =["POST"])
def login():
    mainHeading = "Thanks for logging in"
    username = request.form.get("username")
    password = request.form.get("password")
    return render_template("login.html", mainHeading = mainHeading, username = username, password = password)
