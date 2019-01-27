from datetime import datetime
import re
import sys
import os
try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser
config = ConfigParser()
config.read(os.path.expanduser('~/.simple_todo'))
try:
    TODO_FILE = config.get("data", "todo_file")
except KeyError:
    TODO_FILE = os.path.expanduser("~/todo.txt")

today = datetime.now()
today_string = today.strftime("%Y-%m-%d")

# simple "parser" for todo items
TODO_MATCH = re.compile(r"(?:(?P<done>x)\s+)?"
                        r"(?:(?P<created>\d{4}-\d{2}-\d{2})\s+)?"
                        r"(?:(?P<other>\d{4}-\d{2}-\d{2})\s+)?"
                        r"(?P<text>.*)$")


class Todo(object):
    def __init__(self, text_line):
        m = TODO_MATCH.match(text_line)
        if not m:
            raise ValueError("Can't understand line: {}".format(text_line))
        todo_dict = m.groupdict()
        self.completed = bool(todo_dict['done'] or False)
        self.created = datetime.strptime(todo_dict['created'], "%Y-%m-%d") if todo_dict['created'] else None
        self.other = datetime.strptime(todo_dict['other'], "%Y-%m-%d") if todo_dict['other'] else None
        self.todo_text = todo_dict['text']

    def __str__(self):
        todo_string = []
        if self.completed:
            todo_string.append("x")
        if self.created:
            todo_string.append(self.created.strftime("%Y-%m-%d"))
        if self.other:
            todo_string.append(self.other.strftime("%Y-%m-%d"))
        todo_string.append(self.todo_text)
        return " ".join(todo_string)

    @classmethod
    def create(cls, text):
        return cls("{} {}".format(today_string, text))


class TodoList(object):
    def __init__(self):
        self.todos = []
        self.completed = []
        with open(TODO_FILE, 'r') as todo_file:
            for todo in (Todo(todo_line) for todo_line in todo_file):
                if todo.completed:
                    self.completed.append(todo)
                else:
                    self.todos.append(todo)

    def bump(self, item_num):
        '''Move an item from anywhere in the list to the top'''
        item = self.todos.pop(item_num - 1)
        self.todos.insert(0, item)

    def complete(self, item_num):
        item = self.todos.pop(item_num - 1)
        item.completed = True
        self.completed.insert(0, item)

    def uncomplete(self, item_num):
        item = self.completed.pop(item_num - 1)
        item.completed = False
        self.todos.insert(0, item)

    def add(self, text, priority=1):
        item = Todo.create(text)
        self.todos.insert(priority - 1, item)

    def render(self):
        output = ["-" * 44]
        for idx, todo in enumerate(self.todos):
            output.append("{0}: {1}".format(idx + 1, todo.todo_text))
        output.append("=" * 20 + "done" + "=" * 20)
        for idx, todo in enumerate(self.completed):
            output.append(todo.todo_text)
        return "\n".join(output) + "\n"

    def save(self):
        with open(TODO_FILE, 'w') as todo_file:
            # todo_file = sys.stdout
            for todo in self.todos:
                todo_file.write("{}\n".format(todo))
            for todo in self.completed:
                todo_file.write("{}\n".format(todo))


if __name__ == "__main__":
    tdl = TodoList()
    for todo in tdl.todos:
        print(todo)
    for todo in tdl.completed:
        print(todo)