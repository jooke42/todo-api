
from flask_restplus import Api, Resource, fields
from api import api, db
from api import models
from flask import jsonify


todo = api.model('Todo', {
    'id': fields.Integer(readOnly=True, description='The task unique identifier'),
    'title': fields.String(required=True, description='The task details'),
    'complete': fields.Boolean(required=False, description='The task completed')
})

ns = api.namespace('todos', description='TODO operations')


@api.route('/todos')
class TodoList(Resource):

    @api.doc('create_todo')
    @api.marshal_list_with(todo)
    def get(self):
        return [td.to_dict()for td in models.Todo.query.all()]

    @api.doc('create_todo')
    @api.expect(todo)
    @api.marshal_with(todo, code=201)
    def post(self):
        todo = api.payload
        if not api.payload or 'title' not in api.payload.keys():
            api.abort(401, "Todo need at least a title"+ str(api.payload))
        todo_obj = models.Todo(**todo)
        db.session.add(todo_obj)
        db.session.commit()

        return jsonify(todo_obj.to_dict()), 201


@api.route('/todos/<int:todo_id>')
@api.doc(responses={404: 'Todo not found'}, params={'todo_id': 'The Todo ID'})
@api.param('todo_id', 'The todo identifier')
class Todo(Resource):

    @api.doc(description='todo_id should be in')
    @api.marshal_with(todo)
    def get(self, todo_id):
        return models.Todo.query.get_or_404(todo_id).to_dict()

    @api.doc('delete_todo')
    @api.doc(responses={204: 'Todo deleted'})
    def delete(self, todo_id):
        """Delete a task given its identifier
        """
        todo_obj = models.Todo.query.get_or_404(todo_id)
        db.session.delete(todo_obj)
        db.session.commit()
        return '', 204

    @api.expect(todo)
    @api.marshal_with(todo)
    def put(self, todo_id):
        """Update a task given its identifier"""

        todo_obj = models.Todo.query.get(todo_id)

        if not todo_obj:
            api.abort(404, f"Todo {todo_id} doesn't exist")

        todo_obj.title = api.payload['title']
        if 'complete' in api.payload:
            todo_obj.complete = api.payload['complete']
        db.session.commit()
        return todo_obj.to_dict(), 200


