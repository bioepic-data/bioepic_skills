import io
from urllib import parse
from unittest.mock import patch

import pytest

from bioepic_skills.essdive_api import (
    EssdiveApiError,
    get_essdive_package,
    search_essdive_packages,
)


class DummyResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()


def test_search_essdive_packages_builds_query_and_headers():
    def fake_urlopen(req, timeout=30):
        parsed = parse.urlparse(req.full_url)
        qs = parse.parse_qs(parsed.query)

        assert parsed.path.endswith("/packages")
        assert qs["text"] == ["soil"]
        assert qs["providerName"] == ["Project A"]
        assert qs["page_size"] == ["10"]
        assert qs["row_start"] == ["5"]
        assert qs["isPublic"] == ["true"]

        headers = dict(req.header_items())
        headers_lower = {key.lower(): value for key, value in headers.items()}
        assert headers.get("Authorization") == "Bearer test-token"
        assert headers_lower.get("accept") == "application/json"
        assert headers_lower.get("user-agent") is not None
        assert headers_lower.get("content-type") == "application/json"
        assert headers_lower.get("range") == "bytes=0-1000"

        return DummyResponse(b'{"ok": true}')

    with patch("urllib.request.urlopen", side_effect=fake_urlopen):
        response = search_essdive_packages(
            keyword="soil",
            provider_name="Project A",
            page_size=10,
            row_start=5,
            is_public=True,
            token="test-token",
        )

    assert response == {"ok": True}


def test_get_essdive_package_builds_path():
    def fake_urlopen(req, timeout=30):
        parsed = parse.urlparse(req.full_url)
        qs = parse.parse_qs(parsed.query)

        assert parsed.path.endswith("/packages/abc-123")
        assert qs["isPublic"] == ["false"]

        return DummyResponse(b'{"id": "abc-123"}')

    with patch("urllib.request.urlopen", side_effect=fake_urlopen):
        response = get_essdive_package("abc-123", is_public=False)

    assert response["id"] == "abc-123"


def test_search_essdive_packages_invalid_json_raises():
    def fake_urlopen(req, timeout=30):
        return DummyResponse(b"not-json")

    with patch("urllib.request.urlopen", side_effect=fake_urlopen):
        with pytest.raises(EssdiveApiError):
            search_essdive_packages(keyword="soil")
