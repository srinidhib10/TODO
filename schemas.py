from pydantic import BaseModel, field_validator,ConfigDict

class create(BaseModel):
    title: str
    description: str
    completed: bool

    @field_validator('title')
    def validate_title(cls, value):
        if len(value) < 3:
            raise ValueError("Title must be atleast 3 characters long")
        return value

class update(BaseModel):
    title: str
    description: str
    completed: bool

    @field_validator('completed')
    def validate_completed(cls, value):
        if value is not None and not isinstance(value, bool):
            raise ValueError("Completed is a bool val")
        return value

class response(create):
    id: int
    own_id:int
    class MyModel(BaseModel):
        model_config = ConfigDict(from_attributes=True)
