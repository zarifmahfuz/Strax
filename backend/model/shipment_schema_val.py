from jsonschema import validate
import copy
from model.exceptions.data_format import DataFormatError

class ShipmentSchemaValidator(object):
    """
        This class defines and validates schema for the Shipment collection.
    """
    def __init__(self):
        self.document_schema = {
            "type": "object",
            "properties": {
                "description": {"type": "string"},
                "date_created": {"type": "string", "format": "date-time"},
                "from": {"type": "string"},
                "to": {"type": "string"},
                "completed": {"type": "boolean"},
                "inventory_items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "inventory_id": {"type": "string"},
                            "units": {"type": "integer"}
                        },
                        "required": ["inventory_id", "units"],
                        "additionalProperties": False
                    },
                    "minItems": 1}
            },
            "required": ["date_created", "from", "to", "completed", "inventory_items"],
            "additionalProperties": False
        }
        self.document_list_schema = {
            "type": "array",
            "items": copy.deepcopy(self.document_schema)
        }

    def validate_post(self, data):
        """
            Validates the data given to a POST request.
        """
        if (isinstance(data, dict)):
            validate(instance=data, schema=self.document_schema)
        else:
            raise DataFormatError("Invalid data format")