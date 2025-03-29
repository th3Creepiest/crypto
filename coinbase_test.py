import pytest
from requests import HTTPError

from coinbase import (
    get_server_time,
    list_currencies,
    get_currency,
    get_single_product_pairs,
    list_trading_pairs,
    get_all_product_volume,
    get_single_product_info,
    get_product_candles,
    get_product_stats,
    get_product_ticker,
    get_product_trades,
)


HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36", "Accept-Encoding": "gzip, deflate", "Accept": "application/json", "Connection": "keep-alive"}


class TestGetServerTime:
    URL = "https://api.coinbase.com/v2/time"

    def test_get_server_time_success(self, requests_mock):
        requests_mock.get(self.URL, json={"data": {"iso": "2022-01-01T00:00:00Z", "epoch": 1640995200}})
        assert get_server_time() == {"data": {"iso": "2022-01-01T00:00:00Z", "epoch": 1640995200}}
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


class TestListCurrencies:
    URL = "https://api.coinbase.com/v2/currencies"

    def test_list_currencies_success(self, requests_mock):
        requests_mock.get(self.URL, json={})
        assert list_currencies() == {}
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    @pytest.mark.parametrize(
        "status_code",
        [400, 403, 500],
        ids=[
            "test_list_currencies_failure: Bad Request",
            "test_list_currencies_failure: Forbidden",
            "test_list_currencies_failure: Internal Server Error",
        ],
    )
    def test_list_currencies_failure(self, requests_mock, status_code):
        requests_mock.get(self.URL, status_code=status_code)
        with pytest.raises(HTTPError):
            list_currencies()
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS


class TestGetCurrency:
    URL = "https://api.coinbase.com/v2/currencies"

    def test_get_currency_success(self, requests_mock):
        requests_mock.get(self.URL, json={})
        assert get_currency("EUR") == {}
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "?currency_id=EUR"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    @pytest.mark.parametrize(
        "status_code",
        [400, 403, 500],
        ids=[
            "test_get_currency_failure: Bad Request",
            "test_get_currency_failure: Forbidden",
            "test_get_currency_failure: Internal Server Error",
        ],
    )
    def test_get_currency_failure(self, requests_mock, status_code):
        requests_mock.get(self.URL, status_code=status_code)
        with pytest.raises(HTTPError):
            get_currency("USD")
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "?currency_id=USD"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS


class TestGetSingleProductPairs:
    URL = "https://api.coinbase.com/v2/products"

    def test_get_single_product_pairs_success(self, requests_mock):
        requests_mock.get(self.URL, json=[])
        assert get_single_product_pairs("BTC-USD") == []
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "?product_id=BTC-USD"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    @pytest.mark.parametrize(
        "status_code",
        [400, 403, 500],
        ids=[
            "test_get_single_product_pairs_failure: Bad Request",
            "test_get_single_product_pairs_failure: Forbidden",
            "test_get_single_product_pairs_failure: Internal Server Error",
        ],
    )
    def test_get_single_product_pairs_failure(self, requests_mock, status_code):
        requests_mock.get(self.URL, status_code=status_code)
        with pytest.raises(HTTPError):
            get_single_product_pairs("BTC-USD")
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "?product_id=BTC-USD"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS


class TestListTradingPairs:
    URL = "https://api.exchange.coinbase.com/products"

    def test_list_trading_pairs_success(self, requests_mock):
        requests_mock.get(self.URL, json=[])
        assert list_trading_pairs() == []
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    @pytest.mark.parametrize(
        "status_code",
        [400, 403, 500],
        ids=[
            "test_list_trading_pairs_failure: Bad Request",
            "test_list_trading_pairs_failure: Forbidden",
            "test_list_trading_pairs_failure: Internal Server Error",
        ],
    )
    def test_list_trading_pairs_failure(self, requests_mock, status_code):
        requests_mock.get(self.URL, status_code=status_code)
        with pytest.raises(HTTPError):
            list_trading_pairs()
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS


class TestGetAllProductVolume:
    URL = "https://api.exchange.coinbase.com/products/volume-summary"

    def test_get_all_product_volume_success(self, requests_mock):
        requests_mock.get(self.URL, json=[])
        assert get_all_product_volume() == []
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    @pytest.mark.parametrize(
        "status_code",
        [400, 403, 500],
        ids=[
            "test_get_all_product_volume_failure: Bad Request",
            "test_get_all_product_volume_failure: Forbidden",
            "test_get_all_product_volume_failure: Internal Server Error",
        ],
    )
    def test_get_all_product_volume_failure(self, requests_mock, status_code):
        requests_mock.get(self.URL, status_code=status_code)
        with pytest.raises(HTTPError):
            get_all_product_volume()
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS


class TestGetSingleProductVolume:
    URL = "https://api.exchange.coinbase.com/products"

    def test_get_single_product_volume_success(self, requests_mock):
        requests_mock.get(self.URL, json=[])
        assert get_single_product_info("BTC-USD") == []
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "?product_id=BTC-USD"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    @pytest.mark.parametrize(
        "status_code",
        [400, 403, 500],
        ids=[
            "test_get_single_product_volume_failure: Bad Request",
            "test_get_single_product_volume_failure: Forbidden",
            "test_get_single_product_volume_failure: Internal Server Error",
        ],
    )
    def test_get_single_product_volume_failure(self, requests_mock, status_code):
        requests_mock.get(self.URL, status_code=status_code)
        with pytest.raises(HTTPError):
            get_single_product_info("BTC-USD")
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "?product_id=BTC-USD"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS


class TestGetProductCandles:
    URL = "https://api.exchange.coinbase.com/products"

    def test_get_product_candles_success(self, requests_mock):
        requests_mock.get(self.URL + "/BTC-USD/candles", json={})
        assert get_product_candles("BTC-USD") == {}
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "/BTC-USD/candles"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    def test_get_product_candles_with_granularity_success(self, requests_mock):
        requests_mock.get(self.URL + "/BTC-USD/candles", json={})
        assert get_product_candles("BTC-USD", granularity=60) == {}
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "/BTC-USD/candles?granularity=60"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    @pytest.mark.parametrize(
        "status_code",
        [400, 403, 500],
        ids=[
            "test_get_product_candles_failure: Bad Request",
            "test_get_product_candles_failure: Forbidden",
            "test_get_product_candles_failure: Internal Server Error",
        ],
    )
    def test_get_product_candles_failure(self, requests_mock, status_code):
        requests_mock.get(self.URL + "/BTC-USD/candles", status_code=status_code)
        with pytest.raises(HTTPError):
            get_product_candles("BTC-USD")
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "/BTC-USD/candles"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS


class TestGetProductStats:
    URL = "https://api.exchange.coinbase.com/products"

    def test_get_product_stats_success(self, requests_mock):
        requests_mock.get(
            self.URL + "/BTC/stats",
            json={"open": "84927.78", "high": "85562.07", "low": "83217.26", "last": "83233.97", "volume": "8043.06336134", "volume_30day": "336320.45431582", "rfq_volume_24hour": "40.724795", "rfq_volume_30day": "3146.264482"},
        )
        assert get_product_stats("BTC") == {
            "open": "84927.78",
            "high": "85562.07",
            "low": "83217.26",
            "last": "83233.97",
            "volume": "8043.06336134",
            "volume_30day": "336320.45431582",
            "rfq_volume_24hour": "40.724795",
            "rfq_volume_30day": "3146.264482",
        }
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "/BTC/stats"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    @pytest.mark.parametrize(
        "status_code",
        [400, 403, 500],
        ids=[
            "test_get_product_stats_failure: Bad Request",
            "test_get_product_stats_failure: Forbidden",
            "test_get_product_stats_failure: Internal Server Error",
        ],
    )
    def test_get_product_stats_failure(self, requests_mock, status_code):
        requests_mock.get(self.URL + "/BTC/stats", status_code=status_code)
        with pytest.raises(HTTPError):
            get_product_stats("BTC")
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "/BTC/stats"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS


class TestGetProductTicker:
    URL = "https://api.exchange.coinbase.com/products"

    def test_get_product_ticker_success(self, requests_mock):
        requests_mock.get(
            self.URL + "/BTC-USD/ticker", json={"ask": "83127.85", "bid": "83127.84", "volume": "8059.69043853", "trade_id": 803279920, "price": "83127.85", "size": "0.00040389", "time": "2025-03-29T10:49:07.210762Z", "rfq_volume": "40.699221"}
        )
        assert get_product_ticker("BTC-USD") == {"ask": "83127.85", "bid": "83127.84", "volume": "8059.69043853", "trade_id": 803279920, "price": "83127.85", "size": "0.00040389", "time": "2025-03-29T10:49:07.210762Z", "rfq_volume": "40.699221"}
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "/BTC-USD/ticker"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    @pytest.mark.parametrize(
        "status_code",
        [400, 403, 500],
        ids=[
            "test_get_product_ticker_failure: Bad Request",
            "test_get_product_ticker_failure: Forbidden",
            "test_get_product_ticker_failure: Internal Server Error",
        ],
    )
    def test_get_product_ticker_failure(self, requests_mock, status_code):
        requests_mock.get(self.URL + "/BTC-USD/ticker", status_code=status_code)
        with pytest.raises(HTTPError):
            get_product_ticker("BTC-USD")
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "/BTC-USD/ticker"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS


class TestGetProductTrades:
    URL = "https://api.exchange.coinbase.com/products"

    def test_get_product_trades_success(self, requests_mock):
        requests_mock.get(self.URL + "/BTC-USD/trades", json=[])
        assert get_product_trades("BTC-USD") == []
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "/BTC-USD/trades"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    @pytest.mark.parametrize(
        "status_code",
        [400, 403, 500],
        ids=[
            "test_get_product_trades_failure: Bad Request",
            "test_get_product_trades_failure: Forbidden",
            "test_get_product_trades_failure: Internal Server Error",
        ],
    )
    def test_get_product_trades_failure(self, requests_mock, status_code):
        requests_mock.get(self.URL + "/BTC-USD/trades", status_code=status_code)
        with pytest.raises(HTTPError):
            get_product_trades("BTC-USD")
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "/BTC-USD/trades"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS
