"""Unit tests for linear_cli.py — no network, no LINEAR_API_KEY required."""

from __future__ import annotations

import io
import json
import sys
import urllib.error
from pathlib import Path
from unittest import mock

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import linear_cli  # noqa: E402


class _FakeResp:
    def __init__(self, payload: dict):
        self._data = json.dumps(payload).encode()

    def read(self) -> bytes:
        return self._data

    def __enter__(self) -> "_FakeResp":
        return self

    def __exit__(self, *_exc) -> None:
        return None


class TestGraphqlTransport:
    def test_returns_data_on_success(self):
        with mock.patch.object(
            linear_cli.urllib.request, "urlopen", return_value=_FakeResp({"data": {"ok": 1}})
        ):
            assert linear_cli.graphql("k", "query {}") == {"ok": 1}

    def test_graphql_errors_raise_without_retry(self):
        payload = {"data": None, "errors": [{"message": "bad"}]}
        with mock.patch.object(
            linear_cli.urllib.request, "urlopen", return_value=_FakeResp(payload)
        ) as m:
            with pytest.raises(linear_cli.LinearCliError):
                linear_cli.graphql("k", "query {}")
        assert m.call_count == 1

    def test_4xx_fails_fast(self):
        err = urllib.error.HTTPError(
            linear_cli.GRAPHQL_URL, 400, "Bad Request", {}, io.BytesIO(b"nope")
        )
        with mock.patch.object(linear_cli.urllib.request, "urlopen", side_effect=err) as m:
            with pytest.raises(linear_cli.LinearCliError):
                linear_cli.graphql("k", "query {}")
        assert m.call_count == 1

    def test_5xx_is_retried_then_fails(self):
        err = urllib.error.HTTPError(linear_cli.GRAPHQL_URL, 503, "Unavailable", {}, None)
        with (
            mock.patch.object(linear_cli, "_sleep"),
            mock.patch.object(linear_cli.urllib.request, "urlopen", side_effect=err) as m,
        ):
            with pytest.raises(linear_cli.LinearCliError):
                linear_cli.graphql("k", "query {}")
        assert m.call_count == linear_cli._MAX_ATTEMPTS

    def test_transient_then_success(self):
        good = _FakeResp({"data": {"ok": 2}})
        err = urllib.error.URLError("temporary")
        with (
            mock.patch.object(linear_cli, "_sleep"),
            mock.patch.object(linear_cli.urllib.request, "urlopen", side_effect=[err, good]),
        ):
            assert linear_cli.graphql("k", "query {}") == {"ok": 2}


class TestVerbShape:
    def test_get_issue_projects_fields(self):
        issue = {
            "data": {
                "issue": {
                    "id": "uuid-1",
                    "identifier": "ABC-12",
                    "title": "T",
                    "description": "D",
                    "url": "https://linear.app/x",
                    "state": {"name": "In Progress", "type": "started"},
                    "labels": {"nodes": [{"name": "Chore"}, {"name": "Code Quality"}]},
                    "parent": {"identifier": "ABC-10", "title": "Epic"},
                    "team": {"id": "team-1"},
                }
            }
        }
        with mock.patch.object(
            linear_cli.urllib.request, "urlopen", return_value=_FakeResp(issue)
        ):
            out = linear_cli.cmd_get_issue("k", "ABC-12")
        assert out["identifier"] == "ABC-12"
        assert out["state"] == "In Progress"
        assert out["labels"] == ["Chore", "Code Quality"]
        assert out["parent"] == "ABC-10"

    def test_list_sub_issues_projects_children(self):
        payload = {
            "data": {
                "issue": {
                    "children": {
                        "nodes": [
                            {
                                "identifier": "ABC-13",
                                "title": "Child",
                                "state": {"name": "Backlog"},
                            }
                        ]
                    }
                }
            }
        }
        with mock.patch.object(
            linear_cli.urllib.request, "urlopen", return_value=_FakeResp(payload)
        ):
            out = linear_cli.cmd_list_sub_issues("k", "ABC-12")
        assert out == [{"identifier": "ABC-13", "title": "Child", "state": "Backlog"}]

    def test_set_state_resolves_state_id_case_insensitively(self):
        responses = [
            _FakeResp(
                {
                    "data": {
                        "issue": {
                            "id": "uuid-1",
                            "identifier": "ABC-12",
                            "title": "T",
                            "description": "",
                            "url": "u",
                            "state": {"name": "Backlog", "type": "backlog"},
                            "labels": {"nodes": []},
                            "parent": None,
                            "team": {"id": "team-1"},
                        }
                    }
                }
            ),
            _FakeResp(
                {
                    "data": {
                        "team": {
                            "states": {
                                "nodes": [
                                    {"id": "s-todo", "name": "Todo"},
                                    {"id": "s-prog", "name": "In Progress"},
                                ]
                            }
                        }
                    }
                }
            ),
            _FakeResp(
                {
                    "data": {
                        "issueUpdate": {
                            "success": True,
                            "issue": {"identifier": "ABC-12", "state": {"name": "In Progress"}},
                        }
                    }
                }
            ),
        ]
        with mock.patch.object(linear_cli.urllib.request, "urlopen", side_effect=responses):
            out = linear_cli.cmd_set_state("k", "ABC-12", "in progress")
        assert out == {"identifier": "ABC-12", "state": "In Progress"}


class TestCliEntrypoint:
    def test_missing_key_returns_exit_2(self):
        with mock.patch.dict(linear_cli.os.environ, {"LINEAR_API_KEY": ""}, clear=False):
            with mock.patch("sys.stderr", new=io.StringIO()):
                assert linear_cli.main(["get-issue", "ABC-12"]) == linear_cli.EXIT_NO_KEY

    def test_hard_failure_returns_exit_1(self):
        with mock.patch.dict(linear_cli.os.environ, {"LINEAR_API_KEY": "k"}, clear=False):
            with mock.patch.object(
                linear_cli, "cmd_get_issue", side_effect=linear_cli.LinearCliError("boom")
            ):
                with mock.patch("sys.stderr", new=io.StringIO()):
                    assert linear_cli.main(["get-issue", "ABC-12"]) == linear_cli.EXIT_HARD_FAILURE

    def test_success_prints_json_and_exit_0(self):
        with mock.patch.dict(linear_cli.os.environ, {"LINEAR_API_KEY": "k"}, clear=False):
            with mock.patch.object(
                linear_cli, "cmd_get_issue", return_value={"identifier": "ABC-12"}
            ):
                buf = io.StringIO()
                with mock.patch("sys.stdout", new=buf):
                    assert linear_cli.main(["get-issue", "ABC-12"]) == linear_cli.EXIT_OK
        assert json.loads(buf.getvalue())["identifier"] == "ABC-12"
