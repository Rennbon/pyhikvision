from hkws.model.model import *


#real_data_callback = CFUNCTYPE(None, h_LONG, h_DWORD, POINTER(h_BYTE), h_DWORD, h_DWORD)
@CFUNCTYPE(None, c_long, c_uint, c_byte, c_uint, c_uint)
def g_real_data_call_back(lRealPlayHandle: c_long,
                          dwDataType: c_uint,
                          pBuffer: c_byte,
                          dwBufSize: c_uint,
                          dwUser: c_uint):
    print(' aaaaaaaaaaa callback pBufSize is ', pBuffer, lRealPlayHandle, dwBufSize)


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
