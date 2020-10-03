import csv
import os

from flask import Flask, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from classes import Book



# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
Session(app)

# Set up database on heroku
engine = create_engine(os.getenv("DATABASE_URL"))

# make sure user sessions are seperated from another if happening at the same time
db = scoped_session(sessionmaker(bind=engine))


def main():
    f = open("books.csv")
    reader = csv.reader(f)
    next(f) #skip first line to avoid reading in column titles
    for isbn, title, author, year in reader:
        book = Book(title = title, author = author, isbn=isbn, year=year, rating=0)

        # check if isbn is a number
        isbncheck_int = is_int(book.isbn)
        if isbncheck_int == True:
            ## check if isbn already exists in database
            #isbncheck_existance = is_inDb(book.isbn)
            #if isbncheck_existance == False:
                book.add_bookToDatabase(db)
            #    #print(f"Added the following book to the database: Author: {author}, title: {title}, ISBN: {isbn}, year: {year}")
            #else:
            #    print(f"isbn already exists in database, book not added")
        else:
            print(f"isbn does not consist of numbers only")
    db.commit()
    print(f"import finished")

# check if isbn consist only of numbers
def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# check if isbn already exists in database
def is_inDb(isbn):
    if db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).rowcount > 0:
        return True
    else: return False


if __name__ == "__main__":
        with app.app_context():
            main()