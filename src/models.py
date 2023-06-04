from pydantic import BaseModel, SecretStr


# Pydantic base
class ProjectBase(BaseModel):
    class Config:
        orm_mode = True
        validate_assignment = True
        arbitrary_types_allowed = True
        anystr_strip_whitespace = True

        json_encoders = {
            # custom output conversion for datetime
            SecretStr: lambda v: v.get_secret_value() if v else None,
        }