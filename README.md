# Tradebot
## A python wrapper around the TDAmeritrade API

The only thing that needs to be manually configured by the user is the config file.
As of right now, this needs to be a json file with the following format:

```
{
  "access_token": "oMLcWUb4GFRnSRCztRGy...",
  "refresh_token": "7GWdTz2AdBAz1IEtsErLM...",
  "scope": "PlaceTrades AccountAccess MoveMoney",
  "expires_in": 1800,
  "refresh_token_expires_in": 7776000,
  "token_type": "Bearer",
  "consumer_key": "5SMAF9JAZYKKPIPL5E6IZUQCAKZOV5D7",
  "account_number": "495909744"
}
```

You must make a [developer account](https://developer.tdameritrade.com/) with TDAmeritrade to get your consumer/api key.

Follow the official TDAmeritrade API documentation for instructions on [generating the refresh token](https://developer.tdameritrade.com/content/simple-auth-local-apps).
Following those instructions will provide you with the initial json you need; copy this into a json file in your source code directory. This is the central point of truth for your api configurations.

The *access_token* is essential for all requests and must be kept up-to-date. This expires every 30 minutes. Thankfully, you don't have to manually create a new one. Use the following snippet as an example of how to update the access token with tradebot. This will automatically update the source json file.

```
file = Path(__file__).parent / "configs.json"
configs = TradebotConfigs(file)
requests = TradebotRequests(configs)
bot = Tradebot(configs, requests)

bot.update_access_token()
```
Most request methods will automatically make this call internally if a 401 HTTP status code is initially recieved and reattempt the request, so the user rarely has to call this explicitly.

The *refresh_token* is what is used to get a new access token. The user must follow the [same process](https://developer.tdameritrade.com/content/simple-auth-local-apps) they did to initially get the token data to get a new refresh token. Thankfully, this only expires every 90 days. 

The *account_number* refers to the account number of your TDAmeritrade brokerage account and is only useful if you have a TDAmeritrade account and wish to see account info. It is not necessary to perform the other stock related functions of tradebot.

Here are some code snippets to get started.

**Requesting fundamental data for a given ticker:**
```
from pathlib import Path
from tradebot.configs import TradebotConfigs
from tradebot.backend import Tradebot
from tradebot.requests import TradebotRequests

file = Path(__file__).parent / "configs.json"
configs = TradebotConfigs(file)
requests = TradebotRequests(configs)
bot = Tradebot(configs, requests)

msft_fundamentals = bot.fundamentals("MSFT")
```

**Requesting price history:**
```
from tradebot.backend.enums import CandlePeriodType, CandleFrequencyType

file = Path(__file__).parent / "configs.json"
configs = TradebotConfigs(file)
requests = TradebotRequests(configs)
bot = Tradebot(configs, requests)

aapl_price_history = bot.price_history(
    "AAPL",
    period_type=CandlePeriodType.DAY,
    period=2,
    frequency_type=CandleFrequencyType.MINUTE,
    frequency=1
)
```