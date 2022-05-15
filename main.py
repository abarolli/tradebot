from pathlib import Path
from tradebot.config.tradebot_config import TradeBotConfigs
from tradebot.bot.tradebot import TradeBot

from pprint import pprint
from concurrent import futures as conc_futures
import os


def main():
    this_dir = os.path.dirname(__file__)
    settings = Path(this_dir, "settings.yml")
    configs = TradeBotConfigs.get_config(settings)
    bot = TradeBot(configs)
    configs.write_new_access_token(bot)
    with conc_futures.ThreadPoolExecutor() as executor:
        futures = []
        for ticker in ["MCD", "GOOG", "WMT"]:
            futures.append(executor.submit(bot.get_fundamentals, ticker))

        results = []
        for future in conc_futures.as_completed(futures):
            results.append(future.result())

    for result in results:
        ticker, fundamentals = result
        print(ticker)
        pprint(fundamentals)

    
main()