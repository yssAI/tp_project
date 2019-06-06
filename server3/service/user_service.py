# -*- coding: UTF-8 -*-
import re
import base64
import hashlib
import json
import random
import smtplib
from bson import ObjectId
from datetime import datetime
from copy import deepcopy
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import BytesIO
import eventlet
import tempfile
import requests
from PIL import Image
from mongoengine import DoesNotExist
from mongoengine import NotUniqueError
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity

from server3.business.app_business import AppBusiness
from server3.business.data_set_business import DatasetBusiness
from server3.business.event_business import EventBusiness
from server3.business.module_business import ModuleBusiness
from server3.business.request_answer_business import RequestAnswerBusiness
from server3.business.user_business import UserBusiness
from server3.business.user_business import check_api_key
from server3.business.user_request_business import UserRequestBusiness
from server3.constants import Error, GIT_SERVER
from server3.constants import WEB_ADDR
from server3.entity.general_entity import UserEntity
from server3.entity.phone_message_id import PhoneMessageId
from server3.service.message_service import MessageService
from server3.utility import token_utility
from server3.utility.str_utility import gen_rand_name
from server3.utility.str_utility import secure_name
from server3.utility.str_utility import gen_rand_str
from server3.business.project_business import ProjectBusiness
from server3.constants import Tutorials
from server3.business.level_task_business import LevelTaskBusiness
from server3.constants import GitHubClient
from server3.constants import GitHubConsts
from server3.business.rocket_chat_business import RocketChatBusiness
from server3.business.oss_business import upload_file
from server3.constants import UPLOADED_IMG_BASE
from server3.service.search_service import SearchService
# 标准邮件格式
from server3.email_template import email_template
# 微信常量
from server3.constants import WechatConstants
import logging
# 邀请机制
# import datetime
from server3.utility.str_utility import decode
import os
from server3.entity.user import User
from server3.constants import TEMP_USER_EXPIRE_HOURS
from server3.constants import TEMP_USER_TOTAL_NUM
from server3.constants import INVITATION_CODE


# msg['To'] = '374758875@qq.com'
# text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://localhost:8989/user/login"
# text_plain = MIMEText(text,'plain', 'utf-8')
# msg.attach(text_plain)
# def add_git_http_user(user_ID, password):
#     """
#     auth jupyterhub with user token
#     :param user_ID:
#     :param password:
#     :param user_token:
#     :return: dict of res json
#     """
#     return requests.post(f'{GIT_SERVER}/git/{user_ID}',
#                          json={'password': password})
#
#
# def add(user_ID, password, **kwargs):
#     add_git_http_user(user_ID, password)
#     hashed_password = generate_password_hash(password)
#     return user_business.add(user_ID, hashed_password, **kwargs)
#
#
# def register(user_ID, password, phone, code, **kwargs):
#     # 验证失败会抛出错误
#     # verify_code(code=code, phone=phone)
#     verify_key = token_utility.generate_key()
#     return add(user_ID=user_ID, password=password,
#                phone=phone, api_key=verify_key, **kwargs)
#
#
# def reset_password(phone, message_id, code, new_password):
#     # 验证
#     result = verify_code(code, message_id)
#     if result:
#         user = user_business.get_by_phone(phone=phone)
#         user.password = generate_password_hash(new_password)
#         return user.save()
#         # else:
#         #     raise Error(ErrorMessage)
#
#
# def authenticate(user_ID, password):
#     user = user_business.get_by_user_ID(user_ID)
#     if user and check_password_hash(user.password, password):
#         user.id = str(user.id)
#         return user
#     return False


# def forgot_send(email):
#     user = user_business.get_by_email(email)
#     smtpserver = 'smtp.exmail.qq.com'
#     username = 'service@momodel.ai'
#     password = 'Mo123456'
#     sender = 'service@momodel.ai'
#     # receiver='374758875@qq.com'
#     subject = 'Mo Authentication'
#     msg = MIMEMultipart('mixed')
#     msg['Subject'] = subject
#     msg['From'] = 'service@momodel.ai <service@momodel.ai>'
#     if user:
#         receiver = email
#         msg['To'] = email
#         suiji = str(random.randint(random.randint(1, 999999),
#                                    random.randint(999999, 99999999999)))
#         h = hashlib.md5(bytes(suiji, encoding="utf-8"))
#         h.update(email.encode("utf-8"))
#
#         user.hashEmail = h.hexdigest()
#         user.save()
#
#         text = user.user_ID + ',\n Please click the following link to reset your password. ' \
#                               'Ignore this message if it is not your operation.\n ' + \
#                WEB_ADDR + '/newpassword?email=' + email + '&user=' + user.user_ID + '&hashEmail=' + h.hexdigest()
#         text_plain = MIMEText(text, 'plain', 'utf-8')
#         msg.attach(text_plain)
#         smtp = smtplib.SMTP()
#         smtp.connect(smtpserver)
#         smtp.login(username, password)
#         smtp.sendmail(sender, receiver, msg.as_string())
#         smtp.quit()
#         return user
#     return False


# def newpassword_send(password, email, hashEmail):
#     user = user_business.get_by_hashEmail(email, hashEmail)
#     if user:
#         user['password'] = generate_password_hash(password)
#         del user.hashEmail
#         user.save()
#         return user
#     return False


# def have_hashEmail(email, hashEmail):
#     user = user_business.get_by_hashEmail(email, hashEmail)
#     if user:
#         return user
#     return False


# def check_tourtip(user_ID):
#     user = user_business.get_by_user_ID(user_ID)
#     if user:
#         return user
#     return False
#
#
# def no_tourtip(user_ID):
#     user = user_business.get_by_user_ID(user_ID)
#     if user:
#         user.tourtip = 1
#         user.save()
#         return user
#     return False
#
#
# def check_learning(user_ID):
#     user = user_business.get_by_user_ID(user_ID)
#     if user:
#         return user
#     return False
#
#
# def no_learning(user_ID):
#     user = user_business.get_by_user_ID(user_ID)
#     if user:
#         user['welcome'] = "1"
#         user.save()
#         return user
#     return False


# def update_request_vote(user_request_id, user_ID):
#     user = user_business.get_by_user_ID(user_ID)
#     user_request = user_request_business. \
#         get_by_user_request_id(user_request_id)
#
#     if user_request in user.request_vote_up:
#         user.request_vote_up.remove(user_request)
#         user_result = user.save()
#     else:
#         user.request_vote_up.append(user_request)
#         user_result = user.save()
#
#     if user in user_request.votes_up_user:
#         user_request.votes_up_user.remove(user)
#         user_request_result = user_request.save()
#     else:
#         user_request.votes_up_user.append(user)
#         user_request_result = user_request.save()
#     if user_result and user_request_result:
#         return user_request_result.to_mongo()
#
#
# def update_request_star(user_request_id, user_ID):
#     user = user_business.get_by_user_ID(user_ID)
#     user_request = user_request_business. \
#         get_by_user_request_id(user_request_id)
#
#     if user_request in user.request_star:
#         user.request_star.remove(user_request)
#         user_result = user.save()
#     else:
#         user.request_star.append(user_request)
#         user_result = user.save()
#
#     if user in user_request.star_user:
#         user_request.star_user.remove(user)
#         user_request_result = user_request.save()
#     else:
#         user_request.star_user.append(user)
#         user_request_result = user_request.save()
#     if user_result and user_request_result:
#         return user_request_result
#
#
# def update_answer_vote(request_answer_id, user_ID):
#     user = user_business.get_by_user_ID(user_ID)
#     request_answer = request_answer_business. \
#         get_by_request_answer_id(request_answer_id)
#
#     if request_answer in user.answer_vote_up:
#         user.answer_vote_up.remove(request_answer)
#         user_result = user.save()
#     else:
#         user.answer_vote_up.append(request_answer)
#         user_result = user.save()
#
#     if user in request_answer.votes_up_user:
#         request_answer.votes_up_user.remove(user)
#         request_answer_result = request_answer.save()
#     else:
#         request_answer.votes_up_user.append(user)
#         request_answer_result = request_answer.save()
#
#     if user_result and request_answer_result:
#         return request_answer_result.to_mongo()


# def favor_api(user_ID, api_id):
#     """
#     :param user_ID:
#     :type user_ID:
#     :param api_id:
#     :type api_id:
#     :return:
#     :rtype:
#     """
#     user = user_business.get_by_user_ID(user_ID=user_ID)
#     api = api_business.get_by_api_id(api_id=api_id)
#     # user_result, api_result = None, None
#     # 1. 在user下存favor_apis
#     if api not in user.favor_apis:
#         user.favor_apis.append(api)
#         user_result = user.save()
#     else:
#         user.favor_apis.remove(api)
#         user_result = user.save()
#     # 2. 在api下存favor_users
#     if user not in api.favor_users:
#         api.favor_users.append(user)
#         api_result = api.save()
#     else:
#         api.favor_users.remove(user)
#         api_result = api.save()
#
#     if user_result and api_result:
#         return {
#             "user": user_result.to_mongo(),
#             "api": api_result.to_mongo()
#         }
#
#
# def star_api(user_ID, api_id):
#     """
#     :param user_ID:
#     :type user_ID:
#     :param api_id:
#     :type api_id:
#     :return:
#     :rtype:
#     """
#     user = user_business.get_by_user_ID(user_ID=user_ID)
#     api = api_business.get_by_api_id(api_id=api_id)
#     # user_result, api_result = None, None
#     # 1. 在user下存star_apis
#     if api not in user.star_apis:
#         user.star_apis.append(api)
#         user_result = user.save()
#     else:
#         user.star_apis.remove(api)
#         user_result = user.save()
#     # 2. 在api下存star_users
#     if user not in api.star_users:
#         api.star_users.append(user)
#         api_result = api.save()
#     else:
#         api.star_users.remove(user)
#         api_result = api.save()
#
#     if user_result and api_result:
#         return {
#             "user": user_result.to_mongo(),
#             "api": api_result.to_mongo()
#         }
#
#
# def add_used_api(user_ID, api_id):
#     """
#     为用户增加 使用过的api
#     :param user_ID:
#     :type user_ID:
#     :param api_id:
#     :type api_id:
#     :return:
#     :rtype:
#     """
#     user = user_business.get_by_user_ID(user_ID=user_ID)
#     api = api_business.get_by_api_id(api_id=api_id)
#     user_result = None
#     if api not in user.used_apis:
#         user.used_apis.append(api)
#         user_result = user.save()
#     if user_result:
#         return {
#             "user": user_result.to_mongo(),
#         }

def send_email(email, subject, text):
    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    msg['From'] = 'service@momodel.ai <service@momodel.ai>'
    receiver = email
    msg['To'] = email
    username = 'service@momodel.ai'
    password = 'Mo123456'
    sender = 'service@momodel.ai'
    text_plain = MIMEText(text, 'html', 'utf-8')
    msg.attach(text_plain)
    smtp = smtplib.SMTP()
    smtp.connect('smtp.exmail.qq.com')
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())


def send_verification_code(phone):
    """

    :param phone:
    :type phone:
    :return: {message_id: aalalals}
    :rtype:
    """
    url = "https://api.sms.jpush.cn/v1/codes"
    payload = json.dumps({
        'mobile': phone,
        'temp_id': 1,
    })
    headers = {
        'content-type': "application/json",
        # 'authorization': "Basic MjZlZWFhM2QyNzljMzIyZTg0Zjk1NDQxOmYwMjQ2NzdiOWNjM2QxZWZmNDE0ODQxMA==",
        'authorization': "Basic ZDU4OTA1ZGE2NWQ0ZjRjNjM2NDBjZDdiOmViMmY3Yzg1YmViNDdiMDZjY2VlMzJmNw==",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    result = response.json()
    if "error" in result:
        raise Error(result["error"])
    msg_id = result["msg_id"]
    # 数据库 更改或者创建 get or create
    try:
        obj = PhoneMessageId.objects(phone=phone).get()
        obj.msg_id = msg_id
        return obj.save()
    except DoesNotExist as e:
        obj = PhoneMessageId(phone=phone, msg_id=msg_id)
        return obj.save()

    # if obj:
    #     obj.msg_id = msg_id
    #     return obj.save()
    # else:
    #     obj = PhoneMessageId(phone=phone, msg_id=msg_id)
    #     return obj.save()
    # phone_message_id = PhoneMessageId(phone=phone, msg_id=msg_id)
    # result = phone_message_id.save()
    # return result


def verify_code(code, phone):
    """

    :param code:
    :type code:
    :param phone:
    :type phone:
    :return: 验证成功返回 True, 失败抛出报错信息 {
        "code": *****,
        "message": "******"
    }
    :rtype:
    """
    try:
        msg_id = PhoneMessageId.objects(phone=phone).get().msg_id
    except:
        raise Error("无效的手机号")
    url = 'https://api.sms.jpush.cn/v1/codes/' + msg_id + '/valid'
    payload = json.dumps({
        'code': code
    })
    headers = {
        'content-type': "application/json",
        'authorization': "Basic ZDU4OTA1ZGE2NWQ0ZjRjNjM2NDBjZDdiOmViMmY3Yzg1YmViNDdiMDZjY2VlMzJmNw==",

    }

    response = requests.request("POST", url, data=payload, headers=headers)
    result = response.json()
    if "error" in result:
        raise Error(result["error"])
    return response.json()["is_valid"]
    # if is_valid:
    #     return response.json()
    # else:
    #     return make_response(jsonify({
    #         "response": response.json()
    #     }), 300)


class UserService:
    business = UserBusiness

    @classmethod
    def action_entity(cls, user_ID, entity_id, action, entity):
        user = UserBusiness.get_by_user_ID(user_ID=user_ID)
        business_mapper = {
            "app": AppBusiness,
            "module": ModuleBusiness,
            "request": UserRequestBusiness,
            "dataset": DatasetBusiness,
            "answer": RequestAnswerBusiness
        }
        business = business_mapper[entity]
        object = business.get_by_id(entity_id)
        user_keyword = '{action}_{entity}s'.format(action=action,
                                                   entity=entity)
        object_keyword = '{action}_users'.format(action=action)

        # 1. 在user下存object
        if object not in user[user_keyword]:
            refs = deepcopy(user[user_keyword])
            refs.append(object)
            user[user_keyword] = refs
            user_result = user.save()
        else:
            refs = deepcopy(user[user_keyword])
            refs.remove(object)
            user[user_keyword] = refs
            user_result = user.save()
        # 2. 在object下存users
        if user not in object[object_keyword]:
            refs = deepcopy(object[object_keyword])
            refs.append(user)
            object[object_keyword] = refs
            object_result = object.save()
        else:
            refs = deepcopy(object[object_keyword])
            refs.remove(user)
            object[object_keyword] = refs
            object_result = object.save()

        if user_result and object_result:
            # 记录event
            EventBusiness.create_event(
                user=user,
                target=object_result,
                target_type=entity,
                action=action,
            )
            # 发送 message
            if action == 'star' and user in object[object_keyword]:
                admin_user = UserBusiness.get_by_user_ID('admin')
                kwargs = {}
                if entity == 'answer':
                    message_type = 'star_answer'
                    kwargs['answer'] = object
                elif entity == 'request':
                    message_type = 'star_request'
                    kwargs['user_request'] = object
                else:
                    message_type = 'star_project'
                    kwargs['project'] = object
                receivers = [object.user]
                MessageService.create_message(sender=admin_user,
                                              message_type=message_type,
                                              receivers=receivers,
                                              user=user,
                                              **kwargs
                                              )
            return UserEntity(user=user_result, entity=object_result)

    @classmethod
    def get_statistics(cls, user_ID, page_no, page_size, action, entity_type):
        """
        获取用户统计信息

        这里需要将 app, caller 从objectID转换成json吗？
        1. service可能被其他service调用，应该在route层转换
        2. 在其他service调用时也都需要转换，保证route调用结果一致
        :param user_ID:
        :type user_ID:
        :param page_no:
        :type page_no:
        :param page_size:
        :type page_size:
        :param action:
        :type action:
        :param entity_type:
        :type entity_type:
        :return:
        :rtype:
        """
        from server3.business.statistics_business import StatisticsBusiness
        user_obj = UserBusiness.get_by_user_ID(user_ID=user_ID)
        statistics = StatisticsBusiness.get_pagination(
            query={
                "action": action,
                "entity_type": entity_type,
                "caller": user_obj
            },
            page_no=page_no, page_size=page_size)

        return statistics

    @classmethod
    def send_code_to_email(cls, user_ID, email):
        rand = str(random.randint(100000, 999999))
        user = UserBusiness.get_by_user_ID(user_ID)
        user.emailCaptcha = rand
        user.save()

        """
        f'<html><body><h1>Hi {user.username},</h1>' +
                        '<p>This is your verification code:</p>' +
                        f'<div style="background:#e7f7ff;color:#1890ff;display: inline-block;padding:5px 10px;font-size:30px;">{rand}</div>' +
                        f'<p>Please use it within 30 minute, thank you!</p>' +
                        '</body></html>'
        """
        # text = email_template(
        #     title="<h3 style='margin-left: 12px;'>Hi {0},</h3>".format(
        #         user.username),
        #     middle='<p style=\'margin-left: 24px; margin-top: 16px\'>'
        #            'This is your verification code:</p>'
        #     f'<div style="background:#e7f7ff;color:#1890ff;'
        #     f'display: inline-block;padding:5px 10px;font-size:30px; margin-top: 12px;'
        #     f'margin-left: 24px">{rand}</div>',
        #     tail="<p style='margin-left: 24px; margin-top: -16px'>"
        #          "Please use it within 30 minute, thank you!</p>")

        text = email_template(
            title="<h3 style='margin-left: 24px; line-height: 1.1;"
                  "color: #000; font-size: 27px;'>你好 {0},</h3>"
                .format(user.username),
            middle='<p style=\'margin-left: 24px; margin-top: 16px\'>'
                   '你的验证码为:</p>'
                   f'<div style="background:#e7f7ff;color:#1890ff;'
                   f'display: inline-block;padding:5px 10px;font-size:30px; margin-top: 12px;'
                   f'margin-left: 24px">{rand}</div>',
            tail="<p style='margin-left: 24px; margin-top: -16px'>"
                 "请在30分钟内使用，谢谢！</p>")

        send_email(email=email, subject='Mo Authentication', text=text)

    @classmethod
    def send_pwd_to_email(cls, email, username, password):

        # text = email_template(
        #     title="<h3 style='margin-left: 12px;'>Hi {0},</h3>".format(
        #         username),
        #     middle="<p style='margin-left: 24px; margin-top: 16px'>"
        #            "Here is your login information:</p>"
        #            "<p style='margin-left: 24px; margin-top: 12px'>"
        #            "Username: <span style='font-weight: bold;background: "
        #            "lightgray;padding: 0 5px;'>{username}</span></p>"
        #            "<p style='margin-left: 24px; margin-top: 12px'>"
        #            "Password: <span style='font-weight: bold;background: "
        #            "lightgray;padding: 0 5px;'>{password}</span></p>",
        #     tail="<a href={0}/user/login style='color: #1980FF !important;"
        #          "text-decoration:underline; margin-left: 24px; margin-top: 16px'>"
        #          "Click me to come back~</a>".format(WEB_ADDR))

        text = email_template(
            title="<h3 style='margin-left: 24px;'>Hi {0},</h3>".format(
                username),
            middle="<p style='margin-left: 24px; margin-top: 16px'>"
                   "以下是你的登陆信息：</p>"
                   "<p style='margin-left: 24px; margin-top: 12px'>"
                   "用户名： <span style='font-weight: bold;background: "
                   "lightgray;padding: 0 5px;'>{0}</span></p>"
                   "<p style='margin-left: 24px; margin-top: 12px'>"
                   "密码： <span style='font-weight: bold;background: "
                   "lightgray;padding: 0 5px;'>{1}</span></p>".format(username,
                                                                      password),
            tail="<a href={0}/user/login style='color: #1980FF !important;"
                 "text-decoration:underline; margin-left: 24px; margin-top: 16px'>"
                 "点击返回</a>".format(WEB_ADDR))

        """
        f'<html><body><h1>Hi {username},</h1>' +
                        '<p>Thank you for register!</p>' +
                        '<p>Here is your login information:</p>' +
                        f'<p>Username: <span style="font-weight: bold;background: lightgray;padding: 0 5px;">
                        {username}</span></p>' +
                        f'<p>Password: <span style="font-weight: bold;background: lightgray;padding: 0 5px;">
                        {password}</span></p>' +
                        f'<p><a href="{WEB_ADDR}/user/login" '
                        f'style="">Click me to come back~</a></p>' +
                        '</body></html>'
        """
        send_email(email=email, subject='Mo Password',
                   text=text)

    @classmethod
    def update_user_email(cls, user_ID, email, captcha):
        user = UserBusiness.get_by_user_ID(user_ID)

        if captcha and getattr(user, 'emailCaptcha',
                               None) and captcha == user.emailCaptcha:
            user.email = email
            user.emailCaptcha = None
            user.email_verified = True
            user.save()
            return user
        else:
            raise Error("验证码错误")

    @classmethod
    def add_rss(cls, rss_url=None, title=None, user_ID=None):
        user = UserBusiness.get_by_user_ID(user_ID)
        rss_list = user.rssList
        for rss in rss_list:
            if rss.get('url') == rss_url:
                return False
        new_rss = {
            'url': rss_url,
            'title': title
        }
        user.rssList.append(new_rss)
        user.save()
        return user

    @classmethod
    def del_rss(cls, url=None, user_ID=None):
        user = UserBusiness.get_by_user_ID(user_ID)
        rssList = user.rssList
        findRssIdx = None
        for idx in range(len(rssList)):
            if rssList[idx]['url'] == url:
                findRssIdx = idx
        # print('findRssIdx', findRssIdx)
        if findRssIdx or findRssIdx == 0:
            user.rssList.pop(findRssIdx)
            user.save()
            return user
        else:
            return False

    @classmethod
    def update_user_avatar(cls, user_ID, base64_str):
        base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
        byte_data = base64.b64decode(base64_data)
        img_data = BytesIO(byte_data)
        img = Image.open(img_data)
        img = img.convert('RGB')
        rand_str = gen_rand_str(6)
        rand_name = f'{user_ID}-{rand_str}.jpg'
        with tempfile.TemporaryDirectory() as temp_path:
            tmp_img_path = f'{temp_path}/{user_ID}.jpg'
            img.save(tmp_img_path.replace('\\', '/'))
            upload_file(rand_name, tmp_img_path)
        return cls.business.repo.update_img_url(user_ID,
                                                f'{UPLOADED_IMG_BASE}/{rand_name}')

    @classmethod
    def authenticate(cls, username, password):
        # user = UserBusiness.get_by_user_ID(username)
        user = UserBusiness.get_by_username(username)
        if user and check_password_hash(user.password, password):
            user.id = str(user.id)
            return user
        return False

    @classmethod
    def gen_user_ID(cls, username):
        user_ID = secure_name(username)
        return gen_rand_name(user_ID, cls.business.get_by_user_ID, 3)

    @classmethod
    def gen_temp_user(cls):
        username = ObjectId().__str__()
        password = ObjectId().__str__()
        email = ObjectId().__str__() + '@gmail.com'
        # 邀请码
        invitation_code = UserBusiness.generate_invitation_code()
        return cls.register(username=username, password=password,
                            email=email, register_state=0,
                            invitation_code=invitation_code)

    @classmethod
    def fill_temp_user(cls):
        cls.recycle_temp_user()
        users = cls.business.read({'register_state': 0})
        print('register_state 0 left user number: ', len(users))
        for _ in range(TEMP_USER_TOTAL_NUM - len(users)):
            user, _ = cls.gen_temp_user()
            if user:
                print('gen_temp_user: ', user.user_ID)

    @classmethod
    def recycle_temp_user(cls):
        users = cls.business.read({'register_state': 1})
        print('register_state 1 user number: ', len(users))
        i = 0
        for user in users:
            c = user.register_state_update_time - datetime.utcnow()
            if (c.total_seconds() / 3600.0) > TEMP_USER_EXPIRE_HOURS:
                user.register_state = 0
                user.phases = [0, 0]
                user.save()
                i += 1
        print('register_state 1 user recycled number: ', i)

    @classmethod
    def add_user_wrapper(cls, username, password, **kwargs):
        if 'user_ID' in kwargs:
            user_ID = kwargs.pop('user_ID')
        else:
            user_ID = cls.gen_user_ID(username)

        verify_key = token_utility.generate_key()

        return cls.add(username=username, user_ID=user_ID,
                       password=password,
                       api_key=verify_key, **kwargs)

    @classmethod
    def register(cls, username, password, **kwargs):
        fork = kwargs.pop('fork', None)
        # 验证失败会抛出错误
        # verify_code(code=code, phone=phone)

        # register_state == 0 means temp user generation,
        # register_state != 0 means real registration
        if kwargs.get('register_state') != 0:

            user_ID = get_jwt_identity()
            if len(UserBusiness.filter(user_ID=user_ID,
                                       register_state=2)) > 0:
                raise Error('user already registered')
            if not user_ID:
                user = User._get_collection().find_one_and_update(
                    {'register_state': 0}, {
                        '$set': {'register_state': 1,
                                 'register_state_update_time': datetime.utcnow()}})
                if not user:
                    # set register_state to create tutorial project
                    kwargs['register_state'] = 0
                    user = cls.add_user_wrapper(username, password, **kwargs)
                    user_ID = user.user_ID
                else:
                    user_ID = user.get('user_ID')

            cls.add_git_http_user(user_ID, password)
            cls.change_git_http_user_pwd(user_ID, password)
            hashed_password = generate_password_hash(password)
            data = {
                'username': username,
                'password': hashed_password,
                'register_state': 2,
                'register_state_update_time': datetime.utcnow(),
                'phases': [0, 0]
            }
            data.update(kwargs)
            added_user = cls.business.update_by_user_ID(user_ID, data)

            if 'email_verified' not in kwargs or (
                    'email_verified' in kwargs and not kwargs.get(
                'email_verified',
                False)):
                eventlet.spawn_n(cls.activate_send_email, added_user)

            # todo 增加一个新用户
            try:
                eventlet.spawn_n(SearchService.add_user, added_user.user_ID,
                                 added_user.username,
                                 added_user.bio if added_user.bio else '',
                                 added_user.avatarV if added_user.avatarV else '',
                                 added_user.avatar_url if added_user.avatar_url else '')
            except:
                print('es error')

            try:
                # register on rocket chat
                eventlet.spawn_n(RocketChatBusiness.create,
                                 email=added_user.email,
                                 name=username,
                                 password=password,
                                 username=added_user.rocket_chat_name)
            except:
                print('rc error')

            try:
                eventlet.spawn_n(RocketChatBusiness.update,
                                 user=added_user,
                                 name=username,
                                 username=added_user.rocket_chat_name)
            except:
                print('rc error')
        else:

            added_user = cls.add_user_wrapper(username, password, **kwargs)
            # cls.activate_send_email(added_user)
            # LevelTaskBusiness.init_user_tasks(added_user)

        # added_user = json_utility.convert_to_json(added_user.to_mongo())
        # added_user.pop('password')
        # 为新用户创建tutorial project
        from server3.service.app_service import AppService
        user_token = create_access_token(identity=added_user.user_ID)

        # create first app project
        # app_tut = AppService.create_tutorial_project(
        #     user_ID=added_user["user_ID"],
        #     user_token=user_token,
        #     num=1, level=1
        # )
        # added_user.set_tut('app_tutorial', app_tut)

        # create default tutorial project
        def create_base_tut():
            print('added_user', added_user['user_ID'])
            added_user.save()
            base_tut = AppService.create_tutorial_project(
                user_ID=added_user["user_ID"],
                user_token=user_token)
            added_user.set_tut('base_tutorial', base_tut)

        if fork == 'true':
            eventlet.spawn_n(create_base_tut)
        elif kwargs.get('register_state') == 0:
            create_base_tut()

        return added_user, user_token

    # 激活邮箱
    @classmethod
    def activate_send_email(cls, user):
        email = user.email
        smtpserver = 'smtp.exmail.qq.com'
        username = 'service@momodel.ai'
        password = 'Mo123456'
        sender = 'service@momodel.ai'
        subject = 'Mo Authentication'
        msg = MIMEMultipart('mixed')
        msg['Subject'] = subject
        msg['From'] = 'service@momodel.ai <service@momodel.ai>'
        receiver = email
        msg['To'] = email
        time_number = str(int(datetime.now().timestamp()))

        random_number = str(random.randint(random.randint(1, 999999),
                                           random.randint(999999,
                                                          99999999999)))
        h = hashlib.md5(bytes(random_number, encoding="utf-8"))
        h.update(email.encode("utf-8"))

        user.hash_email = h.hexdigest() + time_number
        user.email_verified = False
        user.save()

        text = email_template(
            title="<h3 style='margin-left: 24px; line-height: 1.1;"
                  "color: #000; font-size: 27px;'>你好 {0},</h3>"
                  "<p style='margin-left: 24px; margin-top: 36px; '>"
                  "请点击以下链接激活你的邮箱，"
                  "如果你没有操作请忽略这条信息：</p>".format(user.username),
            middle="<a href= {0}/confirm_email?"
                   "&hashEmail={1} target='_blank' style='color: #1980FF !important;"
                   "text-decoration:underline;margin-left: 24px;font-size: 24px;'>"
                   "激活邮箱</a>".format(WEB_ADDR, user.hash_email),
            tail="<div style='margin-left: 24px; margin-top: -24px; list-style-position: inside;"
                 " padding: 16px 0 ;'>如果你没有进行这个操作 "
                 "请尽快联系我们 <a href='mailto:service@momodel.ai' "
                 "style='color: #1980FF !important; font-weight: bold;"
                 "text-decoration: none;line-height: 1.8;padding-left: 2px;padding-right: 2px;"
                 "text-decoration:underline;'>"
                 "service@momodel.ai")

        # text = user.user_ID + ',\n please click the following link to reset your password. ' \
        #                       'Ignore this message if it is not your operation.\n ' + \
        #        WEB_ADDR + '/confirm_email?hashEmail=' + user.hash_email
        text_plain = MIMEText(text, 'html', 'utf-8')
        msg.attach(text_plain)
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)
        smtp.login(username, password)
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()

    # 激活邮箱，前端返回后的处理
    @classmethod
    def activate_email(cls, hash_email):
        try:
            user = UserBusiness.get_by_hash_email(hash_email)
            if user.email_verified:
                return True
            time_send_email = int(hash_email[32:])
            time_now = int(datetime.now().timestamp())
            if time_now - time_send_email < 3600 * 48:
                user.email_verified = True
                # del user.hash_email
                invited_by = user.invited_by
                admin_user = UserBusiness.get_by_user_ID('admin')
                if user.special_invitation in INVITATION_CODE:
                    # 使用官方邀请码的人，赠送三小时
                    UserBusiness.change_gpu_time(user, 3600 * 3)
                    UserBusiness.change_project_number_limit(user, [1, 1, 1])
                    MessageService.create_message(admin_user,
                                                  f'gpu_time_extend',
                                                  [user],
                                                  gpu_time_extend=3600 * 3)
                elif invited_by:
                    UserBusiness.change_gpu_time(invited_by, 3600)
                    UserBusiness.change_project_number_limit(invited_by,
                                                             [1, 1, 1])
                    UserBusiness.change_gpu_time(user, 3600)
                    UserBusiness.change_project_number_limit(user, [1, 1, 1])
                    MessageService.create_message(admin_user,
                                                  f'gpu_time_extend',
                                                  [user, invited_by])
                MessageService.create_message(admin_user, f'email_confirm',
                                              [user])
                user.save()
                return True
            else:
                return False
        except DoesNotExist:
            return False

    @classmethod
    def _invited_by_user(cls, invited_by, user):
        """
        被邀请者使用第三方登录获得时长添加
        :param hashcode:
        :return:
        """
        # 解析
        if datetime.date.today() >= datetime.date(2018, 12, 12) and invited_by:
            try:
                # 如果 invited_by 是官方的邀请码
                if invited_by in INVITATION_CODE:
                    # 使用官方邀请码的人，赠送三小时
                    UserBusiness.change_gpu_time(user, 3600 * 3)
                    # 更新刚才注册的用户的 邀请人信息及官方注册码信息
                    admin_user = UserBusiness.get_by_user_ID('admin')
                    UserBusiness.update_by_user_ID(user.user_ID,
                                                   {'invited_by': admin_user,
                                                    'special_invitation': invited_by
                                                    })
                else:
                    invited_by = UserBusiness. \
                        get_by_invitation_code(invited_by)

                    # 保存邀请人信息
                    UserBusiness.update_by_user_ID(user.user_ID,
                                                   {'invited_by': invited_by})
                    # 增加邀请人和被邀请人的 GPU 时长
                    UserBusiness.change_gpu_time(invited_by, 3600)
                    UserBusiness.change_gpu_time(user, 3600)
                    UserBusiness.change_project_number_limit(invited_by,
                                                             [1, 1, 1])
                    UserBusiness.change_project_number_limit(invited_by,
                                                             [1, 1, 1])

                    # 发送消息通知
                    admin_user = UserBusiness.get_by_user_ID('admin')
                    MessageService.create_message(admin_user,
                                                  f'gpu_time_extend',
                                                  [invited_by, user])
            except:
                pass

    @classmethod
    def oauth(cls, code, state):
        user_token = None
        res_json = requests.post(GitHubConsts.TOKEN_URL,
                                 headers={
                                     'Accept': 'application/json'
                                 },
                                 json={'code': code,
                                       'client_id': GitHubClient.CLIENT_ID,
                                       'client_secret':
                                           GitHubClient.CLIENT_SECRET}).json()
        access_token = res_json['access_token']
        github_user_info = requests.get(
            f'{GitHubConsts.GET_USER_URL}{access_token}').json()
        github_user_emails = requests.get(
            f'{GitHubConsts.GET_USER_EMAIL_URL}{access_token}').json()
        github_user_info['email'] = github_user_emails[0]['email']
        for key in GitHubConsts.GITHUB_RENAME_KEYS:
            github_user_info[f'github_{key}'] = github_user_info.pop(key)
        username = github_user_info.pop('login')
        github_user_info['oauth_id'] = username

        # 记录此用户来自 github
        github_user_info['oauth_from'] = 'github'

        try:
            exists_user = UserBusiness.get_by_oauth_id(username)
            if hasattr(exists_user, 'github_id') and exists_user.github_id == \
                    github_user_info['github_id']:
                user = exists_user
            else:
                user = None
        except DoesNotExist:
            password = gen_rand_str(N=8)
            try:
                states = state.split(';')
                user, user_token = cls.register(username=username,
                                                password=password,
                                                **github_user_info)
                if len(states) > 1 and states[1].replace(' ',
                                                         '') != '' and user:
                    # 被邀请的
                    invited_by = states[1]
                    cls._invited_by_user(invited_by, user)
            except NotUniqueError:
                user = None
            else:
                cls.send_pwd_to_email(user.email, username, password)
                user.email_verified = True

        if not user_token and user:
            user_token = create_access_token(identity=user.user_ID)
        return user, user_token

    @classmethod
    def oauth_wechat(cls, code, state=None):
        """
            access_token默认有效期
        :param code:
        :param state:
        :return:
        """
        user_token = None
        # 请求 access_token
        access_token_json = requests.get(WechatConstants.ACCESS_TOKEN_URL.
            format(
            WechatConstants.WECHAT_APP_SECRET, code)).json()
        if 'access_token' in access_token_json:
            refresh_token = access_token_json.get('refresh_token')
        else:
            # code 非法
            error_code = access_token_json.get('errcode')
            error_msg = access_token_json.get('errmsg')
            logging.warning(
                '微信登录获取 access_token 失败, errorCode:{0}, errorMsg: {1}'.format(
                    error_code, error_msg))
            return user_token, user_token
        # 刷新时长
        refresh_token_json = requests.get(
            WechatConstants.REFRESH_TOKEN_URL.format(refresh_token)).json()
        if 'access_token' in refresh_token_json:
            refresh_token = refresh_token_json.get('refresh_token')
            access_token = refresh_token_json.get('access_token')
            openid = refresh_token_json.get('openid')
        else:
            # 刷新失败, token非法
            error_code = refresh_token_json.get('errcode')
            error_msg = refresh_token_json.get('errmsg')
            logging.warning(
                '微信登录 refresh_token 失败, errorCode:{0}, errorMsg: {1}, 所有信息:{2}'.
                    format(error_code, error_msg, refresh_token_json))
            return user_token, user_token
        # 检测Token是否有效
        auth_json = requests.get(
            WechatConstants.TOKEN_IS_AUTH_URL.format(access_token,
                                                     openid)).json()
        logging.warning(auth_json)
        # 请求用户数据
        user_info = requests.get(
            WechatConstants.USER_INFO_URL.format(access_token, openid)).json()
        # print('user_info:', user_info)
        if 'unionid' in user_info:
            unionid = user_info.get('unionid')
            try:
                user = UserBusiness.get_by_oauth_id(unionid)
            except DoesNotExist as e:
                try:
                    user = UserBusiness.get_by_user_ID(unionid)
                except DoesNotExist as e:
                    # 在这里为注册用户
                    user_dict = {}
                    # 解析出一致的字段, 符合我们的数据库, 城市相关信息我们无法使用, 暂时不做读取
                    user_dict['avatar_url'] = user_info.get('headimgurl')
                    if user_info.get('sex') == 1:
                        # 微信端返回时男性
                        user_dict['gender'] = 1
                    elif user_info.get('sex') == 2:
                        user_dict['gender'] = 0
                    else:
                        user_dict['gender'] = 2
                    # user_dict['gender'] = user_info.get('sex')
                    user_dict['email_verified'] = True
                    # 注册完, 让填写一个邮箱账号用于验证
                    # 使用 unionid 作为用户 name 以及 user_id

                    # 记录此用户来自 wechat
                    user_dict['oauth_from'] = 'wechat'
                    password = gen_rand_str(N=8)
                    username = unionid
                    user_dict['oauth_id'] = username
                    print('user_info_创建用户:', user_info)
                    try:
                        states = state.split(';')
                        user, user_token = cls.register(username, password,
                                                        **user_dict)

                        if len(states) > 1 \
                                and states[1].replace(' ', '') != '' \
                                and user:
                            # 被邀请的
                            invited_by = states[1]
                            cls._invited_by_user(invited_by, user)
                        # 获取用户头像, 并更新
                        cls.get_wechat_avatar(user.user_ID,
                                              user_dict['avatar_url'])
                    except NotUniqueError as e:
                        user = None
                        print('用户已存在', e)
            if not user_token and user:
                user_token = create_access_token(identity=user.user_ID)
        else:
            # 获取数据失败
            error_code = refresh_token_json.get('errcode')
            error_msg = refresh_token_json.get('errmsg')
            logging.warning(
                '微信登录获取用户数据失败, errorCode:{0}, errorMsg: {1}, user_info:{2}'.
                    format(error_code, error_msg, user_info))
            user = None
        return user, user_token

    @classmethod
    def get_wechat_avatar(cls, user_ID,
                          url='http://thirdwx.qlogo.cn/mmopen/vi_32/'
                              'Q0j4TwGTfTJ7KibPZesBookqE3Ntbib0Urg5o3jPdS1VHicyaEdi'
                              'bzTP3loWicsDFO4vz9mqJVR4NOdzwAlDqVKgjwg/132'):
        avatar = requests.get(url).content
        rand_str = gen_rand_str(6)
        rand_name = f'{user_ID}-{rand_str}.jpg'
        with tempfile.TemporaryDirectory() as temp_path:
            tmp_img_path = f'{temp_path}/{user_ID}.jpg'
            with open(tmp_img_path, 'wb') as img:
                img.write(avatar)
            print(upload_file(rand_name, tmp_img_path))
            print(f'{UPLOADED_IMG_BASE}/{rand_name}')
            return cls.business.repo.update_img_url(user_ID,
                                                    f'{UPLOADED_IMG_BASE}/{rand_name}')

    @classmethod
    def add(cls, user_ID, password, **kwargs):
        # cls.add_git_http_user(user_ID, password)
        hashed_password = generate_password_hash(password)
        return UserBusiness.add(user_ID, hashed_password, **kwargs)

    @classmethod
    def add_git_http_user(cls, user_ID, password):
        """
        add_git_http_user
        :param user_ID:
        :param password:
        :param user_token:
        :return: dict of res json
        """
        return requests.post(f'{GIT_SERVER}/git/{user_ID}',
                             json={'password': password})

    @classmethod
    def change_git_http_user_pwd(cls, user_ID, password):
        """
        add_git_http_user
        :param user_ID:
        :param password:
        :param user_token:
        :return: dict of res json
        """
        return requests.put(f'{GIT_SERVER}/git/{user_ID}',
                            json={'password': password})

    @classmethod
    def verify_code(cls, code, phone):
        """

        :param code:
        :type code:
        :param phone:
        :type phone:
        :return: 验证成功返回 True, 失败抛出报错信息 {
            "code": *****,
            "message": "******"
        }
        :rtype:
        """
        try:
            msg_id = PhoneMessageId.objects(phone=phone).get().msg_id
        except:
            raise Error("无效的手机号")
        url = 'https://api.sms.jpush.cn/v1/codes/' + msg_id + '/valid'
        payload = json.dumps({
            'code': code
        })
        headers = {
            'content-type': "application/json",
            'authorization': "Basic ZDU4OTA1ZGE2NWQ0ZjRjNjM2NDBjZDdiOmViMmY3Yzg1YmViNDdiMDZjY2VlMzJmNw==",
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        result = response.json()
        if "error" in result:
            raise Error(result["error"])
        return response.json()["is_valid"]

    @classmethod
    @check_api_key
    def auth_and_create_invoke(cls, module_identity, user_ID,
                               project_id=None,
                               project_type=None, source_file_path=None,
                               run_args=None):
        """
        check api_key correctness and count this call
        :param module_identity:
        :param project_id:
        :param project_type:
        :param api_key:
        :param source_file_path:
        :param user_ID:
        :param run_args:
        :return:
        """
        user = UserBusiness.get_by_user_ID(user_ID)
        [encoded_name, version] = module_identity.split('/')
        version = '_'.join(version.split('.'))
        module = ModuleBusiness.get_by_encoded_name(encoded_name)
        in_entity = None
        if project_id and project_type:
            from server3.service.project_service import TypeMapper
            project_cls = TypeMapper.get(project_type)
            in_entity = project_cls.get_by_id(project_id)

        return EventBusiness.create_event(
            user=user,
            target=module,
            target_type='module',
            action="invoke",
            in_entity=in_entity,
            source_file_path=source_file_path,
            input=run_args,
            version=version
        )
        # return response.json()["is_valid"]

    @classmethod
    def compute_fork_star_favor_num(cls, user, access_user_ID=None):
        if access_user_ID and access_user_ID == user.user_ID:
            project = ProjectBusiness.repo.read(
                {'user': user, 'classroom': False})
        else:
            project = ProjectBusiness.repo.read(
                {'user': user, 'privacy': 'public', 'classroom': False})
        request = UserRequestBusiness.get_by_user(user=user)
        answer = RequestAnswerBusiness.get_by_user(user=user)
        project_info = project.aggregate(
            {
                '$lookup':
                    {
                        'from': "project",
                        'localField': "_id",
                        'foreignField': "source_project",
                        'as': "forks"
                    }
            },
            {
                '$group': {
                    '_id': '$_id',
                    'pro_stars_num': {'$sum': {"$size": {"$ifNull": [
                        "$projects.favor_users",
                        []]}}},
                    'pro_favors_num': {'$sum': {"$size": {"$ifNull": [
                        "$projects.star_users",
                        []]}}},
                    'pro_forks_num': {'$sum': {"$size": {"$ifNull": [
                        "$forks",
                        []]}}},
                }
            }
        )
        request_info = request.aggregate(
            {
                '$group': {
                    '_id': '$_id',
                    'request_stars_num': {'$sum': {"$size": {"$ifNull": [
                        "$favor_users",
                        []]}}},
                    'request_favors_num': {'$sum': {"$size": {"$ifNull": [
                        "$star_users",
                        []]}}}
                }
            },
        )
        answer_info = answer.aggregate(
            {
                '$group': {
                    '_id': '$_id',
                    'answer_stars_num': {'$sum': {"$size": {"$ifNull": [
                        "$favor_users",
                        []]}}},
                    'answer_favors_num': {'$sum': {"$size": {"$ifNull": [
                        "$star_users",
                        []]}}}
                }
            },
        )

        star_number = 0
        # 被收藏次数
        by_favor_number = 0
        fork_project_number = 0
        for p_info in project_info:
            if len(p_info) > 0:
                star_number += p_info['pro_stars_num']
                by_favor_number += p_info['pro_favors_num']
                fork_project_number += p_info['pro_forks_num']

        for r_info in request_info:
            if len(r_info) > 0:
                star_number += r_info['request_stars_num']
                by_favor_number += r_info['request_favors_num']

        for a_info in answer_info:
            if len(a_info) > 0:
                star_number += a_info['answer_stars_num']
                by_favor_number += a_info['answer_favors_num']
        favor_number = 0
        # if user.user_ID != access_user_ID:
        for favor in [user.favor_apps, user.favor_modules,
                      user.favor_datasets]:
            for p in favor:
                if p.privacy == 'public' and p.user.user_ID != user.user_ID:
                    favor_number += 1
        for req in user.favor_requests:
            if req.user.user_ID != user.user_ID:
                favor_number += 1
        # else:
        #     favor_number = len(user.favor_requests) + len(user.favor_apps) + \
        #                    len(user.favor_modules) + len(user.favor_datasets) + len(user.favor_requests)
        return star_number, favor_number, fork_project_number, project.count(), request.count(), answer.count()

    @classmethod
    def forgot_send(cls, user):
        email = user.email
        smtpserver = 'smtp.exmail.qq.com'
        username = 'service@momodel.ai'
        password = 'Mo123456'
        sender = 'service@momodel.ai'
        subject = 'Mo Authentication'
        msg = MIMEMultipart('mixed')
        msg['Subject'] = subject
        msg['From'] = 'service@momodel.ai <service@momodel.ai>'
        receiver = email
        msg['To'] = email
        random_number = str(random.randint(random.randint(1, 999999),
                                           random.randint(999999,
                                                          99999999999)))
        h = hashlib.md5(bytes(random_number, encoding="utf-8"))
        h.update(email.encode("utf-8"))

        user.hash_email = h.hexdigest()
        user.save()

        # text = email_template(title="<h3 style='margin-left: 12px;'>Hi {0},</h3>"
        #                             "<p style='margin-left: 24px; margin-top: 36px'>"
        #                             "Please click the following link to reset your password, "
        #                             "ignore this message if it is not your operation:</p>".format(user.username),
        #                       middle="<a href= {0}/newpassword?email={1}&user={2}"
        #                              "&hashEmail={3} target='_blank' style='color: #1980FF !important;"
        #                              "text-decoration:underline;margin-left: 24px;font-size: 24px;'>"
        #                              "Change your password</a>".
        #                       format(WEB_ADDR, email, user.user_ID, h.hexdigest()),
        #                       tail="<div style='margin-left: 24px; margin-top: -24px'>If you did NOT make this change, "
        #                            "please contact us immediately at <a href='mailto:service@momodel.ai' "
        #                            "style='color: #1980FF !important;"
        #                            "text-decoration:underline;'>"
        #                            "service@momodel.ai"
        #                            "</a><div>"
        #                            "<div>Your password won't change "
        #                            "until you access the link above and create a new one.</div>")

        text = email_template(
            title="<h3 style='margin-left: 12px; line-height: 1.1;"
                  "color: #000; font-size: 27px;'>你好 {0},</h3>"
                  "<p style='margin-left: 24px; margin-top: 36px;'>"
                  "请点击以下链接去重置你的密码，"
                  "如果你没有操作请忽略这条信息：</p>".format(user.username),
            middle="<a href= {0}/user/newpassword?email={1}&user={2}"
                   "&hashEmail={3} target='_blank' style='color: #1980FF !important;"
                   "text-decoration:underline;margin-left: 24px;font-size: 24px;'>"
                   "修改密码</a>".
                format(WEB_ADDR, email, user.user_ID, h.hexdigest()),
            tail="<div style='margin-left: 24px; margin-top: -24px; list-style-position: inside;'>"
                 "如果你没有进行密码修改操作，"
                 "请尽快联系我们<a href='mailto:service@momodel.ai' "
                 "style='color: #1980FF !important; font-weight: bold; line-height: 1.8; "
                 "text-decoration:underline; padding-left: 2px; padding-right: 2px;'>"
                 "service@momodel.ai"
                 "</a><div>"
                 "<div style='list-style-position: inside; padding: 16px 0 ;'>"
                 "你的密码不会被修改 "
                 "除非你点击链接修改一个新的密码。</div>")

        # text = f'<html><body><h1>Hi {user.username},</h1>' + \
        #        '<p>please click the following link to reset your password,' \
        #        ' Ignore this message if it is not your operation.:</p>' + \
        #        f'<div style="background:#e7f7ff;color:#1890ff;display: ' \
        #        f'inline-block;padding:5px 10px;font-size:18px;">' \
        #        f'<a href= {WEB_ADDR}/newpassword?email={email}&user={user.user_ID}&hashEmail={h.hexdigest()}> \
        #         change your password</a></div>' + \
        #        f'<p>Don\'t forward this email to anyone else, thank you!</p>' + \
        #        '</body></html>'

        # text = user.user_ID + ',\n please click the following link to reset your password. ' \
        #                       'Ignore this message if it is not your operation.\n ' + \
        #        WEB_ADDR + '/newpassword?email=' + email + '&user=' + user.user_ID + '&hashEmail=' + h.hexdigest()
        text_plain = MIMEText(text, 'html', 'utf-8')
        msg.attach(text_plain)
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)
        smtp.login(username, password)
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()

    @classmethod
    def reset_password(cls, phone, message_id, code, new_password):
        # 验证
        result = cls.verify_code(code, message_id)
        if result:
            user = UserBusiness.get_by_phone(phone=phone)
            user.password = generate_password_hash(new_password)
            cls.change_git_http_user_pwd(user.user_ID,
                                         password=new_password)
            return user.save()

    @classmethod
    def new_password_send(cls, password, hash_email):
        user = UserBusiness.get_by_hash_email(hash_email)
        user['password'] = generate_password_hash(password)
        del user.hash_email
        user.save()
        return user

    @classmethod
    def send_verification_code(cls, phone):
        """

        :param phone:
        :type phone:
        :return: {message_id: aalalals}
        :rtype:
        """
        url = "https://api.sms.jpush.cn/v1/codes"
        payload = json.dumps({
            'mobile': phone,
            'temp_id': 1,
        })
        # authorization 的生成方法见 https://docs.jiguang.cn/jsms/server/rest_api_jsms/
        headers = {
            'content-type': "application/json",
            # 'authorization': "Basic MjZlZWFhM2QyNzljMzIyZTg0Zjk1NDQxOmYwMjQ2NzdiOWNjM2QxZWZmNDE0ODQxMA==",
            'authorization': "Basic ZDU4OTA1ZGE2NWQ0ZjRjNjM2NDBjZDdiOmViMmY3Yzg1YmViNDdiMDZjY2VlMzJmNw==",
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        result = response.json()
        if "error" in result:
            raise Error(result["error"])
        msg_id = result["msg_id"]
        # 数据库 更改或者创建 get or create
        try:
            obj = PhoneMessageId.objects(phone=phone).get()
            obj.msg_id = msg_id
            return obj.save()
        except DoesNotExist as e:
            obj = PhoneMessageId(phone=phone, msg_id=msg_id)
            return obj.save()

    @classmethod
    def check_tourtip(cls, user_ID):
        user = UserBusiness.get_by_user_ID(user_ID)
        if user:
            return user
        return False

    @classmethod
    def no_tourtip(cls, user_ID):
        user = UserBusiness.get_by_user_ID(user_ID)
        if user:
            user.tourtip = 1
            user.save()
            return user
        return False

    @classmethod
    def check_learning(cls, user_ID):
        user = UserBusiness.get_by_user_ID(user_ID)
        if user:
            return user
        return False

    @classmethod
    def no_learning(cls, user_ID):
        user = UserBusiness.get_by_user_ID(user_ID)
        if user:
            user['welcome'] = "1"
            user.save()
            return user
        return False

    @classmethod
    def update_phase(cls, user_ID, phase, type_index, tutorial_finish=None):
        user = cls.business.get_by_user_ID(user_ID)
        user.update_phase(phase, type_index, tutorial_finish)
        return user


# 添加官方账号, 跳过前端的用户名长度判断
if __name__ == '__main__':
    # user = UserBusiness.get_by_user_ID('yss')
    # UserService.activate_send_email(user)
    # UserService.activate_email('1573560752@qq.com', '9c51f04248723ef5c5663e46b66b8ff21545903594')
    # username = 'Mo'
    # password = 'service@momodel.ai'
    # email = 'service@momodel.ai'
    # user = UserService.register(username=username, password=password, email=email)
    # print(user)
    # UserService.get_wechat_avatar('chentiyun')

    # 为每个用户生成邀请码
    from server3.entity.user import User

    users = User.objects()
    print(f'len_users, {len(users)}')
    for key, user in enumerate(users):
        print(key, user.user_ID)
        new_invitation_code = UserBusiness.generate_invitation_code()
        user.invitation_code = new_invitation_code
        user.save()
