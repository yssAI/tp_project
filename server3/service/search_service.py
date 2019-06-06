from server3.service.elasticsearch_service import ElasticSearchSearvice
from server3.business.project_business import ProjectBusiness
from server3.business.user_business import UserBusiness
from server3.business.user_request_business import UserRequestBusiness
from server3.business.event_business import EventBusiness
from server3.business.app_business import AppBusiness
from server3.business.module_business import ModuleBusiness
from server3.business.data_set_business import DatasetBusiness
import copy
import jieba
import numpy as np


bus_type_mapper = {
    "app": AppBusiness,
    "module": ModuleBusiness,
    "dataset": DatasetBusiness,
}

INDICATE_SEARCH = ['app:', 'module:', 'dataset:', 'requests:', 'users:']

MAPPING = ['app', 'module', 'dataset', 'user', 'request', 'code_snippet']

FIELDS = {'app': ['display_name', 'description'],
            'module': ['display_name', 'description'],
            'dataset': ['display_name', 'description'],
            'user': ['username', 'bio'],
            'request': ['request_title', 'description'],
          'code_snippet': ['code_name', 'code_des', 'code_tags', 'code_source', 'detail_url']}

COMBINEKEYS = ['app', 'module', 'dataset']


class SearchService:
    @classmethod
    def __split_with_advanced_search(cls, values):
        selected = ''
        copy_values = values
        for index in INDICATE_SEARCH:
            if index in values:
                selected = index
                break
        if selected != '':
            # 定向搜索
            wait_for_search_values = values.split(selected)[1]
            copy_values = copy.deepcopy(wait_for_search_values)
            # for v_index in range(len(wait_for_search_values)):
            #     if wait_for_search_values[v_index] == '' or wait_for_search_values[v_index] == ' ':
            #         del copy_values[v_index]
            #     else:
            #         continue
        selected = selected.split(':')[0]
        if selected in MAPPING:
            selected += 's'
        return selected, copy_values

    @classmethod
    def __add_project_info(cls, project_id, sample_dict):
        try:
            project = ProjectBusiness.repo.read_by_id(project_id)
            view_num = EventBusiness.get_number({project.type: project, 'action': "view"})
            fork_num = EventBusiness.get_number({project.type: project, 'action': "fork"})
            star_num = EventBusiness.get_number({project.type: project, 'action': "star"})
            sample_dict['view_num'] = view_num
            sample_dict['favor_num'] = fork_num
            sample_dict['star_num'] = star_num
            sample_dict['user_ID'] = project.user.user_ID
            sample_dict['avatarV'] = project.user.avatarV
            sample_dict['avatar_url'] = project.user.avatar_url if project.user.avatar_url else ''
            sample_dict['status'] = project.status
            return sample_dict
        except Exception as e:
            print('项目被删除')
            return False


    @classmethod
    def __add_user_info(cls, user_ID, sample_dict):
        user = UserBusiness.repo.read_by_user_ID(user_ID)
        if 'username' not in sample_dict:
            sample_dict['username'] = user.username
        return sample_dict

    @classmethod
    def __add_request_info(cls, request_id, sample_dict):
        try:
            request = UserRequestBusiness.repo.read_by_id(request_id)
            sample_dict['view_num'] = EventBusiness.get_number({'request': request, 'action': "view"})
            sample_dict['star_num'] = len(request.favor_users)
            sample_dict['favor_num'] = len(request.star_users)
            sample_dict['user_ID'] = request.user.user_ID
            sample_dict['avatarV'] = request.user.avatarV
            sample_dict['create_time'] = str(request.create_time)
            sample_dict['avatar_url'] = request.user.avatar_url if request.user.avatar_url else ''
            return sample_dict
        except Exception as e:
            print('request不存在')
            return False

    @classmethod
    def __pre_process_results(cls, results, search_text, is_title=False):
        if len(results.values()) > 0:
            key = list(results.keys())[0]
            values = results[key]['hits']
            total = values['total']
            hits = values['hits']
            pre_process = []
            for hit in hits:
                if 'highlight' not in hit:
                    continue
                highlight = hit['highlight']
                source = hit['_source']
                search_id = hit['_id']
                sample_data = {}
                # if key[-1] == 's':
                #     fields = FIELDS[key[:-1]]
                # else:
                #     fields = FIELDS[key]
                for field in source:
                    if field in highlight:
                        sample_data[field] = highlight[field][0]
                    else:
                        sample_data[field] = source[field]
                sample_data['id'] = search_id
                # 添加字段
                if not is_title:
                    if 'app' in key or 'module' in key or 'dataset' in key:
                        sample_data = cls.__add_project_info(sample_data['id'], sample_data)
                    elif 'request' in key:
                        sample_data = cls.__add_request_info(sample_data['id'], sample_data)
                if sample_data:
                    pre_process.append(sample_data)
            return key, total, pre_process

    @classmethod
    def __single_table_search(cls, results, selected, search_text, is_title=False):
        hits = results['hits']['hits']
        total = results['hits']['total']
        pre_process = []
        for hit in hits:
            if 'highlight' not in hit:
                continue
            highlight = hit['highlight']
            source = hit['_source']
            search_id = hit['_id']
            for field in highlight.keys():
                source[field] = highlight[field][0]
            source['id'] = search_id
            if not is_title:
                # 添加字段
                if 'app' in selected or 'module' in selected or 'dataset' in selected:
                    source = cls.__add_project_info(source['id'], source)
                # elif 'user' in selected:
                #     source = cls.__add_user_info(source['id'], source)
                elif 'request' in selected:
                    source = cls.__add_request_info(source['id'], source)
                elif 'code_snippet' in selected:
                    source = cls.__add_request_info(source['id'], source)
            if source:
                pre_process.append(source)
        return total, pre_process

    @classmethod
    def search_title(cls, values, start=0, size=3):
        selected, copy_values = cls.__split_with_advanced_search(values)
        # print("copy_valuescopy_values:", copy_values)
        copy_values = jieba.lcut_for_search(copy_values)
        # 处理后的结果
        processed_data = []

        if ElasticSearchSearvice.is_available():
            if selected != '':
                if len(copy_values) > 0:
                    results, count_info = ElasticSearchSearvice.search_title(copy_values, index=selected)
                    total, pre_process = cls.__single_table_search(results, selected, copy_values)
                    # total, data = cls.__single_table_search(results, selected, copy_values, is_title=True)
                    # 单表查询
                    processed_data.append({selected:
                                           {'total': total, 'hits': pre_process}})
                else:
                    # 没有输入就什么也不查询
                    results = {'message': 'no data'}
                    return results
            else:
                # 全局搜索
                # values.split(' ')
                wait_for_search_values = copy_values
                results, count_info = ElasticSearchSearvice.search_title(search_value=wait_for_search_values)
                # 所有表查询结果
                for result in results:
                    # analysis = cls.__pre_process_results(result, wait_for_search_values, is_title=True)
                    # if analysis:
                    #     key, total, pre_process = analysis
                    selected = list(result.keys())[-1]
                    values = list(result.values())[-1]
                    total, pre_process = cls.__single_table_search(values, selected, copy_values)
                    processed_data.append({selected: {'total': total, 'hits': pre_process}})
        else:
            processed_data = []
            count_info = {'apps': 0, 'modules': 0, 'datasets': 0}
        return processed_data, count_info

    @classmethod
    def __get_the_type_array(cls, results):
        apps = []
        modules = []
        datasets = []
        hits = results['hits']['hits']
        for hit in hits:
            source = hit['_source']
            source['id'] = hit['_id']
            source = cls.__add_project_info(project_id=source['id'], sample_dict=source)
            if source['type'] == 'app':
                apps.append(source)
            elif source['type'] == 'module':
                modules.append(source)
            else:
                datasets.append(source)
        return apps, modules, datasets

    @classmethod
    def __parse_search_tag(cls, results, index):
        hits = results['hits']['hits']
        back = []
        for hit in hits:
            values = hit['_source']
            if index == 'project':
                values = cls.__add_project_info(hit['_id'], values)
            else:
                values = cls.__add_request_info(hit['_id'], values)
            back.append(values)
        return back

    @classmethod
    def search_tags(cls, tags, start=0, size=10, index='all', project_type='app'):
        if not isinstance(tags, list):
            tags = tags.split(',')

        if ElasticSearchSearvice.is_available():
            if index == 'all':
                projects, requests = ElasticSearchSearvice.search_tags(tags, start=start, size=size,
                                                                       index=index, project_type=project_type)

                project_total_num = projects['hits']['total']
                request_total_num = requests['hits']['total']

                projects = cls.__parse_search_tag(projects, 'project')

                requests = cls.__parse_search_tag(requests, 'request')

                back_data = {'projects': {'total': project_total_num, 'hits': projects},
                             'requests': {'total': request_total_num, 'hits': requests}}
            else:
                requests = ElasticSearchSearvice.search_tags(tags, start=start, size=size,
                                                             index=index, project_type=project_type)
                request_total_num = requests['hits']['total']
                results = cls.__parse_search_tag(requests, index)
                back_data = {'projects': {'total': request_total_num,
                                          'hits': {project_type: results}}}
        else:
            back_data = {'projects': {'total': 0, 'hints': {}}}

        return back_data

    @classmethod
    def __split_request(cls, datas):
        apps = []
        modules = []
        datasets = []
        for data in datas:
            print(data)
            if data.get('type') == 'app':
                apps.append(data)
            elif data.get('type') == 'module':
                modules.append(data)
            elif data.get('type') == 'dataset':
                datasets.append(data)
        return apps, modules, datasets

    @classmethod
    def search_code_snippet(cls, search_value, start=0, size=10, request_type=None):
        if not isinstance(search_value, list):
            search_value = jieba.lcut_for_search(search_value)
        # print(search_value)
        if ElasticSearchSearvice.is_available():
            results = ElasticSearchSearvice.search_code_snippet(fields=['code_name', 'code_des', 'code_tags', 'code_source'],
                                                                index='code_snippets', search_values=search_value,
                                                                start=start, size=size)
            hits = results['hits']['hits']
            # print(hits)
            total = results['hits']['total']
            pre_process = []
            for hit in hits:
                source = hit['_source']
                search_id = hit['_id']
                # source['id'] = search_id
                source['code_from'] = search_id
                pre_process.append(source)
            # total, pre_process = cls.__single_table_search(results, 'code_snippets', search_value)
            return {'total': total, 'hits': pre_process}
        else:
            print('空的')
            return {'total': 0, 'hints': []}

    @classmethod
    def search(cls, search_value, index='app', start=0, size=3, request_type=None):
        if not isinstance(search_value, list):
            search_value = jieba.lcut_for_search(search_value)
        if index in MAPPING:
            selected = index + 's'
        else:
            selected = index

        if ElasticSearchSearvice.is_available():
            results, count_info = ElasticSearchSearvice.search_fields(fields=FIELDS[index],
                                                                      index=selected, search_values=search_value,
                                                                      start=start, size=size, request_type=request_type)
            print(results, count_info)
            # print(results)
            # 数据处理
            total, pre_process = cls.__single_table_search(results, selected, search_value)
            # if 'request' in selected:
            #     apps, modules, datasets = cls.__split_request(pre_process)
            #     return {selected: {'total': total, 'hits': {'apps': apps, 'modules': modules, 'datasets': datasets}},
            #             'count': count_info}
            # if not count_info['project_nums'] and 'dataset' in selected:
            #     pre_process = []
            return {selected: {'total': total, 'hits': pre_process}, 'count': count_info}
        return {selected: {'total': 0, 'hints': []}, 'count': {}}

    @classmethod
    def related_projects(cls, **args):
        if ElasticSearchSearvice.is_available():
            page_no = args.get('page_no')
            page_size = args.get('page_size')
            project_id = args.get('project_id')
            project_type =args.get('project_type')
            project = ProjectBusiness.get_by_id(project_id)
            tags = [tag.id for tag in project.tags]
            projects = []
            for tag in tags:
                ps = bus_type_mapper[project_type].repo.search(tag, {'tags': 'icontains'})
                ps = ps(status='active')
                for p in ps:
                    if 'tutorial' not in p.display_name.lower():
                        projects.append(p)
                # projects.extend(ps)
            np.random.shuffle(projects)
            if not isinstance(projects, list):
                projects = projects.tolist()
            return projects[(page_no - 1) * page_size: page_no * page_size], len(projects)
        return [], 0

    @classmethod
    def add_all(cls):
        ElasticSearchSearvice.add_all()

    @classmethod
    def delete_all(cls):
        ElasticSearchSearvice.delete_all()

    @classmethod
    def refresh_all(cls):
        ElasticSearchSearvice.refresh_index()

    @classmethod
    def add_user(cls, user_ID, username, bio, avatarV, avatar_url):
        if ElasticSearchSearvice.is_available():
            ElasticSearchSearvice.add_user(user_ID, username, bio, avatarV, avatar_url)

    @classmethod
    def add_project(cls, project_id, display_name, description, tags, project_type, img_v, photo_url, username):

        if ElasticSearchSearvice.is_available():
            cls.project = ElasticSearchSearvice.add_project(project_id, display_name, description, tags, project_type,
                                                            img_v, photo_url, username)

    @classmethod
    def add_request(cls, request_title, description, request_type, username, request_id):
        if ElasticSearchSearvice.is_available():
            ElasticSearchSearvice.add_request(request_title, description, request_type, username, request_id)

    @classmethod
    def add_code_snippet(cls, code_snippet_id,  code_name, code_des, code_tags, code_source, detail_url, insert_num):
        if ElasticSearchSearvice.is_available():
            ElasticSearchSearvice.add_code_snippet(code_snippet_id,  code_name, code_des, code_tags,
                                                   code_source, detail_url, insert_num)

    @classmethod
    def delete_project(cls, project_id):
        if ElasticSearchSearvice.is_available():
            ElasticSearchSearvice.delete_project(project_id)

    @classmethod
    def delete_code_snippet(cls, code_snippet_id):
        if ElasticSearchSearvice.is_available():
            ElasticSearchSearvice.delete_project(code_snippet_id)

    @classmethod
    def delete_users(cls, user_ID):
        if ElasticSearchSearvice.is_available():
            ElasticSearchSearvice.delete_project(user_ID)

    @classmethod
    def delete_request(cls, request_id):
        if ElasticSearchSearvice.is_available():
            ElasticSearchSearvice.delete_request(request_id)


# MARK: 单元测试
if __name__ == '__main__':
    # test_titles1 = 'chentiyun'
    # test_titles2 = 'module: g'
    # test_tags = ['video']
    # # 提取部分
    # import time
    # from pprint import pprint
    # start = time.time()
    # print(SearchService.search_title(test_titles1))
    # # SearchService.search_title(test_titles2)
    # print(SearchService.search(test_titles1))
    from pprint import pprint
    # pprint(SearchService.search_code_snippet('print'))
    # pprint(SearchService.search_tags(tags=test_tags, index='all'))
    # print('end time:', time.time() - start)
    ElasticSearchSearvice.delete_all()
    ElasticSearchSearvice.add_all()

    # 测试删除
    # SearchService.delete_project('5b83fc930c11f3302f4d07c6')
