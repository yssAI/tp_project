# -*- coding: UTF-8 -*-
from server3.repository.general_repo import Repo


class UserRepo(Repo):
    def __init__(self, instance):
        Repo.__init__(self, instance)

    def read_by_user_ID(self, user_ID):
        return Repo.read_unique_one(self, {'user_ID': user_ID})

    def delete_by_user_ID(self, user_ID):
        return Repo.delete_unique_one(self, {'user_ID': user_ID})

    def update_img_url(self, user, url):
        """
        To update project image version.

        :param project: project id
        :return: updated project object
        """
        if isinstance(user, str):
            user = self.read_by_user_ID(user)
        user.avatar_url = url
        user.save()
        return user
