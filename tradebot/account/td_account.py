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


def get_balances(configs:TradebotConfigs):
    '''
    Returns a Dictionary containing balances for the account defined by ``account_number`` in the config file.
    '''
    acct_info = get_account_info(configs)
    sec_acct = acct_info.get("securitiesAccount", dict())
    balances = {
        "currentBalances": sec_acct.get("currentBalances", None),
        "initialBalances": sec_acct.get("initialBalances", None),
        "projectedBalances": sec_acct.get("projectedBalances", None)
    }
    return balances


def get_positions(configs:TradebotConfigs) -> List[Dict] | None:
    '''
    Returns a list of dictionaries, each representing a position in a particular security.\n
    Returns None if the user doesn't have any positions.
    '''
    acct_info = get_account_info(configs, "positions")
    positions = acct_info.get("securitiesAccount", dict()).get("positions", None)
    return positions


def get_orders(configs:TradebotConfigs) -> List[Dict] | None:
    '''
    Returns a list of dictionaries, each representing an order.
    '''
    acct_info = get_account_info(configs, "orders")
    orders = acct_info.get("securitiesAccount", dict()).get("orderStrategies", None)
    return orders