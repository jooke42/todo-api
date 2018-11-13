# tests/test_api.py
from api import create_app, db, models
import json, request, pytest, os
from config import TestingConfig


@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        print("create db")
        yield app
        print("delete db")
        db.drop_all()


@pytest.fixture
def client(app):
    print("return client")
    return app.test_client()


@pytest.fixture
def a_todo(app):

    td = models.Todo(
        title='test 1',
    )
    with app.app_context():
        db.session.add(td)
        print("added td")
        db.session.commit()
        db.session.flush()
        td_dict = td.to_dict()
    return td_dict


class TestIntegrationTodo:

    def test_fixture_add_todo(self, a_todo, app):
        with app.app_context():
            todos = models.Todo.query.all()
        assert todos

    def test_todos_get_all(self, client, a_todo):
        """
        test todos URI with GET return all todos in database
        """

        expected_response = a_todo

        response = client.get(f"/todos/{a_todo['id']}")
        json_response = json.loads(response.data.decode('utf8'))

        assert response.status_code == 200
        assert json_response == expected_response

    def test_todos_get(self, client, a_todo):
        """
        test todos URI with GET return all todos in database
        """
        expected_response = a_todo
        response = client.get('/todos')
        json_response = json.loads(response.data.decode('utf8'))

        assert response.status_code == 200
        assert json_response[0] == expected_response

    def test_todos_post(self, client):
        """
        Test adding a todo resource into the api
        """

        rv = client.post('/todos', json={
            'title': 'post test'
        }, follow_redirects = True)

        assert rv.status_code == 201

    def test_todos_post_failed(self, client):
        """
        test bad post request on posting todo
        """

        rv = client.post('/todos', json={
            'complete': True
        }, follow_redirects=True)

        assert rv.status_code == 401

        rv = client.post('/todos')

        assert rv.status_code == 401

    def test_todos_put_failed(self, client):
        """
        assert failed put if id doesn't exist or json not valid
        :param client:
        :return:
        """
        rv = client.put('/todos/0', json={
            'title': 'put title'
        }, follow_redirects = True)

        assert rv.status_code == 404



    def test_todos_put(self, client,a_todo):
        """
        assert failed put if id doesn't exist or json not valid
        :param client:
        :return:
        """
        rv = client.put(f"/todos/{a_todo['id']}", json={
            'title': 'put title',
        }, follow_redirects = True)

        assert rv.status_code == 200

        json_response = rv.get_json()

        assert json_response['title'] == 'put title'

    def test_todos_delete(self,client,a_todo):
        rv = client.delete(f"/todos/{a_todo['id']}", follow_redirects=True)

        assert rv.status_code == 204

    def test_todos_delete_failed(self,client,a_todo):
        rv = client.delete(f"/todos/{a_todo['id']+8}", follow_redirects=True)

        assert rv.status_code == 404