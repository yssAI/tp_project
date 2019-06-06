from server3.business.kaggle_dataset_business import KaggleDatasetBusiness
import os
import os
from server3.constants import USER_DIR
import asyncio
from server3.business.data_set_business import DatasetBusiness
from server3.business.user_business import UserBusiness
from server3.business.project_business import ProjectBusiness
from server3.utility import json_utility


class KaggleDatasetService:
    @classmethod
    def download_list(cls, project_id, page=1, page_size=10):
        downloadList, total_count = KaggleDatasetBusiness.download_list(page=page, page_size=page_size,
                                                                        project_id=project_id)
        return downloadList, total_count

    @classmethod
    def favor_list(cls, user_ID, page_no, page_size):
        user = UserBusiness.get_by_user_ID(user_ID=user_ID)
        kaggle_favor = user.kaggle_dataset_favor
        print('kaggle_favor', kaggle_favor)
        total_count = len(kaggle_favor)
        user_kaggle_favors = kaggle_favor[(page_no-1)*page_size: page_no*page_size]
        # kaggle_favor_list = KaggleDatasetBusiness.favor_list(user_kaggle_favor, page_no, page_size)
        # kaggle_favor_list = json_utility.me_obj_list_to_json_list(user_kaggle_favor)
        return user_kaggle_favors, total_count

    @classmethod
    def search_kaggle_list(cls, page, search, size, file_type, sort_by, tags):
        search_list = KaggleDatasetBusiness.search_list_from_kaggle(page=page, search=search, size=size,
                                                                    file_type=file_type, sort_by=sort_by, tags=tags)
        return list(search_list)

    @classmethod
    def add_kaggle_download_list(cls, kaggle_obj):
        add_result, overview = KaggleDatasetBusiness.add_kaggle_download_task(kaggle_obj)
        print('添加结果', add_result)
        return add_result, overview

    @classmethod
    def cancel_download(cls, project_id,  mounted_dataset_id):
        task_cancel = KaggleDatasetBusiness.cancel_download(project_id,  mounted_dataset_id)
        return task_cancel

    @classmethod
    def kaggle_dataset_favor_action(cls, user_ID, ref, title, size):
        dataset, overview = KaggleDatasetBusiness.kaggle_dataset_favor_action(user_ID=user_ID, ref=ref, title=title,
                                                                              size=size)
        return dataset, overview

    @classmethod
    def kaggle_dataset_update_status_and_mount(cls, dataset_id=None):
        result = KaggleDatasetBusiness.kaggle_dataset_update_status_and_mount(dataset_id)
        return result

    @classmethod
    def kaggle_download_size_update(cls, dataset_id=None, kaggle_downloading_size=None):
        result = KaggleDatasetBusiness.kaggle_dataset_update_download_size(dataset_id=dataset_id,
                                                                           kaggle_downloading_size=kaggle_downloading_size)
        return result

    @classmethod
    def get_downloading_list(cls, project_id):
        projects = ProjectBusiness.get_by_id(project_id)
        user = UserBusiness.get_by_user_ID('momodel')
        try:
            downloading_list = DatasetBusiness.filter(user=user, mount_kaggle_projects=projects, is_finished=False)
            return downloading_list
        except:
            return False


if __name__ == '__main__':
    # a = KaggleDatasetService.download_list(project_id='5bbeab08e3067c2a709efb91')
    # print(a)
    # KaggleDatasetService.add_kaggle_download_list()
    a = KaggleDatasetService.cancel_download_task(project_id='5c81f2deef2b4b24193202cc', task_id='5c8b8d0fef2b4b81ce3a844e')
    print('a', a)
