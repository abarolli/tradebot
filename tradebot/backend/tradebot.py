from pprint import pprint
from requests.exceptions import RequestException
from requests import Response
from tradebot.backend.enums import CandleFrequencyType, CandlePeriodType

from tradebot.configs import TradebotConfigs
from tradebot.requests import TradebotRequests


class Tradebot:

    def __init__(self, configs:TradebotConfigs, requests:TradebotRequests):
        self.__configs = configs
        self.__tb_requests = requests


    def __request_new_access_token(self, ):

        consumer_key, refresh_token = self.__configs["consumer_key"], self.__configs["refresh_token"]
        url = "https://api.tdameritrade.com/v1/oauth2/token"
        
        req_body = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": consumer_key + "@AMER.OAUTHAP",
        }

        res = self.__tb_requests.post(url, data=req_body, auth=False)
        if res.status_code == 401:
            self.update_access_token()
            res = self.__tb_requests.get(url, data=req_body, auth=False)

        self.__assert_ok_response(res)

        return res.json()


    def update_access_token(self, ):
        new_data = self.__request_new_access_token()
        self.__configs.update(new_data)


    def fundamentals(self, ticker:str):

        url = "https://api.tdameritrade.com/v1/instruments"
        params = {"apikey": self.__configs["consumer_key"], "symbol": ticker, "projection": "fundamental"}
        
        res = self.__tb_requests.get(url, params=params)
        if res.status_code == 401:
            self.update_access_token()
            res = self.__tb_requests.get(url, params=params)

        self.__assert_ok_response(res)

        return res.json()
        

    def quote(self, ticker:str):
        
        url = f"https://api.tdameritrade.com/v1/marketdata/{ticker}/quotes"
        res = self.__tb_requests.get(url)
        if res.status_code == 401:
            self.update_access_token()
            res = self.__tb_requests.get(url)

        self.__assert_ok_response(res)

        return res.json()


    def price_history(
        self,
        ticker:str,
        period_type:CandlePeriodType=None,
        period:int=None,
        frequency_type:CandleFrequencyType=None,
        frequency:int=None,
        end_date:int=None,
        start_date:int=None,
        need_extended_hours:bool=True
    ):
        '''
        Returns the price history for the given ``ticker`` using the conditions defined by the following params:\n
        ``period_type``: The type of period to show. Valid values are 'day', 'month', 'year', or 'ytd' (year to date).\n
        ``period``: number of periods of ``period_type`` to show.\n
        Valid periods by periodType:
            day: 1, 2, 3, 4, 5, 10
            month: 1, 2, 3, 6
            year: 1, 2, 3, 5, 10, 15, 20
            ytd: 1
        ``frequency_type``: The type of frequency with which a new candle is formed.\n
        Valid frequencyTypes by periodType:
            day: minute
            month: daily, weekly
            year: daily, weekly, monthly
            ytd: daily, weekly
        ``frequency``: The number of the frequencyType to be included in each candle.\n
        Valid frequencies by frequencyType:
            minute: 1, 5, 10, 15, 30
            daily: 1
            weekly: 1
            monthly: 1
        '''
        url = f"https://api.tdameritrade.com/v1/marketdata/{ticker}/pricehistory"
        api_key = self.__configs["consumer_key"]
        params = {
            "apikey": api_key,
            "periodType": period_type._value_,
            "period": period,
            "frequencyType": frequency_type._value_,
            "frequencey": frequency,
            "endDate": end_date,
            "startDate": start_date,
            "needExtendedHoursData": need_extended_hours
        }

        res = self.__tb_requests.get(url, params=params)
        if res.status_code == 401:
            self.update_access_token()
            res = self.__tb_requests.get(url, params=params)

        self.__assert_ok_response(res)

        return res.json()


    def __assert_ok_response(self, res:Response):
        if not res.ok:
            raise RequestException(f"The response status code was {res.status_code}", response=res)
