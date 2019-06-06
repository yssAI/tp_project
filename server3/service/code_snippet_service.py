from server3.service.search_service import SearchService
from server3.business.code_snippet_business import CodeSnippetBusiness, MyThread
from server3.business.user_business import UserBusiness


class CodeSnippetService:

    @classmethod
    def get_search_result(cls, key_word, search_type, page_no, page_size):

        start = (page_no - 1) * page_size
        end = page_no * page_size
        if search_type == 'mix' or search_type == 'filter_cloud':
            t1 = MyThread(SearchService.search_code_snippet, (key_word,))
            t2 = MyThread(CodeSnippetBusiness.get_search_code, (key_word,))
            t1.setDaemon(True)
            t2.setDaemon(True)
            t1.start()
            t2.start()
            t1.join()
            t2.join()
            local_result = t1.get_result()
            cloud_result = t2.get_result()
            local_url = []
            for local in local_result['hits']:
                # print(local)
                if 'detail_url' in local:
                    local_url.append(local['detail_url'])
            # print(local_url)

            cloud_result_filter = []
            for cloud in cloud_result:
                if cloud['detail_url'] not in local_url:
                    cloud_result_filter.append(cloud)
            if search_type == 'mix':
                temp_result = sorted(local_result['hits'], key=lambda e: e.__getitem__('insert_num'), reverse=True)
                # temp_result = local_result['hits'].sort(key=lambda k: (k.get('insert_num', 0)), reverse=True)
                all_result = temp_result + cloud_result_filter
            else:
                all_result = cloud_result_filter
            # all_result = local_result['hits'] + cloud_result_filter
        elif search_type == 'local':
            local_result = SearchService.search_code_snippet(key_word)
            all_result = sorted(local_result['hits'], key=lambda e: e.__getitem__('insert_num'), reverse=True)
            # all_result = local_result['hits'].sort(key=lambda k: (k.get('insert_num', 0)), reverse=True)
        elif search_type == 'cloud':
            all_result = CodeSnippetBusiness.get_search_code(key_word)
        else:
            return None

        return all_result[start:end], len(all_result)

    @classmethod
    def create_code_snippet(cls, own_user, code_name=None, code_des=None, code_tags=None, code_source=None,
                            detail_url=None, insert_num=0, action='insert', code_from=None, **kwargs):
        if code_tags is None:
            code_tags = []
        own_user = UserBusiness.get_by_user_ID(own_user)
        # user['insert_code_snippets'].append()
        code_snippet = CodeSnippetBusiness.create_code_snippet(own_user=own_user, code_name=code_name, code_des=code_des,
                                                               code_tags=code_tags, code_source=code_source,
                                                               detail_url=detail_url, insert_num=insert_num,
                                                               action=action, code_from=code_from, **kwargs)

        # code_snippet.update_time = datetime.utcnow()
        # code_snippet.save()
        # print(type(code_snippet))
        if code_snippet in own_user.insert_code_snippets:
            own_user.insert_code_snippets.remove(code_snippet)
            own_user.insert_code_snippets.append(code_snippet)
        else:
            own_user.insert_code_snippets.append(code_snippet)
        # 添加判断
        # 总共个数
        temp_num = len(own_user['insert_code_snippets'])
        if temp_num > 10:
            del own_user['insert_code_snippets'][0:temp_num-10]
        own_user.save()

        SearchService.delete_code_snippet(str(code_snippet.id))
        # 添加到 elasticsearch
        SearchService.add_code_snippet(code_snippet_id=code_snippet.id,
                                       code_name=code_snippet.code_name,
                                       code_des=code_des,
                                       code_tags=[tag for tag in code_snippet.code_tags],
                                       code_source=code_snippet.code_source,
                                       detail_url=code_snippet.detail_url,
                                       insert_num=code_snippet.insert_num)

    @classmethod
    def get_history_list(cls, user):
        user = UserBusiness.get_by_user_ID(user)
        objects = user.insert_code_snippets
        code_list = []
        for tem_object in objects:
            # print(type(tem_object.id))
            body = {
                'code_name': tem_object.code_name,
                'code_des': tem_object.code_des,
                'code_tags': tem_object.code_tags,
                'code_source': tem_object.code_source,
                'code_from': str(tem_object.id)
            }
            code_list.append(body)
        code_list.reverse()
        return code_list


if __name__ == '__main__':
    aa = CodeSnippetService.get_search_result('print')
    print(aa)
