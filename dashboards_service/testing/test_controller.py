def test_get_categories(client):
    response = client.get("/categories")
    assert response.status_code == 200
    assert response.json() == []

def test_create_category(client):
    data = {"category_name": "Electronics", "parentcategory_id": None}
    response = client.post("/categories", json=data)
    assert response.status_code == 201
    assert response.json()["category_name"] == "Electronics"

#TWO FAILURES / BUG REPORT WAITING