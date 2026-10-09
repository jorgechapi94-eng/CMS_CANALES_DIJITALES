import io

def test_upload_pdf_success(client, auth_headers):
    headers = auth_headers()
    # Create fake PDF content
    pdf_content = b'%PDF-1.4\n1 0 obj\n<<>>\nendobj\n'
    data = {
        'file': (io.BytesIO(pdf_content), 'test.pdf')
    }
    
    response = client.post('/api/uploads/pdf', headers=headers, data=data, content_type='multipart/form-data')
    assert response.status_code == 201
    assert 'url' in response.json
    assert response.json['originalName'] == 'test.pdf'

def test_upload_invalid_extension(client, auth_headers):
    headers = auth_headers()
    data = {
        'file': (io.BytesIO(b'dummy content'), 'test.exe')
    }
    
    response = client.post('/api/uploads/pdf', headers=headers, data=data, content_type='multipart/form-data')
    assert response.status_code == 400

def test_upload_without_auth(client):
    data = {
        'file': (io.BytesIO(b'%PDF-1.4\n'), 'test.pdf')
    }
    
    response = client.post('/api/uploads/pdf', data=data, content_type='multipart/form-data')
    assert response.status_code == 401
