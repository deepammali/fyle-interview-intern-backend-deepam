import json


def test_start_root_route(client):
    response = client.get(
        '/',
    )

    assert response.status_code == 200
    data = response.json['status']
    assert data == 'ready'


def test_non_existing_api(client, h_student_1):
    response = client.get(
        '/student/congratulations',
        headers=h_student_1,
        json={
            'id': 1,
        }
    )
    
    assert response.status_code == 404
    error_response = response.json
    assert error_response['error'] == "NotFound"


def test_principle_not_found(client, h_student_1):
    response = client.get(
        '/student/assignments',
        headers={},
        json={}
    )
    
    assert response.status_code == 401
    error_response = response.json
    assert error_response['error'] == "FyleError"

def test_student_id_not_found(client, h_student_1):
    response = client.get(
        '/student/assignments',
        headers = {
            'X-Principal': json.dumps({
                'user_id': 1
            })
        },
        json={}
    )
    
    assert response.status_code == 403
    error_response = response.json
    assert error_response['error'] == "FyleError"
