import json
import pytest
import base64
import models.Plant
from flask import Flask
from app import initialize_app
from collections import namedtuple


app = Flask(__name__)
app = initialize_app(app)
client = app.test_client
generic_plant = models.Plant.Plant(
        scientificName='test',
        commonName='test')

generic_user = models.User.User(
        idType=1,
        email='test@test.com',
        username='test',
        password='password',
        salt='test',
        dateInsertion='03/02/2018',
        dateUpdate='10/02/2018')


def auth(generic_user=generic_user):
    creds = base64.b64encode(
        bytes(
            generic_user.username+":"+generic_user.password,
            'utf-8')).decode('utf-8')
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Basic %s' % creds
    }
    resp = client().post(
        '/api/gyresources/token/',
        headers=headers,
        follow_redirects=True)
    resp = json.loads(resp.get_data(as_text=True))
    token = resp['response']
    generic_user.password = 'password'
    return (generic_user, token)


generic_user = models.User.User(
    id=generic_user.id,
    idType=generic_user.idType,
    email=generic_user.email,
    username=generic_user.username,
    password='password',
    salt=generic_user.salt,
    dateInsertion=generic_user.dateInsertion,
    dateUpdate=generic_user.dateUpdate)


@pytest.mark.order1
def test_search_by_unexistent_id():
    data = {
                "action": "searchByID",
                "id": "1000",
            }
    resp = client().get(
            '/api/gyresources/plants',
            content_type='application/json',
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'dataType': 'json',
                'timeout': 240},
            query_string=data, follow_redirects=True)
    assert json.loads(resp.get_data(as_text=True))['status_code'] == 500


@pytest.mark.order2
def test_search_by_id():
    data = {
                "action": "searchByID",
                "id": "1",
            }
    resp = client().get(
            '/api/gyresources/plants',
            content_type='application/json',
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'dataType': 'json',
                'timeout': 240},
            query_string=data, follow_redirects=True)
    assert json.loads(resp.get_data(as_text=True))['status_code'] == 200
    assert 'Apple' in json.loads(
            resp.get_data(as_text=True))['response']['commonName']


@pytest.mark.order3
def test_search():
    data = {
                "action": "search",
                "scientificName": "Malus domestica",
                "commonName": "Apple",
            }
    resp = client().get(
            '/api/gyresources/plants',
            content_type='application/json',
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'dataType': 'json'},
            query_string=data, follow_redirects=True)
    pagedResponse = json.loads(resp.get_data(as_text=True))
    assert pagedResponse['status_code'] == 200
    for response in pagedResponse['response']:
        assert 'Malus domestica' in response['scientificName']


@pytest.mark.order4
def test_search_with_page_size_and_offset():
    data = {
                "action": "search",
                "scientificName": "Malus domestica",
                "commonName": "Apple",
                "pageSize": 10,
                "offset": 0
            }
    resp = client().get(
            '/api/gyresources/plants',
            content_type='application/json',
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'dataType': 'json'},
            query_string=data, follow_redirects=True)
    pagedResponse = json.loads(resp.get_data(as_text=True))
    assert pagedResponse['status_code'] == 200
    for response in pagedResponse['response']:
        assert 'Malus domestica' in response['scientificName']


@pytest.mark.order5
def test_create(generic_plant=generic_plant, generic_user=generic_user):
    (generic_user, token) = auth(generic_user)
    data = generic_plant.__dict__
    headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % token['token']
            }
    resp = client().post('/api/gyresources/plants/', data=str(
        json.dumps(data)), headers=headers)
    plant = json.loads(
                resp.get_data(as_text=True))['response']
    plant = namedtuple("Plant", plant.keys())(*plant.values())
    generic_plant = plant
    assert resp.status_code == 200
    assert "'id': 0" not in json.loads(resp.get_data(as_text=True))['response']


@pytest.mark.order6
def test_update(generic_plant=generic_plant, generic_user=generic_user):
    (generic_user, token) = auth(generic_user)
    data = generic_plant.__dict__
    data['action'] = 'search'
    resp = client().get(
            '/api/gyresources/plants',
            content_type='application/json',
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'dataType': 'json'},
            query_string=data, follow_redirects=True)
    pagedResponse = json.loads(resp.get_data(as_text=True))
    plant = object()
    for response in pagedResponse['response']:
        plant = namedtuple("Plant", response.keys())(*response.values())

    plant = {
                "action": "string",
                "id": plant.id,
                "scientificName": 'update',
                "commonName": plant.commonName
            }
    generic_plant.scientificName = 'update'
    headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % token['token']
            }
    resp = client().put('/api/gyresources/plants/', data=str(
        json.dumps(plant)), headers=headers)
    assert resp.status_code == 200
    plant = json.loads(
                resp.get_data(as_text=True))
    plant = namedtuple("Plant", plant.keys())(*plant.values())
    assert "update" in plant.response['scientificName']


@pytest.mark.order7
def test_delete(generic_plant=generic_plant, generic_user=generic_user):
    (generic_user, token) = auth(generic_user)
    data = generic_plant.__dict__
    data['action'] = 'search'
    resp = client().get(
            '/api/gyresources/plants',
            content_type='application/json',
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'dataType': 'json'},
            query_string=data, follow_redirects=True)
    pagedResponse = json.loads(resp.get_data(as_text=True))
    plant = object()
    for response in pagedResponse['response']:
        plant = namedtuple("Plant", response.keys())(*response.values())

    plant = {
                "action": "string",
                "id": plant.id,
                "scientificName": plant.scientificName,
                "commonName": plant.commonName
            }
    headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % token['token']
            }
    resp = client().delete('/api/gyresources/plants/', data=str(
        json.dumps(plant)), headers=headers)
    assert resp.status_code == 200
    assert 204 == json.loads(
            resp.get_data(as_text=True))['status_code']


@pytest.mark.order8
def test_create_empty(generic_plant=generic_plant, generic_user=generic_user):
    (generic_user, token) = auth(generic_user)
    plant = generic_plant
    plant.scientificName = ''
    plant.commonName = ''
    data = plant.__dict__
    headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % token['token']
            }
    resp = client().post('/api/gyresources/plants/', data=str(
        json.dumps(data)), headers=headers)
    resp = json.loads(
                resp.get_data(as_text=True))
    assert resp['status_code'] == 500


@pytest.mark.order9
def test_update_wrong_id(
        generic_plant=generic_plant,
        generic_user=generic_user):
    (generic_user, token) = auth(generic_user)
    data = generic_plant.__dict__
    data['action'] = 'search'
    resp = client().get(
            '/api/gyresources/plants',
            content_type='application/json',
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'dataType': 'json'},
            query_string=data, follow_redirects=True)
    pagedResponse = json.loads(resp.get_data(as_text=True))
    plant = object()
    for response in pagedResponse['response']:
        plant = namedtuple("Plant", response.keys())(*response.values())

    plant = {
                "action": "string",
                "id": 1000,
                "scientificName": 'update',
                "commonName": plant.commonName
            }
    headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % token['token']
            }
    resp = client().put('/api/gyresources/plants/', data=str(
        json.dumps(plant)), headers=headers)
    resp = json.loads(
                resp.get_data(as_text=True))
    assert resp['status_code'] == 500
    assert 'Internal server error' in resp['message']


@pytest.mark.order10
def test_delete_non_existent(
        generic_plant=generic_plant,
        generic_user=generic_user):
    (generic_user, token) = auth(generic_user)
    data = generic_plant.__dict__
    data['action'] = 'search'
    resp = client().get(
            '/api/gyresources/plants',
            content_type='application/json',
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'dataType': 'json'},
            query_string=data, follow_redirects=True)
    pagedResponse = json.loads(resp.get_data(as_text=True))
    plant = object()
    for response in pagedResponse['response']:
        plant = namedtuple("Plant", response.keys())(*response.values())

    plant = {
                "action": "string",
                "id": 1000,
                "scientificName": plant.scientificName,
                "commonName": plant.commonName
            }
    headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % token['token']
            }
    resp = client().delete('/api/gyresources/plants/', data=str(
        json.dumps(plant)), headers=headers)
    resp = json.loads(
                resp.get_data(as_text=True))
    assert resp['status_code'] == 500
    assert 'Internal server error' in resp['message']
