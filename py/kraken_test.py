import pytest
from requests import HTTPError

from kraken import (
    get_system_status,
    get_server_time,
    get_asset_info,
    get_tradable_asset_pairs,
    get_ticker_information,
    get_ohlc_data,
    get_order_book,
    get_recent_trades,
    get_recent_spreads,
)


HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36", "Accept-Encoding": "gzip, deflate", "Accept": "application/json", "Connection": "keep-alive"}


class TestGetSystemStatus:
    URL = "https://api.kraken.com/0/public/SystemStatus"

    def test_get_system_status_success(self, requests_mock):
        requests_mock.get(self.URL, json={"error": [], "result": {"status": "online", "timestamp": "2025-03-28T18:30:07Z"}})
        assert get_system_status() == {"error": [], "result": {"status": "online", "timestamp": "2025-03-28T18:30:07Z"}}
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    @pytest.mark.parametrize(
        "status_code",
        [400, 403, 500],
        ids=[
            "test_get_system_status_failure: Bad Request",
            "test_get_system_status_failure: Forbidden",
            "test_get_system_status_failure: Internal Server Error",
        ],
    )
    def test_get_system_status_failure(self, requests_mock, status_code):
        requests_mock.get(self.URL, status_code=status_code)
        with pytest.raises(HTTPError):
            get_system_status()
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS


class TestGetServerTime:
    URL = "https://api.kraken.com/0/public/Time"

    def test_get_server_time_success(self, requests_mock):
        requests_mock.get(self.URL, json={"error": [], "result": {"unixtime": 1743186641, "rfc1123": "Fri, 28 Mar 25 18:30:41 +0000"}})
        assert get_server_time() == {"error": [], "result": {"unixtime": 1743186641, "rfc1123": "Fri, 28 Mar 25 18:30:41 +0000"}}
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


class TestGetAssetInfo:
    URL = "https://api.kraken.com/0/public/Assets"

    def test_get_asset_info_success(self, requests_mock):
        requests_mock.get(self.URL, json={})
        assert get_asset_info() == {}
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "?aclass=currency"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    def test_get_asset_info_with_asset_success(self, requests_mock):
        requests_mock.get(self.URL, json={})
        assert get_asset_info(asset="XBT") == {}
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "?aclass=currency&asset=XBT"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    @pytest.mark.parametrize(
        "status_code",
        [400, 403, 500],
        ids=[
            "test_get_asset_info_failure: Bad Request",
            "test_get_asset_info_failure: Forbidden",
            "test_get_asset_info_failure: Internal Server Error",
        ],
    )
    def test_get_asset_info_failure(self, requests_mock, status_code):
        requests_mock.get(self.URL, status_code=status_code)
        with pytest.raises(HTTPError):
            get_asset_info()
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "?aclass=currency"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS


class TestGetTradableAssetPairs:
    URL = "https://api.kraken.com/0/public/AssetPairs"

    def test_get_tradable_asset_pairs_success(self, requests_mock):
        requests_mock.get(self.URL, json={})
        assert get_tradable_asset_pairs() == {}
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "?info=info"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    def test_get_tradable_asset_pairs_with_pair_success(self, requests_mock):
        requests_mock.get(self.URL, json={})
        assert get_tradable_asset_pairs(pair="BTC/USD") == {}
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "?info=info&pair=BTC%2FUSD"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    def test_get_tradable_asset_pairs_with_country_code_success(self, requests_mock):
        requests_mock.get(self.URL, json={})
        assert get_tradable_asset_pairs(country_code="US") == {}
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "?info=info&country_code=US"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    @pytest.mark.parametrize(
        "status_code",
        [400, 403, 500],
        ids=[
            "test_get_tradable_asset_pairs_failure: Bad Request",
            "test_get_tradable_asset_pairs_failure: Forbidden",
            "test_get_tradable_asset_pairs_failure: Internal Server Error",
        ],
    )
    def test_get_tradable_asset_pairs_failure(self, requests_mock, status_code):
        requests_mock.get(self.URL, status_code=status_code)
        with pytest.raises(HTTPError):
            get_tradable_asset_pairs()
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "?info=info"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS


class TestGetTickerInformation:
    URL = "https://api.kraken.com/0/public/Ticker"

    def test_get_ticker_information_success(self, requests_mock):
        requests_mock.get(self.URL, json={})
        assert get_ticker_information() == {}
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    def test_get_ticker_information_with_pair_success(self, requests_mock):
        requests_mock.get(self.URL, json={})
        assert get_ticker_information(pair="BTC/USD") == {}
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "?pair=BTC%2FUSD"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    @pytest.mark.parametrize(
        "status_code",
        [400, 403, 500],
        ids=[
            "test_get_ticker_information_failure: Bad Request",
            "test_get_ticker_information_failure: Forbidden",
            "test_get_ticker_information_failure: Internal Server Error",
        ],
    )
    def test_get_ticker_information_failure(self, requests_mock, status_code):
        requests_mock.get(self.URL, status_code=status_code)
        with pytest.raises(HTTPError):
            get_ticker_information()
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS


class TestGetOhlcData:
    URL = "https://api.kraken.com/0/public/OHLC"

    def test_get_ohlc_data_success(self, requests_mock):
        requests_mock.get(self.URL, json={})
        assert get_ohlc_data() == {}
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "?interval=60"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    def test_get_ohlc_data_with_pair_success(self, requests_mock):
        requests_mock.get(self.URL, json={})
        assert get_ohlc_data(pair="BTC/USD") == {}
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "?pair=BTC%2FUSD&interval=60"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    @pytest.mark.parametrize(
        "status_code",
        [400, 403, 500],
        ids=[
            "test_get_ohlc_data_failure: Bad Request",
            "test_get_ohlc_data_failure: Forbidden",
            "test_get_ohlc_data_failure: Internal Server Error",
        ],
    )
    def test_get_ohlc_data_failure(self, requests_mock, status_code):
        requests_mock.get(self.URL, status_code=status_code)
        with pytest.raises(HTTPError):
            get_ohlc_data()
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "?interval=60"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS


class TestGetOrderBook:
    URL = "https://api.kraken.com/0/public/Depth"

    def test_get_order_book_success(self, requests_mock):
        requests_mock.get(self.URL, json={})
        assert get_order_book(pair="BTC/USD") == {}
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "?pair=BTC%2FUSD&count=100"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    @pytest.mark.parametrize(
        "status_code",
        [400, 403, 500],
        ids=[
            "test_get_order_book_failure: Bad Request",
            "test_get_order_book_failure: Forbidden",
            "test_get_order_book_failure: Internal Server Error",
        ],
    )
    def test_get_order_book_failure(self, requests_mock, status_code):
        requests_mock.get(self.URL, status_code=status_code)
        with pytest.raises(HTTPError):
            get_order_book(pair="BTC/USD")
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "?pair=BTC%2FUSD&count=100"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS


class TestGetRecentTrades:
    URL = "https://api.kraken.com/0/public/Trades"

    def test_get_recent_trades_success(self, requests_mock):
        requests_mock.get(self.URL, json={})
        assert get_recent_trades(pair="BTC/USD") == {}
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "?pair=BTC%2FUSD&count=1000"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    def test_get_recent_trades_since(self, requests_mock):
        requests_mock.get(self.URL, json={})
        assert get_recent_trades(pair="BTC/USD", since=1616663618) == {}
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "?pair=BTC%2FUSD&count=1000&since=1616663618"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    @pytest.mark.parametrize(
        "status_code",
        [400, 403, 500],
        ids=[
            "test_get_recent_trades_failure: Bad Request",
            "test_get_recent_trades_failure: Forbidden",
            "test_get_recent_trades_failure: Internal Server Error",
        ],
    )
    def test_get_recent_trades_failure(self, requests_mock, status_code):
        requests_mock.get(self.URL, status_code=status_code)
        with pytest.raises(HTTPError):
            get_recent_trades(pair="BTC/USD")
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "?pair=BTC%2FUSD&count=1000"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS


class TestGetRecentSpreads:
    URL = "https://api.kraken.com/0/public/Spread"

    def test_get_recent_spreads_success(self, requests_mock):
        requests_mock.get(self.URL, json={})
        assert get_recent_spreads(pair="BTC/USD") == {}
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "?pair=BTC%2FUSD"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    def test_get_recent_spreads_since(self, requests_mock):
        requests_mock.get(self.URL, json={})
        assert get_recent_spreads(pair="BTC/USD", since=1616663618) == {}
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "?pair=BTC%2FUSD&since=1616663618"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS

    @pytest.mark.parametrize(
        "status_code",
        [400, 403, 500],
        ids=[
            "test_get_recent_spreads_failure: Bad Request",
            "test_get_recent_spreads_failure: Forbidden",
            "test_get_recent_spreads_failure: Internal Server Error",
        ],
    )
    def test_get_recent_spreads_failure(self, requests_mock, status_code):
        requests_mock.get(self.URL, status_code=status_code)
        with pytest.raises(HTTPError):
            get_recent_spreads(pair="BTC/USD")
        assert requests_mock.called_once
        assert requests_mock.last_request.url == self.URL + "?pair=BTC%2FUSD"
        assert requests_mock.last_request.method == "GET"
        assert requests_mock.last_request.headers == HEADERS
