from config.tradebot_config import TradeBotConfigs
from bot.tradebot import TradeBot


def main():
    configs = TradeBotConfigs.get_config()
    bot = TradeBot(configs)
    bot.get_price_history('KO', 'day', 2, 'minute', 1)

main()