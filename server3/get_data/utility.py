# -*- coding: UTF-8 -*-
import time
import xmltodict
from zeep import Client
from bson import ObjectId
import simplejson as json
from requests import Session
from copy import deepcopy
from datetime import datetime, timedelta
from server3.get_data.fsu_transport import FSUTransport
# from server3.get_real_time_data.core_manager.mongo_manager import mongo_manager

try:
    from xml.etree import cElementTree as ET
except ImportError:
    from xml.etree import ElementTree as ET

ts = time.time()
utc_offset = (datetime.fromtimestamp(ts) -
              datetime.utcfromtimestamp(ts)).total_seconds()
UTC_ZONE = int(utc_offset / 3600)


def dict_to_xml(fsu_info, data=None):
    """
    xml构建生成
    :param fsu_info:
    :param data:
    :return:
    """
    root = ET.Element("Request")  # 设置一个根节点，标签为urlset
    pk_type = ET.SubElement(root, "PK_Type")  # 在根节点root下建立子节点
    name = ET.SubElement(pk_type, "Name")
    name.text = fsu_info['PK_Type']
    info = ET.SubElement(root, "Info")
    if fsu_info.get('FSUID'):
        fsuid = ET.SubElement(info, "FSUID")
        if str(fsu_info['FSUID']).find("CTZJ") == -1:
            fsuid.text = 'CTZJ' + str(fsu_info['FSUID']).zfill(7)
        else:
            fsuid.text = fsu_info['FSUID']

    if fsu_info['PK_Type'] == "GET_DATA":
        point_by_device = {}
        if data:
            sofsunodeid = data[0]['SOFSUNODEID']
            point_json = []
            for point in data:
                if point['SOFSUNODEID'] != sofsunodeid:
                    sofsunodeid = point['SOFSUNODEID']
                    point_json = []
                point_json.append(point)
                point_by_device[sofsunodeid] = point_json
        devicelist = ET.SubElement(info, "DeviceList")
        for i in point_by_device:
            deviceid = ET.SubElement(devicelist, "Device")
            deviceid.attrib['ID'] = str(i)
            for point in point_by_device[i]:
                pointid = ET.SubElement(deviceid, "ID")
                pointid.text = str(point['FSUNODEID'])
    result = ET.tostring(root, encoding="utf-8")
    head = '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>'
    result = head + str(result, encoding="utf-8")
    return result


def get_this_time(UTC_TIME=True):
    # this_time = datetime.now().strftime("%Y%m%d %H:%M:%S")
    if UTC_TIME:
        # 获取当前的 UTC时间 -- datetime类型值
        this_time = datetime.utcnow()
    else:
        # 获取当前时区的时间 -- datetime类型值
        this_time = datetime.now()
    return datetime.fromtimestamp(time.mktime(this_time.timetuple()))


def get_data_from_fsu(data, url):
    from os import path
    src = path.dirname(path.abspath(__file__))
    # print src # senseware\mongo目录
    try:
        # 政企版， 无外网访问，调用本地的XMl文件，避免网络的连接错误
        session = Session()
        client = Client(path.join(src, 'FSUService.wsdl'),
                        transport=FSUTransport(session=session, path=src))
    except Exception as e:
        # logging_custom.error(e)
        # 默认省动环版本， 默认执行
        client = Client(path.join(src, 'FSUService.wsdl'))
    # update_url_in_wsdl(url)
    client.service._binding_options['address'] = url
    # print('data的值', data)
    response = client.service.invoke(data)
    # save_xml_info_log_to_db("send_xml", {
    #     "data": data, "response": str(response),
    #     "url": url, "time": get_this_time()
    # })
    elem_dict = {}
    if response:
        resp = response['_value_1']
        # print resp
        # 返回_value_1:None 的情况判断
        if resp:
            try:
                elem_dict = xmltodict.parse(resp)
            except Exception as e:
                print('error is ', e)
                # logging_custom.error(e)
                # save_xml_info_log_to_db(
                #     "error_logs",
                #     {"category": "parseXML", "data": str(response),
                #      "url": url, "time": get_this_time()}
                # )
        else:
            elem_dict = {}
    else:
        # logging_custom.error("get_data_from_fsu data invalid: ")
        # logging_custom.debug(response)
        print('get_data_from_fsu data invalid')
        elem_dict = {}
    return elem_dict


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, datetime):
            time_str = str(o)
            # append microsecond string, because it will be removed when
            # microsecond equal to 0
            if o.microsecond == 0:
                time_str += '.000000'
            return time_str
        return json.JSONEncoder.default(self, o)


def convert_to_json(bson_obj):
    """
    convert bson to json
    将ObjectId去除，用于Restful API传递
    :param bson_obj:
    :return:
    """
    new_json_obj = JSONEncoder(ignore_nan=True).encode(bson_obj)
    new_json_obj = json.loads(new_json_obj)
    return new_json_obj


# def save_xml_info_log_to_db(collection, data):
#     """
#     封装存储日志和XML信息的方法
#     :param collection:
#     :param data:
#     :return:
#     """
#     mongo_manager.save_one(collection, data)


def data_operation(data_dict, x, data_list, b_points=None, PK_Type=None):
    """
    对获取的实时数据结果操作
    :param data_dict:
    :param x:
    :param data_list: 实时数据列表
    :param b_points: 监控点列表
    :param PK_Type: 实时数据来源 GET_DATA or SEND_DATA
    :return:
    """
    data_dict['device_id'] = int(get_attribute("ID", x))
    if b_points:
        # 将b接口的数据列表转换为{FSUNODEID:point}的词典里， 通过调用去快速找到对应监控点
        b_points = {sp["FSUNODEID"]: sp for sp in b_points}
    else:
        b_points = {}

    if 'TSemaphore' in x:
        if isinstance(x['TSemaphore'], list):  # 判断是否是列表
            for y in x['TSemaphore']:
                # 避免内存占用
                sp = b_points.get(int(get_attribute("ID", y)))
                data_dict_copy = deepcopy(point_data_to_dict(data_dict, y, sp, PK_Type))
                data_list.append(data_dict_copy)
        else:
            sp = b_points.get(int(get_attribute("ID", x['TSemaphore'])))
            data_dict_copy = deepcopy(point_data_to_dict(data_dict, x['TSemaphore'], sp, PK_Type))
            data_list.append(data_dict_copy)
    return data_list


def get_attribute(attr, data_dict):
    if attr in data_dict:
        return data_dict[attr]
    else:
        return data_dict.get("@" + attr, "")


def point_data_to_dict(data_dict, data, point=None, origin=None):
    """
    将FSU数据转换成数据库数据格式
    :param data_dict:
    :param data:
    :param point: 监控点的具体内容
    :param origin: 数据来源
    :return:
    """
    data_dict['FSUNODEID'] = int(get_attribute("ID", data))
    data_dict['point_id'] = int(get_attribute("ID", data))
    # if not point:
    #     mongo_manager.find_one("hierarchy_elements", {
    #         "FSUID": data_dict["FSUID"],
    #         "FSUNODEID": data_dict['FSUNODEID'],
    #         "category": "point"
    #     })
    data_dict['pointid'] = point['_id'] if point else None
    data_dict['type'] = int(get_attribute("Type", data))
    data_dict['status'] = int(get_attribute("Status", data))
    try:
        data_dict['create_time'] = format_str_to_datetime(get_attribute("Time", data))
    except:
        data_dict['create_time'] = get_attribute("Time", data)
    try:
        precision = 3
        if point.get('PERCISION') == 0 or point.get('PERCISION'):
            precision = int(point['PERCISION'])
        # 数据值转换为浮点型最多保留小数点后三位
        data_dict["value"] = round(float(get_attribute("Val", data)), precision)
    except:
        data_dict["value"] = get_attribute("Val", data)
    if origin:
        # 区分FSU主动推送过来的还是页面刷新获取到的数据
        data_dict["origin"] = origin
    data_dict['desc'] = get_attribute("Desc", data)
    data_dict['category'] = 'B_fsu'
    data_dict["update_time"] = get_this_time()
    return data_dict


def format_str_to_datetime(date_string):
    # 省动环接口 字符串转换为 UTC时间格式，入库：
    # string："20170102 12:23:40"  --> datetime(2017, 1, 2, 6, 23, 40)
    if isinstance(date_string, datetime):
        return date_string
    else:
        if date_string:
            try:
                date_str = datetime.strptime(date_string, '%Y%m%d %H:%M:%S')
            except ValueError:
                date_str = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
            if date_str.year == 1:
                return date_str
            timestamp = date_str - timedelta(hours=UTC_ZONE)
            return timestamp
        else:
            return None
