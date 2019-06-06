#!/usr/bin/python
# -*- coding: UTF-8 -*-
from server3.lib import modules
from importlib import import_module


def module_general(module_id, action, *args, **kwargs):
    [user_ID, module_name] = module_id.split('/')
    main = import_module(
        'lib.modules.{user_ID}.{module_name}.main'.format(
            user_ID=user_ID, module_name=module_name))
    getattr(main, action)(*args, **kwargs)


def module_run(module_id, *args, **kwargs):
    module_general(module_id, 'run', *args, **kwargs)


def module_train(module_id, *args, **kwargs):
    module_general(module_id, 'train', *args, **kwargs)


def module_predict(module_id, *args, **kwargs):
    module_general(module_id, 'predict', *args, **kwargs)


class Module:
    def __init__(self, module_id):
        [user_ID, module_name] = module_id.split('/')
        self.main = import_module('server3.lib.modules.{}.{}.main'.format(
            user_ID, module_name))

    def run(self, *args, **kwargs):
        return self.main.run(*args, **kwargs)


if __name__ == '__main__':
    pass
