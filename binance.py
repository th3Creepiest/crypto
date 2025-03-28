import requests


BASE_URL = "https://api.binance.com/api/v3/"
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36", "Accept": "application/json"}


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
