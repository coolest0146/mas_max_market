from pydantic import BaseModel
from typing import List, Optional

class VariationOut(BaseModel):
    id: str
    image: str


class RatingOut(BaseModel):
    stars: float
    count: int


class ProductOut(BaseModel):
    id: int
    name: str
    image: Optional[str]
    rating: RatingOut
    variation: List[VariationOut]
    priceCents: int
    keywords: List[str]



class SearchResponse(BaseModel):
    results: List[ProductOut]


