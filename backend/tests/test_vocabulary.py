def test_create_and_list_vocabulary(client):
    response = client.post(
        "/api/v1/vocabulary",
        json={
            "portuguese": "falar",
            "english": "to speak",
            "example_sentence": "Eu gosto de falar português.",
            "category": "verbs",
            "tags": ["verbs", "core"],
            "difficulty": "medium",
        },
    )
    assert response.status_code == 201
    created = response.json()
    assert created["portuguese"] == "falar"
    assert created["tags"] == ["verbs", "core"]
    assert created["mastery_level"] == 0

    list_response = client.get("/api/v1/vocabulary")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1


def test_get_missing_vocabulary_returns_404(client):
    response = client.get("/api/v1/vocabulary/999")
    assert response.status_code == 404


def test_update_vocabulary_partial(client):
    created = client.post(
        "/api/v1/vocabulary",
        json={"portuguese": "casa", "english": "house", "tags": []},
    ).json()

    response = client.patch(
        f"/api/v1/vocabulary/{created['id']}",
        json={"notes": "Feminine noun"},
    )
    assert response.status_code == 200
    assert response.json()["notes"] == "Feminine noun"
    assert response.json()["portuguese"] == "casa"  # untouched fields preserved


def test_delete_vocabulary(client):
    created = client.post(
        "/api/v1/vocabulary",
        json={"portuguese": "livro", "english": "book", "tags": []},
    ).json()

    delete_response = client.delete(f"/api/v1/vocabulary/{created['id']}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/api/v1/vocabulary/{created['id']}")
    assert get_response.status_code == 404


def test_search_filters_results(client):
    client.post("/api/v1/vocabulary", json={"portuguese": "gato", "english": "cat", "tags": []})
    client.post("/api/v1/vocabulary", json={"portuguese": "cachorro", "english": "dog", "tags": []})

    response = client.get("/api/v1/vocabulary", params={"search": "gato"})
    results = response.json()
    assert len(results) == 1
    assert results[0]["portuguese"] == "gato"
