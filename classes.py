class User:

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def add_userToDatabase(self, db):
        # add new user to database
        db.execute("INSERT INTO users (username, password) VALUES (:username,:password)",{"username": self.username, "password": self.password})
        db.commit()

class Book:
    def __init__(self, title, author, isbn, year, rating):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year
        self.rating = rating

    def add_bookToDatabase(self, db):
        # add new book to database
        db.execute("INSERT INTO books (title, author, isbn, year) VALUES (:title,:author,:isbn,:year)",{"title": self.title, "author": self.author, "isbn": self.isbn, "year": self.year})
        db.commit()

    def lookupBookInDatabase(self,db):
        titleInput = True
        authorInput = True
        isbnInput = True

        if self.title == "":
            self.title = "noTitleInput"
            titleInput = False
        if self.author == "":
            self.author = "noAuthorInput"
            authorInput = False
        if self.isbn == "":
            self.isbn = "000000000"
            isbnInput = False

        if (titleInput == False and authorInput == False and isbnInput == False):
            print(f"No book input. Please enter a title, author or isbn")
            bookResult = None
        elif (titleInput == True or authorInput == True or isbnInput == True): 
            bookResult = db.execute("SELECT * FROM books WHERE  title LIKE :title OR author LIKE :author OR CAST(isbn AS TEXT) LIKE :isbn",{"title": "%" + self.title + "%", "author": "%" + self.author + "%", "isbn": "%" + self.isbn + "%"})
        return bookResult        