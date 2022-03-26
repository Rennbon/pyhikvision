# 硬件产品预警布放相关
from hkws.core.type_map import *


# 报警设备信息结构体
class NET_DVR_ALARMER(Structure):
    _fields_ = [
        ("byUserIDValid", h_BYTE),
        ("bySerialValid", h_BYTE),
        ("byVersionValid", h_BYTE),
        ("byDeviceNameValid", h_BYTE),
        ("byMacAddrValid", h_BYTE),
        ("byLinkPortValid", h_BYTE),
        ("byDeviceIPValid", h_BYTE),
        ("bySocketIPValid", h_BYTE),
        ("lUserID", h_LONG),
        ("sSerialNumber", h_BYTE * 48),
        ("dwDeviceVersion", h_DWORD),
        ("sDeviceName", h_CHAR * 32),
        ("byMacAddr", h_CHAR * 6),
        ("wLinkPort", h_WORD),
        ("sDeviceIP", h_CHAR * 128),
        ("sSocketIP", h_CHAR * 128),
        ("byIpProtocol", h_BYTE),
        ("byRes2", h_BYTE * 11),
    ]


# 布防
class NET_DVR_SETUPALARM_PARAM(Structure):
    _fields_ = [
        ("dwSize", h_DWORD),
        ("beLevel", h_BYTE),
        ("byAlarmInfoType", h_BYTE),
        ("byRetAlarmTypeV40", h_BYTE),
        ("byRetDevInfoVersion", h_BYTE),
        ("byRetVQDAlarmType", h_BYTE),
        ("byFaceAlarmDetection", h_BYTE),
        ("bySupport", h_BYTE),
        ("byBrokenNetHttp", h_BYTE),
        ("wTaskNo", h_WORD),
        ("byDeployType", h_BYTE),
        ("byRes1", h_BYTE * 3),
        ("byAlarmTypeURL", h_BYTE),
        ("byCustomCtrl", h_BYTE),
    ]
