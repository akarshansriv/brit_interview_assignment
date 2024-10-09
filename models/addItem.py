from pydantic import BaseModel


class AddItemRequest(BaseModel):
    item_name: str
    quantity: int
