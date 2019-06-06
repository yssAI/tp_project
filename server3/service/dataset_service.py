# -*- coding: UTF-8 -*-
import os

from server3.service.project_service import ProjectService
from server3.business.module_business import ModuleBusiness
from server3.business.data_set_business import DatasetBusiness
from server3.business.event_business import EventBusiness
from server3.constants import MODULE_DIR
from server3.constants import DEFAULT_DEPLOY_VERSION
from server3.constants import IpfsError


class DatasetService(ProjectService):
    business = DatasetBusiness
    name = 'dataset'

    @classmethod
    def get_by_id(cls, project_id, **kwargs):
        project = super().get_by_id(project_id, **kwargs)
        if kwargs['user']:
            project.can_create_app = not cls.check_user_limit(kwargs['user'], 'app')
        if kwargs['user']:
            project.can_create_module = not cls.check_user_limit(kwargs['user'], 'module')
        project.versions = \
            ['.'.join(version.split('_')) for version in
             project.versions]
        return project

    @classmethod
    def deploy(cls, project_id, version=DEFAULT_DEPLOY_VERSION):
        dataset = cls.business.deploy_or_publish(project_id, version)

        try:
            # create ipfs hash
            cls.business.generate_ipfs_hash(project_id, version, dataset.path)
        except IpfsError as e:
            print('IpfsError: {}'.format(e))

        # 发送通知消息
        cls.send_message_favor(dataset, m_type='deploy',
                               project_version=version)
        dataset = cls.get_by_id(project_id)
        return dataset


if __name__ == '__main__':
    pass
