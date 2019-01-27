#!/usr/bin/python -u
import argparse
import sys

from todo_list import TodoList


def render_todos():
    todo_list = TodoList()
    print(todo_list.render())


def add_todo(options):
    todo_list = TodoList()
    todo_list.add(options.text)
    print(todo_list.render())
    todo_list.save()


def bump_todo(options):
    todo_list = TodoList()
    todo_list.bump(options.item)
    print(todo_list.render())
    todo_list.save()


def complete_todo(options):
    todo_list = TodoList()
    todo_list.complete(options.item)
    print(todo_list.render())
    todo_list.save()


def uncomplete_todo(options):
    todo_list = TodoList()
    todo_list.uncomplete(options.item)
    print(todo_list.render())
    todo_list.save()


def run():
    '''Run the appropriate todo command

    usage: [-h] {bump,add,complete,uncomplete}
    '''
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help',
                                       dest="subcommand")
    subparsers.required = True
    parser_add = subparsers.add_parser('add', help='add help')
    parser_add.set_defaults(run=add_todo)
    parser_add.add_argument('--priority', type=int)
    parser_add.add_argument('text')

    parser_bump = subparsers.add_parser('bump', help='bump help')
    parser_bump.set_defaults(run=bump_todo)
    parser_bump.add_argument('item', type=int)

    parser_complete = subparsers.add_parser('complete', help='complete help')
    parser_complete.set_defaults(run=complete_todo)
    parser_complete.add_argument('item', type=int)

    parser_uncomplete = subparsers.add_parser('uncomplete', help='uncomplete help')
    parser_uncomplete.set_defaults(run=uncomplete_todo)
    parser_uncomplete.add_argument('item', type=int)

    if len(sys.argv) == 1:
        render_todos()
        sys.exit(0)

    options = parser.parse_args()
    options.run(options)

if __name__ == "__main__":
    run()
