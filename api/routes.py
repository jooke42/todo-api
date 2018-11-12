from flask import Response, jsonify, abort, request
from flask_restplus import Api, Resource, fields
from api import api

todos = [
        {
            'id': 1,
            'title': 'test 1',
            'description': 'premier test de l\'api todo'
        }
]

todo = api.model('Todo', {
    'id': fields.Integer(readOnly=True, description='The task unique identifier'),
    'title': fields.String(required=True, description='The task details'),
    'description': fields.String(required=False, description='The task details')
})

ns = api.namespace('todos', description='TODO operations')

@api.route('/todos')
class TodoList(Resource):
    def get(self):
        return todos

    @api.marshal_with(todo, code=201)
    def post(self):
        todo = api.payload
        if not api.payload or 'title' not in api.payload.keys():
            api.abort(401, "Todo need at least a title")

        todo['id'] = todos[-1]['id'] + 1
        return todo, 201


@api.route('/todos/<int:todo_id>')
@api.doc(responses={404: 'Todo not found'}, params={'todo_id': 'The Todo ID'})
class Todo(Resource):

    @api.doc(description='todo_id should be in')
    @api.marshal_with(todo)
    def get(self, todo_id):
        return todos[todo_id]

    @api.doc(responses={204: 'Todo deleted'})
    def delete(self, todo_id):
        '''Delete a task given its identifier'''

        del todos[todo_id]
        return '', 204


    @api.marshal_with(todo)
    def put(self, todo_id):
        '''Update a task given its identifier'''

        find_todos = [td for td in todos if td['id'] == todo_id]

        if not find_todos:
            api.abort(404, f"Todo {todo_id} doesn't exist")

        todo = find_todos[0]
        todo['title'] = api.payload['title']
        todo['description'] = api.payload['description']

        return todo, 200

