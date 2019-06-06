# ENV = 'CY'
# 本地跑
# ENV = 'DEFAULT'
ENV = 'SDH'


if ENV == 'LOCAL':
    # LOCAL
    MONGO = 'LOCAL'


elif ENV == 'SDH':
    MONGO = 'SDH'
    TF_SERVING_URL = 'localhost:8500'

elif ENV == 'CY':
    # CY
    MONGO = 'CY'
    # REDIS_SERVER need to be changed to localhost on 小米机器 itself
    REDIS_SERVER = 'redis://192.168.31.9:6379'
    GIT_SERVER = 'http://192.168.31.9:2333'
    GIT_SERVER_IP = '192.168.31.9'
    GIT_LOCAL = f'admin@{GIT_SERVER_IP}:'
    RC_SERVER_URL = 'http://localhost:8818/'
    RC_ADMIN_ID = 'mo'
    RC_ADMIN_PW = '123456'
    IPFS_SERVER = 'http://localhost'
    JOB_IMAGE_CPU = 'magicalion/singleuser-job:dev'
    JOB_IMAGE_GPU = 'magicalion/singleuser-job:dev-gpu'
    HUB_SERVER = 'http://localhost:8000/hub_api'
    NFS_SERVER = 'http://192.168.31.11:2555'
    NFS_IP = '192.168.31.11'
    JOB_STAGING_CLAIM = 'nfs-pvc-job-staging-dev'
    USER_DIR_CLAIM = 'nfs-pvc-user-dir-dev'
    HOST_JOB_STAGING = '/mnt/job_staging_dev'
    HOST_USER_DIRECTORY = '/mnt/user_directory_dev'
    PY_SERVER = 'http://192.168.31.23:8899/pyapi'
    BROKER_SERVICE_HOST = '192.168.31.11:32570'
    SAMPLE_APP_ID = '5baf1488b5113448e5556e29'
    SAMPLE_DEPLOY_APP_ID = '5bfd118f1afd942b66b36b30'
    GPU_NODE = 'node1'
    DOCKER_IP = '127.0.0.1'

    # katib 没装
    KATIB_MYSQL_IP = '192.168.31.11'
    KATIB_MYSQL_PORT = 32004
    KATIB_MYSQL_USER = 'root'
    KATIB_MYSQL_PASSWORD = 'test'
    KATIB_MYSQL_DATABASE = 'vizier'


    class GitHubClient:
        CLIENT_ID = '07eaa6f268c5e511e462'
        CLIENT_SECRET = '649ba17b21b375294d55413549588b69189eb247'

elif ENV == 'HP':
    # HP
    MONGO = 'HP'
    # REDIS_SERVER need to be changed to localhost on 小米机器 itself
    REDIS_SERVER = 'redis://192.168.31.250:6379'
    GIT_SERVER = 'http://192.168.31.250:2333'
    GIT_SERVER_IP = '192.168.31.250'
    GIT_LOCAL = f'vagrant@{GIT_SERVER_IP}:'
    RC_SERVER_URL = 'http://localhost:8818/'
    RC_ADMIN_ID = 'mo'
    RC_ADMIN_PW = '123456'
    IPFS_SERVER = 'http://localhost'
    JOB_IMAGE_CPU = 'magicalion/singleuser-job:dev'
    JOB_IMAGE_GPU = 'magicalion/singleuser-job:dev-gpu'
    HUB_SERVER = 'http://192.168.31.250:8000/hub_api'
    NFS_SERVER = 'http://192.168.31.250:2555'
    NFS_IP = '192.168.31.250'
    JOB_STAGING_CLAIM = 'nfs-pvc-job-staging-dev'
    USER_DIR_CLAIM = 'nfs-pvc-user-dir-dev'
    HOST_JOB_STAGING = '/mnt/job_staging_dev'
    HOST_USER_DIRECTORY = '/mnt/user_directory_dev'
    PY_SERVER = 'http://192.168.31.250:8899/pyapi'
    # kubectl get services
    # 改为 rabbitmq-service 的端口
    BROKER_SERVICE_HOST = '192.168.31.250:32699'

    SAMPLE_APP_ID = '5baf1488b5113448e5556e29'
    SAMPLE_DEPLOY_APP_ID = '5bfd118f1afd942b66b36b30'
    GPU_NODE = 'node1'
    ELASTIC_SERVER = 'http://192.168.31.250:9200'
    DOCKER_IP = '127.0.0.1'

    # katib 没装
    KATIB_MYSQL_IP = '192.168.31.11'
    KATIB_MYSQL_PORT = 32004
    KATIB_MYSQL_USER = 'root'
    KATIB_MYSQL_PASSWORD = 'test'
    KATIB_MYSQL_DATABASE = 'vizier'


    class GitHubClient:
        CLIENT_ID = '07eaa6f268c5e511e462'
        CLIENT_SECRET = '649ba17b21b375294d55413549588b69189eb247'

elif ENV == 'DEFAULT':
    # DEV
    MONGO = 'DEFAULT'
    # REDIS_SERVER need to be changed to localhost on 182 itself
    REDIS_SERVER = 'redis://10.52.14.182:6379'
    GIT_SERVER = 'http://10.52.14.182:2333'
    GIT_SERVER_IP = '10.52.14.182'
    GIT_LOCAL = f'admin@{GIT_SERVER_IP}:'
    RC_SERVER_URL = 'http://localhost:8818/'
    RC_ADMIN_ID = 'mo'
    RC_ADMIN_PW = '123456'
    IPFS_SERVER = 'http://localhost'
    NFS_SERVER = 'http://192.168.31.11:2555'
    NFS_IP = '192.168.31.11'
    JOB_STAGING_CLAIM = 'nfs-pvc-job-staging-dev'
    USER_DIR_CLAIM = 'nfs-pvc-user-dir-dev'
    # PY_SERVER = 'http://192.168.31.4:8899/pyapi'
    PY_SERVER = 'http://192.168.31.23:8899/pyapi'
    # PY_SERVER = 'http://192.168.32.3:8899/pyapi'  # upstairs ip
    BROKER_SERVICE_HOST = '192.168.31.11:31339'
    JOB_IMAGE_CPU = 'magicalion/singleuser-job:dev'
    JOB_IMAGE_GPU = 'magicalion/singleuser-job:dev-gpu'
    HOST_JOB_STAGING = '/mnt/job_staging_dev'
    HOST_USER_DIRECTORY = '/mnt/user_directory_dev'
    HUB_SERVER = 'http://localhost:8000/hub_api'
    SAMPLE_APP_ID = '5baf1488b5113448e5556e29'
    SAMPLE_DEPLOY_APP_ID = '5bfd118f1afd942b66b36b30'
    GPU_NODE = 'node1'
    DOCKER_IP = '192.168.31.11'

    KATIB_MYSQL_IP = '192.168.31.11'
    KATIB_MYSQL_PORT = 32004
    KATIB_MYSQL_USER = 'root'
    KATIB_MYSQL_PASSWORD = 'test'
    KATIB_MYSQL_DATABASE = 'vizier'


    class GitHubClient:
        CLIENT_ID = '07eaa6f268c5e511e462'
        CLIENT_SECRET = '649ba17b21b375294d55413549588b69189eb247'


elif ENV == 'PROD':
    # PROD
    MONGO = 'PROD'
    REDIS_SERVER = 'redis://192.168.31.11:6379'
    GIT_SERVER = 'http://localhost:2333'
    GIT_SERVER_IP = 'momodel-ai.s3.natapp.cc'
    GIT_LOCAL = ''
    RC_SERVER_URL = 'http://localhost:8818/'
    RC_ADMIN_ID = 'mo'
    RC_ADMIN_PW = 'momodel123456'
    IPFS_SERVER = 'http://localhost'
    NFS_SERVER = 'http://192.168.31.11:2666'
    NFS_IP = '192.168.31.11'
    JOB_STAGING_CLAIM = 'nfs-pvc-job-staging'
    USER_DIR_CLAIM = 'nfs-pvc-user-dir'
    PY_SERVER = 'http://192.168.31.11:8899/pyapi'
    BROKER_SERVICE_HOST = '192.168.31.11:30170'
    JOB_IMAGE_CPU = 'magicalion/singleuser-job:dev'
    JOB_IMAGE_GPU = 'magicalion/singleuser-job:dev-gpu'
    HOST_JOB_STAGING = '/mnt/job_staging'
    HOST_USER_DIRECTORY = '/mnt/user_directory'
    HUB_SERVER = 'http://localhost:8000/hub_api'
    SAMPLE_APP_ID = '5c0e1e107b284e7b6cebd18e'
    SAMPLE_DEPLOY_APP_ID = '5c0e20e17b284e7c7c09663c'
    GPU_NODE = 'node1'
    DOCKER_IP = '127.0.0.1'

    KATIB_MYSQL_IP = '192.168.31.11'
    KATIB_MYSQL_PORT = 32004
    KATIB_MYSQL_USER = 'root'
    KATIB_MYSQL_PASSWORD = 'test'
    KATIB_MYSQL_DATABASE = 'vizier'


    class GitHubClient:
        CLIENT_ID = 'aeb7f86c43655cf5c26f'
        CLIENT_SECRET = '8020b4f3c6d3d6447cad55c587b99a8f5ec7babc'

elif ENV == 'MO':
    # MO
    MONGO = 'MO'
    REDIS_SERVER = 'redis://192.168.1.79:6379'
    GIT_SERVER = 'http://localhost:2333'
    GIT_SERVER_IP = '36.26.77.39:6666'
    GIT_LOCAL = ''
    RC_SERVER_URL = 'http://localhost:8818/'
    RC_ADMIN_ID = 'mo'
    RC_ADMIN_PW = 'momodel123456'
    IPFS_SERVER = 'http://localhost'
    NFS_SERVER = 'http://36.26.77.39:2555'
    NFS_IP = '192.168.1.79'
    JOB_STAGING_CLAIM = 'nfs-pvc-job-staging'
    USER_DIR_CLAIM = 'nfs-pvc-user-dir'
    HOST_JOB_STAGING = '/mnt/job_staging'
    HOST_USER_DIRECTORY = '/mnt/user_directory'
    PY_SERVER = 'http://36.26.77.39:8899/pyapi'

    BROKER_SERVICE_HOST = '192.168.1.79:30371'
    JOB_IMAGE_CPU = 'magicalion/singleuser-job:latest'
    JOB_IMAGE_GPU = 'magicalion/singleuser-job:latest-gpu'
    HUB_SERVER = 'http://localhost:8000/hub_api'
    SAMPLE_APP_ID = '5bfb634e1afd943c623dd9cf'  # style transfer
    SAMPLE_DEPLOY_APP_ID = '5bfd118f1afd942b66b36b30'  # poetry
    GPU_NODE = 'production'
    DOCKER_IP = '192.168.1.53'

    # katib 没装
    KATIB_MYSQL_IP = '192.168.31.11'
    KATIB_MYSQL_PORT = 32004
    KATIB_MYSQL_USER = 'root'
    KATIB_MYSQL_PASSWORD = 'test'
    KATIB_MYSQL_DATABASE = 'vizier'


    class GitHubClient:
        CLIENT_ID = '14b08748d1a5418d2c4b'
        CLIENT_SECRET = '09e032e8e7c53df3523e35e848f79fdd5f744ff6'

elif ENV == 'ZJU':
    # ZJU
    MONGO = 'ZJU'
    REDIS_SERVER = 'redis://localhost:6379'
    GIT_SERVER = 'http://localhost:2333'
    GIT_SERVER_IP = '10.214.223.202:6666'
    GIT_LOCAL = 'admin@10.214.223.202:'
    RC_SERVER_URL = 'http://localhost:8818/'
    RC_ADMIN_ID = 'mo'
    RC_ADMIN_PW = 'momodel123456'
    IPFS_SERVER = 'http://localhost'
    NFS_SERVER = 'http://10.214.223.201:2555'
    NFS_IP = '10.214.223.201'
    JOB_STAGING_CLAIM = 'nfs-pvc-job-staging'
    USER_DIR_CLAIM = 'nfs-pvc-user-dir'
    HOST_JOB_STAGING = '/mnt/job_staging'
    HOST_USER_DIRECTORY = '/mnt/user_directory'
    PY_SERVER = 'http://10.214.223.201:8899/pyapi'

    BROKER_SERVICE_HOST = '10.214.223.201:31393'
    JOB_IMAGE_CPU = 'magicalion/singleuser-job:latest'
    JOB_IMAGE_GPU = 'magicalion/singleuser-job:latest-gpu'
    HUB_SERVER = 'http://10.214.223.201:8000/hub_api'
    SAMPLE_APP_ID = '5cc279e9dd75a1ea417e2a6b'  # style transfer
    SAMPLE_DEPLOY_APP_ID = '5cc25d06dd75a1ea417e2a65'  # poetry
    GPU_NODE = 'r730-node1'
    DOCKER_IP = '127.0.0.1'

    # katib 没装
    KATIB_MYSQL_IP = '192.168.31.11'
    KATIB_MYSQL_PORT = 32004
    KATIB_MYSQL_USER = 'root'
    KATIB_MYSQL_PASSWORD = 'test'
    KATIB_MYSQL_DATABASE = 'vizier'


    class GitHubClient:
        CLIENT_ID = '14b08748d1a5418d2c4b'
        CLIENT_SECRET = '09e032e8e7c53df3523e35e848f79fdd5f744ff6'
else:
    raise Exception('Wrong ENV value')

if ENV == 'PROD':
    WEB_ADDR = 'http://momodel-ai.s3.natapp.cc'
elif ENV == 'MO':
    # WEB_ADDR = 'http://36.26.77.39:8899'
    WEB_ADDR = 'http://www.momodel.cn:8899'
elif ENV == 'ZJU':
    WEB_ADDR = 'http://10.214.223.201:8899'
else:
    WEB_ADDR = 'http://localhost:8899'


# Project Status
# PROJECT_STATUS = {'DEPLOYING': 'deploying',
#                   'ACTIVE': 'active',
#                   'INACTIVE': 'inactive'}

class ProjectStatus:
    """
    Project status
    """
    DEPLOYING = 'deploying'
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class ProjectPrivacy:
    """
    Project Privacy
    """
    PUBLIC = 'public'
    PRIVATE = 'private'


class JobStatus:
    """
    Project Privacy
    """
    QUEUING = 'Queuing'
    RUNNING = 'Running'
    COMPLETE = 'Complete'
    TERMINATED = 'Terminated'
    FAILED = 'Failed'


SMTP_SERVER = 'smtp.exmail.qq.com'
USERNAME = 'service@momodel.ai'
PASSWORD = 'Mo123456'
SENDER = 'service@momodel.ai'


class JobConst:
    MAX_AUTO_RESTART_NUM = 4


TEMP_USER_TOTAL_NUM = 200
TEMP_USER_EXPIRE_HOURS = 24 * 3
APP_MAIN_FILE = 'handler.py'
MODULE_MAIN_FILE = 'main.py'
JOB_STAGING_DELETE_TIME = 60 * 60 * 8
JOB_STAGING_DELETE_TIMEOUT = 60 * 60 * 24 * 7
METRICS_API = '/apis/metrics.k8s.io/v1beta1'
FILE_LOCKER_TIMEOUT = 10 * 60
LE_NAME = '.localenv.tar.gz'
IPFS_PORT = 5001
IPFS_GATEWAY_PORT = 9093
CHECKPOINT_DIR_NAME = 'checkpoint'
TB_LOG_DIR_NAME = 'results'
JOB_LOG_DIR_NAME = 'job_logs'
JOB_STAGING_DIR = './job_staging'
UPDATE_USER_INFO_SK = 'secret_mo_mo'
USER_INVITE_SK = 'secret_mo_mo'
PORT = 5005
SOCKET_IO_PORT = 5006
FILL_BLANK = 'BLANK_GRID'
SHUFFLE_RANGE = 18
LARGE_SHUFFLE_RANGE = 50
TOP_DEV_NUM = 4
PROJECT_IMG_DIR = '../project_imgs'
OVERVIEW_FILE_NAME = 'OVERVIEW.md'
JL_CPU_LIMIT = 1  # 1000m
JL_MEM_LIMIT = 4  # 4Gi
UPLOADED_IMG_BASE = 'http://project-images.momodel.cn'
APP_SECRET_KEY = 'super-super-secret'

ALLOWED_EXTENSIONS = {'zip', 'csv', 'png', 'jpg', 'jpeg', 'svg', 'txt', 'py',
                      'pyc',
                      'md', 'h5', 'npz', 'pkl', 'pdf', 'doc', 'docx', 'yml'}
PREDICT_FOLDER = 'predict_data/'
MODEL_EXPORT_BASE = '/tmp'
MODEL_SCRIPT_PATH = './run_model.py'
TEMPLATE_PATH = './functions/template/python3'
SERVING_PORT = 9000
# WEB_ADDR = 'http://momodel-ai.s3.natapp.cc'
REQ_FILE_NAME = 'faas_requirements.txt'

# REDIS_SERVER = 'redis://localhost:6379'
# HUB_SERVER = 'http://192.168.31.11:8000/hub_api'
ADMIN_TOKEN = '1d4afa72b00c4ffd9db82f26e1628f89'
USER_DIR = './user_directory'
NAMESPACE = 'default'
KUBE_NAME = {
    'model': '{job_id}-training-job',
    'jupyter': '{project_id}-jupyter',
    'serving': '{job_id}-serving'
}
MODULE_DIR = './server3/lib/modules'
DATASET_DIR = './datasets'
DEFAULT_DEPLOY_VERSION = 'dev'
APP_DIR = './functions'
UNSPLASH_CLIENT_IDs = [
    # master key
    'fa60305aa82e74134cabc7093ef54c8e2c370c47e73152f72371c828daedfcd7',
    'bef62f508088943cb9a656d6aada8b042689ae0254d4532f1f16ee01a0e7128d',
    '395ff8a1acb473b3f6abf97b15a3fd75bec48e3c5b02f6ab79b17ba4a94ad4cc',
    '3ea2247de5d9d34abe8accb2931c21467bac902d0c9d29334f6c3752f630af6e',
    'cb51f28d8a9193b026ef7eaee4b2c694a05f5e243c03ab9dd73daf27a37f3153'

]
UNSPLASH_RANDOM_PHOTO = 'https://api.unsplash.com/photos/random'
UNSPLASH_QUERY_MAPPER = {
    'app': ['app', 'tech', 'artificial intelligence'],
    'module': ['coding', 'research', 'analytics'],
    'dataset': ['data', 'analytics', 'diagram', 'data-graph']
}
DEFAULT_PHOTO_W = 1200
DEFAULT_PHOTO_H = 800
INIT_RES = [
    r'# You can use other public modules via our Client object with module\'s identifier',
    r'# and parameters.',
    r'# For more details, please see our online document - https://momodel.github.io/docs/#',
    r'import os',
    r'import sys',
    r'# Define root path',
    r"sys.path.append\('(.+)'\)",
    r'# Import necessary packages',
    r"from modules import (.+)",
    r'# Initialise Client object',
    r"client = Client\(api_key='(.+)',",
    r"(\s+)project_id='(.+)', user_ID='(.+)',",
    r"(\s+)project_type='(.+)', source_file_path='(.+)'\)",
    r'# Make run/train/predict command alias for further use',
    r"(\S+) = client\.\((S+)\)",
    # r'# Run a imported module',
    # r'# e.g. ',
    # r'#      conf = json_parser(\'{"rgb_image":null,"gray_image":null}\')',
    # r'#      result = run(\'zhaofengli/new_gender_classifier/0.0.2\', conf)',
    # r'# \'conf\' is the parameters in dict form for the imported module',
    # r'# \'[user_id]/[imported_module_name]/[version]\' is the identifier of the imported module',
    r'(\w+) = client\.(\w+)',
    r'# Make controller alias for further use',
    r'controller = client.controller',
    # r'# IMPORTANT: Add \'work_path\' to the head of every file path in your code.',
    # r'# e.g.',
    # r'#      jpgfile = Image.open(work_path + "picture.jpg") ',
    # r'work_path = \'./\''
]

PARAMETER_SPEC = [
    {
        "name": "validation",
        "type": {
            "key": "float",
            "des": "blablabla",
            "range": [0.1, 10.1]
        },
        "default": None,
        'required': True
    },
    {
        "name": "k",
        "type": {
            "key": "int",
            "des": "blablabla",
            "range": [0, 10]
        },
        "default": 2,
        'required': True
    },
    {
        "name": "heheda",
        "type": {
            "key": "string",
            "des": "blablabla",
        },
        "default": "买了我的瓜",
        'required': True
    },
    {
        "name": "validation",
        "type": {
            "key": "choice",
            "des": "blablabla",
            "range": [0, 10, 234, 5, 6]
        },
        "default": None,
        'required': True
    },
    {
        "name": "validation",
        "type": {
            "key": "float_m",
            "des": "blablabla",
            "range": [0.1, 10.1]
        },
        "default": None,
        'len_range': [2, 2],
        'required': False
    },
    {
        "name": "k",
        "type": {
            "key": "int_m",
            "des": "blablabla",
            "range": [0, 10]
        },
        "default": 2,
        'len_range': [2, 3],
        'required': False
    },
    {
        "name": "heheda",
        "type": {
            "key": "string_m",
            "des": "blablabla",
        },
        "default": "买了我的瓜",
        'len_range': None,
        'required': False
    },
    {
        "name": "validation",
        "type": {
            "key": "choice_m",
            "des": "blablabla",
            "range": [0, 10, 234, 5, 6],
        },
        "default": None,
        'len_range': None,
        'required': False
    },
    {
        'name': 'x_train',
        'type': {
            'key': 'data_set',
            "des": "blablabla",
        },
        "default": None,
        'required': True
    },
    {
        'name': 'x_train',
        'type': {
            'key': 'join_low_high',
            "des": "blablabla",
            'range': [0, 1]
        },
        "default": "0, 1",
        'required': True
    },
    {
        'name': 'x_train',
        'type': {
            'key': 'multiple',
            "des": "blablabla",
            'range': ["aa", 1]
        },
        "default": None,
        'required': True
    },
    {
        'name': 'x_train',
        'type': {
            'key': 'chioce_child',
            "des": "blablabla",
            'range': ["aa", 1]
        },
        "default": None,
        'required': True
    }
]


class SPEC(object):
    value_type = ['int', 'float', 'str']
    general_spec = {
        'name': None,
        'display_name': None,
        'type': 'input',
        'value_type': 'int',
        'range': None,  # [2, None],
        "default": None,
        "required": False,
    }
    ui_spec = {
        'input': {
            **general_spec,
            'value': None,
        },

        "multiple_input": {
            **general_spec,
            "type": "multiple_input",
            'range': [2, None],
            "len_range": None,
            'values': [],
        },

        "choice": {
            **general_spec,
            "type": "choice",
            "range": [
                "aa",
                "bb",
                "cc",
            ],
            'value': None,
        },

        "multiple_choice": {
            **general_spec,
            "type": "multiple_choice",
            "range": [
                "aa",
                "bb",
                "cc",
            ],
            "len_range": None,
            'values': [],
        },

    }


class IpfsError(Exception):
    pass


class Error(Exception):
    pass


class Warning(Exception):
    pass


class RCUserDoesNotExists(Exception):
    pass


class ErrorMessage(Exception):
    no_match_apis = {
        "key": "无匹配服务",
        "hint_message": "提示：无匹配服务\n"
    }

    error_get_type = {
        "key": "错误的获取类型",
        "hint_message": "提示：错误的获取类型\n"
    }

    # verify_failed = {
    #     "key": "验证失败",
    #     'hint_message': '提示：验证失败\n'
    # }


SLACK_TOKEN = 'xoxp-373531663140-373060474208-373225736785-91052efb4e6cbc13428816c28f008714'
LOCAL_ENV = '.localenv'
CS_PATH = 'results/crowdsourcing/'


class Tutorial:
    def __init__(self, num, name, type, project_type, description, path,
                 points, total_step):
        self.name = name
        self.type = type
        self.project_type = project_type
        self.num = num
        self.description = description
        self.path = path
        self.points = points
        self.total_step = total_step
        self.level = 1


# class TutorialPaths:
#     APP_PATH = 'tutorials/app_tutorial'
#     MODULE_PATH = 'tutorials/module_tutorial'
#     DATASET_PATH = 'tutorials/dataset_tutorial'
#     JOB_PATH = 'tutorials/job_tutorial'


# class Tutorials:
#     APP = Tutorial(num=1, description='Deploy 1 App',
#                    path='tutorials/app_tutorial', reward=300, total_step=1)
#     MODULE = Tutorial(num=2, description='Deploy 1 Module',
#                       path='tutorials/module_tutorial', reward=100,
#                       total_step=1)
#     DATASET = Tutorial(num=3, description='Publish 1 Dataset',
#                        path='tutorials/dataset_tutorial', reward=100,
#                        total_step=1)
#     JOB = Tutorial(num=4, description='Run 1 Job',
#                    path='tutorials/job_tutorial', reward=100,
#                    total_step=1)
#     ENTRIES = Tutorial(num=5,
#                        description='Enter following pages: Notebook, Docs',
#                        path=None, reward=200,
#                        total_step=2)
#
#     @classmethod
#     def as_dict(cls):
#         d = {}
#         for attr, value in cls.__dict__.items():
#             if attr not in ['APP', 'MODULE', 'DATASET', 'JOB', 'ENTRIES']:
#                 continue
#             if isinstance(value, Tutorial):
#                 d[attr] = value.__dict__
#             else:
#                 d[attr] = value
#         return d


Tutorials = [
    Tutorial(num=1, name='App Tutorial', type='app', project_type='app',
             description='Deploy 1 App',
             path='tutorials/app_tutorial', points=300, total_step=1),
    Tutorial(num=2, name='Module Tutorial', type='module',
             project_type='module',
             description='Deploy 1 Module',
             path='tutorials/module_tutorial', points=100,
             total_step=1),
    Tutorial(num=3, name='Dataset Tutorial', type='dataset',
             project_type='dataset',
             description='Publish 1 Dataset',
             path='tutorials/dataset_tutorial', points=100,
             total_step=1),
    Tutorial(num=4, name='Job Tutorial', type='job', project_type='module',
             description='Run 1 Job',
             path='tutorials/job_tutorial', points=100,
             total_step=1),
    Tutorial(num=5, name=None, type=None, project_type=None,
             description="Enter 'Docs' Page",
             path=None, points=200,
             total_step=1),
]

for tut in Tutorials:
    tut.level = 1

TutorialDicts = [tut.__dict__ for tut in Tutorials]
TutorialMapper = {f'{tut.level}-{tut.num}': tut for tut in Tutorials}

Official_User_ID = 'momodel'
# print(TutorialDicts)
# TutorialDicts = {
#     Tutorials.APP.__dict__,
#     Tutorials.MODULE.__dict__,
#     Tutorials.DATASET.__dict__,
#     Tutorials.JOB.__dict__,
#     Tutorials.ENTRIES.__dict__,
# }
# import json
# print(json.dumps(Tutorials.as_dict()))

# templates
'''
    'Welcome to Mo': '基本操作',
    'How to Deploy Datasets': '发布数据集',
    'How to Deploy Module-Toolkit': '开发工具模块',
    'How to Deploy Module-Model': '开发模型模块',
    'How to Develop APP': '开发部署应用',
    'How to Train Model ON GPU or CPU': '训练模型',
    'How to Evaluate Model in TensorBoard': '评估模型',
    'How to Convert Model to TensorFlow Lite': '转换模型',
'''

TemplateTutorialTitles = {
    'Basic Operation': '基本操作',
    'Publish Dataset': '发布数据集',
    'Develop Toolkit': '开发工具模块',
    'Develop Model': '开发模型模块',
    'Develop App': '开发部署应用',
    'Train Model': '训练模型',
    'Evaluate Model': '评估模型',
    'Convert Model': '转换模型',
}

TemplateTutorialDocTitles = {
    'Basic Operation': '在 Mo 上运行你的第一段代码',
    'Publish Dataset': '上传发布一个数据集',
    'Develop Toolkit': '开发一个工具模块 (Module-Toolkit)',
    'Develop Model': '开发一个模型模块 (Module-Model)',
    'Develop App': '开发和部署一个应用(APP)',
    'Train Model': '在GPU/CPU资源上训练机器学习模型',
    'Evaluate Model': '利用 TensorBoard 可视化评估模型',
    'Convert Model': '把模型转换为 TensorFlow Lite 格式',
}

'''
    'Welcome to Mo': '了解Mo的基本操作，熟悉基本功能',
    'How to Deploy Datasets': '上传发布一个数据集',
    'How to Deploy Module-Toolkit': '开发一个可预测的模块',
    'How to Deploy Module-Model': '开发一个可预测并可二次训练的模块',
    'How to Develop APP': '开发和部署一个实际应用',
    'How to Train Model ON GPU or CPU': '在GPU/CPU资源上训练机器学习模型',
    'How to Convert Model to TensorFlow Lite': '把模型转换为TensorFlow Lite 格式',
'''

TemplateTutorialDescription = {
    'Basic Operation': 'Understanding basic functions and operations on Mo',
    'Publish Dataset': 'How to publish dataset',
    'Develop Toolkit': 'How to deploy module-toolkit',
    'Develop Model': 'How to deploy module-model',
    'Develop App': 'How to develop app',
    'Train Model': 'How to train model on GPU or CPU',
    'Evaluate Model': 'How to evaluate model in TensorBoard',
    'Convert Model': 'How to convert model to TensorFlow Lite',
}

'''

'''
TemplateClassroomTitles = {
    'Python Tutorial-CN': 'Python 中文教程',
    'Python Tutorial-EN': 'Python 英文教程',
    'ML Tutorial-CN': '机器学习中文教程',
    'ML Tutorial-EN': '机器学习英文教程',
}

'''

'''
TemplateClassroomDescription = {
    'Python Tutorial-CN': 'Python tutorial (in Chinese) with matched ipynb files',
    'Python Tutorial-EN': 'Python tutorial (in English)  with matched ipynb files',
    'ML Tutorial-CN': 'Andrew Ng Machine learning tutorial (in Chinese) with matched ipynb files',
    'ML Tutorial-EN': 'Machine learning tutorial (in English) with matched ipynb files'
}


class GitHubConsts:
    TOKEN_URL = 'https://github.com/login/oauth/access_token'
    GET_USER_URL = 'https://api.github.com/user?access_token='
    GET_USER_EMAIL_URL = 'https://api.github.com/user/emails?access_token='
    GITHUB_RENAME_KEYS = ['blog', 'created_at', 'events_url', 'followers',
                          'followers_url', 'following', 'following_url',
                          'html_url', 'id', 'name', 'node_id',
                          'organizations_url', 'public_repos',
                          'received_events_url', 'repos_url', 'site_admin',
                          'starred_url', 'subscriptions_url', 'type',
                          'updated_at', 'url']


# CourseTemplateID
COURSETEMPLATEPATH = '.CourseTemplate'

# 指定ID
if ENV == 'DEFAULT':
    TOP_TOPIC_ID = ''
elif ENV == 'PROD':
    TOP_TOPIC_ID = ''
elif ENV == 'MO':
    TOP_TOPIC_ID = ''
else:
    TOP_TOPIC_ID = ''


# wxe1ff8db238aee523
class WechatConstants:
    WECHAT_APP_SECRET = 'f3d33890a33bb8f90309a0bf0b2c4b6d'
    ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/sns/oauth2/access_token?' \
                       'appid=wxe1ff8db238aee523&secret={0}&code={1}&grant_type=authorization_code'
    ACCESS_TOKEN_URL_KEYS = ['access_token', 'expires_in', 'refresh_token',
                             'openid', 'scope']

    REFRESH_TOKEN_URL = 'https://api.weixin.qq.com/sns/oauth2/refresh_token?' \
                        'appid=wxe1ff8db238aee523&grant_type=refresh_token&refresh_token={0}'
    REFRESH_TOKEN_URL_KEYS = ['access_token', 'expires_in', 'refresh_token',
                              'openid', 'scope']

    TOKEN_IS_AUTH_URL = 'https://api.weixin.qq.com/sns/auth?access_token={0}&openid={1}'
    # 为零是正确的
    TOKEN_IS_AUTH_URL_KEYS = ['errcode', 'errmsg']
    # 使用 unionid作为 user_id
    USER_INFO_URL = 'https://api.weixin.qq.com/sns/userinfo?access_token={0}&openid={1}'
    USER_INFO_URL_KEYS = ['openid', 'nickname', 'sex', 'province',
                          'city', 'country', 'headimgurl', 'privilege',
                          'unionid']
    OUR_DATABASE_KEYS = ['user_ID', 'username', 'gender', 'avatar_url']


class TagsMapping:
    """
    ()； CSV；Excel； 社会(Society) ；金融(Finance)；
    健康(Health) ；科技(Technology) ；生物(Biology)；语言(Language)；旅行(Travel)；娱乐(Entertainment)；教育(Education)
    """

    # dataset_tags_mapping = {'文本': 'Text', '图片': 'Image', '音频': 'Audio', '视频': 'Video', '教育': 'Education',
    #                         'CSV': 'CSV', 'Excel': 'Excel', '社会': 'Society', '金融': 'Finance', '健康': 'Health',
    #                         '科技': 'Technology', '生物': 'Biology', '语言': 'Language', '旅行': 'Travel',
    #                         '娱乐': 'Entertainment'}

    tags_mapping = {'卷积神经网络': 'CNN', '循环神经网络': 'RNN', '深层神经网络': 'DNN',
                    '回归': 'Regression', '多层感知机': 'MLP',
                    '分类': 'Classification', '聚类': 'Clustering',
                    '序列到序列模型': 'Sequential-to-Sequential',
                    '文本': 'Text', '图片': 'Image', '音频': 'Audio', '视频': 'Video',
                    '教育': 'Education',
                    'CSV': 'CSV', 'Excel': 'Excel', '社会': 'Society',
                    '金融': 'Finance', '健康': 'Health',
                    '科技': 'Technology', '生物': 'Biology', '语言': 'Language',
                    '旅行': 'Travel',
                    '娱乐': 'Entertainment'}

    @classmethod
    def keys(cls):
        return list(cls.tags_mapping.keys())

    @classmethod
    def values(cls):
        return list(cls.tags_mapping.values())


DEFAULT_TAGS = ['卷积神经网络 / CNN', '循环神经网络 / RNN', '深层神经网络 / DNN',
                '回归 / Regression', '多层感知机 / MLP',
                '分类 / Classification', '聚类 / Clustering',
                '序列到序列模型 / Sequential-to-Sequential', '视频 / Video',
                '图片 / Image', '音频 / Audio', '文本 / Text', '社会 / Social',
                '金融 / Finance', '健康 / Health',
                '生活 / Life', '驱动 / Drive', '科学 / Science', '生物 / Biology',
                '语言 / Language',
                '互联网 / Internet', 'CSV', 'Excel']
