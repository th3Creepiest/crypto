from unittest.mock import patch
from datetime import timedelta

import pytest
from requests import HTTPError

from binance import (
    ping,
    get_server_time,
    get_average_price,
    get_latest_price,
    get_exchange_info,
    get_exchange_info_for_symbol,
    get_exchange_info_for_symbols,
    get_24hr_ticker,
    get_24hr_ticker_for_symbol,
    get_24hr_ticker_for_symbols,
    get_trading_day_ticker_for_symbol,
    get_trading_day_ticker_for_symbols,
    get_price_ticker_for_symbol,
    get_price_ticker_for_symbols,
    get_order_book_ticker_for_symbol,
    get_order_book_ticker_for_symbols,
    get_rolling_ticker_for_symbol,
    get_rolling_ticker_for_symbols,
    get_klines,
    get_klines_for_year,
    get_account_info,
    _generate_signature,
    _datetime_str_to_utc_milliseconds,
    _interval_str_to_timedelta,
    _timedelta_to_interval_str,
    _generate_timeframes,
)


HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36", "Accept-Encoding": "gzip, deflate", "Accept": "application/json", "Connection": "keep-alive"}


class TestPing:
    URL = "https://api.binance.com/api/v3/ping"

    def test_ping_success(self, requests_mock):
        requests_mock.get(self.URL, json={})
        assert ping() == {}
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    @pytest.mark.parametrize(
        "status_code",
        [400, 403, 500],
        ids=[
            "test_ping_failure: Bad Request",
            "test_ping_failure: Forbidden",
            "test_ping_failure: Internal Server Error",
        ],
    )
    def test_ping_failure(self, requests_mock, status_code):
        requests_mock.get(self.URL, status_code=status_code)
        with pytest.raises(HTTPError):
            ping()
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS


class TestGetServerTime:
    URL = "https://api.binance.com/api/v3/time"

    def test_get_server_time_success(self, requests_mock):
        requests_mock.get(self.URL, json={"serverTime": 1499827319559})
        assert get_server_time() == {"serverTime": 1499827319559}
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    @pytest.mark.parametrize(
        "status_code",
        [400, 403, 500],
        ids=[
            "test_get_server_time_failure: Bad Request",
            "test_get_server_time_failure: Forbidden",
            "test_get_server_time_failure: Internal Server Error",
        ],
    )
    def test_get_server_time_failure(self, requests_mock, status_code):
        requests_mock.get(self.URL, status_code=status_code)
        with pytest.raises(HTTPError):
            get_server_time()
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS


class TestGetAveragePrice:
    URL = "https://api.binance.com/api/v3/avgPrice"

    def test_get_average_price(self, requests_mock):
        mock_response = {"mins": 5, "price": "0.00932986", "closeTime": 1727289599688}
        requests_mock.get(self.URL, json=mock_response)
        assert get_average_price("BNBBTC") == mock_response
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "?symbol=BNBBTC"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    @pytest.mark.parametrize(
        "status_code",
        [400, 403, 500],
        ids=[
            "test_get_average_price_failure: Bad Request",
            "test_get_average_price_failure: Forbidden",
            "test_get_average_price_failure: Internal Server Error",
        ],
    )
    def test_get_average_price_failure(self, requests_mock, status_code):
        requests_mock.get(self.URL, status_code=status_code)
        with pytest.raises(HTTPError):
            get_average_price("BNBBTC")
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "?symbol=BNBBTC"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS


class TestGetLatestPrice:
    URL = "https://api.binance.com/api/v3/ticker/price"

    def test_get_latest_price(self, requests_mock):
        requests_mock.get(self.URL, json={"symbol": "BTCUSDT", "price": "75000"})
        assert get_latest_price("BTCUSDT") == {"symbol": "BTCUSDT", "price": "75000"}
        assert requests_mock.called_once
        assert requests_mock.last_request.url == f"{self.URL}?symbol=BTCUSDT"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    @pytest.mark.parametrize(
        "status_code",
        [400, 403, 500],
        ids=[
            "test_get_latest_price_failure: Bad Request",
            "test_get_latest_price_failure: Forbidden",
            "test_get_latest_price_failure: Internal Server Error",
        ],
    )
    def test_get_latest_price_failure(self, requests_mock, status_code):
        requests_mock.get(self.URL, status_code=status_code)
        with pytest.raises(HTTPError):
            get_latest_price("BTCUSDT")
        assert requests_mock.called_once


class TestGetExchangeInfo:
    URL = "https://api.binance.com/api/v3/exchangeInfo"

    def test_get_exchange_info(self, requests_mock):
        requests_mock.get(self.URL, json={})
        assert get_exchange_info() == {}
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    def test_get_exchange_info_for_symbol(self, requests_mock):
        requests_mock.get(self.URL, json={})
        assert get_exchange_info_for_symbol("BNBBTC") == {}
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "?symbol=BNBBTC"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    def test_get_exchange_info_for_symbols(self, requests_mock):
        requests_mock.get(self.URL, json={})
        assert get_exchange_info_for_symbols(["BNBBTC", "BTCUSDT"]) == {}
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "?symbols=%5B%22BNBBTC%22,%22BTCUSDT%22%5D"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    @pytest.mark.parametrize(
        "status_code",
        [400, 403, 500],
        ids=[
            "test_get_exchange_info_failure: Bad Request",
            "test_get_exchange_info_failure: Forbidden",
            "test_get_exchange_info_failure: Internal Server Error",
        ],
    )
    def test_get_exchange_info_http_failure(self, requests_mock, status_code):
        requests_mock.get(self.URL, status_code=status_code)
        with pytest.raises(HTTPError):
            get_exchange_info()
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL

    @pytest.mark.parametrize(
        "status_code",
        [400, 403, 500],
        ids=[
            "test_get_exchange_info_for_symbol_failure: Bad Request",
            "test_get_exchange_info_for_symbol_failure: Forbidden",
            "test_get_exchange_info_for_symbol_failure: Internal Server Error",
        ],
    )
    def test_get_exchange_info_for_symbol_http_failure(self, requests_mock, status_code):
        requests_mock.get(self.URL, status_code=status_code)
        with pytest.raises(HTTPError):
            get_exchange_info_for_symbol("BNBBTC")
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "?symbol=BNBBTC"

    @pytest.mark.parametrize(
        "status_code",
        [400, 403, 500],
        ids=[
            "test_get_exchange_info_for_symbols_failure: Bad Request",
            "test_get_exchange_info_for_symbols_failure: Forbidden",
            "test_get_exchange_info_for_symbols_failure: Internal Server Error",
        ],
    )
    def test_get_exchange_info_for_multiple_symbols_http_failure(self, requests_mock, status_code):
        requests_mock.get(self.URL, status_code=status_code)
        with pytest.raises(HTTPError):
            get_exchange_info_for_symbols(["BNBBTC", "BTCUSDT"])
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "?symbols=%5B%22BNBBTC%22,%22BTCUSDT%22%5D"


class TestGet24hrTicker:
    URL = "https://api.binance.com/api/v3/ticker/24hr"

    @pytest.mark.parametrize("request_type", ["FULL", "MINI"])
    def test_get_24hr_ticker(self, requests_mock, request_type):
        requests_mock.get(self.URL, json=[{}])
        assert get_24hr_ticker(request_type) == [{}]
        assert requests_mock.called_once
        assert requests_mock.last_request.url == f"{self.URL}?type={request_type}"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    @pytest.mark.parametrize("request_type", ["FULL", "MINI"])
    def test_get_24hr_ticker_http_failure(self, requests_mock, request_type):
        requests_mock.get(self.URL, status_code=400)
        with pytest.raises(HTTPError):
            get_24hr_ticker(request_type)
        assert requests_mock.called_once

    def test_get_24hr_ticker_with_invalid_request_type(self):
        with pytest.raises(ValueError, match="Invalid type: 'invalid'. Supported types: FULL, MINI"):
            get_24hr_ticker(request_type="invalid")

    @pytest.mark.parametrize("request_type", ["FULL", "MINI"])
    def test_get_24hr_ticker_for_symbol(self, requests_mock, request_type):
        requests_mock.get(self.URL, json={})
        assert get_24hr_ticker_for_symbol("BNBBTC", request_type) == {}
        assert requests_mock.called_once
        assert requests_mock.last_request.url == f"{self.URL}?type={request_type}&symbol=BNBBTC"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    @pytest.mark.parametrize("request_type", ["FULL", "MINI"])
    def test_get_24hr_ticker_for_symbol_http_failure(self, requests_mock, request_type):
        requests_mock.get(self.URL, status_code=400)
        with pytest.raises(HTTPError):
            get_24hr_ticker_for_symbol("BNBBTC", request_type)
        assert requests_mock.called_once

    def test_get_24hr_ticker_for_symbol_with_invalid_request_type(self):
        with pytest.raises(ValueError, match="Invalid type: 'invalid'. Supported types: FULL, MINI"):
            get_24hr_ticker_for_symbol("BNBBTC", request_type="invalid")

    @pytest.mark.parametrize("request_type", ["FULL", "MINI"])
    def test_get_24hr_ticker_for_symbols(self, requests_mock, request_type):
        requests_mock.get(self.URL, json=[{}])
        assert get_24hr_ticker_for_symbols(["BTCUSDT", "BNBUSDT"], request_type) == [{}]
        assert requests_mock.called_once
        assert requests_mock.last_request.url == f"{self.URL}?type={request_type}&symbols=%5B%22BTCUSDT%22,%22BNBUSDT%22%5D"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    @pytest.mark.parametrize("request_type", ["FULL", "MINI"])
    def test_get_24hr_ticker_for_symbols_http_failure(self, requests_mock, request_type):
        requests_mock.get(self.URL, status_code=400)
        with pytest.raises(HTTPError):
            get_24hr_ticker_for_symbols(["BNBBTC", "BTCUSDT"], request_type)
        assert requests_mock.called_once

    def test_get_24hr_ticker_for_symbols_with_invalid_request_type(self):
        with pytest.raises(ValueError, match="Invalid type: 'invalid'. Supported types: FULL, MINI"):
            get_24hr_ticker_for_symbols(["BNBBTC", "BTCUSDT"], request_type="invalid")


class TestGetTradingDayTicker:
    URL = "https://api.binance.com/api/v3/ticker/tradingDay"

    @pytest.mark.parametrize("request_type", ["FULL", "MINI"])
    def test_get_trading_day_ticker(self, requests_mock, request_type):
        requests_mock.get(self.URL, json={})
        assert get_trading_day_ticker_for_symbol("BNBBTC", request_type) == {}
        assert requests_mock.called_once
        assert requests_mock.last_request.url == f"{self.URL}?type={request_type}&symbol=BNBBTC"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    @pytest.mark.parametrize("request_type", ["FULL", "MINI"])
    def test_get_trading_day_ticker_for_symbol_http_failure(self, requests_mock, request_type):
        requests_mock.get(self.URL, status_code=400)
        with pytest.raises(HTTPError):
            get_trading_day_ticker_for_symbol("BNBBTC", request_type)
        assert requests_mock.called_once

    def test_get_trading_day_ticker_for_symbol_with_invalid_request_type(self):
        with pytest.raises(ValueError, match="Invalid type: 'invalid'. Supported types: FULL, MINI"):
            get_trading_day_ticker_for_symbol("BNBBTC", request_type="invalid")

    @pytest.mark.parametrize("request_type", ["FULL", "MINI"])
    def test_get_trading_day_ticker_for_symbols(self, requests_mock, request_type):
        requests_mock.get(self.URL, json=[{}])
        assert get_trading_day_ticker_for_symbols(["BTCUSDT", "BNBUSDT"], request_type) == [{}]
        assert requests_mock.called_once
        assert requests_mock.last_request.url == f"{self.URL}?type={request_type}&symbols=%5B%22BTCUSDT%22,%22BNBUSDT%22%5D"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    @pytest.mark.parametrize("request_type", ["FULL", "MINI"])
    def test_get_trading_day_ticker_for_symbols_http_failure(self, requests_mock, request_type):
        requests_mock.get(self.URL, status_code=400)
        with pytest.raises(HTTPError):
            get_trading_day_ticker_for_symbols(["BNBBTC", "BTCUSDT"], request_type)
        assert requests_mock.called_once

    def test_get_trading_day_ticker_for_symbols_with_invalid_request_type(self):
        with pytest.raises(ValueError, match="Invalid type: 'invalid'. Supported types: FULL, MINI"):
            get_trading_day_ticker_for_symbols(["BNBBTC", "BTCUSDT"], request_type="invalid")


class TestGetPriceTicker:
    URL = "https://api.binance.com/api/v3/ticker/price"

    def test_get_price_ticker_for_symbol(self, requests_mock):
        requests_mock.get(self.URL, json={"symbol": "LTCBTC", "price": "4.00000200"})
        assert get_price_ticker_for_symbol("LTCBTC") == {"symbol": "LTCBTC", "price": "4.00000200"}
        assert requests_mock.called_once
        assert requests_mock.last_request.url == f"{self.URL}?symbol=LTCBTC"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    def test_get_price_ticker_for_symbol_http_failure(self, requests_mock):
        requests_mock.get(self.URL, status_code=400)
        with pytest.raises(HTTPError):
            get_price_ticker_for_symbol("BNBBTC")
        assert requests_mock.called_once

    def test_get_price_ticker_for_symbols(self, requests_mock):
        requests_mock.get(self.URL, json=[{}])
        assert get_price_ticker_for_symbols(["BTCUSDT", "BNBUSDT"]) == [{}]
        assert requests_mock.called_once
        assert requests_mock.last_request.url == f"{self.URL}?symbols=%5B%22BTCUSDT%22,%22BNBUSDT%22%5D"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    def test_get_price_ticker_for_symbols_http_failure(self, requests_mock):
        requests_mock.get(self.URL, status_code=400)
        with pytest.raises(HTTPError):
            get_price_ticker_for_symbols(["BNBBTC", "BTCUSDT"])
        assert requests_mock.called_once


class TestGetOrderBookTicker:
    URL = "https://api.binance.com/api/v3/ticker/bookTicker"

    def test_get_order_book_ticker_for_symbol(self, requests_mock):
        mock_response = {
            "symbol": "LTCBTC",
            "bidPrice": "4.00000000",
            "bidQty": "431.00000000",
            "askPrice": "4.00000200",
            "askQty": "9.00000000",
        }
        requests_mock.get(self.URL, json=mock_response)
        assert get_order_book_ticker_for_symbol("LTCBTC") == mock_response
        assert requests_mock.called_once
        assert requests_mock.last_request.url == f"{self.URL}?symbol=LTCBTC"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    def test_get_order_book_ticker_for_symbol_http_failure(self, requests_mock):
        requests_mock.get(self.URL, status_code=400)
        with pytest.raises(HTTPError):
            get_order_book_ticker_for_symbol("BNBBTC")
        assert requests_mock.called_once

    def test_get_order_book_ticker_for_symbols(self, requests_mock):
        mock_response = [
            {
                "symbol": "LTCBTC",
                "bidPrice": "4.00000000",
                "bidQty": "431.00000000",
                "askPrice": "4.00000200",
                "askQty": "9.00000000",
            },
            {
                "symbol": "ETHBTC",
                "bidPrice": "0.07946700",
                "bidQty": "9.00000000",
                "askPrice": "100000.00000000",
                "askQty": "1000.00000000",
            },
        ]
        requests_mock.get(self.URL, json=mock_response)
        assert get_order_book_ticker_for_symbols(["BTCUSDT", "BNBUSDT"]) == mock_response
        assert requests_mock.called_once
        assert requests_mock.last_request.url == f"{self.URL}?symbols=%5B%22BTCUSDT%22,%22BNBUSDT%22%5D"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    def test_get_order_book_ticker_for_symbols_http_failure(self, requests_mock):
        requests_mock.get(self.URL, status_code=400)
        with pytest.raises(HTTPError):
            get_order_book_ticker_for_symbols(["BNBBTC", "BTCUSDT"])
        assert requests_mock.called_once


class TestGetRollingTicker:
    URL = "https://api.binance.com/api/v3/ticker"

    @pytest.mark.parametrize("window_size", ["1m", "1h", "1d"])
    @pytest.mark.parametrize("request_type", ["FULL", "MINI"])
    def test_get_rolling_ticker_for_symbol(self, requests_mock, request_type, window_size):
        requests_mock.get(self.URL, json={})
        assert get_rolling_ticker_for_symbol("BNBBTC", window_size, request_type) == {}
        assert requests_mock.called_once
        assert requests_mock.last_request.url == f"{self.URL}?type={request_type}&symbol=BNBBTC&windowSize={window_size}"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    def test_get_rolling_ticker_for_symbol_http_failure(self, requests_mock):
        requests_mock.get(self.URL, status_code=400)
        with pytest.raises(HTTPError):
            get_rolling_ticker_for_symbol("BNBBTC")
        assert requests_mock.called_once

    def test_get_rolling_ticker_for_symbol_with_invalid_request_type(self):
        with pytest.raises(ValueError, match="Invalid type: 'invalid'. Supported types: FULL, MINI"):
            get_rolling_ticker_for_symbol("BNBBTC", request_type="invalid")

    def test_get_rolling_ticker_for_symbol_with_invalid_window_size(self):
        with pytest.raises(ValueError, match="Invalid window size: 'invalid'"):
            get_rolling_ticker_for_symbol("BNBBTC", window_size="invalid")

    @pytest.mark.parametrize("window_size", ["1m", "1h", "1d"])
    @pytest.mark.parametrize("request_type", ["FULL", "MINI"])
    def test_get_rolling_ticker_for_symbols(self, requests_mock, request_type, window_size):
        requests_mock.get(self.URL, json=[{}])
        assert get_rolling_ticker_for_symbols(["BTCUSDT", "BNBUSDT"], window_size, request_type) == [{}]
        assert requests_mock.called_once
        assert requests_mock.last_request.url == f"{self.URL}?type={request_type}&symbols=%5B%22BTCUSDT%22,%22BNBUSDT%22%5D&windowSize={window_size}"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    def test_get_rolling_ticker_for_symbols_http_failure(self, requests_mock):
        requests_mock.get(self.URL, status_code=400)
        with pytest.raises(HTTPError):
            get_rolling_ticker_for_symbols(["BNBBTC", "BTCUSDT"])
        assert requests_mock.called_once

    def test_get_rolling_ticker_for_symbols_with_invalid_request_type(self):
        with pytest.raises(ValueError, match="Invalid type: 'invalid'. Supported types: FULL, MINI"):
            get_rolling_ticker_for_symbols(["BNBBTC", "BTCUSDT"], request_type="invalid")

    def test_get_rolling_ticker_for_symbols_with_invalid_window_size(self):
        with pytest.raises(ValueError, match="Invalid window size: 'invalid'"):
            get_rolling_ticker_for_symbols(["BNBBTC", "BTCUSDT"], window_size="invalid")


class TestGetKlines:
    URL = "https://api.binance.com/api/v3/klines"

    @pytest.mark.parametrize(
        ("symbol", "interval", "start_time", "end_time", "limit", "expected_url"),
        (
            pytest.param(
                "BTCUSDT",
                "1h",
                None,
                None,
                500,
                f"{URL}?symbol=BTCUSDT&interval=1h&limit=500",
                id="get_klines(BTCUSDT 1h)",
            ),
            pytest.param(
                "BTCUSDT",
                "1d",
                None,
                None,
                500,
                f"{URL}?symbol=BTCUSDT&interval=1d&limit=500",
                id="get_klines(BTCUSDT 1d)",
            ),
            pytest.param(
                "BTCUSDT",
                "1h",
                "2023-01-01 00:00:00",
                None,
                500,
                f"{URL}?symbol=BTCUSDT&interval=1h&limit=500&startTime=1672531200000",
                id="get_klines(BTCUSDT 1h 2023-01-01 00:00:00 None)",
            ),
            pytest.param(
                "BTCUSDT",
                "1h",
                None,
                "2023-01-02 00:00:00",
                500,
                f"{URL}?symbol=BTCUSDT&interval=1h&limit=500&endTime=1672617600000",
                id="get_klines(BTCUSDT 1h None 2023-01-02 00:00:00)",
            ),
            pytest.param(
                "BTCUSDT",
                "1h",
                "2023-01-01 00:00:00",
                "2023-01-02 00:00:00",
                500,
                f"{URL}?symbol=BTCUSDT&interval=1h&limit=500&startTime=1672531200000&endTime=1672617600000",
                id="get_klines(BTCUSDT 1h 2023-01-01 00:00:00 2023-01-02 00:00:00 500)",
            ),
        ),
    )
    def test_get_klines(self, requests_mock, symbol, interval, start_time, end_time, limit, expected_url):
        requests_mock.get(self.URL, json=[])
        assert get_klines(symbol, interval, start_time, end_time, limit) == []
        assert requests_mock.called_once
        assert requests_mock.last_request.url == expected_url
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    @pytest.mark.parametrize(
        "status_code",
        [400, 403, 500],
        ids=[
            "test_get_klines_failure: Bad Request",
            "test_get_klines_failure: Forbidden",
            "test_get_klines_failure: Internal Server Error",
        ],
    )
    def test_get_klines_http_failure(self, requests_mock, status_code):
        requests_mock.get(self.URL, status_code=status_code)
        with pytest.raises(HTTPError):
            get_klines("BTCUSDT")
        assert requests_mock.called_once

    def test_get_klines_with_invalid_interval(self):
        with pytest.raises(ValueError):
            get_klines("BTCUSDT", interval="invalid")

    @pytest.mark.parametrize(
        "limit",
        [0, 1001],
        ids=["test_get_klines_with_invalid_limit: 0", "test_get_klines_with_invalid_limit: 1001"],
    )
    def test_get_klines_with_invalid_limit(self, limit):
        with pytest.raises(ValueError):
            get_klines("BTCUSDT", limit=limit)


class TestGetKlinesForYear:
    URL = "https://api.binance.com/api/v3/klines"

    @patch("binance.sleep", autospec=True)
    def test_get_klines_for_year_with_daily_interval(self, sleep_mock, requests_mock):
        mock_response = [[] for _ in range(365)]
        requests_mock.get(self.URL, json=mock_response)
        assert get_klines_for_year("BTCUSDT", 2023, "1d") == mock_response
        assert requests_mock.called_once
        assert requests_mock.last_request.url == f"{self.URL}?symbol=BTCUSDT&interval=1d&limit=500&startTime=1672531200000&endTime=1704063600000"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS
        sleep_mock.assert_called_once_with(1)

    @patch("binance.sleep", autospec=True)
    def test_get_klines_for_year_with_hourly_interval(self, sleep_mock, requests_mock):
        requests_mock.get(self.URL, json=[])
        assert get_klines_for_year("BTCUSDT", 2023, "1h") == []
        assert requests_mock.called
        assert requests_mock.call_count == 18
        sleep_mock.assert_called_with(1)
        assert sleep_mock.call_count == 18

    @patch("binance.sleep", autospec=True)
    def test_get_klines_for_year_with_minute_interval(self, sleep_mock, requests_mock):
        requests_mock.get(self.URL, json=[])
        assert get_klines_for_year("BTCUSDT", 2023, "1m") == []
        assert requests_mock.called
        assert requests_mock.call_count == 1052
        sleep_mock.assert_called_with(1)
        assert sleep_mock.call_count == 1052


class TestGetAccountInfo:
    URL = "https://api.binance.com/api/v3/account"

    @pytest.mark.parametrize(
        "omit_zero_balances",
        [True, False],
        ids=["test_get_account_info_with_omit_zero_balances", "test_get_account_info_without_omit_zero_balances"],
    )
    def test_get_account_info(self, requests_mock, omit_zero_balances):
        requests_mock.get(self.URL, json={})
        assert get_account_info("api_key", "shh", omit_zero_balances) == {}
        assert "X-MBX-APIKEY" in requests_mock.last_request.headers
        assert requests_mock.called_once
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.url.startswith(f"{self.URL}?omitZeroBalances={str(omit_zero_balances).lower()}&timestamp=")

    @pytest.mark.parametrize(
        "status_code",
        [400, 403, 500],
        ids=[
            "test_get_account_info_failure: Bad Request",
            "test_get_account_info_failure: Forbidden",
            "test_get_account_info_failure: Internal Server Error",
        ],
    )
    def test_get_account_info_failure(self, requests_mock, status_code):
        requests_mock.get(self.URL, status_code=status_code)
        with pytest.raises(HTTPError):
            get_account_info("api_key", "shh")
        assert "X-MBX-APIKEY" in requests_mock.last_request.headers
        assert requests_mock.called_once
        assert requests_mock.last_request.method == "GET"


def test_generate_signature():
    params = {"symbol": "BTCUSDT", "timestamp": 1634316558000}
    assert _generate_signature("test_secret", params) == "c8351edd351505825f918ad2cce3290adcf7bcef263c4ffb07fdd2bd0af3c1cf"


def test_datetime_str_to_utc_milliseconds():
    assert _datetime_str_to_utc_milliseconds("2023-10-12 10:15:30") == 1697105730000


class TestIntervalStrToTimedelta:

    @pytest.mark.parametrize(
        ["str_interval", "expected_timedelta"],
        [
            ("1s", timedelta(seconds=1)),
            ("2s", timedelta(seconds=2)),
            ("1m", timedelta(minutes=1)),
            ("1min", timedelta(minutes=1)),
            ("1h", timedelta(hours=1)),
            ("2h", timedelta(hours=2)),
            ("1d", timedelta(days=1)),
            ("2d", timedelta(days=2)),
            ("1w", timedelta(weeks=1)),
        ],
        ids=[
            "test_interval_str_to_timedelta: 1s",
            "test_interval_str_to_timedelta: 2s",
            "test_interval_str_to_timedelta: 1m",
            "test_interval_str_to_timedelta: 1min",
            "test_interval_str_to_timedelta: 1h",
            "test_interval_str_to_timedelta: 2h",
            "test_interval_str_to_timedelta: 1d",
            "test_interval_str_to_timedelta: 2d",
            "test_interval_str_to_timedelta: 1w",
        ],
    )
    def test_interval_str_to_timedelta(self, str_interval, expected_timedelta):
        assert _interval_str_to_timedelta(str_interval) == expected_timedelta

    def test_interval_str_to_timedelta_with_unsupported_interval(self):
        with pytest.raises(ValueError):
            _interval_str_to_timedelta("invalid_interval")


class TestTimedeltaToIntervalStr:

    @pytest.mark.parametrize(
        ["timedelta_obj", "expected_interval_str"],
        [
            (timedelta(seconds=1), "1s"),
            (timedelta(seconds=2), "2s"),
            (timedelta(minutes=1), "1m"),
            (timedelta(minutes=2), "2m"),
            (timedelta(hours=1), "1h"),
            (timedelta(hours=2), "2h"),
            (timedelta(days=1), "1d"),
            (timedelta(days=2), "2d"),
            (timedelta(weeks=1), "1w"),
            (timedelta(weeks=2), "2w"),
        ],
        ids=[
            "test_timedelta_to_interval_str: 1s",
            "test_timedelta_to_interval_str: 2s",
            "test_timedelta_to_interval_str: 1m",
            "test_timedelta_to_interval_str: 2m",
            "test_timedelta_to_interval_str: 1h",
            "test_timedelta_to_interval_str: 2h",
            "test_timedelta_to_interval_str: 1d",
            "test_timedelta_to_interval_str: 2d",
            "test_timedelta_to_interval_str: 1w",
            "test_timedelta_to_interval_str: 2w",
        ],
    )
    def test_timedelta_to_interval_str(self, timedelta_obj, expected_interval_str):
        assert _timedelta_to_interval_str(timedelta_obj) == expected_interval_str

    def test_timedelta_to_interval_str_pandas_friendly(self):
        assert _timedelta_to_interval_str(timedelta(minutes=1), pandas_friendly=True) == "1min"
        assert _timedelta_to_interval_str(timedelta(weeks=1), pandas_friendly=True) == "1W"


@pytest.mark.parametrize(
    ["start_time", "end_time", "interval", "limit", "expected_time_frames"],
    [
        (
            "2023-10-12 08:00:00",
            "2023-10-12 12:00:00",
            "1h",
            2,
            [
                ("2023-10-12 08:00:00", "2023-10-12 10:00:00"),
                ("2023-10-12 10:00:00", "2023-10-12 12:00:00"),
            ],
        ),
        (
            "2023-10-13 08:00:00",
            "2023-10-13 09:00:00",
            "1m",
            15,
            [
                ("2023-10-13 08:00:00", "2023-10-13 08:15:00"),
                ("2023-10-13 08:15:00", "2023-10-13 08:30:00"),
                ("2023-10-13 08:30:00", "2023-10-13 08:45:00"),
                ("2023-10-13 08:45:00", "2023-10-13 09:00:00"),
            ],
        ),
    ],
)
def test_generate_time_frames(start_time, end_time, interval, limit, expected_time_frames):
    assert _generate_timeframes(start_time, end_time, interval, limit) == expected_time_frames
