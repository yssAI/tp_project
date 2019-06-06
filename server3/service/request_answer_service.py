# -*- coding: UTF-8 -*-
from server3.business.user_business import UserBusiness
from server3.service.message_service import MessageService
from server3.business.user_request_business import UserRequestBusiness
from server3.business.request_answer_business import RequestAnswerBusiness
from server3.business.event_business import EventBusiness
from server3.business.rocket_chat_business import RocketChatBusiness
from server3.constants import ENV, WEB_ADDR
from server3.utility import json_utility


# def get_all_answer_by_user_ID(user_ID, page_no, page_size, type, search_query,
#                               get_total_number=True):
#     cls = RequestAnswerBusiness
#     user = UserBusiness.get_by_user_ID(user_ID)
#     answers, total_number = cls. \
#         get_by_answer_user(user,
#                            search_query=search_query,
#                            get_total_number=get_total_number,
#                            page_no=page_no,
#                            page_size=page_size,
#                            type=type)
#     for answer in answers:
#         answer.user_request_title = answer.user_request.title
#     return answers, total_number
#
#
# def get_all_answer_of_this_user_request(user_request_id, get_number=False,
#                                         entity_type='requestAnswer'):
#     # request_answer = request_answer_business. \
#     #     get_all_answer_of_this_user_request(user_request)
#     cls = EntityMapper.get(entity_type)
#     request_answer = cls.get_by_user_request_id(user_request_id, get_number)
#     return request_answer
#
#
# def get_answer_number_of_this_user_request(user_request_id):
#     request_answer_number = request_answer_business. \
#         get_answer_number_of_this_user_request(user_request_id)
#     return request_answer_number
#
#
# def get_by_id(request_answer_id):
#     request_answer = request_answer_business. \
#         get_by_request_answer_id(request_answer_id)
#     return request_answer
#
#
# def create_request_answer(**data):
#     # create a new request_answer object
#     created_request_answer = request_answer_business. \
#         add_request_answer(**data)
#     if created_request_answer:
#         # get user object
#         user = data['answer_user']
#         user_request = user_request_business. \
#             get_by_user_request_id(data['user_request'])
#
#         from server3.service.world_service import WorldService
#         from server3.business.statistics_business import StatisticsBusiness
#         from server3.entity.world import CHANNEL
#
#         # 记录历史记录
#         statistics = StatisticsBusiness.action(
#             user_obj=user,
#             entity_obj=created_request_answer,
#             entity_type="requestAnswer",
#             action="create"
#         )
#
#         # 记录世界频道消息  # 推送消息
#         world = WorldService.system_send(
#             channel=CHANNEL.request,
#             message=f"用户{created_request_answer.answer_user.user_ID}为需求"
#                     f"{user_request.title}创建了回答")
#
#         # create ownership relations
#         #  新建通知消息
#         admin_user = UserBusiness.get_by_user_ID('admin')
#
#         receivers = [el for el in user_request.star_user]
#         if message_service.create_message(
#                 sender=admin_user,
#                 message_type='answer',
#                 receivers=receivers,
#                 user=user,
#                 title='Notification',
#                 user_request=user_request,
#         ):
#             return created_request_answer
#         else:
#             raise RuntimeError(
#                 'Cannot create message of the new request_answer')
#
#     else:
#         raise RuntimeError('Cannot create the new request_answer')
#
#
# def accept_request_answer(user_request_id, user_ID, request_answer_id):
#     user_request = user_request_business. \
#         get_by_user_request_id(user_request_id)
#     ownership = ownership_business.get_ownership_by_owned_item(
#         user_request, 'user_request'
#     )
#     if ownership.user.user_ID != user_ID:
#         raise RuntimeError(
#             'this request not belong to this user, cannot update')
#     else:
#         user_request_business.update_user_request_by_id(
#             user_request_id=user_request_id,
#             accept_answer=ObjectId(request_answer_id)
#         )
#
#
# def update_request_answer(request_answer_id, user_id, answer):
#     request_answer = request_answer_business. \
#         get_by_request_answer_id(request_answer_id)
#     ownership = ownership_business.get_ownership_by_owned_item(
#         request_answer, 'request_answer'
#     )
#     if ownership.user.user_ID != user_id:
#         raise RuntimeError(
#             'this request not belong to this user, cannot update')
#     else:
#         request_answer_business.update_request_answer_by_id(
#             request_answer_id=request_answer_id,
#             answer=answer
#         )
#
#
# def list_request_answer_by_user_id(user_ID, order=-1):
#     user = UserBusiness.get_by_user_ID(user_ID)
#     request_answer = ownership_business. \
#         get_ownership_objects_by_user(user, 'request_answer')
#     if order == -1:
#         request_answer.reverse()
#     return request_answer
#
#
# def remove_request_answer_by_id(request_answer_id, user_ID):
#     request_answer = request_answer_business. \
#         get_by_request_answer_id(request_answer_id)
#     # check ownership
#     ownership = ownership_business. \
#         get_ownership_by_owned_item(
#         request_answer, 'request_answer')
#     if user_ID != ownership.user.user_ID:
#         raise ValueError('this request not belong to this user, cannot delete')
#     return request_answer_business.remove_by_id(request_answer_id)


class RequestAnswerService:
    business = RequestAnswerBusiness

    @classmethod
    def get_all_answer_by_user_ID(cls, user_ID, page_no, page_size,
                                  type, search_query):
        user = UserBusiness.get_by_user_ID(user_ID)
        answers, total_number = RequestAnswerBusiness. \
            get_by_answer_user(user,
                               search_query=search_query,
                               page_no=page_no,
                               page_size=page_size,
                               type=type)
        for answer in answers:
            answer.user_request_title = answer.user_request.title
        return answers, total_number

    @classmethod
    def accept_answer(cls, user_request, user, request_answer):
        # user = UserBusiness.get_by_user_ID(user_ID)

        user_request.update(accept_answer=request_answer)
        # UserRequestBusiness.update_by_id(
        #     user_request_id=user_request_id,
        #     accept_answer=request_answer
        # )

        EventBusiness.create_event(
            user=user,
            target=request_answer,
            target_type="answer",
            action="accept",
        )
        # 发消息给回答者（回答者是需求者自己，不通知）
        admin_user = UserBusiness.get_by_user_ID('admin')
        # 发送消息给的用户
        if request_answer.user != user:
            MessageService.create_message(
                sender=admin_user,
                message_type='accept_answer',
                receivers=[request_answer.user],
                user=user,
                title='Notification',
                user_request=user_request,
            )

    @classmethod
    def update_request_answer_by_id(cls, request_answer_id, user, **data):

        old_select_project = RequestAnswerBusiness.get_by_id(request_answer_id).select_project

        new_answer = RequestAnswerBusiness.update_request_answer_by_id(
            request_answer_id, **data)

        EventBusiness.create_event(
            user=user,
            target=new_answer,
            target_type="answer",
            action="update",
        )
        user_request = new_answer.user_request
        # 发消息给request提出者和关注者（回答者也关注了request，不通知回答者自己）
        admin_user = UserBusiness.get_by_user_ID('admin')
        # 发送消息给关注此需求的用户
        receivers = user_request.favor_users
        # 发送消息给提出此需求的用户
        receivers.append(user_request.user)
        # 发送消息给收藏此回答的用户
        receivers.extend(new_answer.favor_users)
        # 剔除回答者自己
        if user in receivers:
            receivers.remove(user)
        MessageService.create_message(
            sender=admin_user,
            message_type='answer_update',
            receivers=receivers,
            user=user,
            title='Notification',
            user_request=user_request,
        )

        # 如果答案有附加project，且与旧的答案项目不一致,发消息给project的,(回答者添加自己的项目，不通知回答者自己)
        if data.get('select_project') and data['select_project'] != old_select_project and data['select_project'].user != user:
            MessageService.create_message(
                sender=admin_user,
                message_type='answer_project',
                receivers=[data['select_project'].user],
                user=user,
                title='Notification',
                user_request=user_request,
                project=data['select_project']
            )
        return new_answer

    @classmethod
    def create_request_answer(cls, **data):
        # create a new request_answer object
        created_request_answer = RequestAnswerBusiness. \
            add_request_answer(**data)
        if created_request_answer:
            # get user object
            user = data['user']

            # 记录历史记录
            # statistics = StatisticsBusiness.action(
            #     user_obj=user,
            #     entity_obj=created_request_answer,
            #     entity_type="requestAnswer",
            #     action="create"
            # )

            EventBusiness.create_event(
                user=user,
                target=created_request_answer,
                target_type="answer",
                action="create",
            )
            if data.get('user_request'):
                user_request = data['user_request']

                # 记录世界频道消息  # 推送消息
                # world = WorldService.system_send(
                #     channel=CHANNEL.request,
                #     message=f"用户{created_request_answer.answer_user.user_ID}为需求"
                #             f"{user_request.title}创建了回答")

                # admin_user = UserBusiness.get_by_user_ID('admin')
                #
                # text = f"<http://localhost:8899/discussion/{user_request.id}?type={user_request.type}|" \
                #        f"用户 {created_request_answer.answer_user.user_ID} 为需求 {user_request.title} 创建了回答>"
                #
                # SlackBusiness.send_message(user=admin_user, text=text, channel='general')
                try:
                    text = f"[{created_request_answer.user.username}]({WEB_ADDR}/profile/{created_request_answer.user.user_ID})" \
                           f" 评论了话题 [{user_request.title}]({WEB_ADDR}/discussion/{user_request.id}?type={user_request.type}) "
                    RocketChatBusiness.post_official_message(text=text)
                except:
                    print('rc error')

                try:
                    # 发消息给request提出者和关注者（回答者也关注了request，不通知回答者自己）
                    admin_user = UserBusiness.get_by_user_ID('admin')
                    # 发送消息给关注此需求的用户
                    receivers = user_request.favor_users
                    # 发送消息给提出此需求的用户
                    receivers.append(user_request.user)
                    # 剔除回答者自己
                    if user in receivers:
                        receivers.remove(user)
                    MessageService.create_message(
                        sender=admin_user,
                        message_type='answer',
                        receivers=receivers,
                        user=user,
                        title='Notification',
                        user_request=user_request,
                    )
                    # 如果答案有附加project，发消息给project的作者,(回答者添加自己的项目，不通知回答者自己)
                    if data.get('select_project') and data['select_project'].user != user:
                        MessageService.create_message(
                            sender=admin_user,
                            message_type='answer_project',
                            receivers=[data['select_project'].user],
                            user=user,
                            title='Notification',
                            user_request=user_request,
                            project=data['select_project']
                        )
                except:
                    raise RuntimeError(
                        'Cannot create message of the new request_answer')
            return created_request_answer
        else:
            raise RuntimeError('Cannot create the new request_answer')

    @classmethod
    def remove_by_id(cls, object_id, user_ID):
        user = UserBusiness.get_by_user_ID(user_ID)
        cls.business.remove_by_id(object_id, user_ID)
        EventBusiness.create_event(
            user=user,
            target_type="comment",
            action="delete"
        )

    # @classmethod
    # def update_request_answer(cls, request_answer_id, answer):
    #     RequestAnswerBusiness.update_request_answer_by_id(
    #         request_answer_id=request_answer_id,
    #         answer=answer
    #     )

    # @classmethod
    # def remove_answer_by_id(cls, request_answer_id, user_ID):
    #     return RequestAnswerBusiness.remove_by_id(request_answer_id, user_ID)

    # @classmethod
    # def get_all_answer_of_this_user_request(cls, user_request_id):
    #     request_answer = RequestAnswerBusiness.get_by_user_request_id(
    #         user_request_id)
    #     return request_answer
