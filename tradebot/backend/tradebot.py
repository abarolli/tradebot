from requests.exceptions import RequestException
from requests import Response

from tradebot.configs import TradebotConfigs
from tradebot.requests import TradebotRequests, assert_ok_response
from tradebot.backend.enums import CandleFrequencyType, CandlePeriodType


class Tradebot:
    '''
    Performs all the essential functionality related to stocks/securities, as defined by the TDAmeritrade API.\n
    '''

    def __init__(self, configs:TradebotConfigs, requests:TradebotRequests):
        self.__configs = configs
        self.__tb_requests = requests


    def fundamentals(self, ticker:str):
        '''
        Returns json containing fundamental data for the given ``ticker``.
        '''
        url = "https://api.tdameritrade.com/v1/instruments"
        params = {"apikey": self.__configs["consumer_key"], "symbol": ticker, "projection": "fundamental"}
        
        res = self.__tb_requests.get(url, params=params)
        assert_ok_response(res)

        return res.json()
        

    def quote(self, ticker:str):
        '''
        Returns json representing the quote for the given ``ticker``.
        '''
        url = f"https://api.tdameritrade.com/v1/marketdata/{ticker}/quotes"
        res = self.__tb_requests.get(url)
        assert_ok_response(res)

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
        assert_ok_response(res)

        return res.json()
