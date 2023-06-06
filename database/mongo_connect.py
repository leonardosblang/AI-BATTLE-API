import os
from pymongo import MongoClient


class MongoDB:
    def __init__(self):
        connection_string = os.getenv('MONGO_CONN_STR')
        if connection_string is None:
            raise Exception("MONGO_CONN_STR is not set in the environment variables")
        self.client = MongoClient(connection_string)
        self.db = self.client['test']

    def insert_into_collection(self, collection_name, data):
        collection = self.db[collection_name]
        result = collection.insert_one(data)
        return result.inserted_id

    def find_in_collection(self, collection_name, query):
        collection = self.db[collection_name]
        results = collection.find(query)
        return results

    def update_in_collection(self, collection_name, query, new_values):
        collection = self.db[collection_name]
        result = collection.update_one(query, new_values)
        return result.modified_count

    def delete_from_collection(self, collection_name, query):
        collection = self.db[collection_name]
        result = collection.delete_one(query)
        return result.deleted_count
