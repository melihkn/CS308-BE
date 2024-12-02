def test_get_categories(client):
    response = client.get("/ProductManager/categories")  # Updated path
    assert response.status_code == 200

def test_create_category(client):
    data = {"category_name": "Electronics", "parentcategory_id": None}
    response = client.post("/ProductManager/categories", json=data)  # Updated path
    assert response.status_code == 201

#TWO FAILURES / BUG REPORT WAITING