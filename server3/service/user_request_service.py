# -*- coding: UTF-8 -*-
# from server3.entity.world import CHANNEL
from server3.business.user_request_business import UserRequestBusiness
from server3.business.request_answer_business import RequestAnswerBusiness
from server3.business.user_business import UserBusiness
# from server3.business.statistics_business import StatisticsBusiness
from server3.business.comments_business import CommentsBusiness
from server3.business.event_business import EventBusiness
# from server3.service.world_service import WorldService
# from server3.service.user_service import UserService
from server3.business.rocket_chat_business import RocketChatBusiness
from server3.business.project_business import ProjectBusiness
from server3.service.general_service import GeneralService
from server3.entity.tag import Tag
from server3.utility import str_utility
from server3.constants import ENV, WEB_ADDR
from server3.constants import WEB_ADDR
from server3.utility import json_utility
from flask_socketio import SocketIO
from server3.constants import REDIS_SERVER
from server3.constants import TOP_TOPIC_ID
from mongoengine import DoesNotExist

socketio = SocketIO(message_queue=REDIS_SERVER)
from server3.service.search_service import SearchService


class UserRequestService(GeneralService):
    @classmethod
    def get_list(cls, type, search_query, user_ID, page_no, page_size,
                 search_tags, sort, query_user_ID, rand, related=False,
                 ref_project=None):
        user = UserBusiness.get_by_user_ID(user_ID) if user_ID else None
        query_user = UserBusiness.get_by_user_ID(
            query_user_ID) if query_user_ID else None
        if user:
            user_request, total_number = UserRequestBusiness. \
                get_list_by_user(type, user, page_no, page_size)
        else:
            user_request, total_number = UserRequestBusiness. \
                get_list(type, search_query, user, False, page_no, page_size,
                         search_tags, sort, query_user, rand, related=related,
                         ref_project=ref_project)

        if sort == 'hot':
            for each_object in user_request:
                each_object['input'] = []
                each_object['output'] = []
                each_object['view_num'] = EventBusiness.get_number(
                    {'request': each_object['_id'], 'action': "view"})
        else:
            for each_object in user_request:
                each_object['input'] = []
                each_object['output'] = []
                each_object.view_num = EventBusiness.get_number(
                    {'request': each_object, 'action': "view"})

        return user_request, total_number

    @classmethod
    def get_by_id(cls, user_request_id):
        user_request = UserRequestBusiness.get_by_id(user_request_id)
        user_request.input = []
        user_request.output = []
        return user_request

    @classmethod
    def remove_by_id(cls, user_request_id, user_ID):
        if (CommentsBusiness.get_comments_of_this_user_request(user_request_id)
                or RequestAnswerBusiness.get_by_user_request_id(
                    user_request_id)):
            raise RuntimeError('Cannot delete user_request')

        removed = UserRequestBusiness.remove_by_id(user_request_id, user_ID)
        # todo 删除 Elasticsearch 的数据
        SearchService.delete_request(user_request_id)
        return removed

    @classmethod
    def remove_by_user_ID(cls, user_ID):
        user = UserBusiness.get_by_user_ID(user_ID)
        removed_requests = UserRequestBusiness.remove_all_by_user(user)

        # # todo 删除 Elasticsearch 的数据
        # for removed in removed_requests:
        #     SearchService.delete_request(removed.id)

        return removed_requests

    @classmethod
    def create_user_request(cls, title, user_ID, **kwargs):
        tags = kwargs.pop('tags', [])
        select_project_id = kwargs.pop('select_project')
        if select_project_id:
            select_project = ProjectBusiness.get_by_id(
                select_project_id)
            kwargs.update({'select_project': select_project})
        # create a new user_request object
        user = UserBusiness.get_by_user_ID(user_ID)
        created_user_request = UserRequestBusiness.add_user_request(
            title=title,
            user=user,
            status=0,
            **kwargs)
        # todo 添加Elasticsearch的Request数据
        SearchService.add_request(created_user_request.title,
                                  created_user_request.description,
                                  created_user_request.type,
                                  created_user_request.user.username,
                                  created_user_request.id)
        # update tags
        cls.update_tags(oldtags=[], newtags=tags,
                        entity_type='request', entities=[created_user_request])

        # created_user_request.add_tags(tags)
        EventBusiness.create_event(
            user=user,
            target=created_user_request,
            target_type="request",
            action="create"
        )
        # 记录世界频道消息  # 推送消息
        # world = WorldService.system_send(
        #     channel=CHANNEL.request,
        #     message=f"用户{created_user_request.user.user_ID}" +
        #             f"发布了需求{created_user_request.title}")
        # admin_user = UserBusiness.get_by_user_ID('admin')
        #
        # text = f"<http://localhost:8899/discussion/{created_user_request.id}?type={created_user_request.type}|" \
        #        f"用户 {created_user_request.user.user_ID} 发布了需求 {created_user_request.title}>"
        #
        # SlackBusiness.send_message(user=admin_user, text=text, channel='general')
        if ENV in ['PROD', 'MO']:
            try:
                text = f"[{created_user_request.user.username}]({WEB_ADDR}/profile/{created_user_request.user.user_ID})" \
                    f" 发布了话题 [{created_user_request.title}]({WEB_ADDR}/discussion/{created_user_request.id}?type={created_user_request.type})"
                RocketChatBusiness.post_official_message(text=text)
            except:
                print('rc error')

        # msg = json_utility.convert_to_json({
        #     'user_ID': user_ID,
        #     'content': '发布了新需求，快去看看吧',
        # })
        # socketio.emit('world_message', msg,
        #               namespace='/log/%s' % user_ID)

        return created_user_request

    @classmethod
    def update_user_request(cls, user_request_id, **kwargs):
        tags = kwargs.pop('tags', [])
        if not isinstance(tags, list):
            tags = str_utility.split_without_empty(tags)
        select_project_id = kwargs.pop('select_project')
        if select_project_id:
            select_project = ProjectBusiness.get_by_id(
                select_project_id)
            kwargs.update({'select_project': select_project})
        request = UserRequestBusiness.update_by_id(
            user_request_id=user_request_id, **kwargs)
        # todo 判断是否更新到Elasticsearch 那边的数据
        if 'description' in kwargs or 'title' in kwargs:
            try:
                SearchService.add_request(request.title, request.description,
                                          request.type, request.user.username,
                                          request.id)
            except:
                pass
        oldtags = [tag.id for tag in request.tags]
        # update tags
        cls.update_tags(oldtags=oldtags, newtags=tags,
                        entity_type='request', entities=[request])
        # request.add_tags(tags)
        return request

    @classmethod
    def update_request_to_top(cls, user_request_id):
        try:
            user_request = cls.get_by_id(user_request_id)
            if user_request.is_top:
                user_request.is_top = 0
                message = '取消置顶成功'
            else:
                user_request.is_top = 1
                message = '置顶成功'
            user_request.save()
            return True, message
        except DoesNotExist as e:
            return False, '置顶失败'


if __name__ == '__main__':
    from server3.business.event_business import EventBusiness
    import datetime
    from time import mktime

    for day in range(13, 18, 1):
        # , hour=0, minute=0, second=0
        # "2018-12-13T00:00:00+08:00"

        start_time = datetime.datetime.strptime("2018-12-13T00:00:00+08:00",
                                                '%Y-%m-%dT%H:%M:%S+08:00')
        # "2018-12-18T00:00:00+08:00"
        end_time = datetime.datetime.strptime("2018-12-18T00:00:00+08:00",
                                              '%Y-%m-%dT%H:%M:%S+08:00')
        print(start_time, end_time, datetime.datetime.utcnow())
        # print(start_time)
        num = EventBusiness.get_unique_number({'action': 'login',
                                               'create_time': {
                                                   'gte': start_time,
                                                   '$lt': end_time}})
        # 新注册用户数
        users = UserBusiness.read(
            {'create_time': {'gte': start_time, '$lt': end_time}})
        print('12月{0}号, 日活用户数{1}, 新注册用户数{2}'.format(day, num, len(users)))
