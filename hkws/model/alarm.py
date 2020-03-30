# 硬件产品预警布放相关
from ctypes import *


# 报警设备信息结构体
class NET_DVR_ALARMER(Structure):
    _fields_ = [
        ("byUserIDValid", c_byte),
        ("bySerialValid", c_byte),
        ("byVersionValid", c_byte),
        ("byDeviceNameValid", c_byte),
        ("byMacAddrValid", c_byte),
        ("byLinkPortValid", c_byte),
        ("byDeviceIPValid", c_byte),
        ("bySocketIPValid", c_byte),
        ("lUserID", c_long),
        ("sSerialNumber", c_byte * 48),
        ("dwDeviceVersion", c_uint32),
        ("sDeviceName", c_char * 32),
        ("byMacAddr", c_char * 6),
        ("wLinkPort", c_uint16),
        ("sDeviceIP", c_char * 128),
        ("sSocketIP", c_char * 128),
        ("byIpProtocol", c_byte),
        ("byRes2", c_byte * 11)
    ]


# 布防
class NET_DVR_SETUPALARM_PARAM(Structure):
    _fields_ = [
        ("dwSize", c_uint32),
        ("beLevel", c_byte),
        ("byAlarmInfoType", c_byte),
        ("byRetAlarmTypeV40", c_byte),
        ("byRetDevInfoVersion", c_byte),
        ("byRetVQDAlarmType", c_byte),
        ("byFaceAlarmDetection", c_byte),
        ("bySupport", c_byte),
        ("byBrokenNetHttp", c_byte),
        ("wTaskNo", c_uint16),
        ("byDeployType", c_byte),
        ("byRes1", c_byte * 3),
        ("byAlarmTypeURL", c_byte),
        ("byCustomCtrl", c_byte)
    ]














