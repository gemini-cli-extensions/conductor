"""Unit tests for linear_create_issue.py — no network, no LINEAR_API_KEY required."""

from __future__ import annotations

import io
import json
import sys
from pathlib import Path
from unittest import mock

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import linear_create_issue as create  # noqa: E402


class _FakeResp:
    def __init__(self, payload: dict):
        self._data = json.dumps(payload).encode()

    def read(self) -> bytes:
        return self._data

    def __enter__(self) -> "_FakeResp":
        return self

    def __exit__(self, *_exc) -> None:
        return None


class TestTeamResolution:
    def test_team_from_flag(self):
        assert create.resolve_team_name("Widgets", {}) == "Widgets"

    def test_team_from_env(self):
        assert create.resolve_team_name("", {"LINEAR_TEAM_NAME": "Widgets"}) == "Widgets"

    def test_flag_overrides_env(self):
        assert create.resolve_team_name("Flag", {"LINEAR_TEAM_NAME": "Env"}) == "Flag"

    def test_missing_team_raises(self):
        with pytest.raises(create.LinearCreateError):
            create.resolve_team_name("", {})

    def test_no_hardcoded_product_team(self):
        assert not hasattr(create, "DEFAULT_TEAM_NAME") or create.DEFAULT_TEAM_NAME in (
            None,
            "",
        )


class TestFetchHelpers:
    def test_fetch_team_returns_first_match(self):
        payload = {"data": {"teams": {"nodes": [{"id": "t1", "name": "Widgets"}]}}}
        with mock.patch.object(
            create.urllib.request, "urlopen", return_value=_FakeResp(payload)
        ):
            assert create.fetch_team("k", "Widgets") == {"id": "t1", "name": "Widgets"}

    def test_fetch_team_missing_raises(self):
        payload = {"data": {"teams": {"nodes": []}}}
        with mock.patch.object(
            create.urllib.request, "urlopen", return_value=_FakeResp(payload)
        ):
            with pytest.raises(create.LinearCreateError):
                create.fetch_team("k", "Missing")

    def test_fetch_label_ids_maps_names(self):
        payload = {
            "data": {
                "team": {
                    "labels": {
                        "nodes": [
                            {"id": "l1", "name": "Bug"},
                            {"id": "l2", "name": "API"},
                        ]
                    }
                }
            }
        }
        with mock.patch.object(
            create.urllib.request, "urlopen", return_value=_FakeResp(payload)
        ):
            assert create.fetch_label_ids("k", "t1", ["Bug", "API"]) == ["l1", "l2"]

    def test_fetch_label_ids_missing_raises(self):
        payload = {"data": {"team": {"labels": {"nodes": [{"id": "l1", "name": "Bug"}]}}}}
        with mock.patch.object(
            create.urllib.request, "urlopen", return_value=_FakeResp(payload)
        ):
            with pytest.raises(create.LinearCreateError):
                create.fetch_label_ids("k", "t1", ["Bug", "Missing"])


class TestCreateIssue:
    def test_create_issue_passes_parent_id(self):
        captured = {}

        def fake_graphql(_key, _query, variables=None):
            captured["variables"] = variables
            return {
                "issueCreate": {
                    "success": True,
                    "issue": {
                        "id": "uuid",
                        "identifier": "ABC-1",
                        "title": "T",
                        "url": "u",
                    },
                }
            }

        with mock.patch.object(create, "graphql", side_effect=fake_graphql):
            out = create.create_issue(
                "k",
                team_id="t1",
                title="T",
                description="D",
                label_ids=["l1"],
                parent_id="parent-uuid",
            )
        assert out["identifier"] == "ABC-1"
        assert captured["variables"]["input"]["parentId"] == "parent-uuid"
        assert captured["variables"]["input"]["labelIds"] == ["l1"]

    def test_create_issue_omits_parent_when_absent(self):
        captured = {}

        def fake_graphql(_key, _query, variables=None):
            captured["variables"] = variables
            return {
                "issueCreate": {
                    "success": True,
                    "issue": {
                        "id": "uuid",
                        "identifier": "ABC-1",
                        "title": "T",
                        "url": "u",
                    },
                }
            }

        with mock.patch.object(create, "graphql", side_effect=fake_graphql):
            create.create_issue(
                "k",
                team_id="t1",
                title="T",
                description="",
                label_ids=[],
            )
        assert "parentId" not in captured["variables"]["input"]


class TestEntrypoint:
    def test_missing_key_returns_exit_2(self):
        with mock.patch.dict(create.os.environ, {"LINEAR_API_KEY": ""}, clear=False):
            with mock.patch("sys.stderr", new=io.StringIO()):
                assert create.main(["--title", "T", "--team", "Widgets"]) == create.EXIT_NO_KEY

    def test_missing_team_returns_exit_1(self):
        env = {"LINEAR_API_KEY": "k"}
        env.pop("LINEAR_TEAM_NAME", None)
        with mock.patch.dict(create.os.environ, env, clear=True):
            with mock.patch("sys.stderr", new=io.StringIO()):
                assert create.main(["--title", "T"]) == create.EXIT_HARD_FAILURE
