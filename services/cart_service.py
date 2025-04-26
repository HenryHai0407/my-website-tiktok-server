from sqlmodel import Session
from models.order_model import AddToCartDTO, CheckoutCartDTO, OrderModel
from models.order_item_model import OrderItemModel
from repositories.order_repository import OrderRepository
from repositories.product_repository import ProductRepository
import uuid

class CartService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = OrderRepository(self.db)
        self.product_repo = ProductRepository(self.db)

    def add_to_cart(self, dto: AddToCartDTO):
        # Step 1: Find existing DRAFT order
        order = self.repo.get_draft_order_by_customer_id(dto.customer_id)

        # Step 2: If no draft order, create one
        if not order:
            order = self.repo.create_draft_order(customer_id=dto.customer_id)

        # Step 3: Fetch product by ID (your style)
        product = self.product_repo.get_by_id(dto.product_id)
        if not product:
            raise Exception("Product not found")

        unit_price = product.price
        description = product.summary

        # Step 4: Check if product already in cart
        order_item = self.repo.get_order_item_by_order_and_product(order.id, dto.product_id)

        # Step 5: If item exists, update quantity
        if order_item:
            self.repo.update_order_item_quantity(order_item, added_quantity=dto.quantity)
        else:
            # Create new order item
            self.repo.create_order_item(
                order_id=order.id,
                product_id=dto.product_id,
                quantity=dto.quantity,
                unit_price=unit_price,
                description=description
            )
    def checkout_cart(self, dto: CheckoutCartDTO):
        # Step 1: Find draft order
        order = self.repo.get_draft_order_by_customer_id(dto.customer_id)
        if not order:
            raise Exception("No draft cart found to checkout.")

        # Step 2: Update order status to ORDERED (add variables)
        order.status = "ORDERED"
        order.order_number = str(uuid).uuid4()
        self.repo.update_order_status(order)
        return order

    def get_cart_items(self, customer_id: int):
        # Step 1: Find draft order
        order = self.repo.get_draft_order_by_customer_id(customer_id)
        if not order:
            return []

        # Step 2: Return order items
        return order.items
