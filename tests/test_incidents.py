def ajouter_incident(client, titre="Projecteur en panne"):
    return client.post(
        "/incidents/ajouter",
        data={
            "titre": titre,
            "description": "Le projecteur ne s'allume pas",
            "lieu": "Salle B12",
            "priorite": "élevée",
        },
        follow_redirects=True,
    )


def test_ajouter_incident(client):
    response = ajouter_incident(client)
    assert response.status_code == 200
    assert b"Projecteur en panne" in response.data


def test_liste_des_incidents(client):
    ajouter_incident(client, "Incident A")
    ajouter_incident(client, "Incident B")
    response = client.get("/")
    assert b"Incident A" in response.data
    assert b"Incident B" in response.data


def test_detail_incident(client):
    ajouter_incident(client)
    response = client.get("/incidents/1")
    assert response.status_code == 200
    assert b"Salle B12" in response.data


def test_modifier_statut(client):
    ajouter_incident(client)
    client.post("/incidents/1/statut", data={"statut": "résolu"})
    response = client.get("/incidents/1")
    assert "résolu".encode() in response.data


def test_supprimer_incident(client):
    ajouter_incident(client)
    client.post("/incidents/1/supprimer")
    response = client.get("/incidents/1")
    assert response.status_code == 404


def test_ajout_invalide_refuse(client):
    response = client.post(
        "/incidents/ajouter",
        data={"titre": "", "description": "x", "lieu": "y", "priorite": "faible"},
    )
    assert response.status_code == 400
