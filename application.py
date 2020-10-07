import os
import sys
import requests 

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
db = db()


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
            mainHeading = f"Welcome, {username}! Find your book."
            loggedInUserTxt = f"Logged in as: {username}"
            return render_template("bookSearch.html", mainHeading = mainHeading, loggedInUserTxt = loggedInUserTxt) 
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
        mainHeading = "Your Registration was successful. Please login."
        return render_template("index.html", mainHeading = mainHeading)
    else:
        mainHeading = "Please register here"
        return render_template("registration.html", mainHeading = mainHeading)

# Log user out of this session
@app.route("/logout")
def logout():
    # check if a user is logged in
    if session.get('username') is None: # no user logged in
        return redirect(url_for('index'))
    else: # user logged in will be logged out
        session.clear()
        mainHeading = "You are logged out, now. Do you want to log in again?"
        return render_template('index.html', mainHeading = mainHeading)


# route to display the book details
@app.route("/bookList", methods=["GET", "POST"])
def bookList():
    loggedInUserTxt = f"Logged in as: {session['username']}"
    mainHeading = "Here are the books resulting from your seach:"
    
    # get bookdetails that were searched
    bookTitleInput = request.form.get("bookTitle")
    bookAuthorInput = request.form.get("bookAuthor")
    bookISBNInput = request.form.get("bookISBN")
    print(f"{bookTitleInput} {bookAuthorInput} {bookISBNInput}")

    # look for book by using function from the Book object
    searchedBook = Book(bookTitleInput, bookAuthorInput, bookISBNInput, 0000, 0)
    resultedBooks = searchedBook.lookupBookInDatabase(db)
    contentCheck_resultedBooks = resultedBooks.rowcount


    if resultedBooks is None: # no search argument was handed over
        mainHeading = f"You did not put in any search arguments, please try again." 
        return render_template("bookSearch.html", mainHeading = mainHeading, loggedInUserTxt = loggedInUserTxt)
    elif contentCheck_resultedBooks == 0:
        mainHeading = f"We could not find that book, please try again." 
        return render_template("bookSearch.html", mainHeading = mainHeading, loggedInUserTxt = loggedInUserTxt)
    else: # at least one book could be found -> display list of found books
        return render_template("bookList.html", mainHeading = mainHeading, loggedInUserTxt = loggedInUserTxt, resultedBooks = resultedBooks)

@app.route("/bookDetail/<int:book_isbn>", methods=["GET", "POST"])
def bookDetail(book_isbn):
    checkBookInGRavl = False
    # when accessing bookDetails.html after clicking on a specific book 
    if request.method == "GET": 
        mainHeading = f"Here is some more detailed info on your book:"
        loggedInUserTxt = f"Logged in as: {session['username']}"
        
        # look up isbn number in books db
        bookDetails = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": book_isbn})    
        # ++++++++++ INFO ++++++++++++
        # When accessing the following for-loop the content of bookDetails disappears 
        # because the SQL object gets discarded after all rows have been accessed
        # ++++++++++++++++++++++++++++
        for book_cnt in bookDetails:
            bookDetail = book_cnt
        book_id = bookDetail.book_id

        bookReviews = db.execute("SELECT * FROM reviews WHERE book_id = :book_id", {"book_id": book_id})
       
        # look up average rating and number of reviews via review_counts on GoodReads via API
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": os.getenv("GOODREADSKEY"), "isbns": book_isbn})
        

        if res.status_code == 200:
            checkBookInGRavl = True
            statisticsGR = res.json()
        else: 
            statisticsGR = []

        db.commit()

        return render_template("bookDetails.html", mainHeading = mainHeading, loggedInUserTxt = loggedInUserTxt, bookDetails = bookDetail, bookReviews = bookReviews, checkBookInGRavl = checkBookInGRavl, statisticsGR = statisticsGR)

    # when accessing bookDetails.html after submitting a review
    if request.method == "POST": #when accessing bookDetails.html after reviewing
        mainHeading = f"Here is some more detailed info on your book:"
        loggedInUserTxt = f"Logged in as: {session['username']}"
        
        # Find out user_id
        username = session['username']
        userList = db.execute("SELECT * FROM users WHERE username = :username", {"username": username}) 
        for user_cnt in userList:
            user = user_cnt
        user_id = user.user_id

        # look up isbn number in books db in order to find book_id
        bookDetails = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": book_isbn})    
        # ++++++++++ INFO ++++++++++++
        # When accessing the following for-loop the content of bookDetails disappears 
        # because the SQL object gets discarded after all rows have been accessed
        # ++++++++++++++++++++++++++++
        for book_cnt in bookDetails:
            bookDetail = book_cnt
        book_id = bookDetail.book_id

        # get review comment and rating from the posted review 
        reviewTxt = request.form.get("review")
        reviewRating = request.form.get("rating")

        # insert review into database
        # check whether book was already reviewed by this user
        if db.execute("SELECT * FROM reviews WHERE book_id = :book_id AND submitting_user = :submitting_user", {"book_id": book_id, "submitting_user": user_id}).rowcount > 0:
            mainHeading = f"This book was already reviewed by you, we therefore did not add another review. Thanks for your participation!"
        else:
            db.execute("INSERT INTO reviews (rating, review, book_id, submitting_user) VALUES (:rating, :review, :book_id, :submitting_user)",{"rating": reviewRating, "review": reviewTxt, "book_id": book_id, "submitting_user": user_id})
        

        # look up all reviews and save them in bookReviews (SQLAlchemy ResponseObject)
        bookReviews = db.execute("SELECT * FROM reviews WHERE book_id = :book_id", {"book_id": book_id})

        # look up average rating and number of reviews via review_counts on GoodReads via API
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": os.getenv("GOODREADSKEY"), "isbns": book_isbn})
        

        if res.status_code == 200:
            checkBookInGRavl = True
            statisticsGR = res.json()
        else: 
            statisticsGR = []
  
        

        
        db.commit()

        return render_template("bookDetails.html", mainHeading = mainHeading, loggedInUserTxt = loggedInUserTxt, bookDetails = bookDetail, bookReviews = bookReviews, checkBookInGRavl = checkBookInGRavl, statisticsGR = statisticsGR)
