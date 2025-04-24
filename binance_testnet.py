import time
from dotenv import dotenv_values
from binance.client import Client


config = dotenv_values()
API_KEY = config["BINANCE_TESTNET_API_KEY"]
API_SECRET = config["BINANCE_TESTNET_API_SECRET"]
CLIENT = Client(API_KEY, API_SECRET, testnet=True)


def print_account_balances():
    account = CLIENT.get_account()
    balances = {item["asset"]: item for item in account["balances"]}
    print("account:", balances["BTC"])
    print("account:", balances["USDT"])


def get_current_price(symbol: str) -> float:
    ticker = CLIENT.get_symbol_ticker(symbol=symbol)
    return float(ticker["price"])


def place_buy_order(symbol: str, quantity: float):
    order = CLIENT.order_market_buy(symbol=symbol, quantity=quantity)
    print(f"Buy order placed: {order}")


def place_sell_order(symbol: str, quantity: float):
    order = CLIENT.order_market_sell(symbol=symbol, quantity=quantity)
    print(f"Sell order placed: {order}")


def trading_bot():
    symbol = "BTCUSDT"
    buy_price_threshold = 60000
    sell_price_threshold = 65000
    trade_quantity = 0.001
    in_position = False

    print_account_balances()

    while True:
        current_price = get_current_price(symbol)
        print(f"Current price: {current_price}")

        if not in_position and current_price < buy_price_threshold:
            print(f"Price is below buy threshold ({buy_price_threshold}), placing buy order...")
            place_buy_order(symbol, trade_quantity)
            print_account_balances()
            in_position = True

        elif in_position and current_price > sell_price_threshold:
            print(f"Price is above sell threshold ({sell_price_threshold}), placing sell order...")
            place_sell_order(symbol, trade_quantity)
            print_account_balances()
            in_position = False

        time.sleep(60)


if __name__ == "__main__":
    trading_bot()
