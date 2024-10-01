from pydantic import BaseModel

class AddItemRequest(BaseModel):
    item_id: int
    quantity: int