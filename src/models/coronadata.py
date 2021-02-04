import uuid
import datetime
from common.database import Database

class CoronaData(object):
    # Constructor for the Coronadata object
    def __init__(self, username, corona, corona_relations, age, gender, province, _id=None):
        self.username = username
        self.corona = corona
        self.corona_relations = corona_relations
        self.age = age
        self.gender = gender.lower() #Double check 
        self.province = province.lower() #Double check
        self._id = uuid.uuid4().hex if _id is None else _id

    # Save the coronadata in a coronadata collection in Mongo DB
    def save_to_mongo(self):
        Database.insert(collection='coronadata', data=self.json())

    # Update the already existing coronadata in MongoDB
    def update_to_mongo(self):
        Database.update_corona(collection='coronadata', query={"username": self.username},data=self.json_update())

    # Formatting the data to json
    def json(self):
        return {
            'username': self.username,
            'corona' : self.corona,
            'corona_relations' : self.corona_relations,
            'age' : self.age,
            'gender' : self.gender,
            'province' : self.province,
            '_id' : self._id
        }
    
    # Formatting the json data with self.id because to update it you can''t change the id
    def json_update(self):
        return {
            'username': self.username,
            'corona' : self.corona,
            'corona_relations' : self.corona_relations,
            'age' : self.age,
            'gender' : self.gender,
            'province' : self.province
        }
        
    # Get the coronadata from mongo_db
    @classmethod
    def from_mongo(cls, email):
        coronadata = Database.find_one(collection='coronadata', query={'username' : email})

        return cls(**coronadata)

