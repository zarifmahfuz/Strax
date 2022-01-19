from flask import request
from flask_restful import Resource
import json
from datetime import datetime
from database_manager import inventory_collection
from bson import json_util
from bson.objectid import ObjectId
import jsonschema
from pymongo import UpdateOne
from utils.date_converter import get_date
from model.inv_col_schema_val import InventoryCollectionSchemaValidator
from model.exceptions.data_format import DataFormatError

inventory_collection_schema_validator = InventoryCollectionSchemaValidator()

class InventoryCollection(Resource):
    def get(self):
        """
            Handles a GET request.
            Returns all inventory documents.
        """
        # retrieve all inventory documents
        try:
            result = inventory_collection.find({})
            return json.loads(json_util.dumps(result)), 200
        except Exception as e:
            return {"reason": str(e)}, 500

    def post(self):
        """
            Handles a POST request.
            Creates a new inventory document with an auto-generated id.
            Accepts only a single document.
        """
        try:
            data = request.get_json()
            inventory_collection_schema_validator.validate_post(data)
            data["date_created"] = get_date(data["date_created"])
            inventory_id = inventory_collection.insert_one(request.get_json()).inserted_id
            response = {"_id": str(inventory_id)}
            return response, 201
        except (jsonschema.exceptions.ValidationError, DataFormatError) as e:
            return {"reason": str(e)}, 400
        except Exception as e:
            return {"reason": str(e)}, 500

    def put(self):
        """
            Handles a PUT request.
            Bulk updates a given list of inventory documents.
            For every given document, all fields of an inventory document must be specified in the request data, including _id.
            Does not support new document creation; if an id does not exist, it will just be skipped over.
        """
        try:
            inventory_collection_schema_validator.validate_put(request.get_json())
            # inventory_collection.delete_many({})
            bulk_update_list = []
            if (isinstance(request.get_json(), dict)):
                data = [request.get_json()]
            else:
                data = request.get_json()
            for doc in data:
                # batch bulk write operations to be sent to the database server
                doc_id = doc["_id"]
                del doc["_id"]                      # cannot update the id
                # create date object
                if ("date_created" in doc):
                    doc["date_created"] = get_date(doc["date_created"])

                bulk_update_list.append(UpdateOne(
                    {"_id": ObjectId(doc_id)},
                    {"$set": doc}
                ))
            # order update
            result = inventory_collection.bulk_write(bulk_update_list)
            return {"result": result.bulk_api_result}, 200
        except (jsonschema.exceptions.ValidationError, DataFormatError) as e:
            return {"request": str(e)}, 400
        except Exception as e:
            return {"reason": json.dumps(str(e))}, 500

    def patch(self):
        """
            Handles a PATCH request.
            Bulk updates a given list of inventory documents.
            Given Inventory documents must contain the "_id" field and any subset of the other fields of
            the Inventory schema.
            Update to "date_created" field is not supported.
        """
        pass

    def delete(self):
        """
            Handles a DELETE request.
            Deletes all the inventory documents in the Inventory collection.
        """
        try:
            inventory_collection.delete_many({})
            return "", 204
        except Exception as e:
            return {"reason": str(e)}, 500