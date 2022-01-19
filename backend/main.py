from flask import Flask, jsonify, request
from flask_restful import Api
import os
from resources.inventory_collection_resource import InventoryCollection
from resources.inventory_resource import Inventory
from resources.shipment_collection_resource import ShipmentCollection

app = Flask(__name__)
api = Api(app)
api.add_resource(InventoryCollection, "/inventory")
api.add_resource(Inventory, "/inventory/<string:inventory_id>")
api.add_resource(ShipmentCollection, "/shipments")


if __name__=='__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 4200)))