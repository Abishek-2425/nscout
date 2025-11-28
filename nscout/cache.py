# nscout/cache.py

import time
from typing import Any, Tuple, Optional

# -------------------------------------------------------------------
# Simple in-memory cache for HTTP responses and parsed data
# -------------------------------------------------------------------

# Internal structure:
# {
#     key: (timestamp, value)
# }
#
# Timestamp allows TTL logic if enabled.
#

_CACHE: dict[str, Tuple[float, Any]] = {}

# Default TTL:
#   None   → never expires
#   number → seconds to keep items alive
DEFAULT_TTL: Optional[float] = None


def make_key(*parts) -> str:
    """
    Build a cache key from arbitrary components (URL, name, registry).
    Everything is converted to string and joined safely.
    """
    return "||".join(str(p) for p in parts)


def get(key: str, ttl: Optional[float] = DEFAULT_TTL) -> Optional[Any]:
    """
    Retrieve from cache.

    Returns:
        value | None (if not found or expired)
    """
    if key not in _CACHE:
        return None

    ts, value = _CACHE[key]

    # TTL check (if enabled)
    if ttl is not None:
        if (time.time() - ts) > ttl:
            # expired → remove entry
            _CACHE.pop(key, None)
            return None

    return value


def set(key: str, value: Any):
    """
    Store a value in the cache with current timestamp.
    """
    _CACHE[key] = (time.time(), value)


def clear():
    """Clear entire cache."""
    _CACHE.clear()


def size() -> int:
    """Return number of entries in cache."""
    return len(_CACHE)
