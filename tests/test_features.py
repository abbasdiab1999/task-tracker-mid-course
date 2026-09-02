from datetime import date, timedelta


def create_task(client, **overrides):
    body = {
        "title": "Demo task",
        "description": "test",
        "status": "ToDo",
        "priority": "Medium",
        "tags": []
    }
    body.update(overrides)
    return client.post("/tasks", json=body)


def test_create_get_and_list_tasks(client):
    res = create_task(client, title="CRUD task")
    assert res.status_code == 201
    created = res.json()

    get_res = client.get(f"/tasks/{created['id']}")
    assert get_res.status_code == 200
    assert get_res.json()["title"] == "CRUD task"

    list_res = client.get("/tasks")
    assert list_res.status_code == 200
    assert [task["id"] for task in list_res.json()] == [created["id"]]


def test_update_task_updates_selected_fields(client):
    created = create_task(client, title="Original", description="Keep", tags=["backend"]).json()
    res = client.patch(f"/tasks/{created['id']}", json={"title": "Updated", "priority": "High"})
    assert res.status_code == 200

    body = res.json()
    assert body["title"] == "Updated"
    assert body["description"] == "Keep"
    assert body["priority"] == "High"
    assert body["tags"] == ["backend"]


def test_delete_task_removes_task(client):
    created = create_task(client, title="Delete me").json()
    res = client.delete(f"/tasks/{created['id']}")
    assert res.status_code == 204

    assert client.get(f"/tasks/{created['id']}").status_code == 404
    assert client.get("/tasks").json() == []


def test_null_title_update_is_rejected_without_corrupting_tasks(client):
    created = create_task(client, title="Stable task").json()
    res = client.patch(f"/tasks/{created['id']}", json={"title": None})
    assert res.status_code == 422

    list_res = client.get("/tasks")
    assert list_res.status_code == 200
    tasks = list_res.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Stable task"

    get_res = client.get(f"/tasks/{created['id']}")
    assert get_res.status_code == 200
    assert get_res.json()["title"] == "Stable task"


def test_valid_due_date_is_saved(client):
    due = (date.today() + timedelta(days=2)).isoformat()
    res = create_task(client, due_date=due)
    assert res.status_code == 201
    assert res.json()["due_date"] == due
    assert res.json()["overdue"] is False


def test_invalid_due_date_format_rejected(client):
    res = create_task(client, due_date="not-a-date")
    assert res.status_code == 422


def test_overdue_detection(client):
    due = (date.today() - timedelta(days=1)).isoformat()
    res = create_task(client, due_date=due)
    assert res.status_code == 201
    assert res.json()["overdue"] is True


def test_overdue_filter_returns_only_overdue_tasks(client):
    old = (date.today() - timedelta(days=2)).isoformat()
    future = (date.today() + timedelta(days=2)).isoformat()
    create_task(client, title="old", due_date=old)
    create_task(client, title="future", due_date=future)

    res = client.get("/tasks?overdue=true")
    assert res.status_code == 200
    assert [x["title"] for x in res.json()] == ["old"]


def test_create_with_tags_trims_and_deduplicates(client):
    res = create_task(client, tags=[" backend ", "urgent", "BACKEND"])
    assert res.status_code == 201
    assert res.json()["tags"] == ["backend", "urgent"]


def test_blank_tag_rejected(client):
    res = create_task(client, tags=["good", "   "])
    assert res.status_code == 422


def test_update_tags_preserves_other_fields(client):
    created = create_task(client, title="Keep me", description="same").json()
    res = client.patch(f"/tasks/{created['id']}", json={"tags": ["api"]})
    assert res.status_code == 200
    body = res.json()
    assert body["title"] == "Keep me"
    assert body["description"] == "same"
    assert body["tags"] == ["api"]


def test_filter_by_tag(client):
    create_task(client, title="one", tags=["backend"])
    create_task(client, title="two", tags=["frontend"])
    res = client.get("/tasks?tag=BACKEND")
    assert res.status_code == 200
    assert [x["title"] for x in res.json()] == ["one"]


def test_invalid_status_transition_returns_422(client):
    created = create_task(client, status="ToDo").json()
    res = client.patch(f"/tasks/{created['id']}", json={"status": "Done"})
    assert res.status_code == 422


def test_patch_without_status_does_not_trigger_transition_validation(client):
    created = create_task(client, status="ToDo").json()
    res = client.patch(f"/tasks/{created['id']}", json={"title": "Updated"})
    assert res.status_code == 200
    assert res.json()["title"] == "Updated"
