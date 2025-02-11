import requests

def get(req: str):
    res = requests.get("http://localhost:8000/" + req)
    return res.json(), res.ok