def test_analytics_summary_requires_auth():
    from fastapi.testclient import TestClient

    from app.main import app

    with TestClient(app) as unauthenticated_client:
        response = unauthenticated_client.get("/api/v1/analytics/summary")
        assert response.status_code == 401


def test_analytics_summary_returns_empty_datasets_for_new_user(client):
    response = client.get("/api/v1/analytics/summary")
    assert response.status_code == 200
    body = response.json()
    assert body == {
        "vocabulary_growth": [],
        "review_activity": [],
        "review_quality": [],
        "mastery_trend": [],
        "writing_insights": [],
    }


def test_analytics_summary_reflects_real_activity(client):
    word = client.post(
        "/api/v1/vocabulary", json={"portuguese": "falar", "english": "to speak", "tags": []}
    ).json()
    client.post(f"/api/v1/flashcards/{word['id']}/review", json={"result": "easy"})

    response = client.get("/api/v1/analytics/summary", params={"range": "all"})
    body = response.json()

    assert len(body["vocabulary_growth"]) == 1
    assert body["vocabulary_growth"][0]["cumulative"] == 1
    assert len(body["review_activity"]) == 1
    assert body["review_activity"][0]["count"] == 1
    assert len(body["mastery_trend"]) >= 1
    assert body["mastery_trend"][-1]["level_1"] == 1  # "easy" bumped mastery to 1


def test_analytics_summary_rejects_invalid_range(client):
    response = client.get("/api/v1/analytics/summary", params={"range": "bogus"})
    assert response.status_code == 422


def test_analytics_data_is_isolated_per_user(client, test_user, second_user):
    from app.core.current_user import get_current_user
    from app.main import app

    app.dependency_overrides[get_current_user] = lambda: test_user
    client.post(
        "/api/v1/vocabulary", json={"portuguese": "falar", "english": "to speak", "tags": []}
    )

    app.dependency_overrides[get_current_user] = lambda: second_user
    response = client.get("/api/v1/analytics/summary")
    assert response.json()["vocabulary_growth"] == []

    app.dependency_overrides[get_current_user] = lambda: test_user


def test_dashboard_widgets_default_to_empty(client):
    response = client.get("/api/v1/auth/me")
    assert response.json()["dashboard_widgets"] == []


def test_dashboard_widgets_can_be_set(client):
    response = client.patch(
        "/api/v1/auth/me/dashboard-widgets",
        json={"widgets": ["vocabulary_growth", "review_activity"]},
    )
    assert response.status_code == 200
    assert response.json()["dashboard_widgets"] == ["vocabulary_growth", "review_activity"]

    # Confirm it actually persisted, not just echoed back
    followup = client.get("/api/v1/auth/me")
    assert followup.json()["dashboard_widgets"] == ["vocabulary_growth", "review_activity"]


def test_dashboard_widgets_rejects_unknown_ids(client):
    response = client.patch(
        "/api/v1/auth/me/dashboard-widgets", json={"widgets": ["not_a_real_widget"]}
    )
    assert response.status_code == 422


def test_dashboard_widgets_isolated_per_user(client, test_user, second_user):
    from app.core.current_user import get_current_user
    from app.main import app

    app.dependency_overrides[get_current_user] = lambda: test_user
    client.patch("/api/v1/auth/me/dashboard-widgets", json={"widgets": ["mastery_trend"]})

    app.dependency_overrides[get_current_user] = lambda: second_user
    response = client.get("/api/v1/auth/me")
    assert response.json()["dashboard_widgets"] == []

    app.dependency_overrides[get_current_user] = lambda: test_user
