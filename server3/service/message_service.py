# -*- coding: UTF-8 -*-
from bson import ObjectId

from server3.business.message_business import MessageBusiness
from server3.business.user_business import UserBusiness
from server3.service import logger_service


# def get_by_user_id(user_id, page_no, page_size):
#     user = UserBusiness.get_by_id(user_id)
#     messages, total_number = MessageBusiness.get_by_user(user, page_no, page_size)
#     return messages
#
#
# def get_by_user_ID(user_ID, page_no, page_size):
#     user = UserBusiness.get_by_user_ID(user_ID)
#     messages = MessageBusiness.get_by_user(user, page_no, page_size)
#     return messages
#
#
# def create_message(sender, message_type, receivers, user=None, **kwargs):
#     if user and isinstance(user, (str, ObjectId)):
#         user = UserBusiness.get_by_id(user)
#     if isinstance(sender, (str, ObjectId)):
#         sender = UserBusiness.get_by_id(sender)
#     receivers = [UserBusiness.get_by_id(r)
#                  if isinstance(r, (str, ObjectId)) else r for r in receivers]
#     # create a new message object
#     created_message, created_receivers = MessageBusiness. \
#         add_message(sender,
#                     message_type,
#                     receivers,
#                     user,
#                     **kwargs)
#     if created_message:
#         logger_service.emit_notification(created_message, created_receivers)
#         return created_message
#     else:
#         raise RuntimeError('Cannot create the new message')
#
#
# def mark_read_message(user_ID, receiver_id):
#     user = UserBusiness.get_by_user_ID(user_ID)
#     # 用户点击未读信息后，将信息状态更改为已读
#     MessageBusiness.mark_read_message(user, receiver_id)


class MessageService:
    business = MessageBusiness

    @classmethod
    def get_by_user_id(cls, user_id, page_no, page_size):
        user = UserBusiness.get_by_id(user_id)
        messages, total_number = MessageBusiness.get_by_user(user, page_no,
                                                             page_size)
        return messages, total_number

    @classmethod
    def get_by_user_ID(cls, user_ID, page_no, page_size):
        user = UserBusiness.get_by_user_ID(user_ID)
        messages, total_number = MessageBusiness.get_by_user(user, page_no,
                                                             page_size)
        return messages, total_number

    @classmethod
    def create_message(cls, sender, message_type, receivers, user=None,
                       **kwargs):
        if user and isinstance(user, (str, ObjectId)):
            user = UserBusiness.get_by_id(user)
        if isinstance(sender, (str, ObjectId)):
            sender = UserBusiness.get_by_id(sender)
        receivers = [
            UserBusiness.get_by_id(r) if isinstance(r, (str, ObjectId)) else r
            for r in
            receivers]
        # create a new message object
        created_message, created_receivers = MessageBusiness. \
            add_message(sender,
                        message_type,
                        receivers,
                        user,
                        **kwargs)
        if created_message:
            logger_service.emit_notification(created_message,
                                             created_receivers)
            return created_message
        else:
            raise RuntimeError('Cannot create the new message')

    @classmethod
    def read_message(cls, user_ID, receiver_id):
        user = UserBusiness.get_by_user_ID(user_ID)
        # 用户点击未读信息后，将信息状态更改为已读
        if receiver_id:
            MessageBusiness.mark_read_message(user, receiver_id)


if __name__ == '__main__':
    pass
    # 删除  某些 message
    # from server3.entity.message import Message

    # messages = Message.objects(message_type='add_collaborator')
    # # messages = Message.objects(id='5cd287d21afd946a25643546')
    # print(len(messages))
    # for message in messages:
    #     MessageBusiness.remove_by_id(message.id, '')
