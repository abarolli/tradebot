#Tradebot
##A python wrapper around the TDAmeritrade API

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

You must make a developer account with TDAmeritrade to get your consumer/api key. https://developer.tdameritrade.com/
Follow the instructions on the official TDAmeritrade API documentation on how to the refresh token. https://developer.tdameritrade.com/content/simple-auth-local-apps
Following those instructions will provide you with the initial json you need; copy this into a json file. This is the central point of truth for your api configurations. 

The access token is essential for all requests and must be kept up-to-date. This expires every 30 minutes. Thankfully, you don't have to manually create a new one. Use the following snippet as an example of how to update the access token with tradebot. This will automatically update the source json file.

```
file = Path(__file__).parent / "configs.json"
configs = TradebotConfigs(file)
requests = TradebotRequests(configs)
bot = Tradebot(configs, requests)

bot.update_access_token()
```

The refresh token is what is used to get new access tokens. This expires every 90 days. The user must follow the same process they did to initially get the token data (https://developer.tdameritrade.com/content/simple-auth-local-apps) to get a new refresh token.

The account number refers to the account number of your TDAmeritrade brokerage account and is only useful if you have a TDAmeritrade account and wish to see account info. It is not necessary to perform the other stock related functions of tradebot.