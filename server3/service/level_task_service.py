#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
# @author   : Zhaofeng Li
# @version  : 1.0
# @date     : 2018-10-19
# @function : level tasks
# @running  : python
"""
import time
from server3.business.user_business import UserBusiness
from server3.business.app_business import AppBusiness
from server3.business.module_business import ModuleBusiness
from server3.business.data_set_business import DatasetBusiness

from server3.business.level_task_business import LevelTaskBusiness
from server3.constants import DEFAULT_DEPLOY_VERSION
from server3.constants import JobStatus

bus_type_mapper = {
    "app": AppBusiness,
    "module": ModuleBusiness,
    "dataset": DatasetBusiness,
}


class LevelTaskService:
    business = LevelTaskBusiness

    @classmethod
    def get_tasks(cls, user_ID=None, **kwargs):
        user = None
        if user_ID is not None:
            user = UserBusiness.get_by_user_ID(user_ID)
        tasks = cls.business.get_tasks(user=user, **kwargs)
        return tasks

    @classmethod
    def check_task_completion(cls, project_id, type, check_type):
        lt = cls.business.get_by_project(project_id, type)
        if lt.project_type:
            project = lt[lt.project_type]
            # job tut check job finished
            if check_type == 'job' and lt.level == 1 and lt.num == 4:
                for job in project.jobs:
                    if job.status == JobStatus.COMPLETE or \
                            job.status == JobStatus.FAILED:
                        lt.finish_task_step()
                        return lt

            if check_type == 'deploy':
                # app tut check app run
                if lt.level == 1 and lt.num == 1:
                    for version in [*project.versions, DEFAULT_DEPLOY_VERSION]:
                        _, output_json, status, _ = AppBusiness.run_app(
                            project.id, {}, version)
                        # print(status, version, output_json)
                        if status == 'success':
                            lt.finish_task_step()
                            return lt
                else:
                    # other projects just deployed is done
                    lt.finish_task_step()
                    return lt
        raise Exception('task checking failed')


if __name__ == '__main__':
    pass
