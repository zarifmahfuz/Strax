from pymongo import MongoClient

# class DatabaseManager:
#     """
#         This is a singleton class that instantiates a connection to the database.
#     """
#     __instance = None

#     @staticmethod 
#     def getInstance():
#         """
#             Gets the instance of this class.
#         """
#         if DatabaseManager.__instance == None:
#             DatabaseManager()
#         return DatabaseManager.__instance
        
#     def __init__(self):
#         """ Virtually private constructor. """
#         if DatabaseManager.__instance != None:
#             raise Exception("DatabaseManager is a singleton class!")
#         else:
#             DatabaseManager.__instance = self

def get_db():
    client = MongoClient(host='test_mongodb',
                         port=27017)
    # create a new db or open existing db
    db = client["shopify_db"]
    return db

db = get_db()
inventory_collection = db["Inventory"]
shipment_collection = db["Shipment"]