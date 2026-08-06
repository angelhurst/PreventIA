import pytest
from fastapi.testclient import TestClient

from preventia.dashboard import auth
from preventia.dashboard.app import app


@pytest.fixture
def client():
    return TestClient(app, follow_redirects=False)


def signed_in(client):
    client.cookies.set(auth.SESSION_COOKIE, auth.session_token())
    return client


def test_the_demo_code_is_four_zeros():
    assert auth.expected_code() == "0000"


def test_the_queue_is_closed_to_anyone_without_a_code(client):
    response = client.get("/cola")
    assert response.status_code == 303
    assert response.headers["location"] == "/entrar"


def test_a_patient_record_is_closed_too(client):
    assert client.get("/cola/PV-001").headers["location"] == "/entrar"


def test_the_check_in_page_is_closed_too(client):
    assert client.get("/consulta").headers["location"] == "/entrar"


def test_the_login_page_itself_is_reachable(client):
    assert client.get("/entrar").status_code == 200


def test_the_login_page_asks_for_four_numbers(client):
    assert "4 números" in client.get("/entrar").text


def test_the_right_code_opens_the_dashboard(client):
    response = client.post("/entrar", data={"code": "0000"})
    assert response.status_code == 303
    assert response.headers["location"] == "/cola"
    assert auth.SESSION_COOKIE in response.cookies


def test_the_wrong_code_does_not(client):
    response = client.post("/entrar", data={"code": "1234"})
    assert response.headers["location"] == "/entrar?error=1"
    assert auth.SESSION_COOKIE not in response.cookies


@pytest.mark.parametrize("code", ["", "12", "12345", "abcd", "00 0"])
def test_a_malformed_code_is_refused(client, code):
    response = client.post("/entrar", data={"code": code})
    assert response.headers["location"] == "/entrar?error=1"


def test_a_signed_in_visitor_reaches_the_queue(client):
    response = signed_in(client).get("/cola")
    assert response.status_code in (200, 503)


def test_leaving_clears_the_session(client):
    response = signed_in(client).get("/salir")
    assert response.headers["location"] == "/entrar"


def test_a_forged_cookie_does_not_work(client):
    client.cookies.set(auth.SESSION_COOKIE, "no-soy-un-token")
    assert client.get("/cola").headers["location"] == "/entrar"


def test_changing_the_code_invalidates_old_sessions(client, monkeypatch):
    stale = auth.session_token()
    monkeypatch.setenv("PREVENTIA_DOCTOR_CODE", "4321")
    client.cookies.set(auth.SESSION_COOKIE, stale)
    assert client.get("/cola").headers["location"] == "/entrar"


def test_the_code_can_be_changed_by_environment(monkeypatch):
    monkeypatch.setenv("PREVENTIA_DOCTOR_CODE", "4321")
    assert auth.verify("4321")
    with pytest.raises(auth.BadCode):
        auth.verify("0000")


def test_static_assets_stay_open(client):
    assert not auth.is_open_path("/cola")
    assert auth.is_open_path("/static/dashboard.css")
    assert auth.is_open_path("/entrar")
