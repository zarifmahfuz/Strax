from flask import request
from flask_restful import Resource
from database_manager import inventory_collection
import bson
from bson.objectid import ObjectId
import jsonschema
import json
from bson import json_util
from pymongo import ReturnDocument
from model.inv_schema_val import InventorySchemaValidator
from model.exceptions.data_format import DataFormatError

inventory_schema_validator = InventorySchemaValidator()

class Inventory(Resource):
    def get(self, inventory_id):
        """
            Handles a GET request.
            Returns an inventory document with the specified id.
            Returns null if an inventory does not exist.

            Parameters:
                inventory_id (str): a 24-character hex string
        """
        try:
            document = inventory_collection.find_one({"_id": ObjectId(inventory_id)})
            if (document is None):
                return document, 404
            return json.loads(json_util.dumps(document)), 200
        except bson.errors.InvalidId as e:
            return {"reason": str(e)}, 400
        except Exception as e:
            return {"reason": str(e)}, 500

    def put(self, inventory_id):
        """
            Handles a PUT request.
            Updates a specific inventory document.
            All fields of an inventory document must be given in the request data, including id.
            It does not support creation of a new document.
        """
        try:
            data = request.get_json()
            inventory_schema_validator.validate_put(data)
            # # can't update id and date
            del data["_id"]
            del data["date_created"]
            result = inventory_collection.find_one_and_update(
                {"_id": ObjectId(inventory_id)},
                {"$set": data},
                return_document=ReturnDocument.AFTER
            )
            if result is None:
                # an inventory document with the given id does not exist
                return result, 404
            return json.loads(json_util.dumps(result)), 200

        except (jsonschema.exceptions.ValidationError, DataFormatError, bson.errors.InvalidId) as e:
            return {"reason": str(e)}, 400
        except Exception as e:
            return {"reason": json.dumps(str(e))}, 500

    def patch(self, inventory_id):
        """
            Handles a PUT request.
            Updates a specific inventory document.
            Only a subset of fields of an inventory document has to be given in the request data.
            It does not support updating the date_created field.
        """
        try:
            data = request.get_json()
            inventory_schema_validator.validate_patch(data)
            if "_id" in data:
                del data["_id"]
            if "date_created" in data:
                del data["date_created"]
            result = inventory_collection.find_one_and_update(
                {"_id": ObjectId(inventory_id)},
                {"$set": data},
                return_document=ReturnDocument.AFTER
            )
            if result is None:
                # an inventory document with the given id does not exist
                return result, 404
            return json.loads(json_util.dumps(result)), 200
        except DataFormatError as e:
            return {"reason", str(e)}, 415
        except (jsonschema.exceptions.ValidationError, bson.errors.InvalidId) as e:
            return {"reason": str(e)}, 400
        except Exception as e:
            return {"reason": json.dumps(str(e))}, 500

    def delete(self, inventory_id):
        """
            Handles a DELETE request.
        """
        try:
            result = inventory_collection.find_one_and_delete({"_id": ObjectId(inventory_id)})
            if result is None:
                return result, 404
            return json.loads(json_util.dumps(result)), 204
        except bson.errors.InvalidId as e:
            return {"request": str(e)}, 400
        except Exception as e:
            return {"reason": json.dumps(str(e))}, 500
