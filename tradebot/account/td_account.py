from tradebot.requests import auth_get_request


def get_account_info(acct_number:int, fields:str=None):
    url = f"https://api.tdameritrade.com/v1/accounts/{acct_number}"
    url_params = {"fields": fields} if fields else ''

    res = auth_get_request(url, params=url_params)
    assert res.ok

    return res.json()