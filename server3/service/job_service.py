#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
# @author   : Zhaofeng Li
# @version  : 1.0
# @date     : 2018-05-08
# @function : Getting all of the job of statics analysis
# @running  : python
# Further to FIXME of None
"""
import os
import py_compile
import time
from flask_jwt_extended import create_access_token

import eventlet
from subprocess import call
from celery import Celery

from server3.business.job_business import JobBusiness
from server3.business.user_business import UserBusiness
from server3.business.app_business import AppBusiness
from server3.business.event_business import EventBusiness
from server3.business.module_business import ModuleBusiness
from server3.business.data_set_business import DatasetBusiness
from server3.business.kube_business import K8sBusiness
from server3.business.kube_business import KubePod
from server3.business.project_business import ProjectBusiness
from server3.business.notebook_log_business import NotebookLogBusiness
# from server3.business import celery_business
from server3.utility.file_utils import copytree
from server3.constants import USER_DIR
from server3.constants import BROKER_SERVICE_HOST
from server3.constants import JobStatus
from server3.constants import PY_SERVER
from server3.constants import JobConst
import logging

# from server3.constants import CHECKPOINT_DIR_NAME

broker_service_host = BROKER_SERVICE_HOST

celery = Celery('tasks', broker='amqp://guest@%s//' % broker_service_host,
                backend='amqp', task_protocol=1)
celery.conf.task_protocol = 1
celery.conf.task_queue_max_priority = 10
celery.conf.task_acks_late = True
celery.conf.worker_prefetch_multiplier = 1


class JobService:
    business = JobBusiness

    business_mapper = {
        'app': AppBusiness,
        'module': ModuleBusiness,
        'dataset': DatasetBusiness,
    }

    # @classmethod
    # def create_job(cls, project_id, type, user_ID, source_file_path,
    #                run_args=None, running_module=None,
    #                running_code=None):
    #     business_mapper = {
    #         'app': AppBusiness,
    #         'module': ModuleBusiness,
    #         'dataset': DatasetBusiness,
    #     }
    #     project = business_mapper[type].get_by_id(project_id)
    #     options = {}
    #     if running_module:
    #         [modole_user_ID, module_name,
    #          module_version] = running_module.split('/')
    #         module_identity = f'{modole_user_ID}+{module_name}'
    #         running_module = ModuleBusiness.get_by_identity(module_identity)
    #         options = {
    #             'running_module': running_module,
    #             'module_version': module_version
    #         }
    #     user = UserBusiness.get_by_user_ID(user_ID)
    #     new_job = JobBusiness.create_job(project=project, type=type, user=user,
    #                                      source_file_path=source_file_path,
    #                                      run_args=run_args,
    #                                      running_code=running_code,
    #                                      **options)
    #     EventBusiness.create_event(
    #         user=user,
    #         target=new_job,
    #         target_type='job',
    #         action="create",
    #     )
    #     # add job to project
    #     project.jobs.append(new_job)
    #     project.save()
    #
    #     return new_job

    @classmethod
    def all_running_pending_jobs_num(cls):
        return K8sBusiness.get_queuing_or_running_gpu_job_num() + \
               JobBusiness.get_pending_job_num()

    @classmethod
    def create_job(cls, project_id, type, user_ID, script_path, env,
                   user_token, task=None, function=None, display_name=None,
                   args='', katib_args={}):
        project = cls.business_mapper[type].get_by_id(project_id)
        user = project.user
        path = os.path.join(project.path, script_path)
        if not os.path.exists(path):
            script_path = f'src/{script_path}'
        new_job = JobBusiness.create_job(project=project, type=type, user=user,
                                         script_path=script_path, env=env,
                                         task=task, function=function,
                                         display_name=display_name, args=args,
                                         katib_args=katib_args)

        def send_job():
            # copy job to staging folder
            staging_path = new_job.staging_path
            staging_project_path = '/'.join(staging_path.split('/')[:-1])
            if not os.path.exists(staging_project_path):
                os.makedirs(staging_project_path)
            time.sleep(2)
            ProjectBusiness.copy_to_ignore_env(new_job.project,
                                               staging_path,
                                               no_site_packages=False,
                                               no_remove=True)

            project_path = f'{user.user_ID}/{project.name}'
            # check if running or pending jobs which makes this job to wait
            wait = False
            if cls.all_running_pending_jobs_num() > 1 and env == 'gpu':
                wait = True
                print('need wait')

            # send job to celery
            celery.send_task('celery_conf.create_job',
                             args=(str(new_job.id),
                                   new_job.script_path,
                                   project_path, env,
                                   user_token, function,
                                   str(task.id) if task else None,
                                   False, PY_SERVER, args, wait,
                                   0),
                             queue=env)

        # 如果是 katib ，状态改为 Queuing
        # 如果不是，执行以前的流程
        if katib_args:
            new_job.status_bak = 'Queuing'
        else:
            eventlet.spawn_n(send_job)

        EventBusiness.create_event(
            user=user,
            target=new_job,
            target_type='job',
            action="create",
        )
        # add job to project
        project.jobs.append(new_job)
        project.save()
        return new_job, False

    @classmethod
    def restart(cls, job_id, user_token, auto_restart_num=0, auto=False):

        job = JobBusiness.get_by_id(job_id)
        project = job[job.project_type]
        project_path = f'{project.user.user_ID}/{project.name}'
        # K8sBusiness.create_k8s_job(job, job.script_path, project_path,
        #                            env=job.env, restart=True, args=job.args)
        wait = False
        if not auto:
            if K8sBusiness.get_queuing_or_running_gpu_job_num() + \
                    JobBusiness.get_pending_job_num() > 1:
                wait = True
                print('restart need wait')
        # print('auto restart: ', auto_restart_num, (str(job.id),
        #                                            job.script_path,
        #                                            project_path, job.env,
        #                                            user_token, wait))
        celery.send_task('celery_conf.create_job',
                         (str(job.id),
                          job.script_path,
                          project_path, job.env,
                          user_token),
                         priority=auto_restart_num,
                         kwargs={
                             'wait': wait,
                             'restart': True,
                             'auto_restart_num': auto_restart_num},
                         queue=job.env
                         )

        EventBusiness.create_event(
            user=project.user,
            target=job,
            target_type='job',
            action="restart",
        )
        return job

    @classmethod
    def insert_modules2job(cls, job_id):
        job = cls.business.get_by_id(job_id)
        project = job.project
        if project.type == 'app':
            for um in project.used_modules:
                src = os.path.join(um.module.module_path, um.version)
                dst = f'/home/jovyan/modules/{um.module.user.user_ID}/' \
                    f'{um.module.name}'
                pod = KubePod(job.pod_name)
                pod.copy_in(src, dst)
                pod.exec([
                    '/bin/bash', '/home/jovyan/add_venv.sh',
                    f'{um.module.user.user_ID}/{um.module.name}/{um.version}',
                    job_id
                ])

    @classmethod
    def insert_modules2trial(cls, job_id, worker_id):
        job = cls.business.get_by_id(job_id)
        project = job.project
        if project.type == 'app':
            for um in project.used_modules:
                src = os.path.join(um.module.module_path, um.version)
                dst = f'/home/jovyan/modules/{um.module.user.user_ID}/' \
                      f'{um.module.name}'
                # pod = KubePod(job.pod_name)
                pod = KubePod(worker_id)
                pod.copy_in(src, dst)
                pod.exec([
                    '/bin/bash', '/home/jovyan/add_venv.sh',
                    f'{um.module.user.user_ID}/{um.module.name}/{um.version}',
                    job_id
                ])

    @classmethod
    def get_by_project(cls, project_type, project_id, page_no, page_size,
                       status):
        business_mapper = {
            'app': AppBusiness,
            'module': ModuleBusiness,
            'dataset': DatasetBusiness,
        }
        project = business_mapper[project_type].get_by_id(project_id)
        jobs, total = cls.business.get_by_project(project_type, project,
                                                  page_no, page_size, status)
        return jobs, total

    @classmethod
    def check_python_syntax(cls, project_id, script_path, project_type):
        """
            检测需要创建job的python是否存在语法错误, 如果没有, 返回None, 有就返回数据
        :param project_id: 当前的项目 ID
        :param script_path: 当前选中的文件
        :param project_type: 要执行的类型
        :return:
        """
        project = cls.business_mapper[project_type].get_by_id(project_id)
        path = os.path.join(project.path, script_path)
        if not os.path.exists(path):
            path = f'src/{script_path}'
        if os.path.exists(path):
            try:
                py_compile.compile(path, doraise=True)
            except py_compile.PyCompileError as e:
                error = e.msg
                error = error.split('\n')
                line_info = error[0].split(',')
                default_info = "File \"{0}\", {1}".format(script_path,
                                                          line_info[1] if len(
                                                              line_info) > 1 else '')
                error[0] = default_info
                error_info = ''
                for s in error:
                    error_info += (s + '\n')
                # ['  File "main.py", line 9', '    cd ..', '        ^', 'SyntaxError: invalid syntax', '']
                # ['File "main.py"', '    cd ..', '        ^', 'SyntaxError: invalid syntax', '']
                logging.warning('error is :' + str(error))
                # 如果有语法错误, 直接返回
                NotebookLogBusiness.add_log('error', error, project,
                                            source='job')
                return [error_info]
        else:
            logging.warning('can not find this file')

    @classmethod
    def finish_job(cls, job_id, if_success):
        job, logs = cls.business.finish_job(job_id, if_success)

        catch_OOM = False
        if not if_success:
            if 'Resource exhausted: OOM' in logs or 'CUDA_ERROR_OUT_OF_MEMORY' in logs:
                catch_OOM = True

        def send():
            # need some time to wait for job truly finish
            time.sleep(10)
            cls.business.send_message(job,
                                      m_type='job_success' if if_success else 'job_error',
                                      logs=logs)

        auto_restart_num = job.auto_restart_num
        if catch_OOM and auto_restart_num <= JobConst.MAX_AUTO_RESTART_NUM:
            job.update_restart_times()
            cls.restart(job_id, create_access_token(
                identity=job[job.project_type].user.user_ID),
                        auto_restart_num + 1,
                        auto=True)
        else:
            eventlet.spawn_n(send)
        return job

    @classmethod
    def finish_katib_job(cls, job_id, if_success):
        job = cls.business.get_by_id(job_id)

        def send():
            time.sleep(10)
            cls.business.send_message(job,
                                      m_type='job_success' if if_success else 'job_error',
                                      logs='')
        eventlet.spawn_n(send)
        return job


if __name__ == '__main__':
    pass
