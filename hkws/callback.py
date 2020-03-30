from ctypes import *
from hkws.model import alarm, camera


# 视频流回调函数
@CFUNCTYPE(None, c_long, c_ulong, POINTER(c_byte), c_ulong, c_ulong)
def g_real_data_call_back(lRealPlayHandle: c_long,
                          dwDataType: c_ulong,
                          pBuffer: POINTER(c_byte),
                          dwBufSize: c_ulong,
                          dwUser: c_ulong):
    print(' aaaaaaaaaaa callback pBufSize is ', lRealPlayHandle, pBuffer, dwBufSize)


alarm_stracture = CFUNCTYPE(
    c_bool,
    c_long,
    alarm.NET_DVR_ALARMER,
    camera.NET_VCA_FACESNAP_RESULT,
    c_ulong,
    c_void_p,
)


@CFUNCTYPE(c_bool, c_long, alarm.NET_DVR_ALARMER, c_char, c_ulong, c_void_p)
def face_alarm_call_back(lCommand: 0x1112,
                         pAlarmer: alarm.NET_DVR_ALARMER,
                         pAlarmInfo: camera.NET_VCA_FACESNAP_RESULT,
                         dwBufLen: c_ulong,
                         pUser: c_void_p):
    print("lCommand ", lCommand)
    print("检测到人脸")
    return True
