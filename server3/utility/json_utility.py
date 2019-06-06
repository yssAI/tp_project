# encoding: utf-8
"""
utility used in all project

Author: BingWei Chen
Date: 2017.05.17
"""
import json
import pandas as pd
import simplejson
from operator import attrgetter
import numpy as np

from mongoengine import Document
from mongoengine import DoesNotExist
from bson import ObjectId
from datetime import datetime


class JSONEncoder(simplejson.JSONEncoder):
    # def default(self, o):
    #     if isinstance(o, ObjectId):
    #         return str(o)
    #     elif isinstance(o, datetime):
    #         return str(o)
    #     elif isinstance(o, np.integer):
    #         return int(o)
    #     elif isinstance(o, np.floating):
    #         return float(o)
    #     elif isinstance(o, np.ndarray):
    #         return o.tolist()
    #     return self.default(self, o)

    # arbitrary iterators
    def default(self, o):
        try:
            iterable = iter(o)
        except TypeError:
            if isinstance(o, ObjectId):
                return str(o)
            elif isinstance(o, datetime):
                return str(o)
            elif isinstance(o, np.ndarray):
                return o.tolist()
            elif isinstance(o, np.generic):
                return np.asscalar(o)
        else:
            return list(iterable)
        print(o)
        # Let the base class default method raise the TypeError
        return JSONEncoder.default(self, o)


def json_load(json_string):
    json_obj = json.loads(json_string)
    return json_obj


# convert bson to json
# 将ObjectId去除，用于Restful API传递
def convert_to_json(bson_obj):
    json_obj = JSONEncoder(ignore_nan=True).encode(bson_obj)
    # new_json_obj = json_load(new_json_obj)
    # new_json_obj = simplejson.dumps(new_json_obj, ignore_nan=True)
    new_json_obj = simplejson.loads(json_obj)
    return new_json_obj


# # 获取ObjectId的实例内容
# def get_object(collection, object_id):
#     return mongo_manager.find_one(collection, {"_id": object_id})


# 将string转成datetime
def convert_string_to_date(timestamp):
    if isinstance(timestamp, datetime):
        return timestamp
    timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    return timestamp


# 将json转化成DataFrame格式
def convert_json_str_to_dataframe(arr):
    """
    convert input data:
    from
        data from staging data => database_type like, which is a list of dicts
    to
        DataFrame in pandas
    """
    col = list(arr[0].keys())
    df_converted = pd.DataFrame([[i[j] for j in col] for i in arr],
                                columns=col)
    return df_converted


def me_obj_list_dict_to_json_list_dict(me_obj_list_dict):
    """
    :param me_obj_list_dict: dict
    :return:
    """
    print('me_obj_list_dict', me_obj_list_dict)
    return {str(key): convert_to_json(me_obj_list_to_json_list(me_obj))
            for key, me_obj in me_obj_list_dict.items() if me_obj}


def me_obj_list_to_json_list(me_obj_list):
    """
    mongoengine object list to json list
    :param me_obj_list: list
    :return:
    """
    return [convert_to_json(me_obj.to_mongo()) for me_obj in
            me_obj_list]


def me_obj_list_to_dict_list(me_obj_list):
    """
    mongoengine object list to dict list
    :param me_obj_list: list
    :return:
    """
    return [me_obj.to_mongo().to_dict() for me_obj in me_obj_list]


def get_args(args):
    return {'args':
                {arg.get('name'): arg.get('value')
                                  or arg.get('values')
                                  or arg.get('default')
                 for arg in args}
            }


def args_converter(args):
    return {key: {'key': key, **arg}
            for key, arg in args.items()}


def objs_to_json_with_arg(objects, arg):
    return [{
        **convert_to_json(me_obj.to_mongo()),
        f'{arg}_obj': convert_to_json(me_obj[arg].to_mongo())} for me_obj in
        objects]


def objs_to_json_with_args(objects, args):
    return_objects = []
    for object in objects:
        new_object = convert_to_json(object.to_mongo())
        for arg in args:
            try:
                attr = attrgetter(arg)(object)
            except AttributeError:
                pass
            else:
                if isinstance(attr, Document):
                    new_object[arg] = \
                        convert_to_json(attr.to_mongo())
                else:
                    new_object[arg] = convert_to_json(attr)
        return_objects.append(new_object)
    return return_objects

    # return [
    #     {
    #     **convert_to_json(me_obj.to_mongo()),
    #
    #     **[{f'{arg}_obj': convert_to_json(me_obj[arg].to_mongo())} for arg in args]
    # } for me_obj in objects]


def convert_action_entity(objects, action_entity):
    if action_entity == 'used_modules':
        ums = []
        for m in objects:
            try:
                ums.append({'module': convert_to_json(m.module.to_mongo()),
                            'version': '.'.join(m.version.split('_'))})
            except DoesNotExist:
                pass
        return ums
    if action_entity == 'used_datasets':
        uds = []
        for m in objects:
            try:
                uds.append({'dataset': convert_to_json(m.dataset.to_mongo()),
                            'version': '.'.join(m.version.split('_'))})
            except DoesNotExist:
                pass
        return uds


def convert_used_modules(app):
    ums = []
    for m in app.used_modules:
        try:
            ums.append({'module': convert_to_json(m.module.to_mongo()),
                        'version': '.'.join(m.version.split('_'))})
        except DoesNotExist:
            pass
    del app.used_modules
    app = convert_to_json(app.to_mongo())
    app['used_modules'] = ums
    return app


def convert_used_datasets(app):
    uds = []
    for m in app.used_datasets:
        try:
            uds.append({'dataset': convert_to_json(m.dataset.to_mongo()),
                        'version': '.'.join(m.version.split('_'))})
        except DoesNotExist:
            pass
    del app.used_datasets
    app = convert_to_json(app.to_mongo())
    app['used_datasets'] = uds
    return app


def parse_select_project(object_info, object):
    if 'select_project' in object_info:
        # 获取commit
        try:
            # commits = ProjectBusiness.get_commits(
            #     request_answer[index].select_project.path)
            select_project = object['select_project']
            if isinstance(select_project, str) or isinstance(select_project,
                                                             ObjectId):
                from server3.business.project_business import ProjectBusiness
                select_project = ProjectBusiness.get_by_id(select_project)
            # select_project.commits = [{
            #     'message': c.message,
            #     'time': datetime.fromtimestamp(c.time[0] + c.time[1]),
            # } for c in commits]
            object_info['select_project'] = convert_to_json(
                select_project.to_mongo())
            object_info['select_project']['commits'].reverse()
            object_info['select_project'][
                'username'] = select_project.user.username
            object_info['select_project'][
                'user_ID'] = select_project.user.user_ID
            object_info['select_project'][
                'avatar_url'] = select_project.user.avatar_url
        except Exception as e:
            object_info['select_project'] = {'deleted': True}
