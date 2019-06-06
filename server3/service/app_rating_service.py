from server3.business.apprating_business import AppRatingBusiness
from server3.business.app_business import AppBusiness
from server3.business.event_business import EventBusiness
from collections import Counter
from server3.business.user_business import UserBusiness
import datetime
import os


filter_choices = ['top_rates', 'most_called', 'recent_add']


class AppRatingService(object):
    @classmethod
    def add_rating(cls, **kwargs):
        # 取出UserId 和 App Id
        # print(kwargs)
        user = UserBusiness.get_by_user_ID(kwargs['user_ID'])
        app = AppBusiness.get_by_id(kwargs['app'])
        if user.user_ID == app.user.user_ID:
            return []
        rate = AppRatingBusiness.app_rating_repo.read({'app': app, 'user': user})
        # print(rate)
        if len(rate) > 0:
            rate = rate[0]
            # 进行更新内容, 但是不会添加新的记录
            del kwargs['user_ID']
            del kwargs['app']
            # rate.update(**kwargs)
            # rate.save()
            # return cls._add_rate_info(rate)
            # print(rate.id, kwargs)
            return cls.update_rating(rate.id, **kwargs)
        else:
            kwargs['create_time'] = datetime.datetime.utcnow()
            kwargs['user'] = user
            kwargs['app'] = app
            rate = AppRatingBusiness.add_rating(**kwargs)
            return cls._add_rate_info(rate)

    @classmethod
    def _add_rate_info(cls, rate):
        rate.user_ID = rate.user.user_ID
        rate.avatarV = rate.user.avatarV
        rate.username = rate.user.username
        rate.avatar_url = rate.user.avatar_url
        return rate

    @classmethod
    def get_rate_by_app_and_user(cls, user_ID, app_id):
        user = UserBusiness.get_by_user_ID(user_ID)
        app = AppBusiness.get_by_id(app_id)
        rate = AppRatingBusiness.app_rating_repo.read({'app': app, 'user': user})
        if len(rate) > 0:
            rate = rate[0]
            return cls._add_rate_info(rate)
        return []

    @classmethod
    def update_rating(cls, rate_id, **kwargs):
        rate = AppRatingBusiness.update_by_rate_id(rate_id, **kwargs)
        return cls._add_rate_info(rate)

    @classmethod
    def get_rate_by_app_id(cls, app_id, page_no=1, page_size=10):
        rates = AppRatingBusiness.get_all_rateing_by_app_id(app_id)
        back_rates = []
        for rate in rates:
            back_rates.append(cls._add_rate_info(rate))
        if page_no is None or page_size is None:
            return rates
        return back_rates[(page_no - 1) * page_size : page_no * page_size], len(back_rates)

    @classmethod
    def delete_by_id(cls, rate_id):
        rate = AppRatingBusiness.app_rating_repo.delete_by_id(rate_id)
        print(rate)
        return cls._add_rate_info(rate)

    @classmethod
    def statistics(cls, app_id):
        comments = cls.get_rate_by_app_id(app_id, page_no=None, page_size=None)
        # 总数
        count = comments.count()
        # 每一个类别的分数
        statistics_info = comments.aggregate({
            '$group': {
                '_id': '$rate',
                'count': {'$push': '$rate'}
            }
        })
        # 添加总数
        back = {'total_count': count}
        for s in statistics_info:
            # trans_dict = {}
            # trans_dict['count'] = len(s['count'])
            # trans_dict['percent'] = s['count'] / count
            # back.append(s)
            if s['_id'] not in back:
                # float('%.2f' %(len(s['count']) / count))
                back[int(s['_id'])] = str(len(s['count']) / count)[:4]
        # 判断还有哪个没有返回
        for key in [1, 2, 3, 4, 5]:
            if key not in back.keys():
                back[key] = 0
        return back

    @classmethod
    def __sort_by(cls, apps, key):
        """
            快速排序, order_by 方法无法通过我后期传入的字段排序
        :param apps:
        :param key:
        :return:
        """
        startStack = [0,]
        endStack = [len(apps)-1,]
        while len(startStack) > 0 and len(endStack) > 0:
            start = startStack.pop()
            end = endStack.pop()
            if start > end:
                continue
            # 判断子数组是否有序
            i = start
            j = end
            while i < j:
                if key == 'avg_rate':
                    if apps[i].avg_rate < apps[j].avg_rate:
                        # 交换位置
                        apps[i], apps[j-1], apps[j] = apps[j-1], apps[j], apps[i]
                        j -= 1
                    else:
                        i += 1
                elif key == 'most_called':
                    if apps[i].most_called < apps[j].most_called:
                        # 交换位置
                        apps[i], apps[j-1], apps[j] = apps[j-1], apps[j], apps[i]
                        j -= 1
                    else:
                        i += 1
                else:
                    if apps[i].create_time < apps[j].create_time:
                        # 交换位置
                        apps[i], apps[j-1], apps[j] = apps[j-1], apps[j], apps[i]
                        j -= 1
                    else:
                        i += 1
            # 把子数组放入栈
            startStack.append(start)
            startStack.append(i + 1)
            endStack.append(i - 1)
            endStack.append(end)
        return apps

    @classmethod
    def _add_app_info(cls, apps):
        # 统计平均得分
        for app in apps:
            app_rates = cls.get_rate_by_app_id(app.id)
            if len(app_rates) > 0:
                avg_rating = app_rates.aggregate({
                    '_id': '$_id',
                    'avg_rate': {'$avg': '$rate'}
                })
                app.avg_rate = avg_rating['avg_rate']
            else:
                app.avg_rate = 0.0
            # 添加调用次数
            app.called = EventBusiness.get_number({'AppBusiness': app['id'], 'action': "call"})
            # 添加参数体, 一定是部署好的
            # if app.yml == 'true' and \
            #         app.status == cls.business.repo.STATUS.ACTIVE:
        return apps

    @classmethod
    def _filter_apps(cls, apps, choose_type):
        # apps = cls._add_app_info(apps)
        # 进行筛选
        if filter_choices.index(choose_type) == 0:
            # top
            # cls.__sort_by(apps, 'avg_rates'), apps.order_by('-avg_rate')
            return apps.order_by('-avg_rate')
        elif filter_choices.index(choose_type) == 1:
            # most_called
            # back = cls.__sort_by(apps, 'called')
            return apps.order_by('-called')
        else:
            # 创建时间
            # back = cls.__sort_by(apps, 'create_time')
            return apps.order_by('-update_time')

    @classmethod
    def list_apps(cls, search_query=None, page_no=1, page_size=5, tag=None, choose_type=None):
        if tag:
            # 通过标签筛选
            if not isinstance(tag, list):
                tag = tag.split(',')
            apps = AppBusiness.get_objects(search_query=None, has_version=True, privacy='public',
                                           tags=tag, page_size=page_size, page_no=page_no)
            apps, total_count = apps.objects, apps.count
            # AppBusiness.read({'tags': tag, 'privacy': 'public'})
            apps = cls._filter_apps(apps, 'top_rates')
        elif choose_type:
            # 其他
            apps = AppBusiness.get_objects(search_query=None, has_version=True, privacy='public',
                                           page_size=page_size, page_no=page_no)
            apps, total_count = apps.objects, apps.count
            # 切换 tab 键
            apps = cls._filter_apps(apps, choose_type)
        else:
            # search_query
            apps = AppBusiness.get_objects(search_query=search_query, has_version=True, privacy='public',
                                           page_size=page_size, page_no=page_no)
            apps, total_count = apps.objects, apps.count
            apps = cls._filter_apps(apps, 'top_rates')

        # 只需要返回最后一个版本
        for app in apps:
            path = app.path + '/OVERVIEW.md'
            if os.path.exists(path):
                with open(path, 'r') as file:
                    app.overview = file.read()
            app.versions = app.versions[-1]
            app.average_rate = app.avg_rate
            app.call_num = app.call
            app.user_ID = app.user.user_ID
            app.user_name = app.user.username
            app.avatarV = app.user.avatarV
            app.avatar_url = app.user.avatar_url
            app.args = AppBusiness.load_app_params(app, app.versions[-1])
        return apps, total_count

    @classmethod
    def phone_search_app(cls, page_size, page, search_query):
        apps = AppBusiness.repo.search(search_query, {'display_name': 'icontains'})
        apps = apps(status='active')
        start = (page - 1) * page_size
        end = page * page_size
        for app in apps:
            path = app.path + '/OVERVIEW.md'
            if os.path.exists(path):
                with open(path, 'r') as file:
                    app.overview = file.read()
            app.user_ID = app.user.user_ID
        return apps[start:end], len(apps)

    @classmethod
    def get_call_num(cls, app_id):
        app = AppBusiness.get_by_id(app_id)
        return app.call

    @classmethod
    def get_single_app(cls, app_id):
        app = AppBusiness.get_by_id(app_id)
        path = app.path + '/OVERVIEW.md'
        if os.path.exists(path):
            with open(path, 'r') as file:
                app.overview = file.read()
        app.versions = [app.versions[-1]]
        app.average_rate = app.avg_rate
        app.call_num = app.call
        app.user_ID = app.user.user_ID
        app.user_name = app.user.username
        app.avatarV = app.user.avatarV
        app.args = AppBusiness.load_app_params(app, app.versions[-1])
        app.avatar_url = app.user.avatar_url
        app.view_num = EventBusiness.get_number(
            {'app': app, 'action': "view"})
        return app

    @classmethod
    def get_call_num(cls, app_id):
        app = AppBusiness.get_by_id(app_id)
        return app.call

    @classmethod
    def self_apps(cls, user_ID):
        apps = AppBusiness.get_objects(user=UserBusiness.get_by_user_ID(user_ID), has_version=True)
        apps, total_count = apps.objects, apps.count
        for app in apps:
            path = app.path + '/OVERVIEW.md'
            if os.path.exists(path):
                with open(path, 'r') as file:
                    app.overview = file.read()
            app.versions = app.versions[-1]
            app.average_rate = app.avg_rate
            app.call_num = app.call
            app.view_num = EventBusiness.get_number(
                {app.type: app, 'action': "view"})
        return apps, total_count

    @classmethod
    def related_app(cls, app_id, user_ID=None, page_size=7):
        app = AppBusiness.get_by_id(app_id)
        tags = app.tags
        related_apps = AppBusiness.get_objects(tags=tags, has_version=True, privacy='public')
        related_apps, _ = related_apps.objects, related_apps.count
        related_ids = [str(a.id) for a in related_apps]
        # 拷贝一份
        back_apps = [app for app in related_apps]
        # 删除重复
        if app_id in related_ids:
            index = related_ids.index(app_id)
            del back_apps[index]
        if user_ID:
            self_app, _ = cls.self_apps(user_ID)
            # 拼接, 去重
            for a in self_app:
                if str(a.id) not in related_ids and 'tutorial' not in a.display_name.lower():
                    back_apps.append(a)
                    related_ids.append(str(a.id))
        # 判断是否小于七个
        if len(related_apps) < page_size:
            # 判断当前个数, 寻找剩余数量
            supplement_apps = AppBusiness.get_objects(page_size=page_size, has_version=True, privacy='public').objects
            for a in supplement_apps:
                if str(a.id) not in related_ids and 'tutorial' not in a.display_name.lower():
                    back_apps.append(a)
        # 添加数据
        for app in back_apps:
            path = app.path + '/OVERVIEW.md'
            if os.path.exists(path):
                with open(path, 'r') as file:
                    app.overview = file.read()
            app.versions = app.versions[-1]
            app.average_rate = app.avg_rate
            app.call_num = app.call
            app.avatar_url = app.user.avatar_url
        return back_apps, page_size

    @classmethod
    def list_tags(cls):
        # get all deployed
        # 'versions': {'$gt': 1}, 'privacy': 'public'
        apps = AppBusiness.read({'privacy': 'public'})
        apps = apps(versions__0__exists=True)
        back_tags = []
        for app in apps:
            tags = app.tags
            back_tags.extend([tag.id for tag in tags])
        back_tags = dict(Counter(back_tags))
        back_tags = sorted(back_tags.items(), key=lambda item: item[1], reverse=True)
        return [{'class': class_name, 'num': num} for class_name, num in back_tags]

    @classmethod
    def update_all_comments_time(cls):
        comments = AppRatingBusiness.read()
        for c in comments:
            if not c.updated_time:
                c.updated_time = c.create_time
                c.save()


if __name__ == '__main__':
    # 添加一个
    # AppRatingService.add_rating(app=AppBusiness.get_by_id('5acece140c11f3ce839249ae'),
    #                             comment='哈哈哈, 好啊', user=UserBusiness.get_by_id('5a68a3a20c11f31e6f3c4bd2'),
    #                             rate=5.0, create_time=datetime.datetime.utcnow(), app_version='0-2-6')
    # print(AppRatingService.get_rate_by_app_and_user('zhaofengli', '5acece140c11f3ce839249ae')[0].to_mongo())
    # print(AppRatingService.update_rating('5bda6c409ebea43581fa08d6', **{'comment': '我真的修改你了', 'rate': 1.0}))
    # print(AppRatingService.get_rate_by_app_and_user('zhaofengli', '5acece140c11f3ce839249ae')[0].to_mongo())
    # 测试添加
    # print(AppRatingService.add_rating(**{'user': 'zhaofengli', 'app': '5acece140c11f3ce839249ae',
    #                                      'rate': 4.5, 'comment': '测试添加一个已存在的, 我是第二次哦',
    #                                      'create_time': datetime.datetime.utcnow(),
    #                                      'app_version': '0-2-6'}).to_mongo())
    # print(AppRatingService.list_apps())
    # print(AppRatingService.statistics('5acece140c11f3ce839249ae'))
    # apps, _ = AppRatingService.list_apps(search_query=None, tag=None, choose_type='recent_add')
    # for app in apps:
    #     print(app.create_time, app.call_num, app.average_rate, app.update_time)
    AppRatingService.update_all_comments_time()
