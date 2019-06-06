# -*- coding: UTF-8 -*-
from server3.business.user_business import UserBusiness
from server3.business.request_answer_business import RequestAnswerBusiness
from server3.business.user_request_business import UserRequestBusiness
from server3.business.comments_business import CommentsBusiness
from server3.business.project_business import ProjectBusiness
from server3.business.event_business import EventBusiness
from server3.service.message_service import MessageService
from flask import jsonify


class CommentsService:
    business = CommentsBusiness

    @classmethod
    def add_comments(cls, _id, c_id, comments_user, comments, comments_type):
        new_comment = cls.business.add_comments(_id, c_id, comments_user,
                                                comments,
                                                comments_type)
        send_noti = True
        EventBusiness.create_event(
            user=comments_user,
            target=new_comment,
            target_type="comment",
            action="create",
            input={'comments': comments}
        )
        admin_user = UserBusiness.get_by_user_ID('admin')
        kwargs = {}
        if comments_type in ['answer', 'comment_answer']:

            answer = RequestAnswerBusiness.get_by_id(_id)
            kwargs['answer'] = answer

            if c_id:
                comment = CommentsBusiness.get_by_id(c_id)
                message_type = 'comment_comment'
                receivers = [comment.user]
            else:
                message_type = 'comment_answer'
                receivers = [answer.user]
            if answer.user.user_ID == comments_user.user_ID:
                send_noti = False

        elif comments_type in ['request', 'comment_request']:
            request = UserRequestBusiness.get_by_id(_id)
            kwargs['user_request'] = request
            if c_id:
                comment = CommentsBusiness.get_by_id(c_id)
                message_type = 'comment_comment'
                receivers = [comment.user]
            else:
                message_type = 'comment_request'
                receivers = [request.user]+request.favor_users
            if request.user.user_ID == comments_user.user_ID:
                send_noti = False

        elif comments_type == 'project':
            message_type = 'comment_project'
            project = ProjectBusiness.get_by_id(_id)
            kwargs['project'] = project
            if project.user.user_ID == comments_user.user_ID:
                send_noti = False
            receivers = [project.user]
        else:
            return jsonify({'response': 'error comments type'}), 400
        if send_noti:
            MessageService.create_message(sender=admin_user,
                                          message_type=message_type,
                                          receivers=receivers,
                                          user=comments_user,
                                          **kwargs)

        return new_comment

    @classmethod
    def update_by_id(cls, _id, user, comments):
        new_comment = cls.business.update_by_id(_id, user, comments)
        EventBusiness.create_event(
            user=user,
            target=new_comment,
            target_type="comment",
            action="update",
            input={'comments': comments}
        )
        return new_comment

    @classmethod
    def remove_by_id(cls, object_id, user_ID):
        user = UserBusiness.get_by_user_ID(user_ID)
        comment = cls.business.get_by_id(object_id)
        comment.minus_num_in_answer()
        comment.delete()
        # cls.business.remove_by_id(object_id, user_ID)
        EventBusiness.create_event(
            user=user,
            target_type="comment",
            action="delete"
        )
