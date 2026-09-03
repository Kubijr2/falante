def test_lookup_batch_returns_matches_and_omits_non_matches(client):
    response = client.post(
        "/api/v1/verbs/lookup-batch", json={"forms": ["falo", "pizza", "sou"]}
    )
    assert response.status_code == 200
    body = response.json()
    assert set(body["matches"].keys()) == {"falo", "sou"}
    assert body["matches"]["falo"]["infinitive"] == "falar"
    assert body["matches"]["falo"]["translation"] == "to speak"
    assert body["matches"]["sou"]["infinitive"] == "ser"


def test_lookup_batch_with_no_matches_returns_empty_matches(client):
    response = client.post("/api/v1/verbs/lookup-batch", json={"forms": ["pizza", "carro"]})
    assert response.status_code == 200
    assert response.json()["matches"] == {}


def test_lookup_batch_rejects_empty_forms_list(client):
    response = client.post("/api/v1/verbs/lookup-batch", json={"forms": []})
    assert response.status_code == 422


def test_lookup_batch_route_is_post_only(client):
    # A GET to this path falls through to GET /verbs/{infinitive} (treating
    # "lookup-batch" as an infinitive to search for) rather than running the
    # batch handler — confirms there's no accidental collision, just a
    # clean 404 for a verb that doesn't exist.
    response = client.get("/api/v1/verbs/lookup-batch")
    assert response.status_code == 404
