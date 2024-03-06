"""
Building a fake data api to test frontend table technologies
"""
import os
import json
import pprint

import fastapi

os.environ.setdefault("FRONTENDS", "http://localhost:5173,http://localhost:3000")
from fastapi import FastAPI
from fastapi.responses import JSONResponse
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

with open("data/fake_categories.json", "r") as f:
    category_table = json.loads(f.read())


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



def filter_by_id(item, _id):
    if item["id"] == _id:
        return True
    return False


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

    # we suggest that our database is ordered. therefor we can pick the item by its list space
    result = database[product_id - 1]
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

    if body.category is not None:
        record["category"] = body.category
    return Mapper.model_to_dto(record)


@app.get("/categories")
def get_categories(search: str = None):
    if search is not None:
        return JSONResponse(status_code=200, content=[x for x in category_table if search.lower() in x["name"].lower()])
    return JSONResponse(status_code=200, content=category_table)


@app.get("/categories/{category_id}")
def get_category_by_id(category_id: int):

    item = None
    for x in category_table:
        if x["id"] == category_id:
            item = x
            break

    return JSONResponse(status_code=200, content=item)


@app.get("/categories/by_name/{category_name}")
def get_category_by_name(category_name: str):
    item = None
    for x in category_table:
        if x["name"] == category_name:
            item = x
            break

    return JSONResponse(status_code=200, content=item)


