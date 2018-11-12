# tests/test_api.py
from api import app
import json, request, pytest, os


@pytest.fixture
def client():
    client = app.test_client()
    yield client


class TestApi:

    def test_todos_get(self, client):
        """
        test todos URI with GET return all todos in database
        """

        expected_response = {
            'id': 1,
            'title': 'test 1',
            'description': 'premier test de l\'api todo'
        }

        response = client.get('/todos')
        json_response = json.loads(response.data.decode('utf8'))

        assert response.status_code == 200
        assert json_response[0] == expected_response

    def test_todos_post(self, client):
        """
        Test adding a todo resource into the api
        """

        rv = client.post('/todos', json={
            'title': 'post test',
            'description': 'testing posting todo with api'
        }, follow_redirects = True)

        assert rv.status_code == 201

    def test_todos_post_failed(self, client):
        """
        test bad post request on posting todo
        """

        rv = client.post('/todos', json={
            'description': 'testing posting todo with api'
        }, follow_redirects=True)

        assert  rv.status_code == 401

        rv = client.post('/todos')

        assert rv.status_code == 401

    def test_todos_put_failed(self, client):
        """
        assert failed put if id doesn't exist or json not valid
        :param client:
        :return:
        """
        rv = client.put('/todos/0', json={
            'title': 'put title',
            'description': 'new description'
        }, follow_redirects = True)

        assert rv.status_code == 404


    def test_todos_put(self, client):
        """
        assert failed put if id doesn't exist or json not valid
        :param client:
        :return:
        """
        rv = client.put('/todos/1', json={
            'title': 'put title',
            'description': 'new description'
        }, follow_redirects = True)

        assert rv.status_code == 201

        json_response = rv.get_json()

        assert json_response['todo']['title'] == 'put title'
        assert json_response['todo']['description'] == 'new description'
