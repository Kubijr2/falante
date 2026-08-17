def test_list_verbs_includes_both_regular_and_irregular(client):
    response = client.get("/api/v1/verbs")
    assert response.status_code == 200
    infinitives = {v["infinitive"] for v in response.json()}
    assert "falar" in infinitives  # regular
    assert "ser" in infinitives  # irregular
    assert len(response.json()) == 85


def test_search_by_infinitive(client):
    response = client.get("/api/v1/verbs", params={"search": "fal"})
    infinitives = {v["infinitive"] for v in response.json()}
    assert infinitives == {"falar"}


def test_search_by_translation(client):
    response = client.get("/api/v1/verbs", params={"search": "to speak"})
    infinitives = {v["infinitive"] for v in response.json()}
    assert "falar" in infinitives


def test_get_regular_verb_conjugations_computed_correctly(client):
    response = client.get("/api/v1/verbs/falar")
    assert response.status_code == 200
    body = response.json()
    assert body["is_irregular"] is False
    assert body["conjugations"]["present"] == ["falo", "fala", "falamos", "falam"]
    assert body["conjugations"]["future"] == ["falarei", "falará", "falaremos", "falarão"]


def test_get_regular_verb_with_orthographic_change(client):
    response = client.get("/api/v1/verbs/ficar")
    body = response.json()
    assert body["conjugations"]["preterito_perfeito"][0] == "fiquei"


def test_get_irregular_verb_conjugations_from_stored_data(client):
    response = client.get("/api/v1/verbs/ser")
    assert response.status_code == 200
    body = response.json()
    assert body["is_irregular"] is True
    assert body["conjugations"]["present"] == ["sou", "é", "somos", "são"]
    assert body["conjugations"]["preterito_perfeito"] == ["fui", "foi", "fomos", "foram"]


def test_get_missing_verb_returns_404(client):
    response = client.get("/api/v1/verbs/naoexiste")
    assert response.status_code == 404


def test_verb_conjugations_include_all_six_tenses(client):
    response = client.get("/api/v1/verbs/comer")
    conjugations = response.json()["conjugations"]
    assert set(conjugations.keys()) == {
        "present",
        "preterito_perfeito",
        "preterito_imperfeito",
        "future",
        "conditional",
        "subjunctive_present",
    }
    for forms in conjugations.values():
        assert len(forms) == 4
