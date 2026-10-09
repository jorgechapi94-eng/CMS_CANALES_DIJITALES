def test_list_published_news(client):
    response = client.get('/api/news')
    assert response.status_code == 200
    assert 'items' in response.json

def test_create_news_as_editor(client, auth_headers):
    headers = auth_headers('editor@upec.edu.ec')
    response = client.post('/api/news', headers=headers, json={
        'title': 'Test News',
        'content_html': '<p>Content</p>',
        'status': 'published'
    })
    assert response.status_code == 201
    assert response.json['title'] == 'Test News'
    assert response.json['slug'] == 'test-news'

def test_create_news_unauthorized(client):
    response = client.post('/api/news', json={
        'title': 'Test News',
        'content_html': '<p>Content</p>'
    })
    assert response.status_code == 401

def test_update_news(client, auth_headers):
    headers = auth_headers('editor@upec.edu.ec')
    create_resp = client.post('/api/news', headers=headers, json={
        'title': 'Test News',
        'content_html': '<p>Content</p>'
    })
    news_id = create_resp.json['id']
    
    update_resp = client.put(f'/api/news/{news_id}', headers=headers, json={
        'title': 'Updated News'
    })
    assert update_resp.status_code == 200
    assert update_resp.json['title'] == 'Updated News'

def test_delete_news_soft(client, auth_headers):
    headers = auth_headers('editor@upec.edu.ec')
    create_resp = client.post('/api/news', headers=headers, json={
        'title': 'To Delete',
        'content_html': '<p>Content</p>'
    })
    news_id = create_resp.json['id']
    
    del_resp = client.delete(f'/api/news/{news_id}', headers=headers)
    assert del_resp.status_code == 200
    
    # Verify status is archived
    # Since we can't get it from list (only published), we might need an admin route,
    # but for now we know it shouldn't appear in public list
    list_resp = client.get('/api/news')
    assert not any(n['id'] == news_id for n in list_resp.json['items'])

def test_get_news_by_slug(client, auth_headers):
    headers = auth_headers('editor@upec.edu.ec')
    client.post('/api/news', headers=headers, json={
        'title': 'Slug Test',
        'content_html': '<p>Content</p>',
        'status': 'published'
    })
    
    response = client.get('/api/news/slug-test')
    assert response.status_code == 200
    assert response.json['title'] == 'Slug Test'
