# -*- coding: UTF-8 -*-

from mongoengine import connect
from mongoengine import DynamicDocument
from pymongo import UpdateOne
import collections

from server3.repository import config
import json

connect(
    db=config.get_mongo_db(),
    username=config.get_mongo_user(),
    password=config.get_mongo_pass(),
    host=config.get_mongo_host(),
    port=config.get_mongo_port(),
)


class GeneralDynamicDocument(DynamicDocument):

    @classmethod
    def read(cls, query):
        return cls.objects(**query).order_by('-_id')


Objects = collections.namedtuple('Objects', ('objects', 'count', 'page_no', 'page_size'))
FavorAppReturn = collections.namedtuple('FavorAppReturn', ('user', 'app'))

UserEntity = collections.namedtuple('UserEntity', ('user', 'entity'))