import time
from dotenv import dotenv_values
from binance.client import Client


config = dotenv_values()
API_KEY = config["BINANCE_TESTNET_API_KEY"]
API_SECRET = config["BINANCE_TESTNET_API_SECRET"]
CLIENT = Client(API_KEY, API_SECRET, testnet=True)


def print_account_balances(coins: list[str]):
    account = CLIENT.get_account()
    balances = {item["asset"]: item for item in account["balances"]}
    for coin in coins:
        print("account balance:", balances[coin])


def get_current_price(symbol: str) -> float:
    ticker = CLIENT.get_symbol_ticker(symbol=symbol)
    return float(ticker["price"])


def place_buy_order(symbol: str, quantity: float):
    order = CLIENT.order_market_buy(symbol=symbol, quantity=quantity)
    print(f"Buy order placed: {order}")


def place_sell_order(symbol: str, quantity: float):
    order = CLIENT.order_market_sell(symbol=symbol, quantity=quantity)
    print(f"Sell order placed: {order}")


def calculate_buy_price(current_price: float) -> float:
    return current_price - 1000


def calculate_sell_price(current_price: float) -> float:
    return current_price + 1000


def run_simple_bot():
    base_currency = "BTC"
    quote_currency = "EUR"
    symbol = base_currency + quote_currency
    current_price: float | None = get_current_price(symbol)
    buy_price_threshold = calculate_buy_price(current_price)
    sell_price_threshold = calculate_sell_price(current_price)
    trade_quantity = 0.001
    in_position = False

    print(symbol)
    print(f"Current price: {current_price}")
    print(f"Buy price threshold: {buy_price_threshold}")
    print(f"Sell price threshold: {sell_price_threshold}")
    print_account_balances([base_currency, quote_currency])

    while True:

        if not current_price:
            current_price = get_current_price(symbol)
            print(f"Current price: {current_price}")

        if not in_position and current_price < buy_price_threshold:
            print(
                f"Price is below buy threshold ({buy_price_threshold}), placing buy order..."
            )
            place_buy_order(symbol, trade_quantity)
            print_account_balances([base_currency, quote_currency])
            in_position = True

        elif in_position and current_price > sell_price_threshold:
            print(
                f"Price is above sell threshold ({sell_price_threshold}), placing sell order..."
            )
            place_sell_order(symbol, trade_quantity)
            print_account_balances([base_currency, quote_currency])
            buy_price_threshold = calculate_buy_price(current_price)
            sell_price_threshold = calculate_sell_price(current_price)
            print(f"New buy price threshold: {buy_price_threshold}")
            print(f"New sell price threshold: {sell_price_threshold}")
            in_position = False

        current_price = None
        time.sleep(60)


if __name__ == "__main__":
    run_simple_bot()
