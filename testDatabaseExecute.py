import os
import sys

from flask import Flask, session, render_template, request, redirect, url_for
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

# Set up database on heroku
engine = create_engine(os.getenv("DATABASE_URL"))

# make sure user sessions are seperated from another if happening at the same time
db = scoped_session(sessionmaker(bind=engine))


def main():
    bookDetails = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": 8129115301})    
    bookResult = db.execute("SELECT * FROM books WHERE book_id=1000")
    booksArr = []
    for books in bookDetails:
        booksArr.append(books)
        print(f"{books.title}")



if __name__ == "__main__":
    main()
