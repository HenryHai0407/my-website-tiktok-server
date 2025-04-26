from fastapi import APIRouter, Depends, Request, HTTPException
from sqlmodel import Session
from database import get_db_session  
from services.cart_service import CartService
from models.order_model import AddToCartDTO, CheckoutCartDTO

router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
)

# POST /cart/add
@router.post("/add")
def add_to_cart(req: AddToCartDTO, db: Session = Depends(get_db_session)):
    service = CartService(db)
    try:
        service.add_to_cart(req)
        return {"message": "Product added to cart successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# GET /cart/
@router.get("/")
def get_cart_items(customer_id: int, db: Session = Depends(get_db_session)):
    service = CartService(db)
    items = service.get_cart_items(customer_id)
    return items


# PUT /cart/checkout
@router.put("/checkout")
def checkout_cart(req: CheckoutCartDTO, db: Session = Depends(get_db_session)):
    service = CartService(db)
    try:
        order = service.checkout_cart(req)
        return {"message": f"Order {order.id} has been placed successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

