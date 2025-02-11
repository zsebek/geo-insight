import json
from config import BASE_URL_V4

def get_game_tokens(session):
    game_tokens = []
    pagination_token = None
    while True:
        response = session.get(f"{BASE_URL_V4}/feed/private", params={'paginationToken': pagination_token})
        pagination_token = entries = response.json()['paginationToken']
        entries = response.json()['entries']
        for entry in entries:
            payload_json = json.loads(entry['payload'])
            for payload in payload_json:
                try:
                    if payload['payload']['gameMode'] == 'Standard':
                        game_tokens.append(payload['payload']['gameToken']) 
                except Exception as e:
                    continue 
        if not pagination_token:
            break
    return game_tokens


def get_game_tokens_other(session):
    game_tokens = []
    pagination_token = None
    while True:
        response = session.get(f"{BASE_URL_V4}/feed/private", params={'paginationToken': pagination_token})
        pagination_token = entries = response.json()['paginationToken']
        entries = response.json()['entries']
        for entry in entries:
            payload_json = json.loads(entry['payload'])
            for payload in payload_json:
                try:
                    if payload['payload']['gameMode'] == 'Standard':
                        game_tokens.append(payload['payload']['gameToken']) 
                except Exception as e:
                    continue 
        if not pagination_token:
            break
    return game_tokens