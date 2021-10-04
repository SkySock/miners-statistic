import os

import requests

from .models import Miner, HashRate, TimeStart, Balance

WALLET = os.environ.get('WALLET')
URL = "https://eth.2miners.com/api/accounts/" + WALLET
headers = {
    "accept": "application/json"
}


def get_json_response(url, hdr):
    r = requests.get(url, headers=hdr)
    if r.status_code == 200:
        src = r.json()
        return src
    else:
        raise Exception("Request error")


def get_balance(response):
    balance = response["stats"]["balance"]
    immature = response["stats"]["immature"]
    return balance + immature


def add_stats_to_db():
    resp = get_json_response(URL, headers)
    miners = Miner.objects.all()

    for miner in miners:
        if resp["workers"].get(miner.worker):
            hr = HashRate(miner=miner, hr=resp["workers"][miner.worker]["hr"])
            miner.is_online = not resp["workers"][miner.worker]["offline"]
            hr.save(force_insert=True)
        else:
            miner.is_online = False
        miner.save()

    balance = Balance.objects.get(description="current")
    balance.value = get_balance(resp)
    balance.save()


if __name__ == "__main__":
    add_stats_to_db()
