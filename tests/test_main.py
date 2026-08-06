from pathlib import Path

import pytest

from preventia.channels.main import DEFAULT_PORT, env_file, load_env_file, webhook_port


def test_an_empty_port_variable_falls_back_to_the_default(monkeypatch):
    monkeypatch.setenv("PREVENTIA_WEBHOOK_PORT", "")

    assert webhook_port() == DEFAULT_PORT


def test_an_unset_port_variable_falls_back_to_the_default(monkeypatch):
    monkeypatch.delenv("PREVENTIA_WEBHOOK_PORT", raising=False)

    assert webhook_port() == DEFAULT_PORT


def test_a_set_port_variable_is_used(monkeypatch):
    monkeypatch.setenv("PREVENTIA_WEBHOOK_PORT", "9001")

    assert webhook_port() == 9001


def test_an_empty_env_file_override_falls_back_to_the_repository_root(monkeypatch):
    monkeypatch.setenv("PREVENTIA_ENV_FILE", "")

    assert env_file().name == ".env"


def test_an_env_file_override_is_used(monkeypatch, tmp_path):
    target = tmp_path / "elsewhere.env"
    monkeypatch.setenv("PREVENTIA_ENV_FILE", str(target))

    assert env_file() == target


def test_values_already_in_the_environment_win_over_the_file(monkeypatch, tmp_path):
    target = tmp_path / ".env"
    target.write_text("WHATSAPP_PHONE_NUMBER_ID=from-file\n", encoding="utf-8")
    monkeypatch.setenv("WHATSAPP_PHONE_NUMBER_ID", "from-environment")

    load_env_file(target)

    import os

    assert os.environ["WHATSAPP_PHONE_NUMBER_ID"] == "from-environment"


def test_a_missing_env_file_is_not_an_error(tmp_path):
    load_env_file(tmp_path / "does-not-exist.env")
