from ctypes import *
from hkws.model.model import *

# import cv2

hikFunc = CFUNCTYPE(
    None,
    c_long,  # lRealHandle 当前的预览句柄，NET_DVR_RealPlay_V40的返回值
    c_ulong,  # dwDataType  数据类型 1-系统头数据， 2-流数据（包括符合流或者音视频分开的流数据），3-音频数据，112-私有数据，包括智能信息
    c_byte,  # *pBuffer 存放数据的缓冲区指针
    c_ulong,  # dwBufSize 缓冲区大小
    c_ulong,  # *pUser 用户数据
)


@CFUNCTYPE(None, c_long, c_uint, c_byte, c_uint, c_uint)
def g_real_data_call_back(lRealPlayHandle: c_long,
                          dwDataType: c_uint,
                          pBuffer: c_byte,
                          dwBufSize: c_uint,
                          dwUser: c_uint):
    print(' aaaaaaaaaaa callback pBufSize is ', pBuffer, lRealPlayHandle, dwBufSize)


alarm_stracture = CFUNCTYPE(
    c_bool,
    c_long,
    NET_DVR_ALARMER,
    c_char_p,
    c_uint32,
    c_void_p,
)


@CFUNCTYPE(c_bool, c_long, NET_DVR_ALARMER, c_char_p, c_uint, c_uint)
def face_alarm_call_back(lCommand: c_long,
                         pAlarmer: NET_DVR_ALARMER,
                         pAlarmInfo: c_char_p,
                         dwBufLen: c_uint,
                         pUser: c_uint):
    if lCommand is 0x1112:
        print("lCommand ", lCommand)
        print("检测到人脸")
    else:
        print("没有")

    return True
