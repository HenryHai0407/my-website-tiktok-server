from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBearer
from sqlmodel import Session
from models.product_model import ProductDTO, ProductDTOCreate, ProductDTOUpdate
from services.product_service import ProductService
from database import get_db_session
from typing import List

router = APIRouter(
    prefix="/products",
    tags=["Products"],
    # dependencies=[Depends(HTTPBearer())]
)


@router.get("/", response_model=List[ProductDTO])
def get_list(request: Request, db: Session = Depends(get_db_session)):
    # print(request.state.user)
    service = ProductService(db)
    return service.get_list()


@router.get("/{id}", response_model=ProductDTO)
def get_by_id(request: Request, id: int, db: Session = Depends(get_db_session)):
    service = ProductService(db)
    return service.get_by_id(id)


@router.post("/", dependencies=[Depends(HTTPBearer())], response_model=ProductDTO)
def create(request: Request, req: ProductDTOCreate, db: Session = Depends(get_db_session)):
    service = ProductService(db)
    return service.create(req)


@router.put("/{id}", dependencies=[Depends(HTTPBearer())], response_model=ProductDTO)
def update(request: Request, id: int, req: ProductDTOUpdate, db: Session = Depends(get_db_session)):
    service = ProductService(db)
    return service.update(id, req)


@router.delete("/{id}", dependencies=[Depends(HTTPBearer())])
def delete(request: Request, id: int, db: Session = Depends(get_db_session)):
    service = ProductService(db)
    return service.delete(id)
