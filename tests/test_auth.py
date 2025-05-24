def test_protected_route(client, token):
    res = client.get("/api/protected", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200