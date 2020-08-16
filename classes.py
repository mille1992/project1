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
