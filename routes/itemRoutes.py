from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.item import Item
from pydantic import BaseModel
from database import get_db
from models.item import AddItemRequest

router = APIRouter()


@router.get("/items")
def get_items(db: Session = Depends(get_db)):
    
    items = db.query(Item).all()
    return [{"id": item.id, "name": item.name, "price": item.price, "stock": item.stock} for item in items]

# API to calculate the cart total
@router.post("/cart/total")
def calculate_cart_total(cart: list[AddItemRequest], db: Session = Depends(get_db)):
    total_cost = 0
    for cart_item in cart:
        # Fetch the item details from the database
        item = db.query(Item).filter(Item.id == cart_item.item_id).first()

        # If item does not exist, raise an error
        if not item:
            raise HTTPException(status_code=404, detail=f"Item with ID {cart_item.item_id} not found.")

        # Check if the requested quantity is available in stock
        if cart_item.quantity > item.stock:
            raise HTTPException(status_code=400, detail=f"Item '{item.name}' quantity ordered ({cart_item.quantity}) is out of stock. Available stock: {item.stock}.")

        # Calculate the total cost for the item
        total_cost += item.price * cart_item.quantity

    return {"total": total_cost}
