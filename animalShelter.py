from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """
    
    def __init__(self, username, password):
        # Initializing the MongoClient. This helps to access the MongoDB databases and collections.
        if username and password:
            print("username and password are: ", username, password)
            self.client = MongoClient('mongodb://%s:%s@localhost:53168/AAC' % (username, password))
            # where xxxx is your unique port number
            self.database = self.client['AAC']
            print("Connection was successful\n")
        else:
            print("username and/or password are empty or null.")

        
# Create method to implement the C in CRUD.
# Inserts data of dictionary type and returns True if successful, else False.
    def create(self, data):
        if data is not None and dict:
            self.database.animals.insert_one(data) # data should be dictionary
            print("New data inserted: \n", data, "\n")
            return "True"
        else:
            return "False"
            
# Read method to implement the R in CRUD.
# Finds documents that include the value/pair searchValue and returns its cursor, else returns an error.
    def read(self, searchValue):
        if searchValue is not None:
            searchResult = self.database.animals.find(searchValue)
            if len(list(searchResult)) > 0:
                searchResult = self.database.animals.find(searchValue, {"_id":False})
                #for data in searchResult:
                    #print("Read found search result ", searchValue, ": \n", data, "\n")
                return searchResult
            else:
                print("ERROR: Read value ", searchValue, " document not found.\n")
        else:
            raise Exception("Error: No valid search value entered.\n")

# Update method to implement the U in CRUD.
# Finds value/pair searchValue and modifies to the updateValue and returns it in JSON format, else return an error.
    def  update(self, searchValue, updateValue):
        if searchValue and updateValue is not None and dict:
            # Stores the UpdateResult
            updated = self.database.animals.update_many(searchValue, {"$set":updateValue})
            # Stores the cursor of the updated documents
            updated_cursor = self.database.animals.find(updateValue, {"_id":False})
            # 
            if updated.modified_count > 0:
                print("Items modified: ", updated.modified_count, "\n")
                print("Returning result in JSON format: \n", dumps(updated_cursor), "\n")
                return dumps(updated_cursor)
            else:
                print("Update value ", searchValue, " not found.\n")
        else:
            raiseException("Error: searchValue or updateValue invalid.\n")
        
    
# Delete method to implement the D in CRUD.
# Deletes all value/pair deleteValue found, else returns error message.
    def delete(self, deleteValue):
        if deleteValue is not None and dict:
            deleted = self.database.animals.delete_many(deleteValue)
            if deleted.deleted_count > 0:
                print("Items ", deleteValue, " deleted: ", deleted.deleted_count, "\n")
            else:
                print("DeleteValue ", deleteValue, " not found.\n")
        else:
            raise Exception("Error: deleteValue is invalid.\n")
