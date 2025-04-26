# from sqlmodel import Session, select
# from models.order_model import OrderModel
# from models.order_item_model import OrderItemModel
# from typing import List


# class OrderRepository:
#     def __init__(self, db: Session):
#         self.db = db

#     def create(self, order: OrderModel, order_items: OrderItemModel) -> OrderModel:
#         self.db.add(order)
#         self.db.flush()

#         for item in order_items:
#             item.order_id = order.id
#             self.db.add(item)

#         self.db.commit()
#         self.db.refresh(order)
#         return order

#     def get_list(self) -> List[OrderModel]:
#         statement = select(OrderModel)
#         result = self.db.execute(statement)
#         return result.all()

#     def get_by_id(self, id: int) -> OrderModel:
#         model = self.db.get(OrderModel, id)
#         self.db.refresh(model)
#         return model

# -----

from sqlmodel import Session, select
from models.order_model import OrderModel
from models.order_item_model import OrderItemModel
from typing import List, Optional

class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    # --- Create a full order with items (existing function) ---
    def create(self, order: OrderModel, order_items: List[OrderItemModel]) -> OrderModel:
        self.db.add(order)
        self.db.flush()

        for item in order_items:
            item.order_id = order.id
            self.db.add(item)

        self.db.commit()
        self.db.refresh(order)
        return order

    # --- Get all orders (existing function) ---
    def get_list(self) -> List[OrderModel]:
        statement = select(OrderModel)
        result = self.db.execute(statement)
        return result.all()

    # --- Get one order by ID (existing function) ---
    def get_by_id(self, id: int) -> OrderModel:
        model = self.db.get(OrderModel, id)
        self.db.refresh(model)
        return model

    # --- Get draft order by customer_id ---
    def get_draft_order_by_customer_id(self, customer_id: int) -> Optional[OrderModel]:
        statement = select(OrderModel).where(
            (OrderModel.customer_id == customer_id) &
            (OrderModel.status == "DRAFT")
        )
        result = self.db.exec(statement)
        return result

    # --- Create new draft order ---
    def create_draft_order(self, customer_id: int, user_id: Optional[int] = None, description: Optional[str] = None) -> OrderModel:
        draft_order = OrderModel(
            customer_id=customer_id,
            user_id=user_id,
            status="DRAFT",
            description=description  # Empty for now, until checkout
        )
        self.db.add(draft_order)
        self.db.commit()
        self.db.refresh(draft_order)
        return draft_order

    # --- Update order status (e.g., DRAFT -> ORDERED) ---
    def update_order_status(self, order: OrderModel):
        self.db.commit()
        self.db.refresh(order)

    # --- Get order_item by order_id and product_id ---
    def get_order_item_by_order_and_product(self, order_id: int, product_id: int) -> Optional[OrderItemModel]:
        statement = select(OrderItemModel).where(
            (OrderItemModel.order_id == order_id) &
            (OrderItemModel.product_id == product_id) &
            (OrderItemModel.delete_flg == False)
        )
        result = self.db.exec(statement)
        return result

    # --- Create new order_item ---
    def create_order_item(self, order_id: int, product_id: int, quantity: int, unit_price: float, description: Optional[str] = None) -> OrderItemModel:
        total_price = quantity * unit_price
        item = OrderItemModel(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price,
            total_price=total_price,
            description=description
        )
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    # --- Update quantity of an existing order_item ---
    def update_order_item_quantity(self, item: OrderItemModel, added_quantity: int):
        item.quantity += added_quantity
        item.total_price = item.quantity * item.unit_price
        self.db.commit()
        self.db.refresh(item)

