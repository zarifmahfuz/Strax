from jsonschema import validate
import copy
from model.exceptions.data_format import DataFormatError
from model.inv_schema_val import InventorySchemaValidator

class InventoryCollectionSchemaValidator(InventorySchemaValidator):
    """
        This class defines schema for Inventory documents and validates any given json payload(s).
    """
    def __init__(self):
        super().__init__()
        # _id has to be a required field to update an Inventory document through the InventoryCollection resource
        self.put_schema = copy.deepcopy(self.document_schema)
        self.put_schema["properties"]["_id"] = {"type": "string"}
        self.put_schema["required"].extend(["_id"])
        self.put_list_schema = {
            "type": "array",
            "items": self.put_schema
        }

    def validate_post(self, data):
        """
            Validates the data given to a POST request.

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

    def validate_put(self, data):
        """
            Validates the data given to a PUT request.

            Parameters:
                data(list or dict): json document(s)

            Raises:
                jsonschema.exceptions.ValidationError: invalid data
                DataFormatError: invalid data format
        """
        
        if (isinstance(data, dict)):
            # a single document
            validate(instance=data, schema=self.put_schema)
        elif (isinstance(data, list)):
            validate(instance=data, schema=self.put_list_schema)
        else:
            raise DataFormatError("Invalid data format")