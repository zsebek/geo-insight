import requests

def get_url(req: str):
    res = requests.get("http://localhost:8000/" + req)
    return res.json(), res.ok