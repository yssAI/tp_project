# -*- coding: UTF-8 -*-
from flask_socketio import SocketIO
from server3.utility import json_utility
from server3.constants import REDIS_SERVER

socketio = SocketIO(message_queue=REDIS_SERVER)

epoch = 0


def emit_notification(message, created_receivers):
    for receiver in created_receivers:
        receiver_user = receiver.user
        message.is_read = False
        message.receiver_id = [receiver.id]
        if message.user:
            message.user_ID = message.user.user_ID
            message.username = message.user.username
        if message.user_request:
            message.user_request_title = message.user_request.title
            message.user_request_type = message.user_request.type
            message.request_user_ID = message.user_request.user.user_ID
            message.request_username = message.user_request.user.username
        if message.project:
            message.project_name = message.project.name
            message.project_display_name = message.project.display_name
            message.project_type = message.project.type
            message.project_id = message.project.id
            message.is_tutorial = message.project.is_tutorial
            message.project_collaborators = [c.to_mongo() for c in
                                             message.project.collaborators]
        if message.answer and message.answer.user_request:
            message.user_request_title = message.answer.user_request.title
            message.user_request_type = message.answer.user_request.type
            message.user_request = message.answer.user_request
        # task
        if message.task:
            message.task_type = message.task.task_type
            message.sponsor = message.task.sponsor.user_ID
            message.task_title = message.task_type + '-' + str(message.task.id)
            message.display_name = message.project.display_name
        # print(22222, message.project)
        msg = json_utility.convert_to_json(
            {'receiver_id': receiver.id,
             'message': message.to_mongo(),
             })
        # print('notification', msg, receiver_user.user_ID)
        socketio.emit('notification', msg,
                      namespace='/log/%s' % receiver_user.user_ID)


def emit_refresh_event(message, user_ID):
    # print(message, user_ID)
    socketio.emit('refresh', message,
                  namespace=f'/log/{user_ID}')


def emit_world_message(world):
    if hasattr(world, "sender") and world.sender:
        world.sender_user_ID = world.sender.user_ID
    else:
        world.sender_user_ID = "system"

    world_message = json_utility.convert_to_json(world.to_mongo())
    socketio.emit('world', world_message, namespace='/log')


def emit_create_project(user_ID, state, source_project, display_name,
                        project_type, rand_num_str=None):
    msg = json_utility.convert_to_json(
        {
            'user_ID': user_ID,
            'state': state,
            'source_project': source_project,
            'project_name': display_name,
            'project_type': project_type,
            'rand_num_str': rand_num_str,
        })
    socketio.emit('create_project', msg,
                  namespace='/log/%s' % user_ID)


def emit_deploy_project(user_ID, project_id, state, version):
    msg = json_utility.convert_to_json(
        {
            'user_ID': user_ID,
            'project_id': project_id,
            'state': state,
            'version': version,
        })
    socketio.emit('deploy_project', msg,
                  namespace='/log/%s' % user_ID)


def send_ping():
    socketio.emit('ping event', '', namespace='/ping_pong')
