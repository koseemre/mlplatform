from dataclasses import dataclass
from typing import Optional

@dataclass
class ModelObject:
    model_name: str
    model_class_name: Optional[str]
    model_type: str
    version: int
    feature_list: Optional[list]
    owner_id: int
    location: str

def check_fields_of_registry(meta_data: dict):
    ''' Check if the fields of the model registry are correct
    Args:
        meta_data: dict : Model metadata
    Returns:
        bool : True if the fields are correct, False otherwise
    '''
    try:
        for field, data_type in ModelObject.__annotations__.items():
            if field not in meta_data:
                raise Exception("Field " + field + " is missing in the metadata")
            if not isinstance(meta_data[field], data_type):
                raise TypeError(f"Field '{field}' must be of type {data_type.__name__}.")        
        return True
    except (ValueError, TypeError) as e:
        raise e

    