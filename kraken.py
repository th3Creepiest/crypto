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
