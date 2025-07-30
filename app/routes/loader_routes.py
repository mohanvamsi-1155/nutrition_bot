from fastapi import APIRouter, HTTPException
from app.models.model import DataLoaderMethod
from app.loader.loader import Loader

router = APIRouter()


@router.post(path="/load/", response_model=None)
def load_data(payload: DataLoaderMethod):
    try:
        loader_class_obj = Loader(payload=payload)
        return loader_class_obj.load_data()
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Unhandled Exception : {e}")
