import requests

def get(req: str):
    res = requests.get("http://localhost:8000/" + req)
    return res.json(), res.ok

def post(req: str):
    res = requests.post("http://localhost:8000/" + req)
    return res.json(), res.ok