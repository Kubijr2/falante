def test_seed_topics_are_present(client):
    response = client.get("/api/v1/grammar")
    assert response.status_code == 200
    slugs = {t["slug"] for t in response.json()}
    assert slugs == {
        "ser-vs-estar",
        "por-vs-para",
        "object-pronouns",
        "past-tenses",
        "subjunctive",
    }


def test_list_items_omit_full_content(client):
    response = client.get("/api/v1/grammar")
    for item in response.json():
        assert "content" not in item


def test_get_topic_by_slug_includes_content(client):
    response = client.get("/api/v1/grammar/ser-vs-estar")
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Ser vs. Estar"
    assert "## The core distinction" in body["content"]


def test_get_missing_topic_returns_404(client):
    response = client.get("/api/v1/grammar/not-a-real-topic")
    assert response.status_code == 404


def test_filter_by_category(client):
    response = client.get("/api/v1/grammar", params={"category": "Verbs"})
    slugs = {t["slug"] for t in response.json()}
    assert slugs == {"ser-vs-estar"}


def test_search_matches_content_not_just_title(client):
    # "subjunctive" article body mentions "doubt" prominently; title doesn't.
    response = client.get("/api/v1/grammar", params={"search": "doubt"})
    slugs = {t["slug"] for t in response.json()}
    assert "subjunctive" in slugs


def test_list_categories(client):
    response = client.get("/api/v1/grammar/categories")
    assert response.status_code == 200
    assert set(response.json()) == {"Verbs", "Prepositions", "Pronouns", "Tenses", "Mood"}
