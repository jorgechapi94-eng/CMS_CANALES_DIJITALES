def test_login_success(client):
    response = client.post('/api/auth/login', json={
        'email': 'superadmin@upec.edu.ec',
        'password': 'password'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json
    assert 'refresh_token' in response.json

def test_login_wrong_domain(client):
    response = client.post('/api/auth/login', json={
        'email': 'user@gmail.com',
        'password': 'password'
    })
    assert response.status_code == 403

def test_login_wrong_password(client):
    response = client.post('/api/auth/login', json={
        'email': 'superadmin@upec.edu.ec',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401

def test_login_inactive_user(client):
    response = client.post('/api/auth/login', json={
        'email': 'inactive@upec.edu.ec',
        'password': 'password'
    })
    assert response.status_code == 403

def test_refresh_token(client):
    login_resp = client.post('/api/auth/login', json={
        'email': 'superadmin@upec.edu.ec',
        'password': 'password'
    })
    refresh_token = login_resp.json['refresh_token']
    
    refresh_resp = client.post('/api/auth/refresh', headers={
        'Authorization': f'Bearer {refresh_token}'
    })
    assert refresh_resp.status_code == 200
    assert 'access_token' in refresh_resp.json

def test_me_endpoint(client, auth_headers):
    headers = auth_headers()
    response = client.get('/api/auth/me', headers=headers)
    assert response.status_code == 200
    assert response.json['email'] == 'superadmin@upec.edu.ec'

def test_logout(client, auth_headers):
    headers = auth_headers()
    response = client.post('/api/auth/logout', headers=headers)
    assert response.status_code == 200
    # Try using token again
    me_resp = client.get('/api/auth/me', headers=headers)
    assert me_resp.status_code == 401
def test_login_missing_data(client):
    response = client.post('/api/auth/login', json={
        'email': 'superadmin@upec.edu.ec'
        # Falta la contraseña intencionalmente
    })
    assert response.status_code == 400
    assert response.json['error'] == 'Email and password are required'
    
    # Try using token again
    me_resp = client.get('/api/auth/me', headers=headers)
    assert me_resp.status_code == 401
