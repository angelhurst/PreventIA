from preventia.channels.main import DEFAULT_PORT, webhook_port


def test_an_empty_port_variable_falls_back_to_the_default(monkeypatch):
    monkeypatch.setenv("PREVENTIA_WEBHOOK_PORT", "")

    assert webhook_port() == DEFAULT_PORT


def test_an_unset_port_variable_falls_back_to_the_default(monkeypatch):
    monkeypatch.delenv("PREVENTIA_WEBHOOK_PORT", raising=False)

    assert webhook_port() == DEFAULT_PORT


def test_a_set_port_variable_is_used(monkeypatch):
    monkeypatch.setenv("PREVENTIA_WEBHOOK_PORT", "9001")

    assert webhook_port() == 9001
