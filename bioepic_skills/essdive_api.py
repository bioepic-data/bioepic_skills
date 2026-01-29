"""
Helpers for ESS-DIVE Dataset API access.

These functions are thin wrappers over the ESS-DIVE REST API and are designed
for use by agent tools and CLI commands in this package.
"""
from __future__ import annotations

import json
import os
from typing import Any, Mapping, Optional
from urllib import error, parse, request

DEFAULT_ESSDIVE_BASE_URL = "https://api.ess-dive.lbl.gov/"
DEFAULT_TIMEOUT_SECONDS = 30


class EssdiveApiError(RuntimeError):
    """Raised when the ESS-DIVE API request fails."""


def _normalize_base_url(base_url: str) -> str:
    if not base_url:
        raise ValueError("base_url must be a non-empty string")
    return base_url if base_url.endswith("/") else f"{base_url}/"


def _build_url(base_url: str, path: str, params: Optional[Mapping[str, Any]] = None) -> str:
    base = _normalize_base_url(base_url)
    url = parse.urljoin(base, path.lstrip("/"))
    if params:
        url = f"{url}?{parse.urlencode(params, doseq=True)}"
    return url


def _resolve_token(token: Optional[str]) -> Optional[str]:
    return token or os.getenv("ESSDIVE_TOKEN")


def essdive_api_get(
    path: str,
    params: Optional[Mapping[str, Any]] = None,
    token: Optional[str] = None,
    base_url: str = DEFAULT_ESSDIVE_BASE_URL,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    """
    Perform a GET request to the ESS-DIVE API and return parsed JSON.
    """
    url = _build_url(base_url, path, params)
    headers = {"Accept": "application/json"}

    resolved_token = _resolve_token(token)
    if resolved_token:
        headers["Authorization"] = f"Bearer {resolved_token}"

    req = request.Request(url, headers=headers, method="GET")

    try:
        with request.urlopen(req, timeout=timeout) as response:
            payload = response.read().decode("utf-8")
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore") if exc.fp else ""
        raise EssdiveApiError(f"ESS-DIVE API error {exc.code}: {detail}") from exc
    except error.URLError as exc:
        raise EssdiveApiError(f"ESS-DIVE API request failed: {exc.reason}") from exc

    try:
        return json.loads(payload)
    except json.JSONDecodeError as exc:
        raise EssdiveApiError("ESS-DIVE API returned non-JSON response") from exc


def search_essdive_packages(
    keyword: Optional[str] = None,
    provider_name: Optional[str] = None,
    page_size: Optional[int] = 25,
    row_start: Optional[int] = 0,
    is_public: bool = True,
    extra_params: Optional[Mapping[str, Any]] = None,
    token: Optional[str] = None,
    base_url: str = DEFAULT_ESSDIVE_BASE_URL,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    """
    Search ESS-DIVE packages (datasets) using the API.

    Args:
        keyword: Search keyword (maps to the API's keyword parameter).
        provider_name: Provider/project name (maps to providerName).
        page_size: Number of records to request per page (page_size).
        row_start: Row offset for pagination (row_start).
        is_public: Whether to search only public packages (isPublic).
        extra_params: Additional query parameters to pass through as-is.
        token: Optional API token; defaults to ESSDIVE_TOKEN env var if set.
        base_url: ESS-DIVE API base URL.
        timeout: Request timeout in seconds.
    """
    params: dict[str, Any] = {}

    if keyword:
        params["keyword"] = keyword
    if provider_name:
        params["providerName"] = provider_name
    if page_size is not None:
        params["page_size"] = page_size
    if row_start is not None:
        params["row_start"] = row_start
    params["isPublic"] = str(is_public).lower()

    if extra_params:
        params.update(extra_params)

    return essdive_api_get(
        "packages",
        params=params,
        token=token,
        base_url=base_url,
        timeout=timeout,
    )


def get_essdive_package(
    package_id: str,
    is_public: bool = True,
    token: Optional[str] = None,
    base_url: str = DEFAULT_ESSDIVE_BASE_URL,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    """
    Retrieve a single ESS-DIVE package (dataset) by package ID.
    """
    if not package_id:
        raise ValueError("package_id must be provided")

    params = {"isPublic": str(is_public).lower()}

    return essdive_api_get(
        f"packages/{package_id}",
        params=params,
        token=token,
        base_url=base_url,
        timeout=timeout,
    )
