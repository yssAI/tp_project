from flask_restplus import Argument
from flask_restplus import RequestParser


class Args:
    page_size = {'name': 'page_size', ...}
    page_no = {'name': 'page_no', ...}
    query = {'name': 'query', ...}
    type = {'name': 'type', ...}
    anything = {'name': 'anything', ...}


def add_args(parser, *args):
    for arg in args:
        parser.add_argument(arg)


general_args = Args()

project_list_args = RequestParser()
add_args(project_list_args, [
    Argument(**{**general_args.query, **{'help': 'nihao'}}),
    Argument(**general_args.type),
    Argument(**{**general_args.page_size, **{'default': 123}})
])
