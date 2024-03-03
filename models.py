from pydantic import BaseModel


class RatingModel(BaseModel):
    rate: float | None = None
    count: int | None = 0


class ProductInModel(BaseModel):
    title: str
    price: float
    description: str
    category: str
    image: str | None = None
    rating: RatingModel | None = None


class ProductModel(ProductInModel):
    id: int


class PaginationIfoModel(BaseModel):
    page: int
    pageSize: int


class FilterItemModel(BaseModel):
    field: str
    operator: str
    value: str | int | float


class SortItemModel(BaseModel):
    field: str
    sort: str


class FilterModel(BaseModel):
    items: list[FilterItemModel] = None