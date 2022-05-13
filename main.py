from config.tradebot_config import TradeBotConfigs
from bot.tradebot import TradeBot

from pprint import pprint
from concurrent import futures as conc_futures


def main():
    configs = TradeBotConfigs.get_config()
    bot = TradeBot(configs)
    configs.write_new_access_token(bot)

    with conc_futures.ThreadPoolExecutor() as executor:
        futures = []
        for ticker in ["MCD"]:
            futures.append(executor.submit(bot.get_price_history, ticker, "day", 2, "minute", 1))

        results = []
        for future in conc_futures.as_completed(futures):
            results.append(future.result())

    
main()