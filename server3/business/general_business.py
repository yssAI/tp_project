import re
from server3.repository.general_repo import Repo
from server3.entity.general_entity import Objects
from operator import itemgetter
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from server3.constants import SMTP_SERVER, USERNAME, PASSWORD, SENDER


def check_auth(func):
    def _deco(cls, object_id, user_ID, *args, **kwargs):
        entity = cls.get_by_id(object_id)
        if entity.user.user_ID == user_ID or user_ID == 'admin':
            return func(cls, object_id, user_ID, *args, **kwargs)
        else:
            raise RuntimeError('no right to delete')

    return _deco


class GeneralBusiness:
    # 实例化后的 instance 走general repo
    repo = Repo(None)
    # class 不走general repo
    entity = None

    @classmethod
    def get_all(cls):
        project = cls.repo.read()
        return project

    # 另一种方式
    # @classmethod
    # def get_all(cls):
    #     return cls.__cls.objects().order_by('-_id')

    @classmethod
    def read(cls, query=None):
        if query is None:
            query = {}
        return cls.entity.objects(**query).order_by('-_id')

    @classmethod
    def filter(cls, **query):
        return cls.entity.objects(**query).order_by('-_id')

    @classmethod
    def get_by_id(cls, object_id):
        return cls.repo.read_by_id(object_id=object_id)

    @classmethod
    def read_unique_one(cls, **kwargs):
        return cls.repo.read_unique_one(kwargs)

    @classmethod
    def get_pagination(cls, query, page_no, page_size):
        start = (page_no - 1) * page_size
        end = page_no * page_size
        objects = cls.repo.read(query=query)
        count = objects.count()
        return Objects(objects=objects[start: end], count=count,
                       page_no=page_no,
                       page_size=page_size)

    @classmethod
    def create(cls, obj):
        return cls.repo.create(obj)

    @classmethod
    def create_one(cls, **kwargs):
        return cls.repo.create_one(**kwargs)

    @classmethod
    @check_auth
    def remove_by_id(cls, object_id, user_ID):
        return cls.repo.delete_by_id(object_id)

    @classmethod
    def get_hot_tag(cls, search_query, object_type, category=None,
                    user_request=False, status=None):
        max_number = 10
        queryJson ={}
        # 项目先不添加任何筛选条件
        if not user_request:
            objects = cls.repo.read_with_no_query()
        else:
            objects = cls.repo.read()
        if object_type != 'project':
            queryJson['type'] = object_type
        if not user_request:
            queryJson['privacy'] = 'public'
            # queryJson['type'] = object_type
            if object_type == 'module' and category:
                queryJson['category'] = category
        if status:
            queryJson['status'] = status
        if search_query:
            regex = re.compile('.*'+search_query+'.*', re.IGNORECASE)
            queryJson['tags__icontains'] = regex
            objects = objects(**queryJson)

            tag_freqs = cls.my_item_frequencies_map_reduce(objects, 'tags', object_type, user_request=user_request)
            top_tags = sorted(
                  ((k, v) for k, v in tag_freqs.items() if
                   search_query.lower() in k.lower()),
                  key=itemgetter(1),
                  reverse=True)[:max_number]
            return top_tags
        else:
            objects = objects(**queryJson)
            tag_freqs = cls.my_item_frequencies_map_reduce(objects, 'tags', object_type, user_request=user_request)
            # tag_freqs = objects.item_frequencies('tags', normalize=False)
            top_tags = sorted(tag_freqs.items(), key=itemgetter(1), reverse=True)[:5]
            return top_tags

    @classmethod
    def my_item_frequencies_map_reduce(cls, objects, field, project_type, user_request=False):
        map_func = """
            function() {
                var path = '{{~%(field)s}}'.split('.');
                var field = this;

                for (p in path) {
                    if (typeof field != 'undefined')
                       field = field[path[p]];
                    else
                       break;
                }
                if (field && field.constructor == Array) {
                    field.forEach(function(item) {
                        emit(item, 1);
                    });
                } else if (typeof field != 'undefined') {
                    emit(field, 1);
                } else {
                    emit(null, 1);
                }
            }
        """ % {'field': field}
        reduce_func = """
            function(key, values) {
                var total = 0;
                var valuesSize = values.length;
                for (var i=0; i < valuesSize; i++) {
                    total += parseInt(values[i], 10);
                }
                return total;
            }
        """
        if user_request:
            table = 'inline' + '_' + 'request_' + project_type
        else:
            table = 'inline' + '_' + project_type
        values = objects.map_reduce(map_func, reduce_func, table)
        frequencies = {}
        for f in values:
            key = f.key
            if isinstance(key, float):
                if int(key) == key:
                    key = int(key)
            frequencies[key] = int(f.value)

        return frequencies

    @classmethod
    def send_email(cls, email, subject, text):
        msg = MIMEMultipart('mixed')
        msg['Subject'] = subject
        msg['From'] = USERNAME+' <'+USERNAME+'>'
        receiver = email
        msg['To'] = email
        text_plain = MIMEText(text, 'html', 'utf-8')
        msg.attach(text_plain)
        smtp = smtplib.SMTP()
        smtp.connect(SMTP_SERVER)
        smtp.login(USERNAME, PASSWORD)
        smtp.sendmail(SENDER, receiver, msg.as_string())
        smtp.quit()


if __name__ == '__main__':
    # GeneralBusiness.load_from_pymongo()
    pass
