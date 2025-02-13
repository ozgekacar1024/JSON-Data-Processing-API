from pydantic import BaseModel
class UpdateItem(BaseModel):
    data_id: int
    key: str
    value: str
