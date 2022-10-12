from pprint import pprint
from pathlib import Path

from tradebot.configs import TradebotConfigs
from tradebot.requests import auth_get_request, auth_post_request


__headers = {
    "Accept": "*/*",
    "Authorization": None, #be sure to update Authorization each time the 'headers' are referenced
    "Content-Type": "application/x-www-form-urlencoded",
}

__this_dir = Path(__file__).parent
__config_file = Path(__this_dir, "configs/configs.json")
__configs = TradebotConfigs(__config_file)



def __request_new_access_token():
    global  __configs

    consumer_key, refresh_token = __configs["consumer_key"], __configs["refresh_token"]
    auth_url = "https://api.tdameritrade.com/v1/oauth2/token"
    
    req_body = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": consumer_key + "@AMER.OAUTHAP",
    }

    res = auth_post_request(auth_url, data=req_body)
    if not res.ok:
        raise Exception("Response was not ok; could not get new access token")

    return res.json()


def update_access_token():
    global __configs
    new_data = __request_new_access_token()
    __configs.update(new_data)


def fundamentals(ticker:str):
    global __headers, __configs

    url = "https://api.tdameritrade.com/v1/instruments"
    url_params = {"apikey": __configs["consumer_key"], "symbol": ticker, "projection": "fundamental"}
    
    res = auth_get_request(url, params=url_params)
    if not res.ok:
        print("Response was not ok for the url:")
        print("URL: " + url)
        return res

    return res.json()
    

def quote(ticker:str):
    global __headers
    
    url = f"https://api.tdameritrade.com/v1/marketdata/{ticker}/quotes"
    res = auth_get_request(url)
    assert res.ok

    return res.json()
