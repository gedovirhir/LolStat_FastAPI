from pydantic import BaseModel, SecretStr, Extra

from typing import Union, Dict, Any, List


# Pydantic base
class ProjectBase(BaseModel):
    class Config:
        orm_mode = True
        validate_assignment = True
        arbitrary_types_allowed = True
        anystr_strip_whitespace = True
        use_enum_values = True

        json_encoders = {
            # custom output conversion for datetime
            SecretStr: lambda v: v.get_secret_value() if v else None,
        }

class AutoSerialized(ProjectBase):
    class Config:
        extra = Extra.allow
    
    def __init__(self, **data):
        super().__init__(**data)
        for key, value in data.items():
            if key not in self.__fields__:
                setattr(self, key, self.__auto_serialize(value))
    
    def __auto_serialize(self, data: Union[Dict[str, Any], List[Any], Any]):
        if isinstance(data, dict):
            return AutoSerialized(**data)
        
        elif isinstance(data, list):
            for i, item in enumerate(data):
                data[i] = self.__auto_serialize(item)
            return data
        
        else:
            return data