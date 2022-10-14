from tradebot.requests import assert_ok_response, TradebotRequests
from tradebot.configs import TradebotConfigs


def __request_new_access_token(configs:TradebotConfigs):

        consumer_key, refresh_token = configs["consumer_key"], configs["refresh_token"]
        url = "https://api.tdameritrade.com/v1/oauth2/token"
        
        req_body = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": consumer_key + "@AMER.OAUTHAP",
        }

        requests = TradebotRequests(configs)
        res = requests.post(url, data=req_body, auth=False)
        assert_ok_response(res)

        return res.json()


def update_access_token(configs:TradebotConfigs):
    '''
    Requests a new access token and writes it to the config file.
    '''
    new_data = __request_new_access_token(configs)
    configs.update(new_data)
