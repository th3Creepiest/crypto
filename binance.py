import json
import logging
import warnings
from time import sleep
from datetime import datetime, timezone, timedelta

import hmac
import hashlib
from urllib.parse import urlencode

import requests
import websockets
import numpy as np
import pandas as pd


BASE_URL = "https://api.binance.com/api/v3/"
BASE_URI = "wss://stream.binance.com:9443/ws/"
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36", "Accept": "application/json"}
KLINE_INTERVALS = ("1s", "1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M")
KLINE_COLUMNS = ("Open Time", "Open", "High", "Low", "Close", "Volume", "Close Time", "Quote Asset Volume", "Number of Trades", "Taker Buy Base Asset Volume", "Taker Buy Quote Asset Volume", "Ignore")


def ping() -> dict:
    """Test connectivity to the Rest API."""
    response = requests.get(url=BASE_URL + "ping", headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.json()


def get_server_time() -> dict[str, int]:
    """Test connectivity to the Rest API and get the current server time."""
    response = requests.get(url=BASE_URL + "time", headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.json()


def get_average_price(symbol: str) -> dict:
    """Get the current average price for a symbol."""
    response = requests.get(url=BASE_URL + "avgPrice", headers=HEADERS, params={"symbol": symbol}, timeout=10)
    response.raise_for_status()
    return response.json()


def get_latest_price(symbol: str) -> dict[str, str]:
    """Get the latest price for a symbol."""
    response = requests.get(url=BASE_URL + "ticker/price", headers=HEADERS, params={"symbol": symbol}, timeout=10)
    response.raise_for_status()
    return response.json()


def get_exchange_info() -> dict:
    """Get current exchange trading rules and symbol information."""
    response = requests.get(url=BASE_URL + "exchangeInfo", headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.json()


def get_exchange_info_for_symbol(symbol: str) -> dict:
    """Get current exchange trading rules and information for symbol."""
    response = requests.get(url=BASE_URL + "exchangeInfo", headers=HEADERS, params={"symbol": symbol}, timeout=10)
    response.raise_for_status()
    return response.json()


def get_exchange_info_for_symbols(symbols: list[str]) -> dict:
    """Get current exchange trading rules and information for symbols."""
    params = {"symbols": f"[{','.join(f'\"{i}\"' for i in symbols)}]"}
    params = urlencode(params).replace("%2C", ",")
    response = requests.get(url=BASE_URL + "exchangeInfo", headers=HEADERS, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def get_24hr_ticker(request_type: str = "MINI") -> list[dict]:
    """24 hour rolling window price change statistics."""
    if request_type not in ("FULL", "MINI"):
        raise ValueError(f"Invalid type: '{request_type}'. Supported types: FULL, MINI")
    response = requests.get(url=BASE_URL + "ticker/24hr", headers=HEADERS, params={"type": request_type}, timeout=10)
    response.raise_for_status()
    return response.json()


def get_24hr_ticker_for_symbol(symbol: str, request_type: str = "MINI") -> dict:
    """24 hour rolling window price change statistics for symbol."""
    if request_type not in ("FULL", "MINI"):
        raise ValueError(f"Invalid type: '{request_type}'. Supported types: FULL, MINI")
    response = requests.get(url=BASE_URL + "ticker/24hr", headers=HEADERS, params={"type": request_type, "symbol": symbol}, timeout=10)
    response.raise_for_status()
    return response.json()


def get_24hr_ticker_for_symbols(symbols: list[str], request_type: str = "MINI") -> list[dict]:
    """24 hour rolling window price change statistics for symbols."""
    if request_type not in ("FULL", "MINI"):
        raise ValueError(f"Invalid type: '{request_type}'. Supported types: FULL, MINI")
    params = {"type": request_type, "symbols": f"[{','.join(f'\"{i}\"' for i in symbols)}]"}
    params = urlencode(params).replace("%2C", ",")
    response = requests.get(url=BASE_URL + "ticker/24hr", headers=HEADERS, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def get_trading_day_ticker_for_symbol(symbol: str, request_type: str = "MINI") -> dict:
    """Price change statistics for a trading day for symbol."""
    if request_type not in ("FULL", "MINI"):
        raise ValueError(f"Invalid type: '{request_type}'. Supported types: FULL, MINI")
    response = requests.get(url=BASE_URL + "ticker/tradingDay", headers=HEADERS, params={"type": request_type, "symbol": symbol}, timeout=10)
    response.raise_for_status()
    return response.json()


def get_trading_day_ticker_for_symbols(symbols: list[str], request_type: str = "MINI") -> list[dict]:
    """Price change statistics for a trading day for symbols."""
    if request_type not in ("FULL", "MINI"):
        raise ValueError(f"Invalid type: '{request_type}'. Supported types: FULL, MINI")
    params = {"type": request_type, "symbols": f"[{','.join(f'\"{i}\"' for i in symbols)}]"}
    params = urlencode(params).replace("%2C", ",")
    response = requests.get(url=BASE_URL + "ticker/tradingDay", headers=HEADERS, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def get_price_ticker_for_symbol(symbol: str) -> dict:
    """Latest price for symbol."""
    response = requests.get(url=BASE_URL + "ticker/price", headers=HEADERS, params={"symbol": symbol}, timeout=10)
    response.raise_for_status()
    return response.json()


def get_price_ticker_for_symbols(symbols: list[str]) -> list[dict]:
    """Latest price for symbols."""
    params = {"symbols": f"[{','.join(f'\"{i}\"' for i in symbols)}]"}
    params = urlencode(params).replace("%2C", ",")
    response = requests.get(url=BASE_URL + "ticker/price", headers=HEADERS, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def get_order_book_ticker_for_symbol(symbol: str) -> dict:
    """Best price/qty on the order book for symbol."""
    response = requests.get(url=BASE_URL + "ticker/bookTicker", headers=HEADERS, params={"symbol": symbol}, timeout=10)
    response.raise_for_status()
    return response.json()


def get_order_book_ticker_for_symbols(symbols: list[str]) -> list[dict]:
    """Best price/qty on the order book for symbols."""
    params = {"symbols": f"[{','.join(f'\"{i}\"' for i in symbols)}]"}
    params = urlencode(params).replace("%2C", ",")
    response = requests.get(url=BASE_URL + "ticker/bookTicker", headers=HEADERS, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def get_rolling_ticker_for_symbol(symbol: str, window_size: str = "1d", request_type: str = "MINI") -> dict:
    """Rolling window price change statistics for symbol."""
    if request_type not in ("FULL", "MINI"):
        raise ValueError(f"Invalid type: '{request_type}'. Supported types: FULL, MINI")
    win_sizes = [f"{i}m" for i in range(1, 60)] + [f"{i}h" for i in range(1, 24)] + [f"{i}d" for i in range(1, 8)]
    if window_size not in win_sizes:
        raise ValueError(f"Invalid window size: '{window_size}'")
    response = requests.get(
        url=BASE_URL + "ticker",
        headers=HEADERS,
        params={"type": request_type, "symbol": symbol, "windowSize": window_size},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def get_rolling_ticker_for_symbols(symbols: list[str], window_size: str = "1d", request_type: str = "MINI") -> list[dict]:
    """Rolling window price change statistics for symbols."""
    if request_type not in ("FULL", "MINI"):
        raise ValueError(f"Invalid type: '{request_type}'. Supported types: FULL, MINI")
    win_sizes = [f"{i}m" for i in range(1, 60)] + [f"{i}h" for i in range(1, 24)] + [f"{i}d" for i in range(1, 8)]
    if window_size not in win_sizes:
        raise ValueError(f"Invalid window size: '{window_size}'")
    params = {"type": request_type, "symbols": f"[{','.join(f'\"{i}\"' for i in symbols)}]", "windowSize": window_size}
    params = urlencode(params).replace("%2C", ",")
    response = requests.get(url=BASE_URL + "ticker", headers=HEADERS, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def get_account_info(api_key: str, api_secret: str, omit_zero_balances: bool = True) -> dict:
    """Get current account information."""
    headers = HEADERS.copy()
    headers["X-MBX-APIKEY"] = api_key
    params = {"omitZeroBalances": str(omit_zero_balances).lower(), "timestamp": int(datetime.now().timestamp() * 1000)}
    params["signature"] = _generate_signature(api_secret, params)
    response = requests.get(url=BASE_URL + "account", headers=headers, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def get_klines(
    symbol: str,
    interval: str = "1h",
    start_time: str | None = None,
    end_time: str | None = None,
    limit: int = 500,
    endpoint: str = "klines",
) -> list[list]:
    """Get Kline/candlestick bars for a symbol. Klines are uniquely identified by their open time."""

    if interval not in KLINE_INTERVALS:
        raise ValueError(f"Invalid interval: {interval}. Supported intervals: {KLINE_INTERVALS}")

    if endpoint not in ("klines", "uiKlines"):
        raise ValueError(f"Invalid endpoint: {endpoint}. Supported endpoints: klines, uiKlines")

    if limit not in range(1, 1001):
        raise ValueError(f"Invalid limit: {limit}. Supported limits: 1-1000")

    params = {"symbol": symbol, "interval": interval, "limit": limit}

    if start_time:
        params["startTime"] = _datetime_str_to_utc_milliseconds(start_time)

    if end_time:
        params["endTime"] = _datetime_str_to_utc_milliseconds(end_time)

    response = requests.get(url=BASE_URL + endpoint, headers=HEADERS, params=params, timeout=10)
    response.raise_for_status()

    return response.json()


def get_klines_for_year(symbol: str, year: int, interval: str = "1d") -> list[list]:
    """Get historical kline/candlestick bars for a symbol for a year."""
    klines = []
    time_frames = _generate_timeframes(f"{year}-01-01 00:00:00", f"{year}-12-31 23:00:00", interval, 500)
    for start_time, end_time in time_frames:
        klines += get_klines(symbol, interval, start_time, end_time)
        sleep(1)
    return klines


def klines_to_df(klines: list[list]) -> pd.DataFrame:
    df = pd.DataFrame(klines)
    df.columns = KLINE_COLUMNS
    df.drop(df.columns[-1], axis=1, inplace=True)
    df["Open Time"] = pd.to_datetime(df["Open Time"], unit="ms", utc=True)
    df["Close Time"] = pd.to_datetime(df["Close Time"], unit="ms", utc=True)
    df["Open"] = pd.to_numeric(df["Open"])
    df["High"] = pd.to_numeric(df["High"])
    df["Low"] = pd.to_numeric(df["Low"])
    df["Close"] = pd.to_numeric(df["Close"])
    df["Volume"] = pd.to_numeric(df["Volume"])
    df["Quote Asset Volume"] = pd.to_numeric(df["Quote Asset Volume"])
    df["Number of Trades"] = pd.to_numeric(df["Number of Trades"])
    df["Taker Buy Base Asset Volume"] = pd.to_numeric(df["Taker Buy Base Asset Volume"])
    df["Taker Buy Quote Asset Volume"] = pd.to_numeric(df["Taker Buy Quote Asset Volume"])
    df.set_index("Open Time", inplace=True)
    return df


def load_klines(csv_filepath: str) -> pd.DataFrame:
    return pd.read_csv(csv_filepath, index_col=0, parse_dates=True)


def klines_df_check(df: pd.DataFrame):

    # check that the dataframe is sorted
    if not df.index.is_monotonic_increasing:
        decreasing_indices = np.where(np.diff(df.index.astype(np.int64)) <= 0)[0]
        if decreasing_indices:
            warnings.warn(f"The dataframe is not sorted by its index. Found breaks at positions: {decreasing_indices}")

    # check for duplicated rows
    if df.duplicated().any():
        warnings.warn(f"The dataframe contains duplicate rows. {df.index[df.duplicated()]}")

    # check for missing timestamps
    date_range = pd.date_range(
        start=df.index.min(),
        end=df.index.max(),
        freq=_timedelta_to_interval_str(df.index[1] - df.index[0], pandas_friendly=True),
    )
    missing_dates = date_range.difference(df.index)
    if not missing_dates.empty:
        warnings.warn(f"The DataFrame is missing entries. {missing_dates}")


def update_klines(csv_filepath: str, symbol: str, interval: str) -> pd.DataFrame:
    df = load_klines(csv_filepath)
    last_entry_date = df.index[-1]
    datetime_now = datetime.now(timezone.utc)

    if not datetime_now - last_entry_date > _interval_str_to_timedelta(interval):
        logging.info("data is up to date")

    else:
        logging.info("Updating %s %s data...", symbol, interval)

        new_data = []
        time_frames = _generate_timeframes(
            start_time=f"{last_entry_date.strftime('%Y-%m-%d %H:%M:%S')}",
            end_time=f"{datetime_now.strftime('%Y-%m-%d %H:%M:%S')}",
            interval=interval,
            limit=500,
        )

        for start_time, end_time in time_frames:
            logging.info("Downloading %s %s data from %s to %s...", symbol, interval, start_time, end_time)
            new_data += get_klines(symbol, interval, start_time, end_time)
            sleep(1)

        new_data = klines_to_df(new_data)

        df = pd.concat([df, new_data])
        df = df[~df.index.duplicated(keep="last")]
        df.to_csv(csv_filepath, index_label="Open Time")

    return df


def _generate_signature(api_secret: str, params: dict) -> str:
    return hmac.new(api_secret.encode("utf-8"), urlencode(params).encode("utf-8"), hashlib.sha256).hexdigest()


def _datetime_str_to_utc_milliseconds(datetime_str: str) -> int:
    return int(datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc).timestamp()) * 1000


def _generate_timeframes(start_time: str, end_time: str, interval: str, limit: int) -> list[tuple]:
    start = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    delta = _interval_str_to_timedelta(interval)
    pair_duration = delta * limit
    result = []
    current_start = start
    while current_start < end:
        current_end = min(current_start + pair_duration, end)
        result.append(
            (
                datetime.strftime(current_start, "%Y-%m-%d %H:%M:%S"),
                datetime.strftime(current_end, "%Y-%m-%d %H:%M:%S"),
            )
        )
        current_start = current_end
    return result


def _interval_str_to_timedelta(interval: str) -> timedelta:
    interval_value = int("".join([c for c in interval if c.isdigit()]))
    interval_unit = "".join([c for c in interval if c.isalpha()])
    if interval_unit in ("s", "sec", "second", "seconds"):
        return timedelta(seconds=interval_value)
    if interval_unit in ("m", "min", "minute", "minutes"):
        return timedelta(minutes=interval_value)
    if interval_unit in ("h", "hr", "hour", "hours"):
        return timedelta(hours=interval_value)
    if interval_unit in ("d", "day", "days"):
        return timedelta(days=interval_value)
    if interval_unit in ("w", "week", "weeks"):
        return timedelta(weeks=interval_value)
    raise ValueError(f"unsupported interval unit: '{interval_unit}'")


def _timedelta_to_interval_str(timedelta_obj: timedelta, pandas_friendly: bool = False) -> str:
    seconds = int(timedelta_obj.total_seconds())
    if seconds < 60:
        return f"{seconds}s"
    if seconds < 60 * 60:
        return f"{seconds // 60}min" if pandas_friendly else f"{seconds // 60}m"
    if seconds < 60 * 60 * 24:
        return f"{seconds // (60 * 60)}h"
    if seconds < 60 * 60 * 24 * 7:
        return f"{seconds // (60 * 60 * 24)}d"
    return f"{seconds // (60 * 60 * 24 * 7)}W" if pandas_friendly else f"{seconds // (60 * 60 * 24 * 7)}w"


async def listen_to_average_price(symbol_pair: str = "btcusdt"):
    """Listen to average price for a symbol pair.
    Average price streams push changes in the average price over a fixed time interval.

    Stream Name: <symbol>@avgPrice
    Update Speed: 1000ms

    Payload
        {
            "e": "avgPrice",          // Event type
            "E": 1693907033000,       // Event time
            "s": "BTCUSDT",           // Symbol
            "i": "5m",                // Average price interval
            "w": "25776.86000000",    // Average price
            "T": 1693907032213        // Last trade time
        }
    """
    symbol_pair = symbol_pair.lower()
    uri = f"{BASE_URI}{symbol_pair}@avgPrice"

    async with websockets.connect(uri) as websocket:
        print(f"Connected to Binance WebSocket for {symbol_pair} avgPrice.")
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            print(f"avgPrice: {data}")


async def listen_to_trades(symbol_pair: str = "btcusdt"):
    """Listen to trades for a symbol pair.
    The Trade Streams push raw trade information; each trade has a unique buyer and seller.

    Stream Name: <symbol>@trade
    Update Speed: real-time

    Payload
        {
            "e": "trade",       // Event type
            "E": 1672515782136, // Event time
            "s": "BNBBTC",      // Symbol
            "t": 12345,         // Trade ID
            "p": "0.001",       // Price
            "q": "100",         // Quantity
            "T": 1672515782136, // Trade time
            "m": true,          // Is the buyer the market maker?
            "M": true           // Ignore
        }
    """
    symbol_pair = symbol_pair.lower()
    uri = f"{BASE_URI}{symbol_pair}@trade"

    async with websockets.connect(uri) as websocket:
        print(f"Connected to Binance WebSocket for {symbol_pair} trades.")
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            print(f"Trade: {data}")


async def listen_to_klines(symbol_pair: str = "btcusdt", interval: str = "1m"):
    """Listen to klines for a symbol pair.
    The Kline/Candlestick Stream push updates to the current klines/candlestick every second in UTC+0 timezone

    Stream Name: <symbol>@kline_<interval>
    Update Speed: 1000ms for 1s, 2000ms for the other intervals

    Payload
        {
            "e": "kline",         // Event type
            "E": 1672515782136,   // Event time
            "s": "BNBBTC",        // Symbol
            "k": {
                "t": 1672515780000, // Kline start time
                "T": 1672515839999, // Kline close time
                "s": "BNBBTC",      // Symbol
                "i": "1m",          // Interval
                "f": 100,           // First trade ID
                "L": 200,           // Last trade ID
                "o": "0.0010",      // Open price
                "c": "0.0020",      // Close price
                "h": "0.0025",      // High price
                "l": "0.0015",      // Low price
                "v": "1000",        // Base asset volume
                "n": 100,           // Number of trades
                "x": false,         // Is this kline closed?
                "q": "1.0000",      // Quote asset volume
                "V": "500",         // Taker buy base asset volume
                "Q": "0.500",       // Taker buy quote asset volume
                "B": "123456"       // Ignore
            }
        }
    """

    if interval not in KLINE_INTERVALS:
        raise ValueError(f"Invalid interval: {interval}. Supported intervals: {KLINE_INTERVALS}")

    symbol_pair = symbol_pair.lower()
    uri = f"{BASE_URI}{symbol_pair}@kline_{interval}"

    async with websockets.connect(uri) as websocket:
        print(f"Connected to Binance WebSocket for {symbol_pair} {interval} klines.")
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            print(f"Klines: {data}")


# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(listen_to_average_price())
#     asyncio.run(listen_to_trades())
#     asyncio.run(listen_to_klines())
