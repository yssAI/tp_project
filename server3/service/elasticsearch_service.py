from elasticsearch5 import Elasticsearch, NotFoundError
from server3.constants import ENV
import copy

TITLESFORTABLES = {'display_name': ['apps', 'modules', 'datasets'],
                   'username': ['users'], 'request_title': ['requests']}

INDEXES = ['projects', 'requests', 'users']

TABLEFOFTITLES = {'apps': 'display_name', 'modules': 'display_name', 'datasets': 'display_name',
                  'username': 'users', 'request_title': 'requests'}

TABLEFORFIELDS = {'projects': ['display_name', 'description'],
                  'users': ['username', 'bio'], 'requests': ['request_title', 'description']}

ALLTITLES = ['display_name', 'username', 'title', 'request_name']

HIGHTLIGHT = {"pre_tags": ["<span style='color: #1890FF'>"],
              "post_tags": ["</span>"]}


class ElasticSearchSearvice:
    # 默认加载本地
    if ENV != 'HP':
        _es = Elasticsearch(hosts='127.0.0.1:9200', sniffer_timeout=60)
    else:
        _es = Elasticsearch(hosts='192.168.31.250:9200', sniffer_timeout=60)
    # _es = Elasticsearch(hosts='192.168.31.16:9200')

    @classmethod
    def is_available(cls):
        return cls._es.ping()

    # create dsl
    # 单子段匹配并且高亮(短语匹配)
    @classmethod
    def __create_dsl_for_single_field(cls, field, text, size=None, highlight={}):
        dsl = {
            'query': {
                'match': {
                    field: text.lower()
                }
            },
            "highlight": {
                "order": "score",
                "require_field_match": False,
                "fields": {
                    field: highlight
                }
            }
        }

        if size:
            dsl['query']['match']['size'] = size

        return dsl

    # 多字段全局检索(短语匹配, 不会有字符程度)
    @classmethod
    def __create_dsl_for_multi_fields(cls, text, fields, operator='or', size=None):
        dsl = {
            "query": {
                "multi_match": {
                    "query":       text,
                    "type":        "most_fields",
                    "operator":    operator,
                    "fields": fields
                }
            }
        }
        if size:
            dsl['query']['multi_match']['size'] = size

        return dsl

    # 单字段检索, 正则表达式
    @classmethod
    def __create_dsl_for_single_field_with_regex(cls, field, texts, start=0, size=3, highlight={}):
        dsl = {
            "query": {
                "constant_score": {
                    "filter": {
                        'bool': {
                            'should': [
                            ]
                        }
                    }
                }
            },
            "highlight": {
                "order": "score",
                "require_field_match": False,
                "fields": {
                    field: highlight
                }
            }
        }
        if size:
            dsl['size'] = size
        if start:
            dsl['from'] = start
        for text in texts:
            dsl['query']['constant_score']['filter']['bool']['should'].append({
                "regexp": {
                    field: {
                        "value": '.*' + text.lower() + '.*'
                    }
                }
            })
        return dsl

    # 多字段多值匹配并且高亮(正则表达式模式, 会匹配单字符包含关系)
    @classmethod
    def __create_dsl_for_multi_field_with_regex(cls, fields, texts, start=0, size=3, highlight={}):
        dsl = {
            "query": {
                "constant_score": {
                    "filter": {
                        'bool': {
                            'should': [
                            ]
                        }
                    }
                }
            },
            "highlight": {
                "order": "score",
                "require_field_match": False,
                "fields": {

                }
            }
        }
        if size:
            dsl['size'] = size
        if start:
            dsl['from'] = start
        for field in fields:
            # 高亮
            dsl['highlight']['fields'][field] = highlight
            for text in texts:
                dsl['query']['constant_score']['filter']['bool']['should'].append({
                    "regexp": {
                        field: {
                            "value": '.*' + text.lower() + '.*'
                        }
                    }
                })
        return dsl

    # 精确查找
    @classmethod
    # 精确查找-tags
    def __create_dsl_for_tags(cls, tags, type, start=0, size=3):
        dsl = {
            'from': start,
            'size': size,
            'query': {
                "constant_score": {
                    "filter": {
                        'bool': {
                            'must':
                                [
                                    {
                                        'term': {
                                            'type': type
                                        }
                                    },
                                    {
                                        'terms': {
                                            'tags': tags
                                        }
                                    }
                                ]
                            }
                        }
                    }
                }
            }
        # 返回Tags
        return dsl

    # 多字段检索并且高亮
    @classmethod
    def match_fields_with_highlight(cls, fields, text, operator='or', size=None, highlight={}):
        dsl = {
            "query": {
                "multi_match": {
                    "query":       text,
                    "type":        "most_fields",
                    "operator":    operator,
                    # "fields": fields
                }
            },
            "highlight": {
                "order": "score",
                "require_field_match": False,
                "fields": {

                }
            }
        }
        weights_fields = []
        for field in fields:
            # 高亮
            dsl['highlight']['fields'][field] = highlight
            # 加权
            if field in ALLTITLES:
                field = field + '^3'
            elif field == 'tags':
                field = field + '^2'
            else:
                field = field + '^1'
            weights_fields.append(field)
        dsl['query']['multi_match']['fields'] = weights_fields
        return dsl

    @classmethod
    def __execute_dsl(cls, dsl, index):
        if index == 'apps':
            print(dsl)
            dsl['query']['constant_score']['filter']['bool']['must'] = {"term": {"type": 'app'}}
            return cls._es.search(index='projects', doc_type='project', body=dsl)
        if index == 'modules':
            dsl['query']['constant_score']['filter']['bool']['must'] = {"term": {"type": 'module'}}
            return cls._es.search(index='projects', doc_type='project', body=dsl)
        if index == 'datasets':
            dsl['query']['constant_score']['filter']['bool']['must'] = {"term": {"type": 'dataset'}}
            return cls._es.search(index='projects', doc_type='project', body=dsl)
        if index == 'users':
            return cls._es.search(index='users', doc_type='user', body=dsl)
        if index == 'requests':
            return cls._es.search(index='requests', doc_type='request', body=dsl)
        if index == 'projects':
            return cls._es.search(index='projects', doc_type='project', body=dsl)
        if index == 'code_snippets':
            return cls._es.search(index='code_snippets', doc_type='code_snippet', body=dsl)

    @classmethod
    def search_title(cls, search_value=None, index=None):
        if not isinstance(search_value, list):
            search_value = [search_value]
        if index:
            # des index
            if not search_value:
                return {'msg': 'failed'}
            fields = TABLEFORFIELDS[index]
            '''
            cls.__create_dsl_for_single_field_with_regex(field=title,
                                                               texts=search_value, size=20,
                                                               highlight=HIGHTLIGHT)
            '''
            dsl = cls.__create_dsl_for_multi_field_with_regex(fields=fields, texts=search_value, start=0, size=3,
                                                              highlight=HIGHTLIGHT)
            results = cls.__execute_dsl(dsl, index=index)
        else:
            # all
            # indexes = list(TITLESFORTABLES.values())
            results = []
            for idx in range(len(INDEXES)):
                '''
                cls.__create_dsl_for_single_field_with_regex(field=titles[title_idx], texts=search_value, size=3,
                                                                   highlight=HIGHTLIGHT)
                '''
                fields = TABLEFORFIELDS[INDEXES[idx]]
                dsl = cls.__create_dsl_for_multi_field_with_regex(fields=fields, texts=search_value, start=0, size=3,
                                                                  highlight=HIGHTLIGHT)
                # for index in indexes[title_idx]:
                search_result = cls.__execute_dsl(dsl, INDEXES[idx])
                results.append({INDEXES[idx]: search_result})
        # 获取数值接口
        count_info = cls.count(search_value)
        return results, count_info

    @classmethod
    def __remove_for_count_api(cls, dsl):
        del dsl['highlight']
        del dsl['size']
        return dsl

    @classmethod
    def count(cls, search_text):
        # 分别求所有
        # request 的数量
        request_dsl = cls.__create_dsl_for_multi_field_with_regex(fields=['request_title', 'description'],
                                                                  texts=search_text)
        request_dsl = cls.__remove_for_count_api(request_dsl)

#        request_count = cls._es.count(index='requests', doc_type='request', body=request_dsl)
        request_count = {}

        total_request_count = 0
        # projects
        project_dsl = cls.__create_dsl_for_multi_field_with_regex(fields=['display_name', 'description'],
                                                                  texts=search_text)
        project_dsl = cls.__remove_for_count_api(project_dsl)

        total_project_count = 0
#        project_count = cls._es.count(index='projects', doc_type='project', body=project_dsl)
        # 创建
        project_count = {}
        for project_type in ['app', 'module', 'dataset']:
            project_type_dsl = copy.deepcopy(project_dsl)
            request_type_dsl = copy.deepcopy(request_dsl)
            project_type_dsl['query']['constant_score']['filter']['bool']['must'] = {"term": {"type": project_type}}
            request_type_dsl['query']['constant_score']['filter']['bool']['must'] = {"term": {"type": project_type}}
            project_type_count = cls._es.count(index='projects', doc_type='project', body=project_type_dsl).get('count')
            request_type_count = cls._es.count(index='requests', doc_type='request', body=request_type_dsl).get('count')
            request_count[project_type] = request_type_count
            project_count[project_type] = project_type_count
            total_request_count += request_type_count
            total_project_count += project_type_count
        # users
        user_dsl = cls.__create_dsl_for_multi_field_with_regex(fields=['username', 'bio'],
                                                               texts=search_text)
        user_dsl = cls.__remove_for_count_api(user_dsl)
        user_count = cls._es.count(index='users', doc_type='user', body=user_dsl)

        return {'project_nums': total_project_count, 'request_nums': total_request_count,
                'user_nums': user_count.get('count'), 'projects': project_count, 'requests': request_count}

    @classmethod
    def search_code_snippet(cls, fields=[], search_values=[], index=None, start=0, size=3):
        # 多字段检索
        if not isinstance(fields, list):
            return {'message': "Please input the valid data"}
        # 是否多值检索
        if not isinstance(search_values, list):
            search_values = [search_values]
        # 创建 DSL 语句
        dsl = cls.__create_dsl_for_multi_field_with_regex(fields=fields, texts=search_values, start=start, size=size,
                                                          highlight=HIGHTLIGHT)
        results = cls.__execute_dsl(dsl, index=index)

        return results

    @classmethod
    def search_fields(cls, fields=[], search_values=[], index=None, start=0, size=3, request_type=None):
        # 多字段检索
        if not isinstance(fields, list):
            return {'message': "Please input the valid data"}
        # 是否多值检索
        if not isinstance(search_values, list):
            search_values = [search_values]
        # 创建 DSL 语句
        dsl = cls.__create_dsl_for_multi_field_with_regex(fields=fields, texts=search_values, start=start, size=size,
                                                          highlight=HIGHTLIGHT)
        # 统计其他的种类的数量
        count_info = cls.count(search_values)
        # 执行出结果
        # if 'request' in index and request_type:
        #     print(dsl)
        #     dsl['query']['constant_score']['filter']['bool']['must'] = { "term": {"type": request_type}}
        results = cls.__execute_dsl(dsl, index=index)
        # 或许会要执行筛选
        return results, count_info

    @classmethod
    def search_tags(cls, tags, start=0, size=10, index='all', project_type = 'app'):
        dsl = cls.__create_dsl_for_tags(tags, project_type, start=start, size=size)
        if index == 'project':
            results = cls._es.search(index='projects', doc_type='project', body=dsl)
        elif index == 'request':
            results = cls._es.search(index='requests', doc_type='request', body=dsl)
        else:
            # 基本不存在所有
            project_results = cls._es.search(index='projects', doc_type='project', body=dsl)
            request_results = cls._es.search(index='requests', doc_type='request', body=dsl)
            return project_results, request_results
        return results

    @classmethod
    def operation_with_index(cls, body, index, doc_type, index_id):
#        if not cls._es.indices.exists(index):
#            body = {
#                "mappings": {
#                    index[:-1]: {
#                        "properties": {
#                            "description": {
#                                "type": "text",
#                                "analyzer": "ik_max_word",
#                                "search_analyzer": "ik_max_word"
#                            }
#                        }
#                    }
#                }
#            }
#            if index == 'requests':
#                body['mappings'][index[:-1]]['properties']['request_title'] = {
#                    "type": "text",
#                    "analyzer": "ik_max_word",
#                    "search_analyzer": "ik_max_word"
#                }
#                cls._es.indices.create(index=index, body=body, ignore=400)
#            else:
#                if index == 'projects':
#                    body['mappings'][index[:-1]]['properties']['display_name'] = {
#                        "type": "text",
#                        "analyzer": "standard"
#                    }
#                else:
#                    body['mappings'][index[:-1]]['properties']['username'] = {
#                        "type": "text",
#                        "analyzer": "standard"
#                    }
#                cls._es.indices.create(index=index, body=body, ignore=400)
        cls.create_index(index=index)
        print(cls._es.index(index=index, doc_type=doc_type, body=body, id=index_id, refresh='true', request_timeout=60))

    @classmethod
    def create_index(cls, index):
        if not cls._es.indices.exists(index):
            body = {
                "mappings": {
                    index[:-1]: {
                        "properties": {
                            "description": {
                                "type": "text",
                                "analyzer": "ik_max_word",
                                "search_analyzer": "ik_max_word"
                            }
                        }
                    }
                }
            }
            if index == 'requests':
                body['mappings'][index[:-1]]['properties']['request_title'] = {
                    "type": "text",
                    "analyzer": "ik_max_word",
                    "search_analyzer": "ik_max_word"
                }
                cls._es.indices.create(index=index, body=body, ignore=400)
            else:
                if index == 'projects':
                    body['mappings'][index[:-1]]['properties'][
                        'display_name'] = {
                        "type": "text",
                        "analyzer": "ik_max_word",
                        "search_analyzer": "ik_max_word"
                    }
                    cls._es.indices.create(index=index, body=body, ignore=400)
                elif index == 'code_snippets':
                    body['mappings'][index[:-1]]['properties'][
                        'code_name'] = {
                        "type": "text",
                        "analyzer": "ik_max_word",
                        "search_analyzer": "ik_max_word"
                    }
                    body['mappings'][index[:-1]]['properties'][
                        'code_source'] = {
                        "type": "text",
                        "analyzer": "ik_max_word",
                        "search_analyzer": "ik_max_word"
                    }
                    body['mappings'][index[:-1]]['properties'][
                        'code_tags'] = {
                        "type": "text",
                        "analyzer": "ik_max_word",
                        "search_analyzer": "ik_max_word"
                    }
                    cls._es.indices.create(index=index, body=body, ignore=400)
                else:
                    body['mappings'][index[:-1]]['properties']['username'] = {
                        "type": "text",
                        "analyzer": "standard"
                    }
                cls._es.indices.create(index=index, body=body, ignore=400)

    @classmethod
    def delete_all(cls):
        if cls._es.indices.exists('apps'):
            cls._es.indices.delete(index='apps')
        if cls._es.indices.exists('modules'):
            cls._es.indices.delete(index='modules')
        if cls._es.indices.exists('datasets'):
            cls._es.indices.delete(index='datasets')
        if cls._es.indices.exists('projects'):
            print('刪除projects')
            cls._es.indices.delete(index='projects')
        if cls._es.indices.exists('requests'):
            print('刪除requests')
            cls._es.indices.delete(index='requests')
        if cls._es.indices.exists('users'):
            print('刪除User')
            cls._es.indices.delete(index='users')
        if cls._es.indices.exists('code_snippets'):
            print('刪除code_snippets')
            cls._es.indices.delete(index='code_snippets')


    @classmethod
    def refresh_index(cls):
        cls._es.indices.refresh()

    @classmethod
    def add_user(cls, user_ID, username, bio, avatarV, avatar_url):
        body = {
            'username': username,
            'bio': bio,
            'avatarV': avatarV,
            'avatar_url': avatar_url
        }
        cls.operation_with_index(index='users', doc_type='user', body=body, index_id=user_ID)

    @classmethod
    def add_project(cls, project_id, display_name, description, tags, project_type, img_v, photo_url, username):
        body = {
            'display_name': display_name,
            'description': description,
            'tags': [tag for tag in tags],
            'type': project_type,
            'img_v': img_v,
            'photo_url': photo_url,
            'username': username
        }
        cls.operation_with_index(index='projects', doc_type='project', body=body, index_id=project_id)

    @classmethod
    def add_request(cls, request_title, description, request_type, username, request_id):
        body = {
            'request_title': request_title,
            'description': description,
            'type': request_type,
            'username': username
        }
        cls.operation_with_index(index='requests', doc_type='request', body=body, index_id=request_id)

    @classmethod
    def add_code_snippet(cls, code_snippet_id,  code_name, code_des, code_tags, code_source, detail_url, insert_num):
        body = {
            'code_name': code_name,
            'code_des': code_des,
            'code_tags': [tag for tag in code_tags],
            'code_source': code_source,
            'detail_url': detail_url,
            'insert_num': insert_num
            # 'key_words': [key_word for key_word in key_words],
        }
        cls.operation_with_index(index='code_snippets', doc_type='code_snippet',
                                 body=body, index_id=code_snippet_id)

    # 添加Projects
    @classmethod
    def add_projects(cls):
        # 添加 Project 的数据
        from server3.business.project_business import ProjectBusiness
        # privacy='public'
        projects = ProjectBusiness.repo.objects()
        projects = projects(privacy='public')
        if len(projects) <= 0:
            cls.create_index(index='projects')
        for project in projects:
            try:
                body = {
                    'display_name': project.display_name,
                    'description': project.description,
                    'tags': [tag.id for tag in project.tags],
                    'type': project.type,
                    'img_v': project.img_v if project.img_v else '',
                    'photo_url': project.photo_url if project.photo_url else '',
                    'username': project.user.username,
                    'create_time': project.create_time
                }
                if project.privacy == 'private':
                    continue
                cls.operation_with_index(index='projects', doc_type='project', body=body, index_id=project.id)
            except Exception as e:
                # project.delete()
                print('项目被删除掉, 无法添加elasticsearch')
                continue

    # 添加Requests
    @classmethod
    def add_requests(cls):
        from server3.business.user_request_business import UserRequestBusiness
        requests = UserRequestBusiness.repo.objects()
        if len(requests) <= 0:
            cls.create_index(index='requests')
        for request in requests:
            try:
                body = {
                    'request_title': request.title,
                    'description': request.description,
                    'type': request.type,
                    'username': request.user.username,
                    'tags': [tag.id for tag in request.tags],
                    'create_time': request.create_time
                }
                cls.operation_with_index(index='requests', doc_type='request', body=body, index_id=request.id)
            except Exception as e:
                print('需求被删除掉, 无法添加到elasticsearch')
                continue

    @classmethod
    def add_code_snippets(cls):
        from server3.business.code_snippet_business import CodeSnippetBusiness
        code_snippets = CodeSnippetBusiness.repo.objects()
        if len(code_snippets) <= 0:
            cls.create_index(index='code_snippets')
        for code_snippet in code_snippets:
            try:
                body = {
                    'code_name': code_snippet.code_name,
                    'code_des': code_snippet.code_des,
                    'code_tags': [tag for tag in code_snippet.code_tags],
                    'code_source': code_snippet.code_source,
                    'detail_url': code_snippet.detail_url,
                    'insert_num': code_snippet.insert_num,
                    # 'key_words': [key_word for key_word in code_snippet.key_words],
                }
                cls.operation_with_index(index='code_snippets', doc_type='code_snippet',
                                         body=body, index_id=code_snippet.id)
            except Exception as e:
                print('代码块不存在')
                continue

    @classmethod
    # 添加 users
    def add_users(cls):
        from server3.business.user_business import UserBusiness
        users = UserBusiness.repo.objects()
        if len(users) <= 0:
            cls.create_index(index='users')
        for user in users:
            try:
                body = {
                    'username': user.username,
                    'bio': user.bio,
                    'avatarV': user.avatarV,
                    'avatar_url': user.avatar_url if user.avatar_url else ''
                }
                cls.operation_with_index(index='users', doc_type='user', body=body, index_id=user.user_ID)
            except Exception as e:
                print('用户不存在, 添加不了elasticsearch')
                continue

    @classmethod
    def delete_project(cls, project_id):
        try:
            print(cls._es.delete(index='projects', doc_type='project', id=project_id, refresh='true', ignore=['400', '404']))
        except NotFoundError as e:
            print('Elastic not found this project with id: ' + project_id)

    @classmethod
    def delete_user(cls, user_ID):
        try:
            print(cls._es.delete(index='users', doc_type='user', id=user_ID, refresh='true', ignore=['400', '404']))
        except NotFoundError as e:
            print('Elastic not found this user with id: ' + user_ID)

    @classmethod
    def delete_request(cls, request_id):
        try:
            print(cls._es.delete(index='requests', doc_type='request', id=request_id, refresh='true', ignore=['400', '404']))
        except NotFoundError as e:
            print('Elastic not found this request with id: ' + request_id)

    @classmethod
    # 添加所有数据
    def add_all(cls):
        if not cls._es.indices.exists('requests'):
            cls.create_index('requests')
            cls.add_requests()
        if not cls._es.indices.exists('projects'):
            cls.create_index('projects')
            cls.add_projects()
        if not cls._es.indices.exists('users'):
            cls.create_index('users')
            cls.add_users()
        if not cls._es.indices.exists('code_snippets'):
            cls.create_index('code_snippets')
            cls.add_code_snippets()

    @classmethod
    def clear_indices(cls):
        cls._es.indices.clear_cache()

# 单元测试
from pprint import pprint
# 搜索标题


def test_search_title():
    text = ['d']
    results = ElasticSearchSearvice.search_title(text, index='apps')
    pprint(results)


# 搜索
def test_search_multi_fields():
    text = [' 大']
    results = ElasticSearchSearvice.search_fields(['request_name', 'description'],
                                                  search_values=text, index='request', request_type='dataset')
    pprint(results)


def test_search_tags():
    tags = ['video']
    dsl = {
        'from': 0,
        'size': 10,
        'query': {
            'terms': {
                'tags': tags
            }
        }
    }
    pprint(ElasticSearchSearvice._es.search(index='projects', doc_type='project', body=dsl)['hits'])


if __name__ == '__main__':
    # add_projects()
    # add_requests()
    # # 单元测试, 每个模块的测试
    # test_search_title()
    # test_search_multi_fields
    # print(test_search_title())
    # add_all()
    # ElasticSearchSearvice.add_project('5b7bd708b5113426162b4f1d', 'App Tutorial', 'Publish 1 App',
    #                                   ['tutorial', 'official'], 'app', 1,
    #                                   'http://php8oeo4r.bkt.clouddn.com/5bd8327de3067c14dae01827-X59VR9.jpg', 'ZZ FF')
    # print(test_search_tags())
    # print(ElasticSearchSearvice.search_tags(['video'], index='project'))
    print(test_search_multi_fields())


'''
如果出现权限403禁止更新操作

这个问题是因为elasticsearch耗光了空间资源所导致.

elasticsearch5.exceptions.AuthorizationException: TransportError(403, 'cluster_block_exception', 'blocked by: [FORBIDDEN/12/index read-only / allow delete (api)];')

curl -H 'Content-Type: application/json' -X PUT -d '{"index": {"blocks": {"read_only_allow_delete": "false"}}}' http://localhost:9200/INDEX-NAME/_settings

INDEX_NAME: 就是建立索引的名字, 目前我们有  projects, requests, users

如果有新增, 记得加入.
'''
