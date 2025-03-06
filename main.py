from fastapi import Request, FastAPI
from typing import List, Tuple

app = FastAPI()


def create_tuple(data: dict) -> List[Tuple[str, int]]:
    users = data.get("users", [])
    tuples = [(user["name"], user["amount"]) for user in users]
    return tuples

def get_git_hash():
    import subprocess

    git_tag = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).strip().decode("utf-8")
    
    return git_tag

def get_btc_data():
    import requests
    import json

    response = requests.get('https://data-api.coindesk.com/spot/v1/latest/tick?market=coinbase&instruments=BTC-USD')
    data = response.json()

    return float(data['Data']['BTC-USD']['PRICE'])


@app.post("/")
async def get_json(request: Request):
    file = await request.json()

    current_price = file['price']

    # Later: Add validation for each field

    # Return the response
    tuples = create_tuple(file)

    results = []
    results.append({"current_price": f'{current_price}'})

    for tuple in tuples:
        value = tuple[1] / current_price
        results.append({
            tuple[0] : f'{value:.8f}'
        })

    return results


@app.get("/btc")
async def btc_price():
    price_data = float(get_btc_data())
    return {"price": f"{price_data:.2f}"}


@app.get("/health")
async def health():
    return {"status": "ok", "git_hash": get_git_hash()}
