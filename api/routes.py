from api import app
from flask import Response, jsonify, abort, request

todos = [
        {
            'id': 1,
            'title': 'test 1',
            'description': 'premier test de l\'api todo'
        }
    ]


@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)


@app.route('/todos', methods=['POST'])
def post_todos():
    if not request.json or not 'title' in request.json:
        abort(401)
    todo = {
        'id': todos[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', "")
    }
    todos.append(todo)
    return jsonify({'todo': todo}), 201

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def put_todos(todo_id):
    find_todos = [todo for todo in todos if todo['id'] == todo_id]

    if not find_todos:
        abort(404)

    todo = find_todos[0]
    todo['title'] = request.json.get('title', todo['title'])
    todo['description'] = request.json.get('description', todo['description'])

    return jsonify({'todo': todo}), 201

