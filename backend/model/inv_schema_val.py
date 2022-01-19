from jsonschema import validate
import copy
from model.exceptions.data_format import DataFormatError

class InventorySchemaValidator(object):
    """
        This class defines and validates schema for the Inventory resource.
    """
    def __init__(self):
        self.document_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "date_created": {"type": "string", "format": "date-time"},
                "description": {"type": "string"},
                "price": {"type": "number"},
                "units_remaining": {"type": "integer"}
            },
            "required": ["name", "date_created", "description", "price", "units_remaining"],
            "additionalProperties": False
        }
        self.patch_schema = copy.deepcopy(self.document_schema)
        del self.patch_schema["required"]

    def validate_put(self, data):
        """
            Validates the data given to a PUT request.

            Parameters:
                data (dict): json document

            Raises:
                jsonschema.exceptions.ValidationError: invalid data
                DataFormatError: invalid data format
        """
        if (isinstance(data, dict)):
            validate(instance=data, schema=self.document_schema)
        else:
            raise DataFormatError("Invalid data format")

    def validate_patch(self, data):
        """
            Validates the data given to a PATCH request.

            Parameters:
                data(dict): json document

            Raises:
                jsonschema.exceptions.ValidationError: invalid data
                DataFormatError: invalid data format
        """
        # only verifies that there are no additional properties other than the properties in the inventory schema
        if (isinstance(data, dict)):
            validate(instance=data, schema=self.patch_schema)
        else:
            raise DataFormatError("Invalid data format")