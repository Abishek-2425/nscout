import httpx
from datetime import datetime
from .cache import get as cache_get, set as cache_set, make_key


PYPI = "https://pypi.org/pypi/{}/json"
TESTPYPI = "https://test.pypi.org/pypi/{}/json"


# ---------------------------------------------------------------------------
# Internal helper: safe HTTP GET
# ---------------------------------------------------------------------------
def _safe_get(url: str):
    # ---- CACHE CHECK ----
    key = make_key("GET", url)
    cached = cache_get(key)
    if cached is not None:
        return cached  # (response, error)

    # ---- NETWORK CALL ----
    try:
        response = httpx.get(url, timeout=3)
        result = (response, None)
    except httpx.TimeoutException:
        result = (None, {"type": "timeout", "detail": "Request timed out"})
    except httpx.RequestError as e:
        result = (None, {"type": "network", "detail": str(e)})

    # ---- STORE IN CACHE ----
    cache_set(key, result)
    return result


# ---------------------------------------------------------------------------
# Internal helper: extract metadata from PyPI JSON
# ---------------------------------------------------------------------------
def _parse_metadata(data: dict) -> dict:
    """Extract structured metadata from PyPI JSON."""

    info = data.get("info", {}) or {}
    releases = data.get("releases", {}) or {}

    # ---- basic fields ----
    version = info.get("version")
    summary = info.get("summary")
    author = info.get("author")
    author_email = info.get("author_email")
    license_ = info.get("license") or info.get("license_expression")
    homepage = info.get("home_page")
    project_url = info.get("project_url")
    project_urls = info.get("project_urls")
    requires_python = info.get("requires_python")
    requires_dist = info.get("requires_dist") or []

    # ---- release processing ----
    all_versions = sorted(releases.keys(), key=lambda v: v)
    release_count = len(all_versions)

    # Find latest release timestamp (if available)
    latest_release = None
    if version in releases and releases[version]:
        # Pick first file entry (wheel/tar.gz) and take its timestamp
        latest_file = releases[version][0]
        ts = latest_file.get("upload_time_iso_8601")
        latest_release = {
            "version": version,
            "timestamp": ts
        }

    return {
        "version": version,
        "summary": summary,
        "author": author,
        "author_email": author_email,
        "license": license_,
        "homepage": homepage,
        "project_url": project_url,
        "project_urls": project_urls,
        "requires_python": requires_python,
        "requires_dist": requires_dist,
        "release_count": release_count,
        "latest_release": latest_release,
        "all_versions": all_versions,
    }


# ---------------------------------------------------------------------------
# Internal: check on a given registry (PyPI/TestPyPI)
# ---------------------------------------------------------------------------
def _check_single_registry(name: str, registry_url: str):
    url = registry_url.format(name)

    response, error = _safe_get(url)
    if error:
        return {"taken": None, "error": error, "metadata": None}

    if response.status_code == 404:
        return {"taken": False, "error": None, "metadata": None}

    if response.status_code == 200:
        # Only PyPI should return metadata
        if "pypi.org" in registry_url:
            data = response.json()
            metadata = _parse_metadata(data)
        else:
            metadata = None

        return {"taken": True, "error": None, "metadata": metadata}

    if 500 <= response.status_code < 600:
        return {
            "taken": None,
            "error": {"type": "server", "detail": f"{response.status_code}"},
            "metadata": None
        }

    return {
        "taken": None,
        "error": {"type": "unknown", "detail": f"{response.status_code}"},
        "metadata": None
    }


# ---------------------------------------------------------------------------
# Public API: check_name(name)
# ---------------------------------------------------------------------------
def check_name(name: str) -> dict:
    """
    Return unified structured info for a package name across PyPI + TestPyPI.
    """

    pypi_result = _check_single_registry(name, PYPI)
    testpypi_result = _check_single_registry(name, TESTPYPI)

    # Determine top-level status
    if pypi_result["taken"] is True:
        status = "taken"
    elif pypi_result["taken"] is False:
        status = "not_taken"
    else:
        status = "error"

    # Global error (if PyPI check exploded)
    top_error = pypi_result["error"] if status == "error" else None

    # Metadata: Only from PyPI, only when taken
    metadata = pypi_result["metadata"] if status == "taken" else None

    return {
        "name": name,
        "status": status,
        "source": {
            "pypi": {"taken": pypi_result["taken"]},
            "testpypi": {"taken": testpypi_result["taken"]},
        },
        "metadata": metadata,
        "error": top_error,
    }
