from typing import Dict, List
from tradebot.requests import TradebotRequests, assert_ok_response
from tradebot.configs import TradebotConfigs


def get_account_info(configs:TradebotConfigs, fields:str=None):
    acct_number = configs["account_number"]
    url = f"https://api.tdameritrade.com/v1/accounts/{acct_number}"
    url_params = {"fields": fields} if fields else ''
    requests = TradebotRequests(configs)
    res = requests.get(url, params=url_params)
    assert_ok_response(res)

    return res.json()


def get_positions(configs:TradebotConfigs) -> List[Dict]:
    '''
    Returns a list of dictionaries, each representing a position in a particular security.
    '''
    acct_info = get_account_info(configs, "positions")
    positions = acct_info["securitiesAccount"]["positions"]
    return positions