def test_new_word_is_immediately_due(client):
    client.post("/api/v1/vocabulary", json={"portuguese": "sol", "english": "sun", "tags": []})

    response = client.get("/api/v1/flashcards/due")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_submitting_review_updates_mastery_and_reschedules(client):
    created = client.post(
        "/api/v1/vocabulary", json={"portuguese": "lua", "english": "moon", "tags": []}
    ).json()

    response = client.post(
        f"/api/v1/flashcards/{created['id']}/review",
        json={"result": "easy"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["mastery_level"] == 1

    # Reviewed word with a future next_review_at should no longer be due today.
    due_response = client.get("/api/v1/flashcards/due")
    assert created["id"] not in [v["id"] for v in due_response.json()]
