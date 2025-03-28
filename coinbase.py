import requests


BASE_URL = "https://api.coinbase.com/v2/"
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36", "Accept": "application/json"}


def get_server_time() -> dict:
    """Test connectivity to the Rest API and get the current server time."""
    response = requests.get(url=BASE_URL + "time", headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.json()
