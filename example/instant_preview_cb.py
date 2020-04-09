from hkws.core.type_map import *


# 视频流回调函数
@CFUNCTYPE(None, h_LONG, h_DWORD, POINTER(h_BYTE), h_DWORD, h_VOID_P)
def g_real_data_call_back(lRealPlayHandle: h_LONG,
                          dwDataType: h_DWORD,
                          pBuffer: POINTER(h_BYTE),
                          dwBufSize: h_DWORD,
                          dwUser: h_VOID_P):
    print(' aaaaaaaaaaa callback pBufSize is ', lRealPlayHandle, pBuffer, dwBufSize)
