from flask import request
from flask_restful import Resource
import json
from utils.date_converter import get_date
from database_manager import inventory_collection, shipment_collection
from bson import json_util
from bson.objectid import ObjectId
import jsonschema
from pymongo import UpdateOne

class Shipment(Resource):
    def get(self, shipment_id):
        """
            Handles a GET request.
            Returns a Shipment document with the specified id.
            Returns null if Shipment does not exist.
        """
        try:
            document = shipment_collection.find_one({"_id": ObjectId(shipment_id)})
            if (document is None):
                return document, 404
            return json.loads(json_util.dumps(document)), 200
        except bson.errors.InvalidId as e:
            return {"reason": str(e)}, 400
        except Exception as e:
            return {"reason": str(e)}, 500

    def delete(self, shipment_id):
        """
            Handles a DELETE request.
            Deletes a Shipment document with the specified id.
        """
        try:
            shipment_doc = shipment_collection.find_one({"_id": ObjectId(shipment_id)})
            if shipment_doc is None:
                return shipment_doc, 404
            if shipment_doc["completed"] is False:
                # increment units of all inventory associated with this shipment
                bulk_inventory_update = []
                for inventory_item in shipment_doc["inventory_items"]:
                    bulk_inventory_update.append(UpdateOne(
                        {"_id": ObjectId(inventory_item["inventory_id"])},
                        {"$inc": {"units_remaining": inventory_item["units"]}}
                    ))
                inventory_collection.bulk_write(bulk_inventory_update)
            
            result = shipment_collection.find_one_and_delete({"_id": ObjectId(shipment_id)})
            return json.loads(json_util.dumps(result)), 204
        except bson.errors.InvalidId as e:
            return {"request": str(e)}, 400
        except Exception as e:
            return {"reason": json.dumps(str(e))}, 500
