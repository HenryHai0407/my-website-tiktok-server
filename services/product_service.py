from sqlmodel import Session
from models.product_model import ProductModel, ProductDTO, ProductDTOCreate, ProductDTOUpdate
from repositories.product_repository import ProductRepository
from typing import List
# from exceptions.custom_exception import AppException, ExceptionType


class ProductService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = ProductRepository(self.db)

    def get_list(self) -> List[ProductDTO]:
        models = self.repo.get_list()
        return [ProductDTO.model_validate(model) for model in models]

    def get_by_id(self, id: int) -> ProductDTO:
        model = self.repo.get_by_id(id)
        # if not model:
        #     raise AppException(ExceptionType.NOT_FOUND)

        return ProductDTO.model_validate(model)

    def create(self, dto: ProductDTOCreate) -> ProductDTO:
        model = ProductModel(**dto.model_dump())
        model_id = self.repo.create(model)
        model.id = model_id
        return ProductDTO.model_validate(model)

    def update(self, id: int, dto: ProductDTOUpdate) -> ProductDTO:
        model = self.repo.get_by_id(id)
        # if not model:
        #     raise AppException(ExceptionType.NOT_FOUND)

        for field, value in dto.model_dump(exclude_unset=True).items():
            setattr(model, field, value)
        self.repo.update(model)

        return ProductDTO.model_validate(model)

    def delete(self, id: int) -> None:
        model = self.repo.get_by_id(id)
        # if not model:
        #     raise AppException(ExceptionType.NOT_FOUND)

        return self.repo.delete(model)
