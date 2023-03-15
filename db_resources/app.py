import os

from flask import Flask, jsonify, request, send_from_directory
from werkzeug.utils import safe_join

from dbDao import DbDAO

static = safe_join(os.path.dirname(__file__), 'static')

app = Flask(__name__)

DAO = DbDAO()


@app.route('/', methods=['GET'])
def _home():
    """Serve index.html at the root url"""
    print('home')

    return send_from_directory(static, 'index.html'), 200


@app.route('/<path:path>', methods=['GET'])
def _static(path):
    """Serve content from the static directory"""
    print('static')
    return send_from_directory(static, path), 200


@app.route('/api/todos/', methods=['GET'])
def list_todos():
    return jsonify(DAO.get_all()), 200


@app.route('/api/todos/', methods=['POST'])
def create_todo():
    json = request.get_json()
    if 'task' not in json:
        return "field 'task' must be set", 400
    # set default values for fav
    if 'fav' not in json:
        json['fav'] = False

    return DAO.insert(json), 201


@app.route('/api/todos/<int:id>', methods=['GET'])
def get_todo(id):
    print('get_todo')
    return DAO.get(id)


@app.route('/api/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    print('delete_todo')
    DAO.delete(id)
    return '', 204


@app.route('/api/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    print('update_todo')
    json = request.get_json()

    return DAO.update(id, json)


if __name__ == '__main__':
    app.run(debug=True)
