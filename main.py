from config.tradebot_config import TradeBotConfigs
from bot.tradebot import TradeBot

from pprint import pprint

def main():
    configs = TradeBotConfigs.get_config()
    bot = TradeBot(configs)
    configs.write_new_access_token(bot)

main()