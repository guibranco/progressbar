import json
from unittest.mock import MagicMock, patch
from urllib.error import URLError

import pytest
from app import JSON_FETCH_MAX_BYTES, JSON_URL_MAX_LENGTH, app, fetch_json_document

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_svg_response(client):
    response = client.get("/28/")

    assert response.status_code == 200

    assert response.content_type == "image/svg+xml"
    assert response.headers.get("X-Content-Type-Options") == "nosniff"

    assert b"<svg" in response.data
    assert b"</svg>" in response.data


def test_svg_escapes_title_in_markup(client):
    response = client.get(
        "/28/",
        query_string={"title": "<script>alert(1)</script>"},
    )
    assert response.status_code == 200
    assert b"<script>" not in response.data
    assert b"&lt;script&gt;" in response.data


def test_dynamic_json_missing_params(client):
    response = client.get("/dynamic/json/")
    assert response.status_code == 400
    assert response.content_type == "image/svg+xml"
    assert b"missing" in response.data.lower()


def test_dynamic_json_localhost_blocked(client):
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "http://127.0.0.1:8080/data.json",
            "query": "$.x",
        },
    )
    assert response.status_code == 400


@patch("app.fetch_json_document")
def test_dynamic_json_query_param(mock_fetch, client):
    mock_fetch.return_value = {"v": 9}
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com/x.json",
            "query": "$.v",
        },
    )
    assert response.status_code == 200
    assert b"9" in response.data
    assert response.headers.get("X-Content-Type-Options") == "nosniff"


@patch("app.fetch_json_document")
def test_dynamic_json_dot_path(mock_fetch, client):
    mock_fetch.return_value = {
        "progress": [{"data": {"approvalProgress": 73}}],
    }
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com/stats.json",
            "query": "progress.0.data.approvalProgress",
        },
    )
    assert response.status_code == 200
    assert response.content_type == "image/svg+xml"
    assert b"<svg" in response.data
    assert b"73" in response.data


@patch("app.fetch_json_document")
def test_dynamic_json_jsonpath_dollar(mock_fetch, client):
    mock_fetch.return_value = {"items": [{"n": 42}]}
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com/x.json",
            "query": "$.items[0].n",
        },
    )
    assert response.status_code == 200
    assert b"42" in response.data


@patch("app.fetch_json_document")
def test_dynamic_json_percent_suffix_string(mock_fetch, client):
    mock_fetch.return_value = {"approvalProgress": "73%"}
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com/x.json",
            "query": "$.approvalProgress",
        },
    )
    assert response.status_code == 200
    assert b"73" in response.data


@patch("app.fetch_json_document", side_effect=URLError("connection failed"))
def test_dynamic_json_fetch_failure_returns_502(mock_fetch, client):
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com/x.json",
            "query": "$.x",
        },
    )
    assert response.status_code == 502
    assert response.content_type == "image/svg+xml"


@patch("app.fetch_json_document")
def test_dynamic_json_query_no_match_returns_422(mock_fetch, client):
    mock_fetch.return_value = {"other": 1}
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com/x.json",
            "query": "$.missing",
        },
    )
    assert response.status_code == 422
    assert response.content_type == "image/svg+xml"


@patch("app.fetch_json_document")
def test_dynamic_json_invalid_query_returns_422(mock_fetch, client):
    mock_fetch.return_value = {"x": 1}
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com/x.json",
            "query": "$$not-valid-jsonpath",
        },
    )
    assert response.status_code == 422


@patch("app.fetch_json_document")
def test_dynamic_json_boolean_value_rejected(mock_fetch, client):
    mock_fetch.return_value = {"flag": True}
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com/x.json",
            "query": "$.flag",
        },
    )
    assert response.status_code == 422


@patch("app.fetch_json_document")
def test_dynamic_json_cache_sets_cache_control(mock_fetch, client):
    mock_fetch.return_value = {"n": 5}
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com/x.json",
            "query": "$.n",
            "cache": "120",
        },
    )
    assert response.status_code == 200
    assert response.headers.get("Cache-Control") == "public, max-age=120"


@patch("app.fetch_json_document")
def test_dynamic_json_cache_seconds_alias(mock_fetch, client):
    mock_fetch.return_value = {"n": 5}
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com/x.json",
            "query": "$.n",
            "cacheSeconds": "60",
        },
    )
    assert response.status_code == 200
    assert response.headers.get("Cache-Control") == "public, max-age=60"


def test_dynamic_json_disallowed_scheme(client):
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "ftp://example.com/data.json",
            "query": "$.x",
        },
    )
    assert response.status_code == 400


def test_dynamic_json_url_with_userinfo_blocked(client):
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "http://user@example.com/data.json",
            "query": "$.x",
        },
    )
    assert response.status_code == 400


def test_dynamic_json_nonstandard_port_blocked(client):
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com:8080/data.json",
            "query": "$.x",
        },
    )
    assert response.status_code == 400


def test_dynamic_json_url_too_long_blocked(client):
    pad_len = JSON_URL_MAX_LENGTH - len("https://example.com/") + 10
    long_url = "https://example.com/" + ("x" * max(1, pad_len))
    assert len(long_url) > JSON_URL_MAX_LENGTH
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": long_url,
            "query": "$.x",
        },
    )
    assert response.status_code == 400


@pytest.mark.parametrize(
    "metadata_url",
    [
        "http://169.254.169.254/latest/meta-data",
        "http://metadata.google.internal/computeMetadata/v1",
    ],
)
def test_dynamic_json_cloud_metadata_hosts_blocked(client, metadata_url):
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": metadata_url,
            "query": "$.x",
        },
    )
    assert response.status_code == 400


@patch("app.fetch_json_document")
def test_dynamic_json_matched_string_empty_returns_422(mock_fetch, client):
    mock_fetch.return_value = {"s": "   "}
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com/x.json",
            "query": "$.s",
        },
    )
    assert response.status_code == 422
    assert b"empty" in response.data.lower()


@patch("app.fetch_json_document")
def test_dynamic_json_matched_string_not_numeric_returns_422(mock_fetch, client):
    mock_fetch.return_value = {"s": "foo"}
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com/x.json",
            "query": "$.s",
        },
    )
    assert response.status_code == 422
    assert b"numeric" in response.data.lower()


@patch("app._fetch_json_opener.open", side_effect=URLError("http redirect not allowed"))
def test_dynamic_json_http_redirect_from_server_is_blocked(mock_open, client):
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com/x.json",
            "query": "$.n",
        },
    )
    assert response.status_code == 502


@patch("app._fetch_json_opener.open")
def test_dynamic_json_malformed_json_body_returns_422(mock_open, client):
    mock_resp = MagicMock()
    mock_resp.headers.get.return_value = "application/json"
    mock_resp.read.return_value = b'{"n": }'
    ctx = MagicMock()
    ctx.__enter__.return_value = mock_resp
    ctx.__exit__.return_value = None
    mock_open.return_value = ctx
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com/x.json",
            "query": "$.n",
        },
    )
    assert response.status_code == 422


@patch("app._fetch_json_opener.open")
def test_dynamic_json_invalid_utf8_body_returns_422(mock_open, client):
    mock_resp = MagicMock()
    mock_resp.headers.get.return_value = "application/json; charset=utf-8"
    mock_resp.read.return_value = b"\xff"
    ctx = MagicMock()
    ctx.__enter__.return_value = mock_resp
    ctx.__exit__.return_value = None
    mock_open.return_value = ctx
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com/x.json",
            "query": "$.n",
        },
    )
    assert response.status_code == 422


@patch("app._fetch_json_opener.open")
def test_dynamic_json_response_too_large_returns_422(mock_open, client):
    mock_resp = MagicMock()
    mock_resp.headers.get.return_value = "application/json"
    mock_resp.read.return_value = b"x" * (JSON_FETCH_MAX_BYTES + 1)
    ctx = MagicMock()
    ctx.__enter__.return_value = mock_resp
    ctx.__exit__.return_value = None
    mock_open.return_value = ctx
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com/x.json",
            "query": "$.n",
        },
    )
    assert response.status_code == 422
    assert b"large" in response.data.lower()


@patch("app._fetch_json_opener.open")
def test_fetch_json_rejects_html_content_type(mock_open):
    mock_resp = MagicMock()
    mock_resp.headers.get.return_value = "text/html; charset=utf-8"
    mock_resp.read.return_value = b"{}"
    ctx = MagicMock()
    ctx.__enter__.return_value = mock_resp
    ctx.__exit__.return_value = None
    mock_open.return_value = ctx
    with pytest.raises(ValueError, match="unsupported content type"):
        fetch_json_document("https://example.com/x.json")


@patch("app._fetch_json_opener.open")
def test_fetch_json_allows_application_json(mock_open):
    mock_resp = MagicMock()
    mock_resp.headers.get.return_value = "application/json; charset=utf-8"
    mock_resp.read.return_value = b'{"n": 3}'
    ctx = MagicMock()
    ctx.__enter__.return_value = mock_resp
    ctx.__exit__.return_value = None
    mock_open.return_value = ctx
    assert fetch_json_document("https://example.com/x.json") == {"n": 3}


@patch("app._fetch_json_opener.open")
def test_fetch_json_respects_charset_iso8859_1(mock_open):
    payload = '{"a": "caf\xe9"}'
    mock_resp = MagicMock()
    mock_resp.headers.get.return_value = "application/json; charset=iso-8859-1"
    mock_resp.read.return_value = payload.encode("iso-8859-1")
    ctx = MagicMock()
    ctx.__enter__.return_value = mock_resp
    ctx.__exit__.return_value = None
    mock_open.return_value = ctx
    assert fetch_json_document("https://example.com/x.json") == {"a": "café"}


@patch("app._fetch_json_opener.open")
def test_fetch_json_unsupported_charset_raises(mock_open):
    mock_resp = MagicMock()
    mock_resp.headers.get.return_value = "application/json; charset=x-unknown-xyz"
    mock_resp.read.return_value = b"{}"
    ctx = MagicMock()
    ctx.__enter__.return_value = mock_resp
    ctx.__exit__.return_value = None
    mock_open.return_value = ctx
    with pytest.raises(ValueError, match="unsupported charset"):
        fetch_json_document("https://example.com/x.json")


@patch("app._fetch_json_opener.open")
def test_fetch_json_response_too_large_raises(mock_open):
    mock_resp = MagicMock()
    mock_resp.headers.get.return_value = "application/json"
    mock_resp.read.return_value = b"x" * (JSON_FETCH_MAX_BYTES + 1)
    ctx = MagicMock()
    ctx.__enter__.return_value = mock_resp
    ctx.__exit__.return_value = None
    mock_open.return_value = ctx
    with pytest.raises(ValueError, match="response too large"):
        fetch_json_document("https://example.com/x.json")


@patch("app._fetch_json_opener.open")
def test_fetch_json_invalid_utf8_raises(mock_open):
    mock_resp = MagicMock()
    mock_resp.headers.get.return_value = "application/json; charset=utf-8"
    mock_resp.read.return_value = b"\xff"
    ctx = MagicMock()
    ctx.__enter__.return_value = mock_resp
    ctx.__exit__.return_value = None
    mock_open.return_value = ctx
    with pytest.raises(UnicodeDecodeError):
        fetch_json_document("https://example.com/x.json")


@patch("app._fetch_json_opener.open")
def test_fetch_json_malformed_json_raises(mock_open):
    mock_resp = MagicMock()
    mock_resp.headers.get.return_value = "application/json"
    mock_resp.read.return_value = b'{"n": }'
    ctx = MagicMock()
    ctx.__enter__.return_value = mock_resp
    ctx.__exit__.return_value = None
    mock_open.return_value = ctx
    with pytest.raises(json.JSONDecodeError):
        fetch_json_document("https://example.com/x.json")
