# -*- coding: UTF-8 -*-
import os
import requests
import json
import re
import shutil
import yaml

from bson import ObjectId
from subprocess import call

from server3.service.project_service import ProjectService
from server3.business.module_business import ModuleBusiness
from server3.business.data_set_business import DatasetBusiness
from server3.business.event_business import EventBusiness
from server3.business.app_business import AppBusiness
from server3.business.user_business import UserBusiness
from server3.business.user_business import check_api_key
from server3.business import user_business
from server3.business.statistics_business import StatisticsBusiness
from server3.service import message_service
from server3.utility.diff_requirements import diff
from server3.constants import DOCKER_IP
from server3.constants import DEFAULT_DEPLOY_VERSION
from server3.constants import TEMPLATE_PATH
from server3.constants import REQ_FILE_NAME
from server3.constants import NFS_SERVER
from server3.constants import ENV
from flask_socketio import SocketIO
from server3.constants import REDIS_SERVER
from server3.business.rocket_chat_business import RocketChatBusiness
from server3.constants import WEB_ADDR
from server3.constants import APP_MAIN_FILE
from server3.constants import PY_SERVER
from server3.service.logger_service import emit_deploy_project

from server3.utility import json_utility

socketio = SocketIO(message_queue=REDIS_SERVER)


class AppService(ProjectService):
    business = AppBusiness
    name = 'app'

    @classmethod
    def add_used_module(cls, app_id, used_module, version):
        used_module = ModuleBusiness.get_by_id(used_module)
        return cls.business.add_used_module(app_id, used_module, version)

    @classmethod
    def insert_module_to_yml(cls, app_id, func, used_module, version):
        used_module = ModuleBusiness.get_by_id(used_module)
        used_module.args = ModuleBusiness.load_module_params(
            used_module, version)
        return cls.business.insert_module_to_yml(app_id, func, used_module,
                                                 version)

    # @classmethod
    # def add_imported_modules(cls, app_id, imported_module, deploy_version):
    #     """
    #     Add imported modules and datasets into app.deployment
    #     while user deploy an app.
    #
    #     :param app_id: app id
    #     :param imported_module: tuple (user_name, project_name, version)
    #     :param version:
    #     :return:
    #     """
    #     app = cls.get_by_id(app_id)
    #     AppBusiness.add_imported_module()
    #     pass

    @classmethod
    def remove_used_module(cls, app_id, used_module, version):
        used_module = ModuleBusiness.get_by_id(used_module)
        return cls.business.remove_used_module(app_id, used_module, version)

    @classmethod
    # @check_api_key
    def run_app(cls, app_id, input_json, user_ID, version, api_key):
        """

        :param app_id: app id
        :param input_json:
        :param user_ID:
        :param version:
        :return:
        :rtype:
        """

        if user_ID:
            user = UserBusiness.get_by_user_ID(user_ID)
        else:
            user = None
        try:
            kwargs = {}
            status = 'error'
            app = cls.get_by_id(app_id)
            app, output_json, status, kwargs = \
                cls.business.run_app(app_id, input_json, version)
            # 运行出错
            if status == 'error':
                cls.send_msg_owner(project=app, m_type='run_error', **kwargs)
            EventBusiness.create_event(
                user=user,
                target=app,
                target_type='app',
                action="invoke",
                input=input_json,
                output=output_json,
                project_id=app.id,
                project_version=version,
                status=status,
                **kwargs
            )
            return output_json

        except Exception as e:
            # 运行出错
            if status == 'error':
                cls.send_msg_owner(project=app, m_type='run_error', **kwargs)
            raise RuntimeError('app run error:', app.display_name)

    @classmethod
    def insert_envs(cls, user_ID, app_name):
        """
        copy used modules and datasets to jl container when start
        :param user_ID:
        :param app_name:
        :return:
        """
        user = UserBusiness.get_by_user_ID(user_ID)
        app = AppBusiness.read_unique_one(name=app_name, user=user)
        for used_module in app.used_modules:
            AppBusiness.insert_module_env(app, used_module.module,
                                          used_module.version)
        # for used_dataset in app.used_datasets:
        #     AppBusiness.insert_dataset(app, used_dataset.dataset,
        #                                used_dataset.version)

    @classmethod
    def get_by_id(cls, project_id, **kwargs):
        project = super().get_by_id(project_id, **kwargs)
        if hasattr(project,
                   'source_project') and project.source_project is not None:
            project.fork_project_display_name = project.source_project.display_name
        if kwargs.get('yml') == 'true' and \
                project.status == cls.business.repo.STATUS.ACTIVE:
            project.args = cls.business.load_app_params(project,
                                                        kwargs.get('version'))

        project = cls.convert_version_format(project)
        return project

    # @classmethod
    # def publish(cls, project_id, commit_msg, handler_file_path, deploy_files,
    #             version):
    #     try:
    #         app = cls.deploy_or_publish(project_id, commit_msg,
    #                                     handler_file_path, deploy_files,
    #                                     version)
    #         # cls.send_message_favor(app, m_type='publish')
    #     except Exception as e:
    #         # app = cls.business.get_by_id(project_id)
    #         # app.status = 'inactive'
    #         # app.save()
    #
    #         # update app status
    #         app = cls.business.repo.update_status(
    #             project_id,
    #             cls.business.repo.STATUS.INACTIVE)
    #
    #         # cls.send_message_favor(app, m_type='publish_fail')
    #         raise e
    #     else:
    #         EventBusiness.create_event(
    #             user=app.user,
    #             target=app,
    #             target_type=app.type,
    #             action="publish",
    #         )
    #         return app

    @classmethod
    def deploy(cls, project_id, commit_msg='', handler_file_path=None,
               deploy_files=None, version=DEFAULT_DEPLOY_VERSION):
        app = AppService.get_by_id(project_id)
        if app == app.user.base_tutorial:
            import time
            from flask_socketio import SocketIO
            from server3.constants import REDIS_SERVER
            socketio = SocketIO(message_queue=REDIS_SERVER)
            cls.business.repo.update_has_dev(app)
            app = cls.business.repo.update_deployment_status(app, 0)
            time.sleep(2)
            # deploy state 2
            # msg = json_utility.convert_to_json({
            #     'user_ID': app.user.user_ID,
            #     'project_id': project_id,
            #     'state': 1,
            #     'version': version,
            # })
            # socketio.emit('deploy_project', msg,
            #               namespace='/log/%s' % app.user.user_ID)

            emit_deploy_project(app.user.user_ID, project_id, 1, version)
            app = cls.business.repo.update_deployment_status(app, 1)

            # time.sleep(3)
            service_name = '-'.join([app.user.user_ID, app.name, version])
            func_path = os.path.join(cls.business.base_func_path, service_name)
            cls.business.copy_to_ignore_env(app, func_path)
            # deploy state 2
            # msg = json_utility.convert_to_json({
            #     'user_ID': app.user.user_ID,
            #     'project_id': project_id,
            #     'state': 2,
            #     'version': version,
            # })
            # socketio.emit('deploy_project', msg,
            #               namespace='/log/%s' % app.user.user_ID)
            emit_deploy_project(app.user.user_ID, project_id, 2, version)
            app = cls.business.repo.update_deployment_status(app, 2)

            time.sleep(5)
            # msg = json_utility.convert_to_json({
            #     'user_ID': app.user.user_ID,
            #     'project_id': project_id,
            #     'state': 3,
            #     'version': version,
            # })
            # socketio.emit('deploy_project', msg,
            #               namespace='/log/%s' % app.user.user_ID)
            emit_deploy_project(app.user.user_ID, project_id, 3, version)

            # update app status
            cls.business.repo.update_privacy(
                app, cls.business.repo.PRIVACY.PUBLIC)
            app = cls.business.repo.update_status(
                app,
                cls.business.repo.STATUS.ACTIVE)
            app = cls.business.repo.update_deployment_status(app, -1)

            cls.send_message_favor(app, m_type='deploy',
                                   project_version=version)
            return app

        cls.business.freeze_env(project_id)
        app = cls.deploy_or_publish(project_id, commit_msg,
                                    handler_file_path, deploy_files,
                                    version)
        cls.send_message_favor(app, m_type='deploy',
                               project_version=version)
        for u in [app.user] + app.collaborators:
            RocketChatBusiness.post_direct_message(user=u,
                                                   text=f'Your {app.type} : [{app.name}]({WEB_ADDR}/workspace/{app.id}?type={app.type}) '
                                                   'was deployed successfully.')
        return app

    @classmethod
    def get_action_entity(cls, app_id, **kwargs):
        app = AppBusiness.get_by_id(app_id)
        return AppBusiness.get_action_entity(app, **kwargs)

    # FIXME: Deprecated
    @classmethod
    def find_imported_modules(cls, script):
        """
        Scan python script to get imported modules.

        :param script: python script
        :return: list of imported modules in
                 (user_id, module_name, version) tuple format.
        """
        pattern = \
            r"""^(?!#).*(run|predict|train)\s*\(('|")(([\w\d_-]+)/([\w\d_-]+)/(\d+\.\d+\.\d+))('|")"""

        modules = []
        for match in re.finditer(pattern, script, re.MULTILINE):
            if '#' not in match.group(0):
                modules.append(
                    (match.group(4), match.group(5), match.group(6)))

        return modules

    @classmethod
    def read_handler_py(cls, script, app):
        """

        Get imported modules/dataset from py script.

        :param script: py script in str format
        :param app: app object
        :return:
        """

        # 1. get possible imported dataset list from
        # app.used_datasets[n].dataset.path
        # e.g. './user_directory/zhaofengli/anone
        possible_used_datasets = [d for d in app.used_datasets]

        # 2. get possible imported module list from
        # app.used_modules in list of
        # tuple (module_object, module_version) format
        possible_used_modules = [m for m in app.used_modules]

        # 3. check if there is any matches in script
        # TODO to be updated
        # for d in possible_used_datasets:
        #     pattern = r"""^(?!#).*({})/({})""".format(
        #         d.dataset.path.replace('./user_directory', 'dataset'),
        #         d.version)
        #     matches = re.finditer(pattern, script, re.MULTILINE)
        #     for ma in matches:
        #         if '#' not in ma.group(0):
        #             break
        #     else:
        #         app.used_datasets.remove(d)
        #
        # for m in possible_used_modules:
        #     pattern = \
        #         r"""^(?!#).*(run|predict|train)\s*\(('|")({}/{}/{})('|")""" \
        #             .format(m.module.user.user_ID,
        #                     m.module.name,
        #                     m.version.replace('_', '.'))
        #     matches = re.finditer(pattern, script, re.MULTILINE)
        #     for ma in matches:
        #         if '#' not in ma.group(0):
        #             break
        #     else:
        #         app.used_modules.remove(m)
        return possible_used_datasets, possible_used_modules

    @classmethod
    def copy_entities(cls, app, version, possible_used_datasets,
                      possible_used_modules):
        """

        Copy imported modules/datasets into right place for deployment.

        :param container: app project docker
        :param app: app object
        :param version: deployment version
        :param possible_used_datasets:
        list of dataset objects in imported history
        :param possible_used_modules:
        list of module objects in imported history
        :return:
        """
        # Move module from project.module_path
        # ./server3/lib/modules/zhaofengli/newttt/[module_version]/ to
        # ./fucntion/[user_ID]-[app_name]-[app_version]/modules/
        # [user_ID]/[module_name]/[module_version]
        for m in possible_used_modules:
            cls.copy_entity(app, version, m, m.module.module_path, m.module,
                            'modules')

        # Move dataset from 引用者的DOCKER CONTAINER 里面的
        # ~/dataset/[user_ID] to
        # ./fucntion/[user_ID]-[app_name]-[app_version]/
        # dataset/[user_ID]/[dataset_name]/

        for d in possible_used_datasets:
            cls.copy_entity(app, version, d, d.dataset.path,
                            d.dataset, 'datasets')

    @staticmethod
    def copy_entity(app, app_version, entity, entity_path, entity_obj,
                    entity_dir):
        # print('nnn', entity_obj.name)
        if entity_obj.type == 'module':
            src = '{}/{}/'.format(entity_path,
                                  entity.version.replace('.', '_'))
            dst = './functions/{}-{}-{}/{}/{}/{}/{}/'.format(
                app.user.user_ID, app.name, app_version,
                entity_dir,
                entity_obj.user.user_ID, entity_obj.name,
                entity.version.replace('.', '_'))
        else:
            src = '{}/'.format(entity_path)
            dst = './functions/{}-{}-{}/{}/{}-{}/'.format(
                app.user.user_ID, app.name, app_version,
                entity_dir,
                entity_obj.user.user_ID, entity_obj.name)
        if os.path.isdir(dst):
            shutil.rmtree(dst, ignore_errors=True)
        shutil.copytree(src, dst, symlinks=True)

    @classmethod
    def rename_handler_py(cls, handler_file_path, func_path):
        """
        Rename *.py to 'handler.py' for deplyment.

        :param handler_file_path:
        :param func_path: path of function folder
        :return:
        """
        has_handler = handler_file_path == APP_MAIN_FILE
        handler_file_path = handler_file_path.replace('work', func_path)
        handler_file_path = os.path.join(func_path, handler_file_path)
        handler_file_name = handler_file_path.split('/')[-1]
        handler_dst_path = handler_file_path.replace(handler_file_name,
                                                     APP_MAIN_FILE)
        if not has_handler:
            shutil.copy(handler_file_path, handler_dst_path)
        return handler_file_path, handler_dst_path

    @classmethod
    def diff_n_gen_new_requirements(cls, func_path):
        """
        diff two requirements.txt for package installation in deployed docker.

        :param func_path:
        :return:
        """
        old = os.path.join(TEMPLATE_PATH, REQ_FILE_NAME)
        new = os.path.join(func_path, REQ_FILE_NAME)
        r = os.path.join(func_path, '_tmp.'.join(REQ_FILE_NAME.split('.')))
        diff(old_req=old, new_req=new, result_req=r)
        # shutil.move(new, new+'1')
        shutil.move(r, new)

    @classmethod
    def deploy_or_publish(cls, app_id, commit_msg, handler_file_path,
                          deploy_files,
                          version=DEFAULT_DEPLOY_VERSION):
        """

        App project go deploy or publish.

        :param app_id: app project id
        :param commit_msg: commit msg
        :param handler_file_path: work/XXXX.py file, source
        :param deploy_files
        :param version: app project go production version
        :return: app object
        """
        # parse json to list
        deploy_files = json.loads(deploy_files)
        # update app status to 'deploying
        app = cls.business.repo.update_status(
            app_id,
            cls.business.repo.STATUS.DEPLOYING)

        for u in [app.user] + app.collaborators:
            emit_deploy_project(u.user_ID, app_id, 0, version)
        app = cls.business.repo.update_deployment_status(app, 0)

        pod = app.pod
        # freeze working env
        pod.exec(['/bin/bash', '/home/jovyan/freeze_venv.sh'])
        # print(app_id, commit_msg, version)
        cls.business.commit(app_id, commit_msg, version)

        service_name = '-'.join([app.user.user_ID, app.name, version])
        service_name_no_v = '-'.join([app.user.user_ID, app.name])

        # faas new in functions dir
        s_path = os.path.join(cls.business.base_func_path, service_name)
        if os.path.exists(s_path):
            shutil.rmtree(s_path)

        # create faas yml
        with open(f'{s_path}.yml', 'w', encoding="utf-8",
                  errors='ignore') as wf:
            yaml.dump({'functions': {
                service_name: {
                    'environment': {
                        'PY_SERVER': PY_SERVER},
                    'handler': './' + service_name,
                    'image': service_name + ':latest',
                    'lang': 'python3'}},
                'provider': {'gateway': f'http://{DOCKER_IP}:8080',
                             'name': 'openfaas'}}, wf,
                default_flow_style=False)

        # deploy state 1
        for u in [app.user] + app.collaborators:
            emit_deploy_project(u.user_ID, app_id, 1, version)
        app = cls.business.repo.update_deployment_status(app, 1)

        # target path = new path
        func_path = os.path.join(cls.business.base_func_path, service_name)
        all_files = os.listdir(app.path)
        deploy_files.append(REQ_FILE_NAME)
        ignore_files = set(all_files) - set(deploy_files)
        # if ENV == 'DEFAULT':
        #     requests.put(
        #         f'{NFS_SERVER}/nfs/deploy/app/{app.user.user_ID}/{app.name}/{version}',
        #         json={'ignore_files': list(ignore_files)}).json()
        # else:
        cls.business.copy_to_ignore_env(app, func_path, *ignore_files)
        try:
            os.remove(os.path.join(app.path, REQ_FILE_NAME))
        except FileNotFoundError:
            pass

        # rename py to handler.py
        handler_file_path, handler_dst_path = cls.rename_handler_py(
            handler_file_path, func_path)

        # change some configurable variable to deploy required
        # cls.business.process_handler_py(handler_dst_path)

        with open(handler_file_path, 'r',
                  encoding="utf-8", errors='ignore') as f:
            script = f.read()

            possible_used_datasets, possible_used_modules = \
                cls.read_handler_py(script, app)

            # 4. save verified possible_imported_modules/datasets
            # to app.deployments
            possible_used_datasets = []

            cls.business.add_imported_entities(
                app_id, version,
                used_modules=possible_used_modules,
                used_datasets=possible_used_datasets)

            cls.copy_entities(app, version,
                              possible_used_datasets, possible_used_modules)

        # copy path edited __init__.py
        # shutil.copy(
        #     f'{TEMPLATE_PATH}/function/modules/__init__.py',
        #     os.path.join(func_path, 'modules')
        # )

        # gen diffed requirements.txt
        cls.diff_n_gen_new_requirements(func_path)

        # deploy
        if ENV in ['DEFAULT', 'HP']:
            call(
                f"""ssh admin@{DOCKER_IP} 'cd /mnt/functions_dev && faas-cli build -f ./{service_name}.yml && faas-cli deploy -f ./{service_name}.yml'""",
                shell=True)
        else:
            call(
                f"""ssh admin@{DOCKER_IP} 'cd /mnt/functions && faas-cli build -f ./{service_name}.yml && faas-cli deploy -f ./{service_name}.yml'""",
                shell=True)

        # deploy state 2
        for u in [app.user] + app.collaborators:
            emit_deploy_project(u.user_ID, app_id, 2, version)
        app = cls.business.repo.update_deployment_status(app, 2)

        # when not dev(publish), change the privacy etc
        if version != DEFAULT_DEPLOY_VERSION:
            # update privacy
            cls.business.repo.update_privacy(
                app, cls.business.repo.PRIVACY.PUBLIC)
            # add version
            cls.business.repo.add_version(app, version)
        else:
            cls.business.repo.update_has_dev(app)

        # update app status
        app = cls.business.repo.update_status(
            app,
            cls.business.repo.STATUS.ACTIVE)
        app = cls.business.repo.update_deployment_status(app, -1)
        # deploy state 3 关闭
        for u in [app.user] + app.collaborators:
            emit_deploy_project(u.user_ID, app_id, 3, version)

        return app

# @classmethod
# def add_used_app(cls, user_ID, app_id):
#     user = UserBusiness.get_by_user_ID(user_ID=user_ID)
#     app = cls.business.get_by_id(app_id)
#     user.used_apis.append(app)
#     user_result = user.save()
#     if user_result:
#         return {
#             "user": user_result.to_mongo(),
#         }

# def test_create_app():
#     data = {
#         "name": "预测航班延误",
#         "description": "预测航班延误信息",
#     }
#     AppService.create_project(name="预测航班延误", description="description")

#
# if __name__ == '__main__':
#     import sys
#
#     sys.path.append('../../')
#
#     AppService.app_deploy_or_publish("5af50c74ea8db714444d7205", "test",
#                                      "/Users/Chun/Documents/workspace/momodel/mo/pyserver/user_directory/chun/my_exercise/Untitled.py")
#
#     pass
