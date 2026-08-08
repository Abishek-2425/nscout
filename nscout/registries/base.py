import httpx
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import Optional, Any, Tuple, List, Dict
from nscout.cache import get as cache_get, set as cache_set, make_key


def safe_get(url: str) -> Tuple[Optional[httpx.Response], Optional[Dict[str, Any]]]:
    """
    Shared cache-backed HTTP GET helper.
    Returns a tuple of (response, error_dict).
    """
    key = make_key("GET", url)
    cached = cache_get(key)
    if cached is not None:
        return cached

    try:
        response = httpx.get(url, timeout=3)
        result = (response, None)
    except httpx.TimeoutException:
        result = (None, {"type": "timeout", "detail": "Request timed out"})
    except httpx.RequestError as e:
        result = (None, {"type": "network", "detail": str(e)})

    cache_set(key, result)
    return result


@dataclass
class PackageMetadata:
    name: str
    registry: str
    version: str
    description: Optional[str]
    homepage: Optional[str]
    repository: Optional[str]
    author: Optional[str]
    license: Optional[str]
    keywords: Optional[List[str]]
    latest_publish: Optional[str]
    extra: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PackageResult:
    name: str
    registry: str
    taken: Optional[bool]
    metadata: Optional[PackageMetadata]
    error: Optional[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "name": self.name,
            "registry": self.registry,
            "taken": self.taken,
            "metadata": self.metadata.to_dict() if self.metadata else None,
            "error": self.error,
        }
        return d


class Registry(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the registry."""
        pass

    @abstractmethod
    def check(self, package_name: str) -> PackageResult:
        """Check package availability on the registry."""
        pass
