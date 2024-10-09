from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.item import Item
from models.addItem import AddItemRequest
from database import get_db
from auth import get_authorization_header

router = APIRouter()

carts = {}


# Get store items
@router.get("/items")
def get_items(
    db: Session = Depends(get_db), authorization=Depends(get_authorization_header)
):
    items = db.query(Item).all()
    return [
        {"id": item.id, "name": item.name, "price": item.price, "stock": item.stock}
        for item in items
    ]


# Add item to cart
@router.post("/cart/add")
def add_item_to_cart(
    item_request: AddItemRequest,
    db: Session = Depends(get_db),
    authorization=Depends(get_authorization_header),
):
    user_token = authorization

    item = db.query(Item).filter(Item.name == item_request.item_name.strip()).first()

    if not item:
        raise HTTPException(
            status_code=404, detail=f"Item with ID {item_request.item_id} not found."
        )

    if item_request.quantity > item.stock:
        raise HTTPException(
            status_code=400,
            detail=f"Item '{item.name}' quantity ordered ({item_request.quantity}) is out of stock. Available stock: {item.stock}.",
        )

    if user_token not in carts:
        carts[user_token] = []

    cart = carts[user_token]
    for cart_item in cart:
        if cart_item["item_name"] == item_request.item_name:
            cart_item["quantity"] += item_request.quantity
            break
    else:
        cart.append({"item_name": item.name, "quantity": item_request.quantity})

    return {"cart": cart}


# Calculate the cart total
@router.post("/cart/total")
def calculate_cart_total(
    db: Session = Depends(get_db),
    authorization=Depends(get_authorization_header),
):
    user_token = authorization

    if user_token not in carts:
        return {"total": 0}

    cart = carts[user_token]
    total_cost = 0

    for cart_item in cart:
        item = db.query(Item).filter(Item.name == cart_item["item_name"]).first()

        if not item:
            raise HTTPException(
                status_code=404,
                detail=f"Item with name {cart_item['item_name']} not found.",
            )

        if cart_item["quantity"] > item.stock:
            raise HTTPException(
                status_code=400,
                detail=f"Item '{item.name}' quantity ordered ({cart_item['quantity']}) is out of stock. Available stock: {item.stock}.",
            )

        total_cost += item.price * cart_item["quantity"]

    return {"total": total_cost}
