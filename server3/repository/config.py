# encoding: utf-8
# import platform
# https://docs.python.org/3/library/configparser.html
# import codecs

import sys
import os

PY2 = sys.version_info[0] == 2
if PY2:
    import ConfigParser
    config = ConfigParser.ConfigParser()
else:
    # change to configparser instead of ConfigParse in favor of python3
    import configparser
    config = configparser.ConfigParser()

from server3.constants import MONGO

config_url = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          'config.ini')

config.read(config_url, encoding='utf-8')

mongo = MONGO


def get_mongo_host():
    return config.get(mongo, 'HOST')


def get_mongo_port():
    return int(config.get(mongo, 'PORT'))


def get_mongo_user():
    return config.get(mongo, 'USER')


def get_mongo_pass():
    return config.get(mongo, 'PASS')


def get_mongo_db():
    return config.get(mongo, 'DB')


def get_named_query(name):
    return config.get('NAMED_QUERY', name)


def get_named_return(name):
    return config.get('NAMED_RETURN', name)


def get_file_prop(name):
    return config.get('FILE', name)

# def test():
#     #print config.sections()
#     print config['NAMED_QUERY']['ALL_TEMP_WARNING']
#     #print config['NAMED_QUERY']['ALL_TEMP_WARNING'].encode('utf-8')
#
# if __name__ == "__main__":
#     getMongoHost()
