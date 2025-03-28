import pytest
from requests import HTTPError

from coinbase import get_server_time


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
