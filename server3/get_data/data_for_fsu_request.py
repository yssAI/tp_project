# encoding: utf-8
"""
用于存放向fsu发送请求所需要的所有数据
"""
import datetime
from bson import ObjectId

data_dict = {
    21766: {
        'b_point_list': [
            {u'SOID': 21766, u'NETTYPE': 0, u'CID': 16, 'SOFSUNODEID': 3708928,
             u'DESCRIBE': u'', u'NODEID': 3708929, u'HILIMIT4': -99999.0,
             u'HILIMIT2': -99999.0, u'HILIMIT3': -99999.0, u'HILIMIT1': 1.0,
             u'AID': 103, u'FSUID': 197, u'STORAGEMODE': u'', u'SUID': 2644,
             u'NODECODE': u'0224173001', u'ALARMTHRESBHOLD': u'',
             u'DEVICETYPEID': 24,
             u'parents': {u'town': u'衢州_衢州市',
                          u'city': u'衢州市',
                          u'station': u'衢_C_衢州航埠局',
                          u'device': u'新风设备(2F程控机房_1#浙邮工程KYS-XFII-24000)'},
             u'SYID': 213626, u'ALARMLEVEL': 1, u'category': u'point',
             u'NODENAME': u'室外温度',
             u'NODEDESC': u'室外温度', u'FSUNODEID': 3708929,
             u'STANDER': 0.0, u'LOLIMIT1': 0.0, u'LOLIMIT3': -99999.0,
             u'SPID': 1254511, u'CONTROLENABLE': u'', u'STORAGETHRESHOLD': u'',
             u'UNIT': u'℃', u'MAXVAL': 100.0,
             u'UPDATETIME': datetime.datetime(2019, 6, 3, 16, 55, 56),
             u'STORAGEINTERVAL': u'', u'NODETYPE': 3,
             u'name': u'室外温度', u'ALARMLOGTYPE': None,
             u'VIRTUALTYPE': 0, u'MINVAL': 0.0, u'PERCISION': 2, u'SCID': 8,
             u'organization': ObjectId('5a1a6065c1ebde099c1bcbcd'),
             u'LOLIMIT2': -99999.0,
             u'_id': ObjectId('5a425e6887ea64b6c0515384'),
             u'LOLIMIT4': -99999.0, u'operate': u'update_aic'},
            {u'SOID': 21766, u'NETTYPE': 0, u'CID': 16, 'SOFSUNODEID': 3708928,
             u'DESCRIBE': u'', u'NODEID': 3708930, u'HILIMIT4': -99999.0,
             u'HILIMIT2': -99999.0, u'HILIMIT3': -99999.0, u'HILIMIT1': 1.0,
             u'AID': 103, u'FSUID': 197, u'STORAGEMODE': u'', u'SUID': 2644,
             u'NODECODE': u'0224174001', u'ALARMTHRESBHOLD': u'',
             u'DEVICETYPEID': 24,
             u'parents': {u'town': u'衢州_衢州市',
                          u'city': u'衢州市',
                          u'station': u'衢_C_衢州航埠局',
                          u'device': u'新风设备(2F程控机房_1#浙邮工程KYS-XFII-24000)'},
             u'SYID': 213626, u'ALARMLEVEL': 3, u'category': u'point',
             u'NODENAME': u'室外湿度',
             u'NODEDESC': u'室外相对湿度',
             u'FSUNODEID': 3708930, u'STANDER': 0.0, u'LOLIMIT1': 0.0,
             u'LOLIMIT3': -99999.0, u'SPID': 1254512, u'CONTROLENABLE': u'',
             u'STORAGETHRESHOLD': u'', u'UNIT': u'%RH', u'MAXVAL': 100.0,
             u'UPDATETIME': datetime.datetime(2019, 6, 3, 16, 55, 56),
             u'STORAGEINTERVAL': u'', u'NODETYPE': 3,
             u'name': u'室外湿度', u'ALARMLOGTYPE': None,
             u'VIRTUALTYPE': 0, u'MINVAL': 0.0, u'PERCISION': 2, u'SCID': 8,
             u'organization': ObjectId('5a1a6065c1ebde099c1bcbcd'),
             u'LOLIMIT2': -99999.0,
             u'_id': ObjectId('5a425e6887ea64b6c0515385'),
             u'LOLIMIT4': -99999.0, u'operate': u'update_aic'},
            {u'SOID': 21766, u'NETTYPE': 0, u'CID': 16, 'SOFSUNODEID': 3708928,
             u'DESCRIBE': u'', u'NODEID': 3708938, u'HILIMIT4': -99999.0,
             u'HILIMIT2': -99999.0, u'HILIMIT3': -99999.0, u'HILIMIT1': 1.0,
             u'AID': 103, u'FSUID': 197, u'STORAGEMODE': u'', u'SUID': 2644,
             u'NODECODE': u'0224171001', u'ALARMTHRESBHOLD': u'',
             u'DEVICETYPEID': 24,
             u'parents': {u'town': u'衢州_衢州市',
                          u'city': u'衢州市',
                          u'station': u'衢_C_衢州航埠局',
                          u'device': u'新风设备(2F程控机房_1#浙邮工程KYS-XFII-24000)'},
             u'SYID': 213626, u'ALARMLEVEL': 3, u'category': u'point',
             u'NODENAME': u'室内温度',
             u'NODEDESC': u'室内温度', u'FSUNODEID': 3708938,
             u'STANDER': 0.0, u'LOLIMIT1': 0.0, u'LOLIMIT3': -99999.0,
             u'SPID': 1254519, u'CONTROLENABLE': u'', u'STORAGETHRESHOLD': u'',
             u'UNIT': u'℃', u'MAXVAL': 100.0,
             u'UPDATETIME': datetime.datetime(2019, 6, 3, 16, 55, 57),
             u'STORAGEINTERVAL': u'', u'NODETYPE': 3,
             u'name': u'室内温度', u'ALARMLOGTYPE': None,
             u'VIRTUALTYPE': 0, u'MINVAL': 0.0, u'PERCISION': 2, u'SCID': 8,
             u'organization': ObjectId('5a1a6065c1ebde099c1bcbcd'),
             u'LOLIMIT2': -99999.0,
             u'_id': ObjectId('5a425e8187ea64b6c051567a'),
             u'LOLIMIT4': -99999.0, u'operate': u'update_aic'},
            {u'SOID': 21766, u'NETTYPE': 0, u'CID': 16, 'SOFSUNODEID': 3708928,
             u'DESCRIBE': u'', u'NODEID': 3708939, u'HILIMIT4': -99999.0,
             u'HILIMIT2': -99999.0, u'HILIMIT3': -99999.0, u'HILIMIT1': 1.0,
             u'AID': 103, u'FSUID': 197, u'STORAGEMODE': u'', u'SUID': 2644,
             u'NODECODE': u'0224172001', u'ALARMTHRESBHOLD': u'',
             u'DEVICETYPEID': 24,
             u'parents': {u'town': u'衢州_衢州市',
                          u'city': u'衢州市',
                          u'station': u'衢_C_衢州航埠局',
                          u'device': u'新风设备(2F程控机房_1#浙邮工程KYS-XFII-24000)'},
             u'SYID': 213626, u'ALARMLEVEL': 3, u'category': u'point',
             u'NODENAME': u'室内湿度',
             u'NODEDESC': u'室内相对湿度',
             u'FSUNODEID': 3708939, u'STANDER': 0.0, u'LOLIMIT1': 0.0,
             u'LOLIMIT3': -99999.0, u'SPID': 1254520, u'CONTROLENABLE': u'',
             u'STORAGETHRESHOLD': u'', u'UNIT': u'%RH', u'MAXVAL': 100.0,
             u'UPDATETIME': datetime.datetime(2019, 6, 3, 16, 55, 57),
             u'STORAGEINTERVAL': u'', u'NODETYPE': 3,
             u'name': u'室内湿度', u'ALARMLOGTYPE': None,
             u'VIRTUALTYPE': 0, u'MINVAL': 0.0, u'PERCISION': 2, u'SCID': 8,
             u'organization': ObjectId('5a1a6065c1ebde099c1bcbcd'),
             u'LOLIMIT2': -99999.0,
             u'_id': ObjectId('5a425e8187ea64b6c051567b'),
             u'LOLIMIT4': -99999.0, u'operate': u'update_aic'},
            {u'SOID': 21766, u'NETTYPE': 0, u'CID': 16, 'SOFSUNODEID': 3708928,
             u'DESCRIBE': u'254&自定义', u'NODEID': 3708954,
             u'HILIMIT4': u'', u'HILIMIT2': u'', u'HILIMIT3': u'',
             u'HILIMIT1': u'', u'AID': 103, u'FSUID': 197, u'STORAGEMODE': u'',
             u'SUID': 2644, u'NODECODE': u'0224000001', u'ALARMTHRESBHOLD': 1,
             u'parents': {u'town': u'衢州_衢州市',
                          u'city': u'衢州市',
                          u'station': u'衢_C_衢州航埠局',
                          u'device': u'新风设备(2F程控机房_1#浙邮工程KYS-XFII-24000)'},
             u'SYID': 213626, u'ALARMLEVEL': 3, u'category': u'point',
             u'NODENAME': u'开关状态',
             u'NODEDESC': u'开关状态(自定义)',
             u'FSUNODEID': 3708954, u'STANDER': u'', u'LOLIMIT1': u'',
             u'LOLIMIT3': u'', u'SPID': 12284121, u'CONTROLENABLE': u'',
             u'STORAGETHRESHOLD': u'', u'UNIT': u'', u'MAXVAL': u'',
             u'UPDATETIME': datetime.datetime(2016, 12, 7, 9, 21, 45),
             u'STORAGEINTERVAL': u'', u'NODETYPE': 2,
             u'name': u'开关状态', u'ALARMLOGTYPE': u'',
             u'VIRTUALTYPE': 0, u'MINVAL': u'', u'PERCISION': u'', u'SCID': 8,
             u'organization': ObjectId('5a1a6065c1ebde099c1bcbcd'),
             u'LOLIMIT2': u'', u'_id': ObjectId('5a460a7f87ea64ade40f399d'),
             u'LOLIMIT4': u''},
            {u'SOID': 21766, u'NETTYPE': 0, u'CID': 16, 'SOFSUNODEID': 3708928,
             u'DESCRIBE': u'254&自定义', u'NODEID': 3708955,
             u'HILIMIT4': u'', u'HILIMIT2': u'', u'HILIMIT3': u'',
             u'HILIMIT1': u'', u'AID': 103, u'FSUID': 197, u'STORAGEMODE': u'',
             u'SUID': 2644, u'NODECODE': u'0224000001', u'ALARMTHRESBHOLD': 1,
             u'parents': {u'town': u'衢州_衢州市',
                          u'city': u'衢州市',
                          u'station': u'衢_C_衢州航埠局',
                          u'device': u'新风设备(2F程控机房_1#浙邮工程KYS-XFII-24000)'},
             u'SYID': 213626, u'ALARMLEVEL': 3, u'category': u'point',
             u'NODENAME': u'加湿机状态',
             u'NODEDESC': u'加湿机状态(自定义)',
             u'FSUNODEID': 3708955, u'STANDER': u'', u'LOLIMIT1': u'',
             u'LOLIMIT3': u'', u'SPID': 12284122, u'CONTROLENABLE': u'',
             u'STORAGETHRESHOLD': u'', u'UNIT': u'', u'MAXVAL': u'',
             u'UPDATETIME': datetime.datetime(2016, 12, 7, 9, 21, 45),
             u'STORAGEINTERVAL': u'', u'NODETYPE': 2,
             u'name': u'加湿机状态', u'ALARMLOGTYPE': u'',
             u'VIRTUALTYPE': 0, u'MINVAL': u'', u'PERCISION': u'', u'SCID': 8,
             u'organization': ObjectId('5a1a6065c1ebde099c1bcbcd'),
             u'LOLIMIT2': u'', u'_id': ObjectId('5a460a7f87ea64ade40f399e'),
             u'LOLIMIT4': u''},
            {u'SOID': 21766, u'NETTYPE': 0, u'CID': 16, 'SOFSUNODEID': 3708928,
             u'DESCRIBE': u'254&自定义', u'NODEID': 3708956,
             u'HILIMIT4': u'', u'HILIMIT2': u'', u'HILIMIT3': u'',
             u'HILIMIT1': u'', u'AID': 103, u'FSUID': 197, u'STORAGEMODE': u'',
             u'SUID': 2644, u'NODECODE': u'0224000001', u'ALARMTHRESBHOLD': 1,
             u'parents': {u'town': u'衢州_衢州市',
                          u'city': u'衢州市',
                          u'station': u'衢_C_衢州航埠局',
                          u'device': u'新风设备(2F程控机房_1#浙邮工程KYS-XFII-24000)'},
             u'SYID': 213626, u'ALARMLEVEL': 3, u'category': u'point',
             u'NODENAME': u'风机状态',
             u'NODEDESC': u'风机状态(自定义)',
             u'FSUNODEID': 3708956, u'STANDER': u'', u'LOLIMIT1': u'',
             u'LOLIMIT3': u'', u'SPID': 12284123, u'CONTROLENABLE': u'',
             u'STORAGETHRESHOLD': u'', u'UNIT': u'', u'MAXVAL': u'',
             u'UPDATETIME': datetime.datetime(2016, 12, 7, 9, 21, 45),
             u'STORAGEINTERVAL': u'', u'NODETYPE': 2,
             u'name': u'风机状态', u'ALARMLOGTYPE': u'',
             u'VIRTUALTYPE': 0, u'MINVAL': u'', u'PERCISION': u'', u'SCID': 8,
             u'organization': ObjectId('5a1a6065c1ebde099c1bcbcd'),
             u'LOLIMIT2': u'', u'_id': ObjectId('5a460a7f87ea64ade40f399f'),
             u'LOLIMIT4': u''},
            {u'SOID': 21766, u'NETTYPE': 0, u'CID': 16, 'SOFSUNODEID': 3708928,
             u'DESCRIBE': u'254&自定义', u'NODEID': 3708957,
             u'HILIMIT4': u'', u'HILIMIT2': u'', u'HILIMIT3': u'',
             u'HILIMIT1': u'', u'AID': 103, u'FSUID': 197, u'STORAGEMODE': u'',
             u'SUID': 2644, u'NODECODE': u'0224000001', u'ALARMTHRESBHOLD': 1,
             u'parents': {u'town': u'衢州_衢州市',
                          u'city': u'衢州市',
                          u'station': u'衢_C_衢州航埠局',
                          u'device': u'新风设备(2F程控机房_1#浙邮工程KYS-XFII-24000)'},
             u'SYID': 213626, u'ALARMLEVEL': 3, u'category': u'point',
             u'NODENAME': u'空调状态',
             u'NODEDESC': u'空调状态(自定义)',
             u'FSUNODEID': 3708957, u'STANDER': u'', u'LOLIMIT1': u'',
             u'LOLIMIT3': u'', u'SPID': 12284124, u'CONTROLENABLE': u'',
             u'STORAGETHRESHOLD': u'', u'UNIT': u'', u'MAXVAL': u'',
             u'UPDATETIME': datetime.datetime(2016, 12, 7, 9, 21, 45),
             u'STORAGEINTERVAL': u'', u'NODETYPE': 2,
             u'name': u'空调状态', u'ALARMLOGTYPE': u'',
             u'VIRTUALTYPE': 0, u'MINVAL': u'', u'PERCISION': u'', u'SCID': 8,
             u'organization': ObjectId('5a1a6065c1ebde099c1bcbcd'),
             u'LOLIMIT2': u'', u'_id': ObjectId('5a460a7f87ea64ade40f39a0'),
             u'LOLIMIT4': u''},
            {u'SOID': 21766, u'NETTYPE': 0, u'CID': 16, 'SOFSUNODEID': 3708928,
             u'DESCRIBE': u'254&自定义', u'NODEID': 3708958,
             u'HILIMIT4': u'', u'HILIMIT2': u'', u'HILIMIT3': u'',
             u'HILIMIT1': u'', u'AID': 103, u'FSUID': 197, u'STORAGEMODE': u'',
             u'SUID': 2644, u'NODECODE': u'0224000001', u'ALARMTHRESBHOLD': 1,
             u'parents': {u'town': u'衢州_衢州市',
                          u'city': u'衢州市',
                          u'station': u'衢_C_衢州航埠局',
                          u'device': u'新风设备(2F程控机房_1#浙邮工程KYS-XFII-24000)'},
             u'SYID': 213626, u'ALARMLEVEL': 3, u'category': u'point',
             u'NODENAME': u'排风阀状态',
             u'NODEDESC': u'排风阀状态(自定义)',
             u'FSUNODEID': 3708958, u'STANDER': u'', u'LOLIMIT1': u'',
             u'LOLIMIT3': u'', u'SPID': 12284125, u'CONTROLENABLE': u'',
             u'STORAGETHRESHOLD': u'', u'UNIT': u'', u'MAXVAL': u'',
             u'UPDATETIME': datetime.datetime(2016, 12, 7, 9, 21, 45),
             u'STORAGEINTERVAL': u'', u'NODETYPE': 2,
             u'name': u'排风阀状态', u'ALARMLOGTYPE': u'',
             u'VIRTUALTYPE': 0, u'MINVAL': u'', u'PERCISION': u'', u'SCID': 8,
             u'organization': ObjectId('5a1a6065c1ebde099c1bcbcd'),
             u'LOLIMIT2': u'', u'_id': ObjectId('5a460a7f87ea64ade40f39a1'),
             u'LOLIMIT4': u''},
            {u'SOID': 21766, u'NETTYPE': 0, u'CID': 16, 'SOFSUNODEID': 3708928,
             u'DESCRIBE': u'254&自定义', u'NODEID': 3708959,
             u'HILIMIT4': u'', u'HILIMIT2': u'', u'HILIMIT3': u'',
             u'HILIMIT1': u'', u'AID': 103, u'FSUID': 197, u'STORAGEMODE': u'',
             u'SUID': 2644, u'NODECODE': u'0224000001', u'ALARMTHRESBHOLD': 1,
             u'parents': {u'town': u'衢州_衢州市',
                          u'city': u'衢州市',
                          u'station': u'衢_C_衢州航埠局',
                          u'device': u'新风设备(2F程控机房_1#浙邮工程KYS-XFII-24000)'},
             u'SYID': 213626, u'ALARMLEVEL': 3, u'category': u'point',
             u'NODENAME': u'新风阀状态',
             u'NODEDESC': u'新风阀状态(自定义)',
             u'FSUNODEID': 3708959, u'STANDER': u'', u'LOLIMIT1': u'',
             u'LOLIMIT3': u'', u'SPID': 12284126, u'CONTROLENABLE': u'',
             u'STORAGETHRESHOLD': u'', u'UNIT': u'', u'MAXVAL': u'',
             u'UPDATETIME': datetime.datetime(2016, 12, 7, 9, 21, 45),
             u'STORAGEINTERVAL': u'', u'NODETYPE': 2,
             u'name': u'新风阀状态', u'ALARMLOGTYPE': u'',
             u'VIRTUALTYPE': 0, u'MINVAL': u'', u'PERCISION': u'', u'SCID': 8,
             u'organization': ObjectId('5a1a6065c1ebde099c1bcbcd'),
             u'LOLIMIT2': u'', u'_id': ObjectId('5a460a7f87ea64ade40f39a2'),
             u'LOLIMIT4': u''},
            {u'SOID': 21766, u'NETTYPE': 0, u'CID': 16, 'SOFSUNODEID': 3708928,
             u'DESCRIBE': u'254&自定义', u'NODEID': 3708960,
             u'HILIMIT4': u'', u'HILIMIT2': u'', u'HILIMIT3': u'',
             u'HILIMIT1': u'', u'AID': 103, u'FSUID': 197, u'STORAGEMODE': u'',
             u'SUID': 2644, u'NODECODE': u'0224000001', u'ALARMTHRESBHOLD': 1,
             u'parents': {u'town': u'衢州_衢州市',
                          u'city': u'衢州市',
                          u'station': u'衢_C_衢州航埠局',
                          u'device': u'新风设备(2F程控机房_1#浙邮工程KYS-XFII-24000)'},
             u'SYID': 213626, u'ALARMLEVEL': 3, u'category': u'point',
             u'NODENAME': u'回风阀状态',
             u'NODEDESC': u'回风阀状态(自定义)',
             u'FSUNODEID': 3708960, u'STANDER': u'', u'LOLIMIT1': u'',
             u'LOLIMIT3': u'', u'SPID': 12284127, u'CONTROLENABLE': u'',
             u'STORAGETHRESHOLD': u'', u'UNIT': u'', u'MAXVAL': u'',
             u'UPDATETIME': datetime.datetime(2016, 12, 7, 9, 21, 45),
             u'STORAGEINTERVAL': u'', u'NODETYPE': 2,
             u'name': u'回风阀状态', u'ALARMLOGTYPE': u'',
             u'VIRTUALTYPE': 0, u'MINVAL': u'', u'PERCISION': u'', u'SCID': 8,
             u'organization': ObjectId('5a1a6065c1ebde099c1bcbcd'),
             u'LOLIMIT2': u'', u'_id': ObjectId('5a460a7f87ea64ade40f39a3'),
             u'LOLIMIT4': u''},
            {u'SOID': 21766, u'NETTYPE': 0, u'CID': 16, 'SOFSUNODEID': 3708928,
             u'DESCRIBE': u'254&自定义', u'NODEID': 3708961,
             u'HILIMIT4': u'', u'HILIMIT2': u'', u'HILIMIT3': u'',
             u'HILIMIT1': u'', u'AID': 103, u'FSUID': 197, u'STORAGEMODE': u'',
             u'SUID': 2644, u'NODECODE': u'0224000001', u'ALARMTHRESBHOLD': 1,
             u'parents': {u'town': u'衢州_衢州市',
                          u'city': u'衢州市',
                          u'station': u'衢_C_衢州航埠局',
                          u'device': u'新风设备(2F程控机房_1#浙邮工程KYS-XFII-24000)'},
             u'SYID': 213626, u'ALARMLEVEL': 3, u'category': u'point',
             u'NODENAME': u'进水阀状态',
             u'NODEDESC': u'进水阀状态(自定义)',
             u'FSUNODEID': 3708961, u'STANDER': u'', u'LOLIMIT1': u'',
             u'LOLIMIT3': u'', u'SPID': 12284128, u'CONTROLENABLE': u'',
             u'STORAGETHRESHOLD': u'', u'UNIT': u'', u'MAXVAL': u'',
             u'UPDATETIME': datetime.datetime(2016, 12, 7, 9, 21, 45),
             u'STORAGEINTERVAL': u'', u'NODETYPE': 2,
             u'name': u'进水阀状态', u'ALARMLOGTYPE': u'',
             u'VIRTUALTYPE': 0, u'MINVAL': u'', u'PERCISION': u'', u'SCID': 8,
             u'organization': ObjectId('5a1a6065c1ebde099c1bcbcd'),
             u'LOLIMIT2': u'', u'_id': ObjectId('5a460a7f87ea64ade40f39a4'),
             u'LOLIMIT4': u''},
            {u'SOID': 21766, u'NETTYPE': 0, u'CID': 16, 'SOFSUNODEID': 3708928,
             u'DESCRIBE': u'254&自定义', u'NODEID': 3708962,
             u'HILIMIT4': u'', u'HILIMIT2': u'', u'HILIMIT3': u'',
             u'HILIMIT1': u'', u'AID': 103, u'FSUID': 197, u'STORAGEMODE': u'',
             u'SUID': 2644, u'NODECODE': u'0224000001', u'ALARMTHRESBHOLD': 1,
             u'parents': {u'town': u'衢州_衢州市',
                          u'city': u'衢州市',
                          u'station': u'衢_C_衢州航埠局',
                          u'device': u'新风设备(2F程控机房_1#浙邮工程KYS-XFII-24000)'},
             u'SYID': 213626, u'ALARMLEVEL': 3, u'category': u'point',
             u'NODENAME': u'强制通风状态',
             u'NODEDESC': u'强制通风状态(自定义)',
             u'FSUNODEID': 3708962, u'STANDER': u'', u'LOLIMIT1': u'',
             u'LOLIMIT3': u'', u'SPID': 12284129, u'CONTROLENABLE': u'',
             u'STORAGETHRESHOLD': u'', u'UNIT': u'', u'MAXVAL': u'',
             u'UPDATETIME': datetime.datetime(2016, 12, 7, 9, 21, 45),
             u'STORAGEINTERVAL': u'', u'NODETYPE': 2,
             u'name': u'强制通风状态',
             u'ALARMLOGTYPE': u'', u'VIRTUALTYPE': 0, u'MINVAL': u'',
             u'PERCISION': u'', u'SCID': 8,
             u'organization': ObjectId('5a1a6065c1ebde099c1bcbcd'),
             u'LOLIMIT2': u'', u'_id': ObjectId('5a460a7f87ea64ade40f39a5'),
             u'LOLIMIT4': u''}],
        'FSUID': 197,
        'fsu_info': {u'ENABLE': 1,
                     u'GETSTATETIME': datetime.datetime(2019, 1, 10, 7, 28, 8),
                     u'CHECKTIMETIME': datetime.datetime(2019, 6, 5, 19, 46,
                                                         51),
                     u'CHECKSTATUSTIME': datetime.datetime(2019, 1, 10, 7, 28,
                                                           8),
                     u'FTPPORT': u'21',
                     u'GETALARMTIME': datetime.datetime(2019, 1, 10, 7, 28, 8),
                     u'LASTLOGINTIME': datetime.datetime(2019, 6, 5, 19, 46,
                                                         51),
                     u'MODEL': u'虚拟现场采集器',
                     'FSUID': 'CTZJ0000197', u'SUID': 2644,
                     u'CONFIGUPDATETIME': None, u'ALARMSERIALNO': -246083,
                     u'FTPPASSWORD': u'8107', u'FSUIP': u'134.97.31.42',
                     'SERVERPORT': 3081,
                     u'SUPPLIER': u'浙江邮电工程建设有限公司',
                     u'USERNAME': u'JKQZ', u'ALARMSTATUS': 0, u'SERIALNO': u'',
                     'SERVERNAME': u'DCN B接口服务器',
                     u'BALARMSERIALNO': 4689387, u'SPID': 12341182,
                     u'SERVERID': 5, u'PASSWORD': u'JKQZ123456', u'ID': 197,
                     u'UPDATETIME': datetime.datetime(2019, 6, 5, 19, 46, 51),
                     u'NAME': u'衢_C_衢州航埠局虚拟现场采集器',
                     'PK_Type': 'GET_DATA',
                     u'GETDATATIME': datetime.datetime(2019, 1, 10, 7, 28, 8),
                     u'LASTCOMMUNICATETIME': datetime.datetime(2019, 1, 10, 7,
                                                               28, 8),
                     u'FSUPORT': u'42006',
                     u'MESSAGE': u'ORA-01653: unable to extend table PSCUSER.B_ALARM_LOG by 1024 in tablespace B_DATADATA',
                     u'_id': ObjectId('5c0e1458aca03d344accb111'),
                     u'FTPUSERNAME': u'8107',
                     u'UPDATESTATUSTIME': datetime.datetime(2019, 1, 10, 7, 28,
                                                            8)}
    },
    384764: {
        'b_point_list': [
            {u'pue_calc_type': u'E', u'SOID': 384764, u'NETTYPE': 0, u'CID': 16,
             'SOFSUNODEID': 3729408, u'DESCRIBE': u'', u'NODEID': 3729409,
             u'HILIMIT4': -99999.0, u'HILIMIT2': -99999.0,
             u'HILIMIT3': -99999.0, u'HILIMIT1': 99999997952.0, u'AID': 103,
             u'FSUID': 197, u'STORAGEMODE': u'', u'SUID': 2644,
             u'NODECODE': u'0416171001', u'ALARMTHRESBHOLD': u'',
             u'parents': {u'town': u'衢州_衢州市',
                          u'city': u'衢州市',
                          u'station': u'衢_C_衢州航埠局',
                          u'device': u'智能电表(1F低配室_机房动力用电_安科瑞DTSF)'},
             u'SYID': 239181, u'ALARMLEVEL': 3, u'category': u'point',
             u'NODENAME': u'总电度',
             u'NODEDESC': u'总电度', u'FSUNODEID': 3729409,
             u'STANDER': 0.0, u'LOLIMIT1': 0.0, u'LOLIMIT3': -99999.0,
             u'SPID': 7355034, u'CONTROLENABLE': u'', u'STORAGETHRESHOLD': u'',
             u'UNIT': u'Kwh', u'MAXVAL': 999999986991104.0,
             u'UPDATETIME': datetime.datetime(2016, 12, 7, 9, 21, 45),
             u'STORAGEINTERVAL': u'', u'NODETYPE': 3,
             u'name': u'总电度', u'ALARMLOGTYPE': u'',
             u'VIRTUALTYPE': 0, u'MINVAL': 0.0, u'PERCISION': 0, u'SCID': 8,
             u'organization': ObjectId('5a1a6065c1ebde099c1bcbcd'),
             u'LOLIMIT2': -99999.0,
             u'_id': ObjectId('5a43168887ea64b6c0619042'),
             u'LOLIMIT4': -99999.0}],
        'FSUID': 197,
        'fsu_info': {u'ENABLE': 1,
                     u'GETSTATETIME': datetime.datetime(2019, 1, 10, 7, 28, 8),
                     u'CHECKTIMETIME': datetime.datetime(2019, 6, 5, 19, 46,
                                                         51),
                     u'CHECKSTATUSTIME': datetime.datetime(2019, 1, 10, 7, 28,
                                                           8),
                     u'FTPPORT': u'21',
                     u'GETALARMTIME': datetime.datetime(2019, 1, 10, 7, 28, 8),
                     u'LASTLOGINTIME': datetime.datetime(2019, 6, 5, 19, 46,
                                                         51),
                     u'MODEL': u'虚拟现场采集器',
                     'FSUID': 'CTZJ0000197', u'SUID': 2644,
                     u'CONFIGUPDATETIME': None, u'ALARMSERIALNO': -246083,
                     u'FTPPASSWORD': u'8107', u'FSUIP': u'134.97.31.42',
                     'SERVERPORT': 3081,
                     u'SUPPLIER': u'浙江邮电工程建设有限公司',
                     u'USERNAME': u'JKQZ', u'ALARMSTATUS': 0, u'SERIALNO': u'',
                     'SERVERNAME': u'DCN B接口服务器',
                     u'BALARMSERIALNO': 4689387, u'SPID': 12341182,
                     u'SERVERID': 5, u'PASSWORD': u'JKQZ123456', u'ID': 197,
                     u'UPDATETIME': datetime.datetime(2019, 6, 5, 19, 46, 51),
                     u'NAME': u'衢_C_衢州航埠局虚拟现场采集器',
                     'PK_Type': 'GET_DATA',
                     u'GETDATATIME': datetime.datetime(2019, 1, 10, 7, 28, 8),
                     u'LASTCOMMUNICATETIME': datetime.datetime(2019, 1, 10, 7,
                                                               28, 8),
                     u'FSUPORT': u'42006',
                     u'MESSAGE': u'ORA-01653: unable to extend table PSCUSER.B_ALARM_LOG by 1024 in tablespace B_DATADATA',
                     u'_id': ObjectId('5c0e1458aca03d344accb111'),
                     u'FTPUSERNAME': u'8107',
                     u'UPDATESTATUSTIME': datetime.datetime(2019, 1, 10, 7, 28,
                                                            8)}
    },
    21758: {
        'b_point_list': [
            {u'SOID': 21758, u'NETTYPE': 0, u'CID': 16, 'SOFSUNODEID': 3692544,
             u'DESCRIBE': u'', u'NODEID': 3692545, u'HILIMIT4': -99999.0,
             u'HILIMIT2': -99999.0, u'HILIMIT3': -99999.0, u'HILIMIT1': 33.0,
             u'AID': 103, u'FSUID': 197, u'STORAGEMODE': u'', u'SUID': 2644,
             u'NODECODE': u'0218101001', u'ALARMTHRESBHOLD': u'',
             u'DEVICETYPEID': 18,
             u'parents': {u'town': u'衢州_衢州市',
                          u'city': u'衢州市',
                          u'station': u'衢_C_衢州航埠局',
                          u'device': u'机房环境(2F程控室)'},
             u'SYID': 213625, u'ALARMLEVEL': 1, u'category': u'point',
             u'NODENAME': u'环境信号(1#温度_2F程控室南侧)',
             u'NODEDESC': u'温度', u'FSUNODEID': 3692545,
             u'STANDER': 0.0, u'LOLIMIT1': 7.0, u'LOLIMIT3': -99999.0,
             u'SPID': 1254493, u'CONTROLENABLE': u'', u'STORAGETHRESHOLD': u'',
             u'UNIT': u'℃', u'MAXVAL': 100.0,
             u'UPDATETIME': datetime.datetime(2019, 6, 3, 16, 55, 55),
             u'STORAGEINTERVAL': u'', u'NODETYPE': 3,
             u'name': u'环境信号(1#温度_2F程控室南侧)',
             u'ALARMLOGTYPE': None, u'VIRTUALTYPE': 0, u'MINVAL': 0.0,
             u'PERCISION': 1, u'SCID': 8,
             u'organization': ObjectId('5a1a6065c1ebde099c1bcbcd'),
             u'LOLIMIT2': -99999.0,
             u'_id': ObjectId('5a425fee87ea64b6c051812d'),
             u'LOLIMIT4': -99999.0, u'operate': u'update_aic'},
            {u'SOID': 21758, u'NETTYPE': 0, u'CID': 16, 'SOFSUNODEID': 3692544,
             u'DESCRIBE': u'', u'NODEID': 3692548, u'HILIMIT4': -99999.0,
             u'HILIMIT2': -99999.0, u'HILIMIT3': -99999.0, u'HILIMIT1': 95.0,
             u'AID': 103, u'FSUID': 197, u'STORAGEMODE': u'', u'SUID': 2644,
             u'NODECODE': u'0218102001', u'ALARMTHRESBHOLD': u'',
             u'DEVICETYPEID': 18,
             u'parents': {u'town': u'衢州_衢州市',
                          u'city': u'衢州市',
                          u'station': u'衢_C_衢州航埠局',
                          u'device': u'机房环境(2F程控室)'},
             u'SYID': 213625, u'ALARMLEVEL': 3, u'category': u'point',
             u'NODENAME': u'环境信号(1#湿度_2F传输室南侧)',
             u'NODEDESC': u'湿度', u'FSUNODEID': 3692548,
             u'STANDER': 0.0, u'LOLIMIT1': 35.0, u'LOLIMIT3': -99999.0,
             u'SPID': 1254494, u'CONTROLENABLE': u'', u'STORAGETHRESHOLD': u'',
             u'UNIT': u'%RH', u'MAXVAL': 100.0,
             u'UPDATETIME': datetime.datetime(2019, 6, 3, 16, 55, 55),
             u'STORAGEINTERVAL': u'', u'NODETYPE': 3,
             u'name': u'环境信号(1#湿度_2F传输室南侧)',
             u'ALARMLOGTYPE': None, u'VIRTUALTYPE': 0, u'MINVAL': 0.0,
             u'PERCISION': 1, u'SCID': 8,
             u'organization': ObjectId('5a1a6065c1ebde099c1bcbcd'),
             u'LOLIMIT2': -99999.0,
             u'_id': ObjectId('5a425fee87ea64b6c0518133'),
             u'LOLIMIT4': -99999.0, u'operate': u'update_aic'}],
        'FSUID': 197,
        'fsu_info': {u'ENABLE': 1,
                     u'GETSTATETIME': datetime.datetime(2019, 1, 10, 7, 28, 8),
                     u'CHECKTIMETIME': datetime.datetime(2019, 6, 5, 19, 46,
                                                         51),
                     u'CHECKSTATUSTIME': datetime.datetime(2019, 1, 10, 7, 28,
                                                           8),
                     u'FTPPORT': u'21',
                     u'GETALARMTIME': datetime.datetime(2019, 1, 10, 7, 28, 8),
                     u'LASTLOGINTIME': datetime.datetime(2019, 6, 5, 19, 46,
                                                         51),
                     u'MODEL': u'虚拟现场采集器',
                     'FSUID': 'CTZJ0000197', u'SUID': 2644,
                     u'CONFIGUPDATETIME': None, u'ALARMSERIALNO': -246083,
                     u'FTPPASSWORD': u'8107', u'FSUIP': u'134.97.31.42',
                     'SERVERPORT': 3081,
                     u'SUPPLIER': u'浙江邮电工程建设有限公司',
                     u'USERNAME': u'JKQZ', u'ALARMSTATUS': 0, u'SERIALNO': u'',
                     'SERVERNAME': u'DCN B接口服务器',
                     u'BALARMSERIALNO': 4689387, u'SPID': 12341182,
                     u'SERVERID': 5, u'PASSWORD': u'JKQZ123456', u'ID': 197,
                     u'UPDATETIME': datetime.datetime(2019, 6, 5, 19, 46, 51),
                     u'NAME': u'衢_C_衢州航埠局虚拟现场采集器',
                     'PK_Type': 'GET_DATA',
                     u'GETDATATIME': datetime.datetime(2019, 1, 10, 7, 28, 8),
                     u'LASTCOMMUNICATETIME': datetime.datetime(2019, 1, 10, 7,
                                                               28, 8),
                     u'FSUPORT': u'42006',
                     u'MESSAGE': u'ORA-01653: unable to extend table PSCUSER.B_ALARM_LOG by 1024 in tablespace B_DATADATA',
                     u'_id': ObjectId('5c0e1458aca03d344accb111'),
                     u'FTPUSERNAME': u'8107',
                     u'UPDATESTATUSTIME': datetime.datetime(2019, 1, 10, 7, 28,
                                                            8)}
    }

}


def get_data_for_fsu_info_by_soid(soid):
    """
    根据soid获取fsu请求需要的参数
    :param soid:
    :return:
    """
    return data_dict[soid]
