from hkws.core.type_map import *
from hkws.model import callbacks


# 视频流回调函数
@callbacks.real_data_callback
def f_real_data_call_back(lRealHandle,
                          dwDataType,
                          pBuffer,
                          dwBufSize,
                          dwUser):
    print('callback pBufSize is ', lRealHandle, pBuffer, dwBufSize)
    return


@CFUNCTYPE(None, c_long, c_uint, c_byte, c_uint, c_uint)
def g_real_data_call_back2(lRealPlayHandle: c_long,
                          dwDataType: c_uint,
                          pBuffer: c_byte,
                          dwBufSize: c_uint,
                          dwUser: c_uint):
    print(' aaaaaaaaaaa callback pBufSize is ', lRealPlayHandle, dwBufSize)
    # if dwBufSize > 0:
    #     f = open(filePath, 'wb')
    #     f.write(pBuffer)