def test_home_page_accessible(client):
    response = client.get("/")
    assert response.status_code == 200


def test_home_page_contains_title(client):
    response = client.get("/")
    assert b"Liste des incidents" in response.data
