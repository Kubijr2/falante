def test_dashboard_summary_reflects_activity(client):
    word_a = client.post(
        "/api/v1/vocabulary", json={"portuguese": "praia", "english": "beach", "tags": []}
    ).json()
    client.post(
        "/api/v1/vocabulary", json={"portuguese": "montanha", "english": "mountain", "tags": []}
    )

    client.post(f"/api/v1/flashcards/{word_a['id']}/review", json={"result": "easy"})

    response = client.get("/api/v1/dashboard/summary")
    assert response.status_code == 200
    body = response.json()

    assert body["total_words"] == 2
    assert body["total_reviews"] == 1
    assert body["streak"] == 1
    assert body["mastery_distribution"]["1"] == 1  # word_a leveled up to mastery 1
    assert body["mastery_distribution"]["0"] == 1  # the untouched word
    assert len(body["recently_learned"]) == 1
    assert body["recently_learned"][0]["portuguese"] == "praia"


def test_dashboard_summary_with_no_activity(client):
    response = client.get("/api/v1/dashboard/summary")
    assert response.status_code == 200
    body = response.json()
    assert body["streak"] == 0
    assert body["total_words"] == 0
    assert body["recently_learned"] == []


def test_hard_review_does_not_count_as_recently_learned(client):
    word = client.post(
        "/api/v1/vocabulary", json={"portuguese": "chuva", "english": "rain", "tags": []}
    ).json()
    client.post(f"/api/v1/flashcards/{word['id']}/review", json={"result": "hard"})

    response = client.get("/api/v1/dashboard/summary")
    assert response.json()["recently_learned"] == []
