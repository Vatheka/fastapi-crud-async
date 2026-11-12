import json

from app.api import events_crud


def test_create_event(test_app, monkeypatch):
    payload = {
        "title": "Mekong Jazz Night",
        "city": "Phnom Penh",
        "price_usd": 15,
        "seats_left": 320,
    }

    async def mock_post(event):
        return 1

    monkeypatch.setattr(events_crud, "post", mock_post)

    response = test_app.post("/events/", content=json.dumps(payload))

    assert response.status_code == 201
    assert response.json() == {"id": 1, **payload}


def test_create_event_invalid_title(test_app):
    payload = {
        "title": "PP",
        "city": "Phnom Penh",
        "price_usd": 15,
        "seats_left": 320,
    }

    response = test_app.post("/events/", content=json.dumps(payload))

    assert response.status_code == 422


def test_read_event(test_app, monkeypatch):
    event = {
        "id": 1,
        "title": "Mekong Jazz Night",
        "city": "Phnom Penh",
        "price_usd": 15,
        "seats_left": 320,
    }

    async def mock_get(id):
        return event

    monkeypatch.setattr(events_crud, "get", mock_get)

    response = test_app.get("/events/1/")

    assert response.status_code == 200
    assert response.json() == event


def test_read_missing_event_and_invalid_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(events_crud, "get", mock_get)

    response = test_app.get("/events/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"

    response = test_app.get("/events/0/")
    assert response.status_code == 422


def test_read_all_events(test_app, monkeypatch):
    events = [
        {
            "id": 1,
            "title": "Mekong Jazz Night",
            "city": "Phnom Penh",
            "price_usd": 15,
            "seats_left": 320,
        }
    ]

    async def mock_get_all():
        return events

    monkeypatch.setattr(events_crud, "get_all", mock_get_all)

    response = test_app.get("/events/")

    assert response.status_code == 200
    assert response.json() == events


def test_update_event_invalid_data(test_app, monkeypatch):
    async def mock_get(id):
        return True

    monkeypatch.setattr(events_crud, "get", mock_get)
    payload = {
        "title": "PP",
        "city": "Phnom Penh",
        "price_usd": 15,
        "seats_left": 320,
    }

    response = test_app.put("/events/1/", content=json.dumps(payload))

    assert response.status_code == 422


def test_delete_event(test_app, monkeypatch):
    event = {
        "id": 1,
        "title": "Mekong Jazz Night",
        "city": "Phnom Penh",
        "price_usd": 15,
        "seats_left": 320,
    }

    async def mock_get(id):
        return event

    async def mock_delete(id):
        return id

    monkeypatch.setattr(events_crud, "get", mock_get)
    monkeypatch.setattr(events_crud, "delete", mock_delete)

    response = test_app.delete("/events/1/")

    assert response.status_code == 200
    assert response.json() == event
