
from pydantic import BaseModel
from models import PaginationIfoModel, SortItemModel, FilterItemModel


class ProductOutDataDto(BaseModel):
    id: int
    title: str
    price: float
    description: str
    category: str
    image: str | None = None
    rating_value: float | None = None
    rating_count: int | None = None


class ProductInDto(BaseModel):
    title: str
    price: float
    description: str
    category: str
    image: str | None = None
    rating_value: float | None = None
    rating_count: int | None = None


class ProductPatchDto(BaseModel):
    title: str | None = None
    price: float | None = None


class TableOutDto(BaseModel):
    pagination_info: PaginationIfoModel | None = None
    data: list[ProductOutDataDto]


class TableFilterDto(BaseModel):
    page: int = 0
    pageSize: int = 10
    sorting: list[SortItemModel]
    filters: list[FilterItemModel]



class ProductFilter(BaseModel):
    title: str | None = None
    price: float | None = None
    description: str | None = None
    category: str | None = None
    rating: float | None = None
    rating_count: int | None = None
    offset: int | None = None
    limit: int | None = None
