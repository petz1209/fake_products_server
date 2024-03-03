"""
Building a fake data api to test frontend table technologies
"""
import os
import json
import pprint
os.environ.setdefault("FRONTENDS", "http://localhost:5173,http://localhost:3000")
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dtos import ProductInDto, ProductOutDataDto, TableOutDto, TableFilterDto, ProductFilter, ProductPatchDto
from models import ProductModel, RatingModel, PaginationIfoModel, ProductInModel, FilterModel, FilterItemModel,\
    SortItemModel


# we just add the models here
class Mapper:

    @staticmethod
    def model_to_dto(item: dict) -> ProductOutDataDto:
        return ProductOutDataDto(id=item.get("id"),
                             title=item.get("title"),
                             price=item.get("price"),
                             description=item.get("description"),
                             category=item.get("category"),
                             image=item.get("image"),
                             rating_value=item.get("rating").get("rate"),
                             rating_count=item.get("rating").get("count")
                             )

    @staticmethod
    def dto_to_model(dto: ProductInDto) -> ProductInModel:
        if isinstance(dto, ProductInDto):
            return ProductInModel(title=dto.title,
                                  price=dto.price,
                                  description=dto.description,
                                  category=dto.category,
                                  image=dto.image,
                                  rating=RatingModel(rate=dto.rating_value, count=dto.rating_count))


# initialize database as list of dict
with open("data/big_data_products.json", "r") as f:
    database = json.loads(f.read())


app = FastAPI()

origins = os.environ["FRONTENDS"].split(",")
print(f"origins: {origins}")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/products")
def get_products(offset: int = None, limit: int = None,
                 title: str = None, price: float = None, description: str = None, category: str = None,
                 rating: float = None, rating_count: int = None,
                 ) -> list[ProductOutDataDto]:

    filter_model = ProductFilter(title=title, price=price, description=description, category=category,
                                 rating=rating, rating_count=rating_count, offset=offset, limit=limit)

    # make a deep copy
    data = json.loads(json.dumps(database))

    if filter_model.title is not None:
        data = [row for row in data if filter_model.title.lower() in row["title"].lower()]
    if filter_model.price is not None:
        pass
    if filter_model.description is not None:
        data = [row for row in data if filter_model.description.lower() in row["description"].lower()]

    if filter_model.category is not None:
        data = [row for row in data if filter_model.category.lower() in row["category"].lower()]


    # manage size restrictions
    offset = filter_model.offset if filter_model.offset is not None else 0
    if filter_model.limit is not None:
        data = data[offset: offset + filter_model.limit]
    else:
        data = data[offset:]

    return [Mapper.model_to_dto(item) for item in data]


@app.get("/products/{product_id}")
def get_product_by_id(product_id: int) -> ProductOutDataDto:
    result = None
    for item in database:
        print(item)
        if item["id"] == product_id:
            result = item
            break
    print(f"result: {result}")
    if result:
        return Mapper.model_to_dto(result)


@app.post("/products")
def post_product(body: ProductInDto) -> ProductOutDataDto:

    in_model = Mapper.dto_to_model(body)
    id = database[-1].get("id") + 1
    product = ProductModel(id=id, **in_model.model_dump())
    database.append(product.model_dump())
    return Mapper.model_to_dto(database[-1])


@app.patch("/products/{product_id}")
def patch_product(product_id: int, body: ProductPatchDto) -> ProductOutDataDto:

    record = None
    for item in database:
        if item["id"] == product_id:
            record = item
            break
    if body.title is not None:
        record["title"] = body.title
    if body.price is not None:
        record["price"] = body.price
    return Mapper.model_to_dto(record)





#
# @app.post("/pagination")
# def get_products_pagination(body: TableFilterDto
#                  ) -> TableOutDto:
#
#     pprint.pprint(body)
#     with open("data/fake_products.json", "r") as f:
#         data = json.loads(f.read())
#         # return JSONResponse(status_code=200, content={"data": data})
#
#     fm = body
#
#     offset = fm.page * fm.pageSize
#
#
#     # filter_model = ProductFilter(title=title, price=price, description=description, category=category,
#     #                              rating=rating, rating_count=rating_count, offset=offset, limit=limit)
#     # with open("data/fake_products.json", "r") as f:
#     #     data = json.loads(f.read())
#     #
#     if isinstance(fm.filters, list) and len(fm.filters) > 0:
#         for f in fm.filters:
#             data = do_filering(f.operator, f.value, f.field, data)
#
#     if isinstance(fm.sorting, list) and len(fm.sorting) > 0:
#         for f in fm.sorting:
#             if f.sort == "asc":
#                 data = sorted(data, key=lambda d: d[f.field], reverse=False)
#             else:
#                 data = sorted(data, key=lambda d: d[f.field], reverse=True)
#
#     if offset + fm.pageSize > len(data):
#         result = data[offset:]
#     else:
#         result = data[offset: offset + fm.pageSize]
#
#     dto_data = [Mapper.model_to_dto(item) for item in result]
#
#     pagination_info = None
#     # if offset == 0:
#     #     total_pages = int(len(data) / fm.pageSize)
#     #     total_pages = total_pages if total_pages > 0 else 1
#     #
#
#     print(dto_data)
#     pagination_info = PaginationIfoModel(page=fm.page,
#                                          pageSize=fm.pageSize
#                                          )
#     return TableOutDto(pagination_info=pagination_info, data=dto_data)
#
#
# def do_filering(operator, value, field, obj) -> list[dict]:
#     if operator == "contains":
#         return contains(value, field, obj)
#     if operator == "equals":
#         return equals(value, field, obj)
#     if operator == "starts with":
#         return starts_with(value, field, obj)
#     if operator == "ends with":
#         return ends_with(value, field, obj)
#     if operator == "is empty":
#         return is_empty(value, field, obj)
#     if operator == "is not empty":
#         return is_not_empty(value, field, obj)
#     if operator == "is any of":
#         return is_any_of(value, field, obj)
#     return obj
#
#
# def contains(value, search_key, obj: list[dict]):
#     return [x for x in obj if value.lower() in x[search_key].lower()]
#
#
# def equals(value, search_key, obj: list[dict]):
#     return [x for x in obj if value.lower() == x[search_key].lower()]
#
#
# def starts_with(value, search_key, obj: list[dict]):
#     return [x for x in obj if x[search_key].lower().startswith(value.lower())]
#
#
# def ends_with(value, search_key, obj: list[dict]):
#     return [x for x in obj if x[search_key].lower().endsswith(value.lower())]
#
#
# def is_empty(value, search_key, obj: list[dict]):
#     return obj
#
#
# def is_not_empty(value, search_key, obj: list[dict]):
#     return obj
#
#
# def is_any_of(value, search_key, obj: list[dict]):
#     return obj
#
#
