from fastapi import APIRouter, HTTPException
from app.models.model import DataSearcherMethod
from app.searcher.searcher import Searcher

router = APIRouter()


@router.post(path="/search/", response_model=None)
def load_data(payload: DataSearcherMethod):
    try:
        searcher_obj = Searcher(query=payload.query)
        return searcher_obj.search(metadata=payload.metadata)
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Unhandled Exception : {e}")
