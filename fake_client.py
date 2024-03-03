import pprint

import httpx


with httpx.Client(timeout=20) as session:
    req = session.get("http://localhost:8000/products")
    if req.status_code == 200:
        res = req.json()
        print(len(res))
