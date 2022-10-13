from typing import Dict
import requests
from requests import Response
from requests.exceptions import RequestException

from tradebot.configs import TradebotConfigs


class TradebotRequests:
    '''
    Performs the essential CRUD requests, using the ``access_token`` defined in the config file\n
    to perform Bearer authorization.
    '''
    def __init__(self, configs:TradebotConfigs):
        self.__configs = configs

        self.__headers = {
            "Accept": "*/*",
            "Authorization": None, #be sure to update Authorization each time the 'headers' are referenced
            "Content-Type": "application/x-www-form-urlencoded",
        }


    def __update_headers(self, auth:bool):
        auth_str = f"Bearer {self.__configs['access_token']}" if auth else None
        self.__headers.update({"Authorization": auth_str})


    def get(self, url:str, data:Dict=None, params:Dict=None, auth:bool=True):
        '''
        Uses the ``access_token`` defined in the configs file to make a Bearer authorized request if ``auth`` is True.
        '''
        self.__update_headers(auth)

        return requests.get(url, data=data, params=params, headers=self.__headers)


    def post(self, url:str, data:Dict=None, params:Dict=None, auth:bool=True):
        '''
        Uses the ``access_token`` defined in the configs file to make a Bearer authorized request if ``auth`` is True.
        '''
        self.__update_headers(auth)

        return requests.post(url, data=data, params=params, headers=self.__headers)


def assert_ok_response(res:Response):
        if not res.ok:
            raise RequestException(f"The response status code was {res.status_code}", response=res)