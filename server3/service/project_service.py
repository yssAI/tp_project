# -*- coding: UTF-8 -*-
import os
import base64
import tempfile
import re
import random
import string
from io import BytesIO
from PIL import Image
from mongoengine import DoesNotExist
import logging
import copy
from flask_jwt_extended import get_jwt_identity
from server3.business.project_business import ProjectBusiness
from server3.business.app_business import AppBusiness
from server3.business.module_business import ModuleBusiness
from server3.business.data_set_business import DatasetBusiness
from server3.business.user_business import UserBusiness
from server3.business.event_business import EventBusiness
from server3.business.kube_business import KubePod
from server3.business.request_answer_business import RequestAnswerBusiness
from server3.business.oss_business import upload_file
from server3.service.message_service import MessageService
from server3.entity.world import CHANNEL
from server3.entity.tag import Tag
from server3.business.rocket_chat_business import RocketChatBusiness
from server3.business.level_task_business import LevelTaskBusiness
from server3.service.general_service import GeneralService
from server3.repository import config
from server3.constants import ENV, WEB_ADDR
from server3.utility.str_utility import secure_name
from server3.utility.str_utility import gen_rand_name
from server3.utility.str_utility import gen_rand_str
from server3.constants import PROJECT_IMG_DIR
from server3.constants import DEFAULT_DEPLOY_VERSION
from server3.constants import OVERVIEW_FILE_NAME
from server3.constants import JL_CPU_LIMIT
from server3.constants import JL_MEM_LIMIT
from server3.constants import UPLOADED_IMG_BASE
from server3.constants import Tutorials
from server3.business.rocket_chat_business import RocketChatBusiness
from server3.constants import WEB_ADDR
from server3.service.search_service import SearchService
from server3.constants import Official_User_ID
from server3.constants import TemplateClassroomDescription, \
    TemplateClassroomTitles
from server3.constants import TemplateTutorialDescription, \
    TemplateTutorialTitles
from server3.constants import TagsMapping
from server3.constants import TemplateTutorialDocTitles
from mongoengine import DoesNotExist
import time

UPLOAD_FOLDER = config.get_file_prop('UPLOAD_FOLDER')

TUTORIAL_PATH = './tutorial/'


class TypeMapper:
    project = ProjectBusiness
    app = AppBusiness
    module = ModuleBusiness
    dataset = DatasetBusiness

    @classmethod
    def get(cls, attr='project'):
        return getattr(cls, attr)


# def list_projects(search_query=None, page_no=1, page_size=10,
#                   default_max_score=0.4, privacy=None, type='project',
#                   user_ID=None, tags=None, status=None):
#     user = None
#     if user_ID:
#         user = UserBusiness.get_by_user_ID(user_ID)
#     cls = TypeMapper.get(type)
#     return cls.get_objects(
#         search_query=search_query,
#         privacy=privacy,
#         page_no=page_no,
#         page_size=page_size,
#         default_max_score=default_max_score,
#         user=user,
#         tags=tags,
#         status=status,
#     )


# def add_job_and_result_to_project(result_obj, project_id):
#     """
#     add job and result to project
#     :param result_obj:
#     :param project_id:
#     :return:
#     """
#     job_obj = job_service.get_job_from_result(result_obj)
#     return project_business.add_and_update_one_by_id(project_id, result_obj,
#                                                      job_obj)


# def get_all_jobs_of_project(project_id, categories, status=None):
#     """
#     get all jobs and job info of a project
#     :param project_id:
#     :param categories:
#     :param status:
#     :return:
#     """
#     from server3.business import job_business
#
#     # jobs = project_business.get_by_id(project_id)['jobs']
#
#     jobs = job_business.get_by_project(project_id).order_by('-create_time')
#
#     history_jobs = {c: [] for c in categories}
#     for job in jobs:
#         # keys = history_jobs.keys()
#         for key in categories:
#             if status is None:
#                 check = job[key]
#             else:
#                 check = job[key] and (job['status'] == status)
#             if check:
#                 job_info = job.to_mongo()
#                 # model/toolkit info
#                 # job_info[key] = {
#                 #     'item_id': job[key]['id'],
#                 #     'name': job[key]['name'],
#                 #     'category': job[key]['category'],
#                 #     'parameter_spec': job[key]['parameter_spec'],
#                 #     'steps': job[key]['steps']
#                 # }
#                 job_info[key] = job[key].to_mongo()
#
#                 # source staging data set info
#                 job_info['staging_data_set'] = job['staging_data_set'][
#                     'name'] if job['staging_data_set'] else None
#                 job_info['staging_data_set_id'] = job['staging_data_set'][
#                     'id'] if job['staging_data_set'] else None
#
#                 # result sds info
#                 # object 用的是 .id  json用 _id
#                 if key == 'model':
#                     try:
#                         result_sds = staging_data_set_business.get_by_job_id(
#                             job['id']).to_mongo()
#                         if result_sds:
#                             # model results
#                             job_info['results'] = result_sds
#                             metrics_status = [sd.to_mongo() for sd in
#                                               staging_data_business.get_by_staging_data_set_id(
#                                                   result_sds['_id']).order_by(
#                                                   'n')]
#                             # metrics_status.sort(key=lambda x: x['n'])
#                             job_info['metrics_status'] = metrics_status
#                             if len(metrics_status) > 0:
#                                 total_steps = get_total_steps(job)
#                                 job_info['percent'] = \
#                                     metrics_status[-1]['n'] / total_steps * 100
#                             if job_info['status'] == 200:
#                                 job_info['percent'] = 100
#                             job_info['results_staging_data_set_id'] = \
#                                 result_sds[
#                                     '_id'] if result_sds else None
#                     except DoesNotExist:
#                         result_sds = None
#                 if job['status'] == 200 and key == 'model':
#                     temp_data_fields = job_info['params']['fit']['data_fields']
#                     if not isinstance(temp_data_fields[0], list):
#                         job_info['params']['fit']['data_fields'] = [
#                             temp_data_fields]
#                     print(job_info['params']['fit']['data_fields'][0])
#                 # model running status info
#                 # if key == 'model':
#                 #     job_name = KUBE_NAME['model'].format(job_id=job['id'])
#                 #     job_info = kube_service.get_job_status(job_info, job_name)
#
#                 # 获取 served_model 数据库中的信息
#                 served_model_id = job_info.get('served_model')
#                 if served_model_id:
#                     served_model = served_model_business.get_by_id(
#                         served_model_id)
#                     # 获取 kube 中部署模型的状态
#                     served_model = kube_service.get_deployment_status(
#                         served_model)
#                     served_model = served_model.to_mongo()
#
#                     # 获取训练 served_model 时所用的数据的第一条
#                     staging_data_demo = staging_data_service.get_first_one_by_staging_data_set_id(
#                         job_info['staging_data_set_id'])
#                     one_input_data_demo = []
#                     for each_feture in \
#                             job_info['params']['fit']['data_fields'][0]:
#                         one_input_data_demo.append(
#                             staging_data_demo[each_feture])
#                     input_data_demo_string = '[' + ",".join(
#                         str(x) for x in one_input_data_demo) + ']'
#                     input_data_demo_string = '[' + input_data_demo_string + ',' + input_data_demo_string + ']'
#                     print(input_data_demo_string)
#                     # 生成use代码
#                     job_info["served_model"] = served_model
#                     job_info["served_model"][
#                         "input_data_demo_string"] = input_data_demo_string
#                     job_info = build_how_to_use_code(job_info)
#                 else:
#                     served_model = None
#                     job_info["served_model"] = served_model
#                 history_jobs[key].append(job_info)
#                 break
#     return history_jobs


# def get_total_steps(job):
#     try:
#         total_steps = \
#             job['run_args']['conf']['fit']['args'][
#                 'steps']
#     except KeyError:
#         total_steps = None
#     if not total_steps:
#         try:
#             total_steps = \
#                 job['run_args']['conf']['fit'][
#                     'args'][
#                     'epochs']
#         except KeyError:
#             total_steps = 1
#     return total_steps


# def build_how_to_use_code(job_info):
#     served_model_id = str(job_info['served_model']['_id'])
#     server = str(job_info['served_model']['server'])
#     served_model_name = job_info['served_model']['model_name']
#     features = job_info['params']['fit']['data_fields'][0]
#     features_str = '[' + ",".join(
#         ('\'' + str(x) + '\'') for x in features) + ']'
#
#     str_js = "let url = 'http://localhost:5000/served_model/predict/" + \
#              served_model_id + "';\n"
#     str_js += "let data = {\n"
#     str_js += "  input_value: "
#     str_js += job_info["served_model"]["input_data_demo_string"] + ",\n"
#     str_js += "  served_model_id:\"" + served_model_id + "\",\n"
#     str_js += "  server:\"" + server + "\",\n"
#     str_js += "  model_name: \"" + served_model_name + "\",\n"
#     str_js += "  features: " + features_str + ",\n"
#     str_js += "};\n"
#     str_js += "fetch(url, {\n"
#     str_js += "  method: \"POST\",\n"
#     str_js += "  body: JSON.stringify(data),\n"
#     str_js += "  headers: {\n"
#     str_js += "     \"Content-Type\": \"application/json\",\n"
#     str_js += "  },\n"
#     str_js += "}).then(function (response) {\n"
#     str_js += "  return response.json();\n"
#     str_js += "}).then(function (responseData) {\n"
#     str_js += "  console.log(responseData);\n"
#     str_js += "}).catch(function () {\n"
#     str_js += "  console.log('error');\n"
#     str_js += "});"
#
#     str_py = "import requests\n"
#     str_py += "import json\n"
#     str_py += "data = { \n"
#     str_py += "  \"server\":\"" + server + "\",\n"
#     str_py += "  \"input_value\": " + job_info["served_model"][
#         "input_data_demo_string"] + ",\n"
#     str_py += "  \"served_model_id\":\"" + served_model_id + "\",\n"
#     str_py += "  \"model_name\":\"" + served_model_name + "\",\n"
#     str_py += "  \"features\":" + features_str + ",\n"
#     str_py += " }\n"
#     str_py += "r = requests.post(\"http://localhost:5000/served_model/predict/" + \
#               served_model_id + "\",json=data) \n"
#     str_py += "result = r.json()['response']['result']\n"
#     str_py += "print(result)\n"
#     job_info['how_to_use_code'] = {}
#     job_info['how_to_use_code']['js'] = str_js
#     job_info['how_to_use_code']['py'] = str_py
#     return job_info


# def publish_project(project_id):
#     project = project_business.get_by_id(project_id)
#     ow = ownership_business.get_ownership_by_owned_item(project, 'project')
#     return ownership_business.update_by_id(ow['id'], private=False)


# def unpublish_project(project_id):
#     project = project_business.get_by_id(project_id)
#     ow = ownership_business.get_ownership_by_owned_item(project, 'project')
#     return ownership_business.update_by_id(ow['id'], private=True)


class ProjectService(GeneralService):
    business = ProjectBusiness
    channel = CHANNEL.project
    name = 'project'

    @classmethod
    def mount_all_dataset(cls, user_ID, project):
        user = UserBusiness.get_by_user_ID(user_ID)
        for used_dataset in project.used_datasets:
            ProjectBusiness.insert_dataset(project, used_dataset.dataset)

    @classmethod
    def create_tutorial_project(cls, user_ID, user_token, num=None,
                                level=None, lt_id=None, **kwargs):
        """
        Create a tutorial project

        :param user_ID:
        :param user_token:
        :param num:
        :param level:
        :param lt_id:
        :param kwargs:
        :return: a new created project object
        """

        # display_name = 'Novice Tutorial'
        # description = 'This is a official tutorial for our platform beginner'
        # type = 'app'
        # path = 'tutorial'
        # # auto_show_help = True
        # tags = ['tutorial', 'official']

        # 修改
        display_name = '古诗词生成器'
        description = '利用 LSTM 神经网络，输入提供的词语，可以输出对应的藏头诗或藏字诗。每次提交生成的结果都不一样，你可以从中选择一个最好的，赶快来体验吧～'
        type = 'app'
        path = 'tutorial'
        # auto_show_help = True
        tags = ['循环神经网络', '序列到序列模型', 'tutorial', 'official']

        # ltask = None
        # if lt_id:
        #     ltask = LevelTaskBusiness.get_task(id_=lt_id)
        # elif num or level:
        #     user = UserBusiness.get_by_user_ID(user_ID)
        #     ltask = LevelTaskBusiness.get_task(user=user, num=num, level=level)
        #

        # if ltask is not None:
        #     display_name = ltask.name
        #     description = ltask.description
        #     type = ltask.project_type
        #     path = ltask.path
        #     auto_show_help = False
        #     if ltask.level == 1 and ltask.num == 1:
        #         auto_show_help = True
        #     elif (ltask.level == 1 and ltask.num == 2) or \
        #             (ltask.level == 1 and ltask.num == 3):
        #         kwargs['category'] = 'toolkit'

        project = cls.create_project(
            # name=name,
            display_name=display_name,
            description=description, user_ID=user_ID,
            type=type, tags=tags,
            user_token=user_token,
            tutorial_path=path,
            auto_show_help=False,
            **kwargs)
        # if ltask is not None:
        #     ltask[type] = project
        #     ltask.save()
        return project

    @classmethod
    def create_project(cls, display_name, description, user_ID,
                       tags=None,
                       user_token=None, type='project', is_course=False,
                       course_ID=None, unit_ID=None, course_type=None,
                       **kwargs):
        """
        Create a new project

        :param name: str
        :param description: str
        :param user_ID: ObjectId
        :param type: string (app/module/dataset)
        :param tags: list of string
        :param user_token: string
        :return: a new created project object
        """
        if tags is None:
            tags = []
        if user_token is None:
            raise Exception('user token is required')
        project_type = type
        user = UserBusiness.get_by_user_ID(user_ID)
        # message = "{}创建了app{}".format(user.name, name)
        # world_business.system_send(channel=cls.channel, message=message)
        name = cls.gen_name(display_name, user_ID, type)
        project = cls.business.create_project(name=name,
                                              display_name=display_name,
                                              description=description,
                                              type=type, tags=[], user=user,
                                              user_token=user_token,
                                              is_course=is_course,
                                              course_ID=course_ID,
                                              unit_ID=unit_ID,
                                              course_type=course_type,
                                              **kwargs)

        # update tags
        cls.update_tags(oldtags=[], newtags=tags,
                        entity_type=project.type, entities=[project])
        EventBusiness.create_event(
            user=user,
            target=project,
            target_type=type,
            action="create"
        )

        # from server3.service.user_service import UserService
        # user, project = UserService.action_entity(user_ID=project.user.user_ID,
        #                                           entity_id=project.id,
        #                                           action='favor',
        #                                           entity=project.type)

        from server3.service.world_service import WorldService
        from server3.business.statistics_business import StatisticsBusiness
        # 记录历史记录
        # statistics = StatisticsBusiness.action(
        #     user_obj=user,
        #     entity_obj=project,
        #     entity_type=type,
        #     action="create"
        # )
        # 记录世界频道消息  # 推送消息
        # world = WorldService.system_send(
        #     channel=CHANNEL.request,
        #     message=f"用户{project.user.user_ID}创建了{project_type}: {project.name}")

        # admin_user = UserBusiness.get_by_user_ID('admin')
        #
        # text = f"<http://localhost:8899/explore/{project.id}?type={project_type}|" \
        #        f"用户 {project.user.user_ID} 创建了 {project_type}: {project.name}>"
        #
        # SlackBusiness.send_message(user=admin_user, text=text, channel='general')
        if project.privacy == 'public':
            try:
                text = f"[{project.user.username}]({WEB_ADDR}/profile/{project.user.user_ID})" \
                       f" 创建了 {project.type} :[{project.display_name}]({WEB_ADDR}/explore/{project.id}?type={project.type})"
                RocketChatBusiness.post_official_message(text=text)
            except:
                print('rc error')
        project.username = project.user.username
        project.user_ID = project.user.user_ID
        return project

    @classmethod
    def create_project_with_no_info(cls, user_ID, project_type, datasetId=None,
                                    user_token=None, source_repo=None,
                                    rand_num_str=None,
                                    **kwargs):
        """

        :param user_ID: user
        :param project_type: app, module, dataset
        :param category:  model or toolkit
        :return:
        """
        if project_type == 'module':
            category = 'model'
        else:
            category = None
        display_name = kwargs.get('display_name', None)
        if display_name is None:
            current_time = time.time()
            user = UserBusiness.get_by_user_ID(user_ID)
            display_name = user.username + str(int(current_time))
        project = cls.create_project(display_name=display_name,
                                     user_ID=user_ID,
                                     description='', tags=None,
                                     datasetId=datasetId,
                                     user_token=user_token,
                                     category=category, type=project_type,
                                     source_repo=source_repo,
                                     rand_num_str=rand_num_str)
        return project

    @classmethod
    def create_course_template_project(cls, user_ID, display_name,
                                       project_type, category='model',
                                       course_ID=None, user_token=None,
                                       unit_ID=None, course_type=None,
                                       rand_num_str=None):
        project = cls.create_project(display_name=display_name,
                                     user_ID=user_ID,
                                     description='', tags=None, datasetId=None,
                                     user_token=user_token,
                                     category=category, type=project_type,
                                     source_repo=None, is_course=True,
                                     course_ID=course_ID,
                                     unit_ID=unit_ID, course_type=course_type,
                                     rand_num_str=rand_num_str)
        return project

    @classmethod
    def list_projects(cls, search_query=None, page_no=1, page_size=5,
                      default_max_score=0.4, privacy=None, user_ID=None,
                      tags=None, status=None, sort=None, query_user_ID=None,
                      has_version=False, category=None, with_dataset=None,
                      classification=None, group=None):
        """
        list projects
        :param search_query:
        :type search_query:
        :param page_no:
        :type page_no:
        :param page_size:
        :type page_size:
        :param default_max_score:
        :type default_max_score:
        :param privacy:
        :type privacy:
        :param user_ID:
        :type user_ID:
        :return:
        :rtype:
        """
        user = None
        if user_ID:
            user = UserBusiness.get_by_user_ID(user_ID)
        query_user = None
        if query_user_ID:
            query_user = UserBusiness.get_by_user_ID(query_user_ID)
        objects = cls.business.get_objects(
            search_query=search_query,
            privacy=privacy,
            page_no=page_no,
            page_size=page_size,
            default_max_score=default_max_score,
            user=user,
            tags=tags,
            status=status,
            sort=sort,
            query_user=query_user,
            has_version=has_version,
            category=category,
            with_dataset=with_dataset,
            classification=classification,
            group=group
        )
        if sort == 'hot':
            for each_object in objects.objects:
                # user = UserBusiness.get_by_id(each_object['user'])
                each_object['view_num'] = EventBusiness.get_number(
                    {each_object['type']: each_object['_id'],
                     'action': "view"})
                # each_object['app_number_limit'] = user.app_number_limit
                # each_object['module_number_limit'] = user.module_number_limit
                # each_object['dataset_number_limit'] = user.dataset_number_limit

        else:
            for each_object in objects.objects:
                each_object.view_num = EventBusiness.get_number(
                    {each_object.type: each_object, 'action': "view"})
                # each_object.app_number_limit = each_object.user.app_number_limit
                # each_object.module_number_limit = each_object.user.module_number_limit
                # each_object.dataset_number_limit = each_object.user.dataset_number_limit

        return objects

    @classmethod
    def get_latest_overview(cls, project):
        # get README.md
        try:
            version = None
            ov_path = cls.get_overview_or_yml_path(version, project)
            with open(os.path.join(ov_path, OVERVIEW_FILE_NAME), 'rb') as f:
                md = f.read().decode('utf-8')
                project.overview = md
        except NotADirectoryError:
            project.overview = ''
        except FileNotFoundError:
            project.overview = ''
        return project

    @classmethod
    def get_by_id(cls, project_id, **kwargs):
        project = cls.business.get_by_id(project_id)
        if 'user' in kwargs and kwargs['user']:
            # 获取当前用户
            user = kwargs['user']
            project.view_user_can_fork = not cls.check_user_limit(user,
                                                                  project.type)
        else:
            project.view_user_can_fork = True
        # 添加其他数据
        if project.source_project:
            project.source_project_user_ID = project.source_project.user.user_ID
            project.source_project_username = project.source_project.user.username
            project.source_project_name = project.source_project.name
        # get README.md
        try:
            version = kwargs.pop('version', None)
            ov_path = cls.get_overview_or_yml_path(version, project)
            with open(os.path.join(ov_path, OVERVIEW_FILE_NAME), 'rb') as f:
                md = f.read().decode('utf-8')
                project.overview = md
        except NotADirectoryError:
            project.overview = ''
        except FileNotFoundError:
            project.overview = ''
        return project

    @classmethod
    def get_by_identity(cls, user_ID, project_name):
        identity = '+'.join((user_ID, project_name))
        project = cls.business.get_by_identity(identity)
        return project

    @classmethod
    def get_by_display_name_and_user(cls, user_ID, display_name):
        user = UserBusiness.get_by_user_ID(user_ID)
        project = cls.business.repo.read_unique_one(
            dict(display_name=display_name, user=user))
        return project

    @classmethod
    def commit(cls, project_id, commit_msg, wait=False):
        project = cls.business.commit(project_id, commit_msg, wait=wait)
        # cls.send_message_favor(project, m_type='commit')
        return project

    @classmethod
    def send_message_favor(cls, project, m_type='deploy',
                           project_version='dev'):
        """
        send message to project favor user
        :param project:
        :param m_type:
        :return:
        """
        admin_user = UserBusiness.get_by_user_ID('admin')
        # 成功发布带版本号的 project，通知其他人，否则只通知自己
        if m_type == 'deploy' and project_version != 'dev':
            # 获取所有包含此project的答案
            answers_has_project = RequestAnswerBusiness. \
                get_by_anwser_project_id(project.id)
            for each_answer in answers_has_project:
                user_request = each_answer.user_request
                request_owner = user_request.user
                # send to request owner
                MessageService.create_message(admin_user, f'{m_type}_request',
                                              [request_owner],
                                              project.user,
                                              project=project,
                                              user_request=user_request,
                                              project_version=project_version,
                                              )

                # send to answer favor user
                MessageService.create_message(admin_user, f'{m_type}_request',
                                              each_answer.favor_users,
                                              project.user,
                                              project=project,
                                              user_request=user_request,
                                              project_version=project_version, )
            # send to project favor user
            receivers = project.favor_users
            MessageService.create_message(admin_user, m_type,
                                          receivers,
                                          project.user,
                                          project=project,
                                          project_version=project_version, )
        # send to project owner
        MessageService.create_message(admin_user, m_type,
                                      [project.user],
                                      project.user,
                                      project=project,
                                      project_version=project_version, )

        # # 根据答案获取对应的 request 的 owner
        # if not any(x in m_type for x in ['fail', 'error', 'job']):
        #     for each_answer in answers_has_project:
        #         user_request = each_answer.user_request
        #         request_owner = user_request.user
        #         # send to request owner
        #         MessageService.create_message(admin_user, f'{m_type}_request',
        #                                       [request_owner],
        #                                       project.user,
        #                                       project=project,
        #                                       user_request=user_request,
        #                                       **kwargs,)
        #
        #         # send to answer favor user
        #         MessageService.create_message(admin_user, f'{m_type}_request',
        #                                       each_answer.favor_users,
        #                                       project.user,
        #                                       project=project,
        #                                       user_request=user_request,
        #                                       **kwargs,)
        #
        #     # send to project favor user
        #     MessageService.create_message(admin_user, m_type,
        #                                   receivers,
        #                                   project.user,
        #                                   project=project,
        #                                   **kwargs,)
        #
        # # send to project owner
        # MessageService.create_message(admin_user, m_type,
        #                               [project.user],
        #                               project.user,
        #                               project=project,
        #                               **kwargs,)

    @staticmethod
    def send_msg_owner(project, m_type='run_error', **kwargs):
        """
        send message to project owner
        :param project:
        :param m_type:
        :return:
        """
        admin_user = UserBusiness.get_by_user_ID('admin')
        MessageService.create_message(admin_user, m_type, [project.user],
                                      project.user, project=project, **kwargs)

    @staticmethod
    def get_hot_tag(search_query, object_type, category, **kwargs):
        return TypeMapper.get(object_type).get_hot_tag(search_query,
                                                       object_type,
                                                       category=category,
                                                       **kwargs)

    @classmethod
    def fork(cls, project_id, new_display_name, new_user_ID,
             user_token='', type=None, classroom=False):
        """
        fork project

        :param project_id:
        :param new_name:
        :param new_user_ID:
        :param type:
        :param user_token:
        :return:
        """
        project = cls.business.get_by_id(project_id)

        new_user = UserBusiness.get_by_user_ID(new_user_ID)
        new_user.skip_novice()
        new_name = cls.gen_name(new_display_name, new_user_ID, type)
        # fork project
        # 是否超过了限制
        is_limit = cls.check_user_limit(new_user, project.type)
        if not is_limit:
            new_project = cls.business.fork(project, new_name,
                                            new_display_name,
                                            new_user,
                                            user_token, classroom=classroom)
            EventBusiness.create_event(
                user=new_user,
                target=project,
                target_type=project.type,
                action="fork"
            )

            # 发送给原项目的创建者
            admin_user = UserBusiness.get_by_user_ID('admin')
            MessageService.create_message(admin_user, 'fork',
                                          [project.user],
                                          new_project.user,
                                          project=project, )

            # from server3.service.user_service import UserService
            # new_user, new_project = UserService.action_entity(
            #     user_ID=new_project.user.user_ID,
            #     entity_id=new_project.id,
            #     action='favor',
            #     entity=new_project.type)
            from server3.service.world_service import WorldService
            from server3.business.statistics_business import StatisticsBusiness
            # 记录历史记录
            # statistics = StatisticsBusiness.action(
            #     user_obj=user,
            #     entity_obj=project,
            #     entity_type=type,
            #     action="create"
            # )
            # 记录世界频道消息  # 推送消息
            # world = WorldService.system_send(
            #     channel=CHANNEL.request,
            #     message=f"用户{project.user.user_ID}创建了{new_project.type}: {project.name}")

            # admin_user = UserBusiness.get_by_user_ID('admin')
            #
            # text = f"<http://localhost:8899/explore/{project.id}?type={new_project.type}|" \
            #        f"用户 {project.user.user_ID} 创建了 {new_project.type}: {project.name}>"
            #
            # SlackBusiness.send_message(user=admin_user, text=text, channel='general')
            if ENV in ['PROD', 'MO']:
                try:
                    text = f"[{new_project.user.username}]({WEB_ADDR}/profile/{new_project.user.user_ID})" \
                           f" fork了 [{project.user.username}]({WEB_ADDR}/profile/{project.user.user_ID}) 的 " \
                           f"{project.type}: [{project.display_name}]({WEB_ADDR}/explore/{project.id}?type={project.type})"
                    RocketChatBusiness.post_official_message(text=text)
                except:
                    print('local rc error')
            return new_project
        else:
            return False

    @classmethod
    def duplicate(cls, project_id,
                  new_display_name,
                  user_token='',
                  new_type=None):
        """
        duplicate project

        :param project_id:
        :param new_name:
        :param new_user_ID:
        :param type:
        :param user_token:
        :return:
        """
        # project = cls.business.get_by_id(project_id)

        # 先 commit
        project = cls.commit(project_id, 'duplicate', wait=True)

        user = project.user
        new_name = cls.gen_name(new_display_name, user.user_ID, new_type)
        # fork project
        # 是否超过了限制
        is_limit = cls.check_user_limit(user, new_type)
        if not is_limit:
            if new_type == 'app':
                new_project = AppBusiness.fork(project, new_name,
                                               new_display_name,
                                               user,
                                               user_token, new_type=new_type,
                                               duplicate=True)
            elif new_type == 'module':
                new_project = ModuleBusiness.fork(project, new_name,
                                                  new_display_name,
                                                  user,
                                                  user_token,
                                                  new_type=new_type,
                                                  duplicate=True)
            else:
                raise TypeError(f'Duplicate type error: {new_type}')
            EventBusiness.create_event(
                user=user,
                target=project,
                target_type=project.type,
                action="duplicate"
            )

            return new_project
        else:
            return False

    @classmethod
    def get_docker_stats(cls, project_id):
        project = cls.business.get_by_id(project_id)
        pod = project.pod
        cntr = pod.first_container
        stats = cntr.stats()
        # for s in stats:
        #     print(s)
        return stats

    @classmethod
    def get_pod_stats(cls, project_id):
        project = cls.business.get_by_id(project_id)
        pod = project.pod
        cpu = pod.usage.get('cpu') or '...'
        mem = pod.usage.get('memory') or '...'
        mem_limit = False
        if cpu != '...' and mem != '...':
            cpu = int(cpu.split('n')[0]) * 100 / (
                    JL_CPU_LIMIT * 1000 * 1000 * 1000)
            cpu = f'{cpu:.2f} %'
            if 'Ki' in mem:
                mem = int(mem.split('Ki')[0]) / 1024
                if mem > 3072:
                    mem_limit = True
                mem = f'{mem:.2f} MB / {JL_MEM_LIMIT} GB'
            elif 'Mi' in mem:
                mem = int(mem.split('Mi')[0])
                print('yss', mem)
                if mem > 3072:
                    mem_limit = True
                mem = f'{mem:.2f} MB / {JL_MEM_LIMIT} GB'
            else:
                mem = int(mem.split('Gi')[0])
                if mem > 3:
                    mem_limit = True
                mem = f'{mem:.2f} GB / {JL_MEM_LIMIT} GB'
        return {'cpu': cpu, 'memory': mem, 'mem_limit': mem_limit}

    @classmethod
    def update_project(cls, by, project_id, user_ID, **data):
        overview = data.pop('overview', None)
        tags = data.pop('tags', [])
        user = UserBusiness.get_by_user_ID(user_ID)
        if by == 'name':
            project = ProjectBusiness.update_project_by_identity(project_id,
                                                                 **data)
        else:
            project = ProjectBusiness.update_project(project_id, **data)

        oldtags = [tag.id for tag in project.tags]
        cls.update_tags(oldtags=oldtags, newtags=tags,
                        entity_type=project.type, entities=[project])
        # todo 更新到指定内容才去刷新Elasticsearch的数据
        if not project.classroom and len(
                tags) > 0 or 'description' in data or 'display_name' in data or 'img_v' in data or \
                'photo_url' in data or (
                'privacy' in data and data['privacy'] == 'public'):
            # 添加
            SearchService.add_project(project.id, project.display_name,
                                      project.description,
                                      [tag.id for tag in project.tags],
                                      project.type,
                                      project.img_v if project.img_v else '',
                                      project.photo_url if project.photo_url else '',
                                      project.user.username)
        if not project.classroom and 'privacy' in data and data[
            'privacy'] == 'private':
            print('隐藏删除操作')
            # 删除
            SearchService.delete_project(project_id)
            # SearchService.delete_project(project_id)

        # update overview
        if overview is not None:
            version = data.pop('version', None)
            ov_path = cls.get_overview_or_yml_path(version, project)
            # print('更新overview', overview, flush=True)
            # update README.md
            with open(os.path.join(ov_path, OVERVIEW_FILE_NAME), 'wb+') as f:
                f.write(overview.encode('utf-8'))

            if project.type != 'dataset':
                # commit README.md
                project = ProjectBusiness.commit(project,
                                                 'update overview',
                                                 None,
                                                 True)

        project.overview = overview

        project = cls.convert_version_format(project)

        EventBusiness.create_event(
            user=user,
            target=project,
            target_type=project.type,
            action="update",
        )
        return project

    @classmethod
    def convert_version_format(cls, project):
        # if project.type == 'app':
        #     # temp solution for app version
        #     project.versions = \
        #         ['-'.join(version.split('_')) for version in
        #          project.versions]
        #     project.save()

        split_char = '-' if project.type == 'app' else '_'
        project.versions = \
            ['.'.join(version.split(split_char)) for version in
             project.versions]
        for commit in project.commits:
            if commit.version:
                commit.version = '.'.join(commit.version.split(split_char))
        return project

    @classmethod
    def get_overview_or_yml_path(cls, version, project):
        ov_path = project.path
        version = cls.process_version(version, project)
        if version:
            if project.type == 'app':
                ov_path = '-'.join([project.app_path, version])
            if project.type == 'module':
                ov_path = os.path.join(project.module_path, version)
        return ov_path

    @classmethod
    def process_version(cls, version, project):
        if version is None:
            if len(project.versions) > 0:
                return project.versions[-1]
            elif project.has_dev:
                return DEFAULT_DEPLOY_VERSION
        return version

    #    @classmethod
    #    def remove_project_by_id(cls, project_id, user_ID):
    #        user = UserBusiness.get_by_user_ID(user_ID)
    #        project_type = cls.business.get_by_id(project_id).type
    #        project = cls.business.remove_project_by_id(project_id, user_ID)
    #        # todo 删除项目
    #        if not project.classroom:
    #            SearchService.delete_project(project_id)
    #
    #        EventBusiness.create_event(
    #            user=user,
    #            target_type=project_type,
    #            action="delete",
    #        )
    #        # 处理tags
    #        project.tags = cls.handle_tags(project.tags)
    #        return project
    @classmethod
    def remove_project_by_id(cls, project_id, user_ID):
        user = UserBusiness.get_by_user_ID(user_ID)
        project_type = cls.business.get_by_id(project_id).type
        project = cls.business.remove_project_by_id(project_id, user_ID)
        # todo 删除项目
        if project and not project.classroom:
            SearchService.delete_project(project_id)

        EventBusiness.create_event(user=user,
                                   target_type=project_type,
                                   action="delete")
        return project

    # @classmethod
    # def reset_project_by_id(cls, project_id, user_ID):
    #     user = UserBusiness.get_by_user_ID(user_ID)
    #     project_type = cls.business.get_by_id(project_id).type
    #     project = cls.business.reset_project_by_id(project_id, user_ID)
    #     return project

    @classmethod
    def add_used_dataset(cls, app_id, used_dataset, version=None):
        """
        add dataset to project
        :param app_id:
        :param used_dataset:
        :param version:
        :return:
        """
        used_dataset = DatasetBusiness.get_by_id(used_dataset)
        app = cls.business.get_by_id(app_id)
        return cls.business.insert_dataset(app, used_dataset, version)

    @classmethod
    def remove_used_dataset(cls, app_id, used_dataset, version):
        """
        remove dataset from project
        :param app_id:
        :param used_dataset:
        :return:
        """
        used_dataset = DatasetBusiness.get_by_id(used_dataset)
        return cls.business.remove_used_dataset(app_id, used_dataset, version)

    @classmethod
    def get_file_dir_size(cls, directory):
        # return 0
        size = 0
        import os
        if os.path.isdir(directory):
            for root, dirs, files in os.walk(directory):
                for f in files:
                    check_path = os.path.join(root, f)
                    if 'localenv' in check_path and 'site-packages' not in check_path:
                        continue
                    size += os.path.getsize(check_path)
        return size

    @classmethod
    def gen_name(cls, display_name, user_ID, type):
        user = UserBusiness.get_by_user_ID(user_ID)
        name = secure_name(display_name, type=type)
        return gen_rand_name(name,
                             cls.business.check_user_project_name_exists,
                             3, user=user)

    @classmethod
    def install_reset_req(cls, user_ID, app_name):
        """
        copy used modules and datasets to jl container when start
        :param user_ID:
        :param app_name:
        :return:
        """
        user = UserBusiness.get_by_user_ID(user_ID)
        project = cls.business.read_unique_one(name=app_name, user=user)
        cls.business.install_reset_req(project)

    @classmethod
    def update_project_img(cls, project_id, base64_str):
        base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
        byte_data = base64.b64decode(base64_data)
        img_data = BytesIO(byte_data)
        img = Image.open(img_data)
        img = img.convert('RGB')
        # save_path = PROJECT_IMG_DIR
        # image_path = save_path + f'/{project_id}.jpg'
        rand_str = gen_rand_str(6)
        rand_name = f'{project_id}-{rand_str}.jpg'
        with tempfile.TemporaryDirectory() as temp_path:
            tmp_img_path = f'{temp_path}/{project_id}.jpg'
            img.save(tmp_img_path.replace('\\', '/'))
            upload_file(rand_name, tmp_img_path)
        cls.business.repo.update_img_url(project_id,
                                         f'{UPLOADED_IMG_BASE}/{rand_name}')
        # 存储压缩后的图片
        # width, height = img.size
        # target_width = 300
        # target_height = int(target_width / width * height)
        # small_img = img.resize((target_width, target_height))
        # small_img_path = save_path + f'/{project_id}_s.jpg'
        # small_img.save(small_img_path.replace('\\', '/'))
        # cls.business.repo.update_img_v(project_id)
        return cls.business.repo.set_img_uploaded(project_id)

    @classmethod
    def deploy(cls, *args, **kwargs):
        pass

    @classmethod
    def deploy_project(cls, project_id, version=None, **kwargs):

        original_project = cls.business.get_by_id(project_id)

        try:
            project = cls.deploy(project_id, version=version, **kwargs)
            # todo 添加进Elasticsearch
            if not project.classroom:
                SearchService.add_project(project.id, project.display_name,
                                          project.description,
                                          [tag.id for tag in project.tags],
                                          project.type,
                                          project.img_v if project.img_v else '',
                                          project.photo_url if project.photo_url else '',
                                          project.user.username)
        except Exception as e:
            project = cls.business.repo.update_status(
                project_id, original_project.status)
            cls.business.repo.update_privacy(project, original_project.privacy)
            if version != DEFAULT_DEPLOY_VERSION:
                cls.business.repo.remove_version(project, version)
            cls.send_message_favor(project, m_type='deploy_fail',
                                   project_version=version)
            raise e
        else:
            EventBusiness.create_event(
                user=project.user,
                target=project,
                target_type=project.type,
                action="deploy",
            )
            RocketChatBusiness.post_direct_message(
                user=project.user,
                text=f'Your {project.type} : [{project.name}]({WEB_ADDR}/workspace/{project.id}?type={project.type}) '
                     'was deployed successfully.')
            return project

    @classmethod
    def add_collaborator(cls, project_id, user_id):
        collaborator = UserBusiness.get_by_id(user_id)
        project = cls.business.entity.get_by_id(project_id)
        project.add_to_list_field('collaborators', [collaborator])
        RocketChatBusiness.add_collaborator(project, collaborator)
        return project, collaborator

    @classmethod
    def delete_collaborator(cls, project_id, user_id):
        collaborator = UserBusiness.get_by_id(user_id)
        project = cls.business.entity.get_by_id(project_id)
        if get_jwt_identity() != project.user.user_ID:
            raise Exception('Auth failed')
        project.pull_from_list_field('collaborators', [collaborator])
        RocketChatBusiness.remove_collaborator(project, collaborator)
        return project, collaborator

    @classmethod
    def start_hub_with_project_id(cls, user_ID, project_id, hub_token):
        project = cls.business.get_by_id(project_id)
        # 如果不是同一个用户, 直接报错
        user = UserBusiness.get_by_user_ID(user_ID)
        if user != project.user and user not in project.collaborators:
            raise RuntimeError('Auth failed')
        return ProjectBusiness.start_hub(project.user.user_ID, project.name,
                                         hub_token)

    @classmethod
    def insert_hub_with_project_id(cls, user_ID, project_id, hub_token):
        project = cls.business.get_by_id(project_id)
        # 判断是否是同一个用户
        user = UserBusiness.get_by_user_ID(user_ID)
        if user != project.user and user not in project.collaborators:
            raise RuntimeError('Auth failed')
        return ProjectBusiness.insert_hub(project.user.user_ID, project.name,
                                          hub_token)

    @classmethod
    def get_content(cls, user_ID, project_id, hub_token):
        project = cls.business.get_by_id(project_id)
        # 如果不是同一个用户, 直接报错
        user = UserBusiness.get_by_user_ID(user_ID)
        if user != project.user and user not in project.collaborators:
            raise RuntimeError('Auth failed')
        return ProjectBusiness.get_jl_content(project.user.user_ID,
                                              project.name,
                                              hub_token)

    @classmethod
    def update_file_locker(cls, user_ID, project_id, file_path):
        project = cls.business.get_by_id(project_id)
        user = UserBusiness.get_by_user_ID(user_ID)
        if user != project.user and user not in project.collaborators:
            raise RuntimeError('Auth failed')
        return project.update_file_locker(user, file_path)

    @classmethod
    def check_file_locker(cls, user_ID, project_id, file_path):
        project = cls.business.get_by_id(project_id)
        user = UserBusiness.get_by_user_ID(user_ID)

        if user != project.user and user not in project.collaborators:
            raise RuntimeError('Auth failed')
        return project.check_file_locker(user, file_path)

    @classmethod
    def update_insert_handler(cls, user_ID, project_id):
        project = cls.business.get_by_id(project_id)
        user = UserBusiness.get_by_user_ID(user_ID)
        if user != project.user and user not in project.collaborators:
            raise RuntimeError('Auth failed')
        return project.update_insert_handler()

    @classmethod
    def create_template_project(cls, template_type, user_ID, **args):
        display_name = args.get('display_name')
        display_name += user_ID
        display_name += gen_rand_str(2)
        # 检测到不重名的才通过
        while True:
            if cls.check_project_exist(user_ID, project_type=template_type,
                                       project_name=display_name):
                display_name = args.get('display_name') + gen_rand_str(2)
            else:
                break
        user = UserBusiness.get_by_user_ID(user_ID)
        tags = args.get('tags')
        description = args.get('description')
        name = cls.gen_name(display_name, user_ID, type='app')
        if template_type == 'tutorial':
            return ProjectBusiness.create_template_project(name=name,
                                                           display_name=display_name,
                                                           description=description,
                                                           user=user,
                                                           tags=tags,
                                                           source_path=TUTORIAL_PATH)
        elif template_type == 'classroom':
            return ProjectBusiness.create_template_project(name=name,
                                                           display_name=display_name,
                                                           description=description,
                                                           user=user,
                                                           tags=tags,
                                                           source_path=TUTORIAL_PATH)
        elif template_type == 'app_tutorial':
            return ProjectBusiness.create_template_project(name=name,
                                                           display_name=display_name,
                                                           description=description,
                                                           user=user,
                                                           tags=tags,
                                                           source_path=TUTORIAL_PATH)

    @classmethod
    def get_all_template_project(cls, page, page_size, project_type):
        try:
            user = UserBusiness.get_by_user_ID(Official_User_ID)
            projects = cls.business.get_by_user(user)
            projects = projects(privacy="public")
            # class and tutorial
            classrooms = []
            sort_classrooms = []
            classroom_names = []
            tutorials = []
            sort_tutorials = []
            tutorial_names = []
            # 分析Projects
            for project in projects:
                tags = [tag.id for tag in project.tags]
                if project.display_name in TemplateTutorialDocTitles:
                    project.doc_name = TemplateTutorialDocTitles[
                        project.display_name]
                else:
                    logging.error("没有找到该项目" + project.display_name)
                    project.doc_name = ''
                # print(project.display_name, list(TemplateTutorialTitles.keys()), list(TemplateClassroomTitles.keys()))
                # 筛选区分, 添加一种条件判断
                if 'Classroom' in tags or 'classroom' in tags or project.display_name in TemplateClassroomTitles.keys():
                    classrooms.append(project)
                    classroom_names.append(project.display_name.strip())
                    # 中文标题
                    project.display_name_cn = TemplateClassroomTitles[
                        project.display_name] if \
                        project.display_name in TemplateClassroomTitles.keys() else project.display_name
                    # 英文描述
                    project.description_en = TemplateClassroomDescription[
                        project.display_name] if \
                        project.display_name in TemplateClassroomDescription.keys() else project.description
                else:
                    tutorials.append(project)
                    tutorial_names.append(project.display_name.strip())
                    # 中文标题
                    project.display_name_cn = TemplateTutorialTitles[
                        project.display_name] if \
                        project.display_name in TemplateTutorialTitles.keys() else project.display_name
                    # 英文描述
                    project.description_en = TemplateTutorialDescription[
                        project.display_name] if \
                        project.display_name in TemplateTutorialDescription.keys() else project.description
            # 排序
            default_sort_tutorial_names = list(TemplateTutorialTitles.keys())
            default_sort_classroom_names = list(TemplateClassroomTitles.keys())

            # 挑选
            final_tutorial_names = default_sort_tutorial_names[
                                   (page - 1) * page_size: (page * page_size)]
            final_classroom_names = default_sort_classroom_names[
                                    (page - 1) * page_size: (page * page_size)]

            # 获取返回的Projects
            for name in final_tutorial_names:
                try:
                    index = tutorial_names.index(name.strip())
                    sort_tutorials.append(tutorials[index])
                except ValueError as e:
                    # 没有找到该教程项目
                    print("没有找到该教程项目", name, tutorial_names)
                    continue

            for name in final_classroom_names:
                try:
                    index = classroom_names.index(name.strip())
                    sort_classrooms.append(classrooms[index])
                except ValueError as e:
                    # 没有找到该教程项目
                    print("没有找到该教室项目", name, classroom_names)
                    continue

            # 考虑做拆件, 只返回需要的字段, 展示的字段应该很少
            return sort_classrooms, len(sort_classrooms), \
                   sort_tutorials, len(sort_tutorials)
        except DoesNotExist as e:
            return [], 0, [], 0

    @classmethod
    def get_all_template_project_for_classroom(cls, page, page_size,
                                               project_type='project'):
        classrooms, classroom_count, tutorials, tutorial_count = cls.get_all_template_project(
            page,
            page_size, project_type)
        for i in range(len(classrooms)):
            if i != len(classrooms) - 2:
                tutorials.append(classrooms[i])
        total_count = classroom_count + tutorial_count

        return tutorials[(page - 1) * page_size: page * page_size], total_count

    @classmethod
    def get_video_and_doc_template(cls):
        classrooms, classroom_count, tutorials, tutorial_count = cls.get_all_template_project(
            1, 10, 'project')
        video_classrooms = [None] * 2
        docs_classrooms = [None] * 2
        for classroom in classrooms:
            if classroom.display_name.lower() == 'ML Tutorial-CN'.lower():
                video_classrooms[0] = classroom
            elif classroom.display_name.lower() == 'ML Tutorial-EN'.lower():
                video_classrooms[1] = classroom
            elif classroom.display_name.lower() == 'Python Tutorial-CN'.lower():
                docs_classrooms[0] = classroom
            elif classroom.display_name.lower() == 'Python Tutorial-EN'.lower():
                docs_classrooms[1] = classroom
        # 安全检测
        for ps in [video_classrooms, docs_classrooms]:
            for index in range(len(ps)):
                if ps[index] is None:
                    ps[index] = random.choice(tutorials)

        return video_classrooms, docs_classrooms

    @classmethod
    def check_project_exist(cls, user_ID, project_name, project_type):
        name = secure_name(project_name, type=project_type)
        try:
            project = cls.get_by_identity(user_ID=user_ID, project_name=name)
            return project
        except Exception as e:
            print(e)
            return False
        # print([project.path, project.app_path])
        # cls.business.remove_project_by_id(project.id, user_ID=user_ID)

    @classmethod
    def check_user_limit(cls, user, project_type):
        if isinstance(user, str):
            user = UserBusiness.get_by_user_ID(user)

        is_limit = True
        if project_type == 'app':
            # app
            if user.app_number < user.app_number_limit:
                is_limit = False
        elif project_type == 'module':
            # module
            if user.module_number < user.module_number_limit:
                is_limit = False
        else:
            # dataset
            if user.dataset_number < user.dataset_number_limit:
                is_limit = False
        return is_limit

    @classmethod
    def add_project_classroom_info(cls):
        from server3.service.course_service import CourseService
        projects = cls.business.read()
        names = list(TemplateClassroomTitles.keys()) + list(
            TemplateTutorialTitles.keys())
        courses = CourseService.get_all_course(page_no=1, page_size=100)
        sections = []
        course_names = []
        for key in courses[0].keys():
            for c in courses[0][key]:
                course_names.append(c['name'])
                if c['name'] != "Machine Learning":
                    read = CourseService.get_sections(user_ID="chentiyun",
                                                      course=c['_id'],
                                                      page_size=100)[0]
                    temp_sections = [s['name_en'] for s in read]
                    sections += temp_sections
        print(course_names + sections, len(course_names + sections))
        names = names + course_names + sections
        for project in projects:
            # project.classroom = True
            condition = False
            for name in names:
                if project.display_name.lower() in name.lower() or name.lower() in project.display_name.lower() \
                        or 'tutorial' in project.display_name.lower():
                    condition = True
                    break
            try:
                project = cls.business.repo.update_one_by_id(project.id, {
                    'classroom': condition})
                print('updated:', project.display_name, project.classroom,
                      condition)
            except DoesNotExist as e:
                continue

    @classmethod
    def update_production_info(cls):
        # class_type = ('cv', 'nlp', 'dp', 'tutorial', 'others')
        # classification
        input_dict = {'python_tutorial': 'tutorial', 'Style Transfer': 'cv',
                      'count people': 'cv', 'image2txt': 'cv',
                      'Couples Face': 'cv',
                      'mnist': 'cv', 'starGAN': 'cv', 'pix2pixGAN': 'cv',
                      'MNISTNUMBERREADER': 'cv', 'MNIST GAN': 'cv',
                      'Poetry': 'nlp',
                      'summerschool_materials': 'tutorial',
                      'python_tutorial_series': 'tutorial',
                      'ML NoteBooK': 'tutorial',
                      'Python Tutorial-EN': 'tutorial',
                      'ML Tutorial-EN': 'tutorial',
                      'ML Tutorial-CN': 'tutorial',
                      'Python Tutorial-CN': 'tutorial',
                      'Evaluate Model': 'tutorial',
                      'Publish Dataset': 'tutorial', 'Train Model': 'tutorial',
                      'Develop App': 'tutorial',
                      'Convert Model': 'tutorial',
                      'Basic Operation': 'tutorial',
                      'NN backpropagation': 'tutorial',
                      'hands-on-machine-learning': 'tutorial',
                      'Outlier Detection': 'dp', 'iris-classifier': 'dp',
                      'squeezenet': 'dp', 'btcModel': 'dp',
                      'Develop Model': 'tutorial',
                      'Develop Toolkit': 'tutorial',
                      'classification': 'dp',
                      'sceneClassification_VGG19': 'cv',
                      'sceneClassification_VGG16': 'cv',
                      'sceneClassification_10': 'cv',
                      'logicregression': 'others', 'image2base64': 'dp',
                      'VGG16': 'cv', 'base64 to img': 'dp',
                      'seq classification': 'nlp', 'windowTransfer': 'dp',
                      'Variational Auto Encoder': 'nlp',
                      'new_face_feature': 'cv', 'new_gender_classifier': 'cv'}

        projects = cls.business.repo.read({'privacy': 'public'})

        for project in projects:
            cls = 'others'
            if project.display_name in input_dict:
                cls = input_dict[project.display_name]
            elif project.user.username == 'Coder' or project.user.username == 'coder':
                cls = 'dp'
            project = ProjectBusiness.repo.update_one_by_id(project.id, {
                'classification': cls})
            print('updated:', project.display_name, project.classification)

    # 处理Tags
    @classmethod
    def handle_tags(cls, tags):
        if len(tags) > 0 and not isinstance(tags[0], str):
            tags = [tag.id for tag in tags]
        new_tags = []
        # 中文
        keys = TagsMapping.keys()
        # 英文
        values = TagsMapping.values()
        for tag in tags:
            if '/' in tag or '\\' in tag:
                new_tags.append(tag)
            else:
                if tag in keys:
                    new_tags.append(tag + ' / ' + values[keys.index(tag)])
                elif tag in values:
                    new_tags.append(keys[values.index(tag)] + ' / ' + tag)
                else:
                    new_tags.append(tag)
        # print('我请求多少遍:', tags)
        return new_tags


if __name__ == '__main__':
    # print(ProjectService.get_all_template_project(1, 10))
    # import time
    # start = time.time()
    # ProjectService.add_project_classroom_info()
    # print('cost:', time.time() - start)
    # ProjectService.update_production_info()

    # 删除 luxu99 下自动创建的项目
    from server3.entity.project import Project

    user = UserBusiness.get_by_username('luxu99')
    projects = Project.objects(user=user, type='app')
    print('总的项目数：', len(projects))
    for key, e in enumerate(projects):
        print(f'正在删除 {key} 个')
        ProjectService.remove_project_by_id(e.id, user.user_ID)
        time.sleep(2)
