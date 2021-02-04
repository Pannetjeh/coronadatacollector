import pymongo

class Database(object):
    URI = "mongodb+srv://<username>:<password>@microblog-application.kiw0s.mongodb.net/test"
    DATABASE = None

    # Initialize the database
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['microblog']

    # Insert data into the collection
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    # Find all the data based on the query
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    # Find piece of data based on the query
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    # Update the data in the database.
    def update_corona(collection, query, data):
        Database.DATABASE[collection].update(query, data, upsert=True)
