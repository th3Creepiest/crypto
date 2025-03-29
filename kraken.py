import requests


BASE_URL = "https://api.kraken.com/0/public/"
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36", "Accept": "application/json"}


def get_system_status() -> dict:
    """Get the system status or trading mode."""
    response = requests.get(url=BASE_URL + "SystemStatus", headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.json()


def get_server_time() -> dict:
    """Get the server time."""
    response = requests.get(url=BASE_URL + "Time", headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.json()


def get_asset_info(asset: str | None = None, asset_class: str = "currency") -> dict:
    """Get information about the assets that are available for deposit, withdrawal, trading and earn.
    asset : string (optional, default: all available assets). Example: XBT,ETH
    asset_class : string (optional, default: currency)
    """
    params = {"aclass": asset_class}
    if asset:
        params["asset"] = asset

    response = requests.get(url=BASE_URL + "Assets", headers=HEADERS, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def get_tradable_asset_pairs(pair: str | None = None, info: str = "info", country_code: str | None = None) -> dict:
    """Get tradable asset pairs.
    pair : string (optional) - Asset pairs to get data for. Example: BTC/USD,ETH/BTC
    info : string (optional, default: info) - Possible values: [info, leverage, fees, margin]
    country_code : string (optional) - Filter for response to only include pairs available in provided countries/regions. Example: US,TX,GB,CA
    """
    possible_info = ["info", "leverage", "fees", "margin"]
    if info not in possible_info:
        raise ValueError(f"Invalid info value. Possible values: {possible_info}")

    params = {"info": info}

    if pair:
        params["pair"] = pair

    if country_code:
        params["country_code"] = country_code

    response = requests.get(url=BASE_URL + "AssetPairs", headers=HEADERS, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def get_ticker_information(pair: str | None = None) -> dict:
    """Get ticker information for all or requested markets.

    To clarify usage, note that:
        * Today's prices start at midnight UTC
        * Leaving the pair parameter blank will return tickers for all tradeable assets on Kraken

    pair: string - Asset pair to get data for (optional, default: all tradeable exchange pairs) - Example: XBTUSD
    """
    params = {}
    if pair:
        params["pair"] = pair

    response = requests.get(url=BASE_URL + "Ticker", headers=HEADERS, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def get_ohlc_data(pair: str | None = None, interval: int = 60, since: int | None = None) -> dict:
    """Retrieve OHLC market data.

    The last entry in the OHLC array is for the current, not-yet-committed timeframe, and will always be present, regardless of the value of since.
    Returns up to 720 of the most recent entries (older data cannot be retrieved, regardless of the value of since).

    pair: string - Asset pair to get data for (optional, default: all tradeable exchange pairs) - Example: XBTUSD
    interval: integer - Time frame interval in minutes (optional, default: 1) - Possible values: 1, 5, 15, 30, 60, 240, 1440, 10080, 21600
    since: integer - Return only data from this timestamp onwards (optional)
    """
    possible_intervals = [1, 5, 15, 30, 60, 240, 1440, 10080, 21600]
    if interval not in possible_intervals:
        raise ValueError(f"Invalid interval value. Possible values: {possible_intervals}")

    params = {}

    if pair:
        params["pair"] = pair

    if since:
        params["since"] = since

    params["interval"] = interval

    response = requests.get(url=BASE_URL + "OHLC", headers=HEADERS, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def get_order_book(pair: str, count: int = 100) -> dict:
    """Returns level 2 (L2) order book, which describes the individual price levels in the book with aggregated order quantities at each level.
    pair: string - Asset pair to get data for (required) - Example: XBTUSD
    count: integer - Possible values: >= 1 and <= 500 - Default value: 100 - Maximum number of asks/bids
    """
    if count < 1 or count > 500:
        raise ValueError("Count must be between 1 and 500")

    params = {"pair": pair, "count": count}

    response = requests.get(url=BASE_URL + "Depth", headers=HEADERS, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def get_recent_trades(pair: str, count: int = 1000, since: int | None = None) -> dict:
    """Returns the last 1000 trades by default.
    pair: string - Asset pair to get data for (required) - Example: XBTUSD
    since: string - Return trade data since given timestamp (optional) - Example: 1616663618
    count: integer - Possible values: >= 1 and <= 1000 - Default value: 1000 - Return specific number of trades, up to 1000
    """
    if count < 1 or count > 1000:
        raise ValueError("Count must be between 1 and 1000")

    params = {"pair": pair, "count": count}

    if since:
        params["since"] = since

    response = requests.get(url=BASE_URL + "Trades", headers=HEADERS, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def get_recent_spreads(pair: str, since: int | None = None) -> dict:
    """Returns the last ~200 top-of-book spreads for a given pair.
    pair: string - Asset pair to get data for (required) - Example: XBTUSD
    since: integer - Returns spread data since given timestamp. Optional, intended for incremental updates within available dataset (does not contain all historical spreads).
        * Example: 1678219570
    """
    params = {}
    params["pair"] = pair

    if since:
        params["since"] = since

    response = requests.get(url=BASE_URL + "Spread", headers=HEADERS, params=params, timeout=10)
    response.raise_for_status()
    return response.json()
