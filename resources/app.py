import os

from flask import Flask, jsonify, request, send_from_directory
from dao import MemDAO
from werkzeug.utils import safe_join

static = safe_join(os.path.dirname(__file__), 'static')

app = Flask(__name__)

DAO = MemDAO()

# Legger til eksempel-innhold i databasen:
DAO.insert({'task': 'Steg 1: Last ned avhengigheter med pip', 'fav': False})
DAO.insert({'task': 'Steg 2: Start flask', 'fav': False})
DAO.insert({'task': 'Steg 3: Skriv kode!', 'fav': False})


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
    """OPPGAVE 1: hent alle todos"""
    print('list_todos')
    return jsonify(DAO.get_all()), 200


def create_todo():
    """OPPGAVE 2: opprett en ny todo"""
    print('create_todo')


def delete_todo(id):
    """OPPGAVE 3: slett en todo"""
    print('delete_todo')


def update_todo(id):
    """OPPGAVE 4: oppdatere en todo"""
    print('update_todo')


def get_todo(id):
    print('get_todo')


if __name__ == '__main__':
    app.run(debug=True)
