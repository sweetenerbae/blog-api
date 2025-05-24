def test_get_posts(client):
    response = client.get("/api/posts")
    assert response.status_code == 200