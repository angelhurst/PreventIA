import os
import subprocess
import sys
from pathlib import Path

from preventia.environment import env_file, load_env_file

ROOT = Path(__file__).resolve().parents[1]


def test_an_empty_env_file_override_falls_back_to_the_repository_root(monkeypatch):
    monkeypatch.setenv("PREVENTIA_ENV_FILE", "")

    assert env_file() == ROOT / ".env"


def test_an_env_file_override_is_used(monkeypatch, tmp_path):
    target = tmp_path / "elsewhere.env"
    monkeypatch.setenv("PREVENTIA_ENV_FILE", str(target))

    assert env_file() == target


def test_values_already_in_the_environment_win_over_the_file(monkeypatch, tmp_path):
    target = tmp_path / ".env"
    target.write_text("WHATSAPP_PHONE_NUMBER_ID=from-file\n", encoding="utf-8")
    monkeypatch.setenv("WHATSAPP_PHONE_NUMBER_ID", "from-environment")

    load_env_file(target)

    assert os.environ["WHATSAPP_PHONE_NUMBER_ID"] == "from-environment"


def test_a_missing_env_file_is_not_an_error(tmp_path):
    load_env_file(tmp_path / "does-not-exist.env")


def test_the_webhook_and_the_dashboard_share_one_loader():
    from preventia.channels import main
    from preventia.dashboard import app

    assert main.load_env_file is load_env_file
    assert app.load_env_file is load_env_file


def run_dashboard_import(env_path, extra=None):
    environment = dict(os.environ)
    environment.pop("PREVENTIA_CHANNEL", None)
    environment.pop("PREVENTIA_DB", None)
    environment["PREVENTIA_ENV_FILE"] = str(env_path)
    environment.update(extra or {})
    script = (
        "import os\n"
        "import preventia.dashboard.app\n"
        "print(os.environ.get('PREVENTIA_CHANNEL', ''))\n"
        "print(os.environ.get('PREVENTIA_DB', ''))\n"
    )
    finished = subprocess.run(
        [sys.executable, "-c", script],
        cwd=str(ROOT),
        env=environment,
        capture_output=True,
        text=True,
    )
    assert finished.returncode == 0, finished.stderr
    channel, database = finished.stdout.splitlines()[:2]
    return channel, database


def test_importing_the_dashboard_loads_the_env_file(tmp_path):
    target = tmp_path / ".env"
    target.write_text(
        "PREVENTIA_CHANNEL=whatsapp\nPREVENTIA_DB=C:/desde/el/archivo.db\n", encoding="utf-8"
    )

    channel, database = run_dashboard_import(target)

    assert channel == "whatsapp"
    assert database == "C:/desde/el/archivo.db"


def test_the_service_environment_still_beats_the_env_file(tmp_path):
    target = tmp_path / ".env"
    target.write_text(
        "PREVENTIA_CHANNEL=whatsapp\nPREVENTIA_DB=C:/desde/el/archivo.db\n", encoding="utf-8"
    )

    channel, database = run_dashboard_import(
        target, extra={"PREVENTIA_DB": "/opt/preventia/preventia/data/preventia.db"}
    )

    assert channel == "whatsapp"
    assert database == "/opt/preventia/preventia/data/preventia.db"
