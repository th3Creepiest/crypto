import time
import requests
import pandas as pd
from dotenv import dotenv_values
from binance import Client
from binance.helpers import round_step_size


BASE_ASSET = "BTC"
QUOTE_ASSET = "EUR"
SYMBOL = BASE_ASSET + QUOTE_ASSET

in_position = False

secrets = dotenv_values()
client = Client(secrets["BINANCE_API_KEY"], secrets["BINANCE_API_SECRET"])

symbol_info = client.get_symbol_info(SYMBOL)
assert symbol_info, f"symbol {SYMBOL} not found"

lot_size = next(
    (f for f in symbol_info["filters"] if f["filterType"] == "LOT_SIZE"), None
)
assert lot_size, f"lot size filter not found for symbol {SYMBOL}"

step_size = float(lot_size["stepSize"])
min_qty = float(lot_size["minQty"])


def calculate_buy_quantity() -> float:
    balance = client.get_asset_balance(asset=QUOTE_ASSET)
    assert balance, f"balance for asset {BASE_ASSET} not found"
    free_balance = float(balance["free"])
    price = float(client.get_symbol_ticker(symbol=SYMBOL)["price"])
    buy_quantity = free_balance / price
    assert (
        buy_quantity >= min_qty
    ), f"buy quantity {buy_quantity} is less than min qty {min_qty}"
    adjusted_quantity = round_step_size(buy_quantity, step_size)
    assert (
        adjusted_quantity >= min_qty
    ), f"buy adjusted quantity {adjusted_quantity} is less than min qty {min_qty}"
    return adjusted_quantity


def calculate_sell_quantity() -> float:
    balance = client.get_asset_balance(asset=BASE_ASSET)
    assert balance, f"balance for asset {BASE_ASSET} not found"
    sell_quantity = float(balance["free"])
    assert (
        sell_quantity >= min_qty
    ), f"sell quantity {sell_quantity} is less than min qty {min_qty}"
    adjusted_quantity = round_step_size(sell_quantity, step_size)
    assert (
        adjusted_quantity >= min_qty
    ), f"sell adjusted quantity {adjusted_quantity} is less than min qty {min_qty}"
    return adjusted_quantity


def klines_to_df(klines: list) -> pd.DataFrame:
    df = pd.DataFrame(klines)
    df = df.iloc[:, :6]
    df.columns = ["time", "open", "high", "low", "close", "volume"]
    df = df.set_index("time")
    df.index = pd.to_datetime(df.index, unit="ms")
    df = df.astype(float)
    return df


klines = klines_to_df(
    client.get_historical_klines(SYMBOL, interval="1m", start_str="30 min ago UTC")
)


while True:
    cumulative_return = (klines.open.pct_change() + 1).cumprod() - 1
    print("cumulative return:", cumulative_return.iloc[-1])

    if not in_position:
        if cumulative_return.iloc[-1] < -0.002:
            print("Buying assets...")
            order = client.create_order(
                symbol=SYMBOL,
                side="BUY",
                type="MARKET",
                quantity=calculate_buy_quantity(),
            )
            print(order)
            in_position = True

    else:
        if cumulative_return.iloc[-1] > 0.0015:
            print("Selling assets...")
            order = client.create_order(
                symbol=SYMBOL,
                side="SELL",
                type="MARKET",
                quantity=calculate_sell_quantity(),
            )
            print(order)
            in_position = False

    time.sleep(60)

    last_kline_time = str(klines.index[-1])

    try:
        new_klines = klines_to_df(
            client.get_historical_klines(
                SYMBOL, interval="1m", start_str=last_kline_time
            )
        )
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error fetching klines: {e}")
        print("Skipping this update cycle due to connection error.")
        continue

    klines = pd.concat([klines, new_klines]).drop_duplicates()

    if len(klines) > 120:
        klines = klines.iloc[-120:]
