import httpx

PYPI = "https://pypi.org/pypi/{}/json"
TESTPYPI = "https://test.pypi.org/pypi/{}/json"

def check_name(name: str, registry_url: str) -> str:
    url = registry_url.format(name)
    try:
        response = httpx.get(url, timeout=3)
    except httpx.TimeoutException:
        return "error"  # or "timeout"
    except httpx.RequestError:
        return "error"  # DNS/network etc.

    if response.status_code == 404:
        return "not taken"
    if response.status_code == 200:
        return "taken"
    if 500 <= response.status_code < 600:
        return "error"  # server-side failure

    return "error"
