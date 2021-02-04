import datetime
import uuid
from common.database import Database
from flask import Flask, session
from models.coronadata import CoronaData


class User(object):
    # Constructer for the User object (For login)
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    # Find the user by using the username
    def get_by_email(cls, email):
        data = Database.find_one("users", {"email": email})
        if data is not None:
            return cls(**data)

    @classmethod
    # Done this way, because the object doesn't exist before creation
    def get_by_id(cls, _id):
        data = Database.find_one("users", {"_id": _id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email, password):
        # User.login_valid("email", "password")
        user = User.get_by_email(email)
        if user is not None:
            #Check password
            return user.password == password
        return False

    @classmethod
    def register(cls, email, password):
        user = cls.get_by_email(email)
        if user is None:
            #User doesn't exist, so we can create one
            new_user = cls(email, password)
            new_user.save_to_mongo()
            session['email'] = email
            return True
        else:
            return False

    @staticmethod
    def login(user_email):
        # Login_valid has already been called
        session['email'] = user_email

    @staticmethod
    def logout():
        sesion['email'] = None

    def get_information(self):
        return CoronaData.from_mongo(self._id)

    def json(self):
        # Return the user in JSON format for MongoDB (NoSQL)
        return {
            "email": self.email,
            "_id": self._id,
            "password": self.password
        }
    # Insert the new user into the Database
    def save_to_mongo(self):
        Database.insert("users", self.json())

    # Get the coronadata from the user
    def get_coronadata(self):
        return CoronaData.from_mongo(self.email)