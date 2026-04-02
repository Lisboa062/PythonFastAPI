def create_user_and_get_token(client, email="user.com", password="123456", admin=False):
    client.post("/auth/create_account",
                json={
                    "name": "User",
                    "email": email,
                    "password": password,
                    "active": True,
                    "admin": admin
                })
    
    response = client.post("/auth/login",
                           json={
                               "email": email,
                               "password": password
                           })
    
    return response.json()["access_token"]


def test_create_order(client):
    token = create_user_and_get_token(client)

    response = client.post("/orders/",
                           json={},
                               headers={"Authorization": f"Bearer {token}"}
                           )
    
    assert response.status_code == 200
    assert "Order created successfully" in response.json()["message"]


def test_create_order_without_token(client):
    response = client.post("/orders/",
                           json={})
    
    assert response.status_code == 401


def test_get_order_not_found(client):
    token = create_user_and_get_token(client)

    response = client.get("/orders/order/999",
                          headers={"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 404


def test_user_cannot_access_other_user_order(client):
    token_user_1 = create_user_and_get_token(client, email="user1@email.com")

    response_order = client.post("/orders/",
                                 json={},
                                 headers={"Authorization": f"Bearer {token_user_1}"})
    
    message = response_order.json()["message"]
    order_id = int(message.split(":")[-1].strip())

    token_user_2 = create_user_and_get_token(client, email="user2@email.com")

    response = client.get(f"/orders/order/{order_id}",
                          headers={"Authorization": f"Bearer {token_user_2}"})
    
    assert response.status_code == 403

