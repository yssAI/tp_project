# -*- coding: UTF-8 -*-
"""
数据采集脚本
"""
import xmltodict
from server3.get_data import utility

from copy import deepcopy
import logging as logging_custom

try:
    from xml.etree import cElementTree as ET
except ImportError:
    from xml.etree import ElementTree as ET

from server3.get_data.data_for_fsu_request import get_data_for_fsu_info_by_soid
# from data_for_fsu_request import get_data_for_fsu_info_by_soid
# from core_manager.mongo_manager import mongo_manager

# 设置log的格式, 默认的level为DEBUG
logging_custom.basicConfig(
    level=logging_custom.INFO,
    format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
)


# def async_real_time_data(data):
#     cid = data.get('cid')
#     point_ids = data['SPID']  # 监控点的SPID
#     group_id = data.get('grpid')  # 默认是设备SOID
#
#     result = list(mongo_manager.find(
#         'hierarchy_elements',
#         {"category": "point",
#          'SPID': {"$in": point_ids}
#          }))
#     device = mongo_manager.find_one(
#         'hierarchy_elements',
#         {"category": "device", "SOID": group_id}
#     )
#     b_point_list = []
#     c_point_dict = {}
#     node_ids = []
#
#     for i in result:
#         if i.get("NBIOTID"):
#             continue
#         elif i.get("FSUID"):
#             i["SOFSUNODEID"] = device.get("FSUNODEID")
#             b_point_list.append(i)
#         elif i.get("CID"):
#             c_point_dict[i["NODEID"]] = i
#             node_ids.append(i["NODEID"])
#
#     if b_point_list:
#         # print b_point_list
#         res = get_real_time_data({"FSUID": b_point_list[0]['FSUID'],
#                                   "b_point_list": b_point_list
#                                   })
#         return res
#     if node_ids:
#         querystring = {
#             "code": "401",
#             "grpid": group_id,
#             "paramters": "[{ids:%s, count:%s, cid:%s}]" % (node_ids, len(node_ids), cid)
#         }
#         headers = {
#             'Content-Type': "application/json"
#         }
#
#         response = requests.request("GET", mongo_manager.active_interface,
#                                     headers=headers, params=querystring)
#         try:
#             json_str = response.json()
#         except Exception as e:
#             print '实时数据获取异常： ', e
#             json_str = {"count": 0}
#
#         new_list = []
#         if json_str.get("count") != 0:
#             nodes = utility.convert_to_json(json_str['ids'][0]['nodes'])
#             for i in nodes:
#                 # 更新正确的cid进入实时数据表
#                 i['cid'] = cid
#                 new_list.append(i)
#
#         return new_list


def get_real_time_data(soid):
    """
    实时数据接口根据mode决定何种类型点获取
    :param data:
    :return:
    """

    # fsuid = data.get('FSUID')
    # b_point_list = data.get("b_point_list")

    # fsu_info = B_FSU.get_b_fsu_info(fsuid)
    # fsu_info = mongo_manager.find_one('sdh_b_fsu', {'ID': int(fsuid)})
    # if fsu_info:
    #     fsu_server = mongo_manager.find_one('sdh_b_server', {'ID': int(fsu_info["SERVERID"])})
    #     if fsu_server:
    #         fsu_info["SERVERNAME"] = fsu_server["NAME"]
    #         fsu_info["SERVERPORT"] = fsu_server["PORT"]
    #     fsu_info['FSUID'] = 'CTZJ' + str(fsu_info['ID']).zfill(7)
    #     fsu_info['PK_Type'] = "GET_DATA"

        # elem_dict = B_FSU.get_fsu_data(fsu_info, b_point_list)

    data = get_data_for_fsu_info_by_soid(soid)
    fsu_info = data.get('fsu_info')
    b_point_list = data.get('b_point_list')
    url = 'http://{0}:{1}/services/FSUService'.format(fsu_info['FSUIP'],
                                                      fsu_info['FSUPORT'])
    xml_data = utility.dict_to_xml(fsu_info, b_point_list)
    elem_dict = utility.get_data_from_fsu(xml_data, url)

    result = translate_data_to_mongo(elem_dict, b_points=b_point_list)
    return result


def translate_data_to_mongo(data, b_points=None):
    data_list = []
    data_dict = {}
    if data:
        if 'Request' in data:
            data_copy = deepcopy(data['Request']['Info'])
            data_dict = {'FSUID': int(data_copy['FSUID'][4:])}
        else:
            try:
                data_copy = deepcopy(data['Response']['Info'])
            except:
                # 处理传入的数据 中嵌套新的xml，尽量解析完整
                data_xml = data['s:Envelope']['s:Body']['q1:invoke']['xmlData']
                data_dict = xmltodict.parse(data_xml['#text'])
                data_copy = deepcopy(data_dict['Response']['Info'])
            if 'FSUID' in data_copy:
                data_dict = {'FSUID': int(data_copy['FSUID'][4:])}
    else:
        # 异常信息, 获取不到, 或者格式不标准
        return []

    if data_copy.get('Result') == '1':
        if data_copy['Values'] and data_copy['Values'].get('DeviceList'):
            if isinstance(data_copy['Values']['DeviceList']['Device'], list):
                for x in data_copy['Values']['DeviceList']['Device']:
                    data_list = utility.data_operation(data_dict, x, data_list, b_points)
            else:
                x = data_copy['Values']['DeviceList']['Device']
                data_list = utility.data_operation(data_dict, x, data_list, b_points)

            data_real_time = deepcopy(data_list)
            result = "success"
            if result == 'success':
                return data_real_time
            else:
                return result
        else:
            return data_list


def get_197_data():
    all_data = [
        [{"cid": 1, "grpid": 21766,
          "SPID": [1254519, 1254520, 1254511, 1254512, 12284122, 12284127,
                   12284121, 12284129, 12284125,
                   12284126, 12284124, 12284128, 12284123]},
         {"cid": 1, "grpid": 384764, "SPID": [7355034]},
         {"cid": 1, "grpid": 21758, "SPID": [1254493, 1254494]}]
    ]

    down_list = []
    for i in all_data:
        now_time = utility.get_this_time()
        for one_data in i:
            try:
                new_list = get_real_time_data(one_data['grpid'])
            except:
                return None
            for data_json in new_list:
                # 统一修改时间  或者  统一添加新时间
                # i.update(get_time=now_time)
                data_json["update_time"] = now_time
                down_list.append(deepcopy(data_json))
    dic_data = {}
    for i in down_list:
        key = 'pointID_' + str(i['point_id'])
        dic_data[key] = i['value']
    dic_data['create_time'] = down_list[0]['create_time']
    dic_data['update_time'] = down_list[0]['update_time']
    return dic_data


if __name__ == '__main__':
    # while True:
    data_dic = get_197_data()
    print(data_dic)
    # time.sleep(10)
