import json
import pprint
import random
import uuid


def main():
    data = get_original_data()
    print(data)
    new_data = multiply(data, 5000)
    print(len(new_data))
    write_big_data(new_data)

def get_original_data():
    with open("fake_products.json", "r") as f:
        return json.loads(f.read())


def multiply(orig_data: list[dict], factor: int):

    new_data = []
    current_id = len(orig_data)
    for x in range(factor):

        cdata = json.loads(json.dumps(orig_data))
        for item in cdata:
            if x == 0:
                new_data.append(item)
                continue

            item["title"] = adjust_title(item["title"])
            current_id += 1
            item["id"] = current_id
            new_data.append(item)
    return new_data


def adjust_title(string):

    unique = str(uuid.uuid4())
    append = unique[:random.randint(0, len(unique))]
    # print(f"append: {append}")
    return string+" " + append


def write_big_data(data):
    with open("big_data_products.json", "w") as f:
        f.write(json.dumps(data))


def create_categories_json():
    data = get_original_data()
    _id = 0
    existing = set()
    categories = []
    for x in data:

        if x["category"] not in existing:
            _id += 1
            categories.append({"id": _id, "name": x["category"]})
            existing.add(x["category"])
        else:
            continue
    with open("fake_categories.json", "w") as f:
        f.write(json.dumps(categories))







if __name__ == '__main__':
    # main()
    create_categories_json()