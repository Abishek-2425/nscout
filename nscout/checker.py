import httpx

PYPI = "https://pypi.org/pypi/{}/json"
TESTPYPI = "https://test.pypi.org/pypi/{}/json"

def check_name(name: str, registry_url: str) -> str:
    """
    Check package availability on PyPI or TestPyPI.

    Returns:
        "taken"      – if the endpoint returns 200
        "not taken"  – if the endpoint returns 404
        "error"      – for timeouts, DNS issues, 5xx responses, or anything else
    """
    url = registry_url.format(name)

    try:
        response = httpx.get(url, timeout=3)
    except httpx.RequestError:
        return "error"

    if response.status_code == 404:
        return "not taken"

    if response.status_code == 200:
        return "taken"

    return "error"
