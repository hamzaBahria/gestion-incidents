import pytest
from app import create_app, db


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Base temporaire: chaque test a sa propre base vide
    monkeypatch.setattr(db, "DB_PATH", str(tmp_path / "test.db"))
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()
