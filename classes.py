class User:

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def add_userToDatabase(self, db):
        # add new user to database
        db.execute("INSERT INTO users (username, password) VALUES (:username,:password)",{"username": self.username, "password": self.password})
        db.commit()
