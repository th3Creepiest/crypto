import json
import asyncio
import websockets
import pandas as pd
from dotenv import dotenv_values
from binance import Client
from binance.helpers import round_step_size


BASE_ASSET = "BTC"
QUOTE_ASSET = "EUR"
SYMBOL = BASE_ASSET + QUOTE_ASSET
TSL_PERCENTAGE = 0.995  # 0.5%

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

stream = websockets.connect(
    f"wss://stream.binance.com:9443/stream?streams={SYMBOL.lower()}@miniTicker"
)


async def main():
    df = pd.DataFrame()
    while True:
        payload = await get_data()

        df = pd.concat([df, payload])
        df["benchmark"] = df.price.cummax()
        df["tsl"] = df.benchmark * TSL_PERCENTAGE
        df["cumret"] = (df.price.pct_change() + 1).cumprod() - 1
        print(df.iloc[-1].to_dict())

        if df[df.price < df.tsl].first_valid_index():
            print("stop loss triggered")
            order = client.create_order(
                symbol=SYMBOL,
                side="SELL",
                type="MARKET",
                quantity=calculate_sell_quantity(),
            )
            print(order)
            break


async def get_data() -> pd.DataFrame:
    async with stream as receiver:
        data = await receiver.recv()
        data = json.loads(data)["data"]
        df = pd.DataFrame([data])
        df = df.loc[:, ["s", "E", "c"]]
        df.columns = ["symbol", "time", "price"]
        df.price = df.price.astype(float)
        df.time = pd.to_datetime(df.time, unit="ms")
        df = df.set_index("time")
    return df


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


if __name__ == "__main__":
    asyncio.run(main())
