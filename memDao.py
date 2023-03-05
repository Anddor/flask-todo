from collections import OrderedDict

from daoInterface import DaoInterface


class MemDAO(DaoInterface):
    def __init__(self):
        self.todos = OrderedDict()
        self._id_counter = 0

    def get_all(self):
        # fetch all todos from database
        todos = list(self.todos.values())
        return todos

    def get(self, id):
        # fetch the todo with the given id
        return self.todos[id]

    def insert(self, data):
        todo = data
        # get new id
        new_id = self._id_counter
        self._id_counter += 1

        todo['id'] = new_id
        self.todos[new_id] = todo
        return todo

    def update_fields(self, data, todo):
        # Update todo with only the fields in data
        for key in data:
            todo[key] = data[key]
        return todo

    def update(self, id, data):
        # update todo
        todo = self.todos[id]
        updated_todo = self.update_fields(data, todo)
        self.todos[id] = updated_todo
        return todo

    def delete(self, id):
        # delete todo
        print(self.todos.items())
        del self.todos[id]
