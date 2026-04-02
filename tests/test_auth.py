def test_create_account(client):
    response = client.post("/auth/create_account",
                           json={
                               "name": "Wagner",
                               "email": "wagner.com",
                               "password": "123456",
                               "active": True,
                               "admin": False
                               })
    
    assert response.status_code == 200
    assert "successfully registered" in response.json()["message"]


def test_login_success(client):
    client.post("/auth/create_account",
                json={
                    "name": "Wagner",
                    "email": "wagner.com",
                    "password": "123456",
                    "active": True,
                    "admin": False
                    })
    
    response = client.post("/auth/login",
                           json={
                               "email": "wagner.com",
                               "password": "123456"
                               })
    
    body = response.json()
    assert response.status_code == 200
    assert "access_token" in body
    assert "refresh_token" in body
    assert body["token_type"] == "Bearer"


def test_login_invalid_credentials(client):
    client.post("/auth/create_account",
                json={
                    "name": "Wagner",
                    "email": "wagner.com",
                    "password": "123456",
                    "active": True,
                    "admin": False
                })

    response = client.post("/auth/login",
                           json={
                               "email": "wagner.com",
                               "password": "wrong_password"
                           })
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid Email or Password."


def test_create_account_duplicated_email(client):
    dic_info = {
        "name": "Wagner",
        "email": "wagner.com",
        "password": "123456",
        "active": True,
        "admin": False
    }

    client.post("/auth/create_account", json=dic_info)
    response = client.post("/auth/create_account", json=dic_info)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "E-mail already used."