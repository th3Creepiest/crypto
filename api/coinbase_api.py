import requests


HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36", "Accept-Encoding": "gzip, deflate", "Accept": "application/json", "Connection": "keep-alive"}


def get_server_time() -> dict:
    """Test connectivity to the Rest API and get the current server time."""
    response = requests.get(url="https://api.coinbase.com/v2/time", headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.json()


def list_currencies() -> dict:
    """Get a list of all known currencies."""
    response = requests.get(url="https://api.coinbase.com/v2/currencies", headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.json()


def get_currency(currency_id: str) -> dict:
    """Get a currency by ID."""
    params = {"currency_id": currency_id}
    response = requests.get(url="https://api.coinbase.com/v2/currencies", headers=HEADERS, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def get_single_product_pairs(product_id: str) -> dict:
    """Get a list of available currency pairs for trading."""
    params = {"product_id": product_id}
    response = requests.get(url="https://api.coinbase.com/v2/products", headers=HEADERS, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def list_trading_pairs() -> dict:
    """Get a list of available currency pairs for trading."""
    response = requests.get(url="https://api.exchange.coinbase.com/products", headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.json()


def get_all_product_volume() -> dict:
    """Gets 30day and 24hour volume for all products and market types."""
    response = requests.get(url="https://api.exchange.coinbase.com/products/volume-summary", headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.json()


def get_single_product_info(product_id: str) -> dict:
    """Get information on a single product."""
    params = {"product_id": product_id}
    response = requests.get(url="https://api.exchange.coinbase.com/products", headers=HEADERS, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def get_product_candles(product_id: str, granularity: int | None = None, start: str | None = None, end: str | None = None) -> dict:
    """Historic rates for a product.
    Rates are returned in grouped buckets.
    Candle schema is of the form [timestamp, price_low, price_high, price_open, price_close]

    Parameters
    ----------
    product_id : str
        The product ID. Example: "BTC-USD"
    granularity : int | None
        The granularity field must be one of the following "second" values: {60, 300, 900, 3600, 21600, 86400}, or your request is rejected.
        These values correspond to time-slices representing one minute, five minutes, fifteen minutes, one hour, six hours, and one day, respectively.
    start : str | None
        Timestamp for starting range of aggregations.
    end : str | None
        Timestamp for ending range of aggregations.

    Returns
    -------
    dict
        A dictionary of the candles.

    Max Candles
        The maximum number of data points for a single request is 300 candles.
        If your selection of start/end time and granularity results in more than 300 data points, your request is rejected.
        To retrieve fine granularity data over a larger time range, you must make multiple requests with new start/end ranges.
    """

    if granularity and granularity not in [60, 300, 900, 3600, 21600, 86400]:
        raise ValueError("Granularity must be 60, 300, 900, 3600, 21600, or 86400")

    params = {}

    if granularity:
        params["granularity"] = granularity

    if start:
        params["start"] = start

    if end:
        params["end"] = end

    response = requests.get(url=f"https://api.exchange.coinbase.com/products/{product_id}/candles", headers=HEADERS, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def get_product_stats(product_id: str) -> dict:
    """Gets 30day and 24hour stats for a product.
    product_id : str - Example: "BTC-USD"
    """
    response = requests.get(url=f"https://api.exchange.coinbase.com/products/{product_id}/stats", headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.json()


def get_product_ticker(product_id: str) -> dict:
    """Gets snapshot information about the last trade (tick), best bid/ask and 24h volume.
    product_id : str - Example: "BTC-USD"
    """
    response = requests.get(url=f"https://api.exchange.coinbase.com/products/{product_id}/ticker", headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.json()


def get_product_trades(product_id: str) -> dict:
    """Gets a list of the latest trades for a product.
    product_id : str - Example: "BTC-USD"
    """
    response = requests.get(url=f"https://api.exchange.coinbase.com/products/{product_id}/trades", headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.json()
