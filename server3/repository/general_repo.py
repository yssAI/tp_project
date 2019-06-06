# -*- coding: UTF-8 -*-
from mongoengine import Q
from mongoengine import connect
from pymongo import UpdateOne
from pymongo import ReadPreference

from server3.repository import config
import json

connect(
    db=config.get_mongo_db(),
    username=config.get_mongo_user(),
    password=config.get_mongo_pass(),
    host=config.get_mongo_host(),
    port=config.get_mongo_port(),
    read_preference=ReadPreference.SECONDARY_PREFERRED
)


class Repo:
    def __init__(self, instance):
        self.__instance = instance

    def create(self, obj):
        return obj.save()

    def create_many(self, objects):
        return self.__instance.objects.insert(objects, load_bulk=False)

    def create_one(self, **content):
        return self.__instance(**content).save()

    def read(self, query=None):
        if query is None:
            query = {}
        return self.__instance.objects(**query).order_by('-_id')

    def filter(self, **query):
        return self.__instance.objects(**query).order_by('-_id')

    def objects(self, **kwargs):
        return self.__instance.objects(**kwargs).order_by('-_id')

    def read_skipping_order(self, query, skipping):
        return self.__instance.objects(**query).order_by('-_id')[
               int(skipping):int(skipping) + 10]

    def read_first_one(self, query):
        return self.__instance.objects(**query).first()

    def read_last(self, **query):
        return self.__instance.objects(**query).order_by('-_id')

    def read_last_limit(self, limit, **query):
        return self.__instance.objects(**query).order_by('-_id').limit(limit)

    def read_unique_one(self, query):
        return self.__instance.objects.get(**query)

    def read_by_unique_field(self, field_name, field_value):
        """
        general function to query the db by unique field
        :param field_name:
        :param field_value:
        :return: return the unique object corresponding to the query
        """
        return Repo.read_unique_one(self, {field_name: field_value})

    def read_by_two_field(self, field_name, field_value, field_name_2,
                          field_value_2):
        """
        general function to query the db by unique field
        :param field_name:
        :param field_value:
        :return: return the unique object corresponding to the query
        """
        return Repo.read_unique_one(self, {field_name: field_value,
                                           field_name_2: field_value_2})

    def read_by_non_unique_field(self, field_name, field_value):
        """
        general function to query the db by non unique field, thus return a list
        :param field_name:str
        :param field_value:
        :return: a list of objects corresponding to the query
        """
        return Repo.read(self, {field_name: field_value})

    def read_by_non_unique_field_subset(self, field_name,
                                        field_value, subset):
        """
        general function to query the db by non unique field, thus return a list
        :param field_name:str
        :param field_value:
        :return: a list of objects corresponding to the query
        """
        return Repo.read(self, {field_name: field_value}).only(*subset)

    def read_by_non_unique_field_limit(self, field_name, field_value, limit):
        """
        general function to query the db by non unique field, thus return a list
        :param field_name:str
        :param field_value:
        :param limit: int
        :return: a list of objects corresponding to the query
        """
        return Repo.read(self, {field_name: field_value}).limit(limit)

    def read_by_id(self, object_id):
        return self.__instance.objects.get(id=object_id)

    def update(self, query, update):
        return self.__instance.objects(**query).update(**update)

    # def update_one(self, query, update):
    #     modified_obj = self.__instance.objects(**query).modify(**update)
    #     return modified_obj.reload()

    def update_one_by_id(self, obj_id, update):
        update.pop('id', None)
        update.pop('type', None)
        update.pop('size', None)
        modified_obj = self.__instance.objects.get(id=obj_id)
        modified_obj.modify(**update)
        return modified_obj.reload()

    def update_unique_one(self, query, update):
        modified_obj = self.__instance.objects.get(**query)
        modified_obj.modify(**update)
        return modified_obj.reload()

    def update_unset_fields_by_non_unique_field(self, field_name, field_value,
                                                fields):
        update = {'unset__' + k: '' for k in fields}
        return self.__instance.objects(**{field_name: field_value}) \
            .update(**update)

    # for List field add only one new element- update={'job': new_job_obj,
    #                                                  'result': new_result_obj}
    def insert_to_list_fields_by_id(self, obj_id, update):
        """
        insert item to list fields of document with given object id
        :param obj_id: ObjectId
        :param update: dict
        :return: modified_obj
        """
        # print '2*', type(obj), obj
        # print '3*', update
        update = {'push__' + k: v for k, v in list(update.items())}
        # for key in update.keys():
        #     update['push__'+key] = update.pop(key)
        # print 'update', update
        modified_obj = self.__instance.objects(id=obj_id).modify(**update)
        return modified_obj.reload()

    def add_to_set(self, obj_id, **update):
        """
        insert items to list fields of document with given object id
        :param obj_id:
        :param update:
        :return:
        """
        update = {'add_to_set__' + k: v for k, v in list(update.items())}
        modified_obj = self.__instance.objects(id=obj_id).modify(**update)
        return modified_obj.reload()

    def pull_from_set(self, obj_id, **update):
        """
        remove item from list fields of document with given object id
        :param obj_id:
        :param update:
        :return:
        """
        update = {'pull__' + k: v for k, v in list(update.items())}
        modified_obj = self.__instance.objects(id=obj_id).modify(**update)
        return modified_obj.reload()

    def delete(self, obj):
        return obj.delete()

    def delete_many(self, query):
        return self.__instance.objects(**query).delete()

    def delete_first_one(self, query):
        return self.__instance.objects(**query).first().delete()

    def delete_unique_one(self, query):
        return self.__instance.objects.get(**query).delete()

    def delete_by_id(self, object_id):
        return self.__instance.objects.get(id=object_id).delete()

    def delete_by_non_unique_field(self, field_name, field_value):
        """
        general function to query the db by non unique field, thus return a list
        :param field_name: str
        :param field_value:
        :return: a list of objects corresponding to the query
        """
        return Repo.delete_many(self, {field_name: field_value})

    def update_many(self, list_dicts):
        """
        update many columns into database
        :param list_dicts: update values
        :return: None
        """
        # 组合时候添加一笔资料
        update_list_dicts = [
            UpdateOne({'_id': item.pop('_id')}, {'$set': item}) for item in
            list_dicts]
        self.__instance._get_collection().bulk_write(update_list_dicts,
                                                     ordered=False)

    def search(self, search_query, q_dict):
        # Turn list of values into list of Q objects
        q_list = [Q(**{field + '__' + q: search_query})
                  for field, q in list(q_dict.items())]
        # Take one Q object from the list
        query = q_list.pop()

        # Or the Q object with the ones remaining in the list
        for item in q_list:
            query |= item
        return self.__instance.objects(query).order_by('-_id')

    # delete fields
    def update_by_or_filters(self, filters, update):
        # Turn list of values into list of Q objects
        q_list = [Q(**f) for f in filters]
        # Take one Q object from the list
        query = q_list.pop()

        # Or the Q object with the ones remaining in the list
        for item in q_list:
            query |= item
        return self.__instance.objects(query).update(**update)

    def or_filter(self, filters):
        if not filters:
            return self.__instance.objects()
        # Turn list of values into list of Q objects
        q_list = [Q(**f) for f in filters]
        # Take one Q object from the list
        query = q_list.pop()

        # Or the Q object with the ones remaining in the list
        for item in q_list:
            query |= item
        return self.__instance.objects(query)
