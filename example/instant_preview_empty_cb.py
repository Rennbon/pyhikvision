from hkws.core.type_map import *
from hkws.model import callbacks

NET_DVR_SYSHEAD = 1
NET_DVR_STREAMDATA = 2
NET_DVR_AUDIOSTRAMDATA = 3
NET_DVR_PRIVATE_DATA = 112


# 视频流回调函数
# CFUNCTYPE(None, h_LONG, h_DWORD, POINTER(h_BYTE), h_DWORD, h_DWORD)
# dwDataType：数据类型   1：系统头数据 2：流数据 3：音频数据 112：私有数据，包括智能信息
# pBuffer：存放数据的缓冲区指针
# dwBufSize：缓冲区大小
# dwUser： 用户数据
@callbacks.real_data_callback
def f_real_data_call_back(lRealHandle,
                          dwDataType,
                          pBuffer,
                          dwBufSize,
                          dwUser):
    print("dwDataType:{},pBuffer:{},dwBufSize:{}".format(dwDataType, pBuffer, dwBufSize))
    if dwDataType is NET_DVR_SYSHEAD:  # 系统头数据
        print("头数据")
    elif dwDataType is NET_DVR_STREAMDATA:  # 流数据
        print("流数据")
    elif dwDataType is NET_DVR_AUDIOSTRAMDATA:  # 音频数据
        print("音频数据")
    elif dwDataType is NET_DVR_PRIVATE_DATA:  # 私有数据
        print("私有数据")

    if dwBufSize > 0:
        # 从指针中取数据
        res = bytearray(dwBufSize)
        rptr = (c_byte * dwBufSize).from_buffer(res)
        if not memmove(rptr, pBuffer, dwBufSize):
            raise RuntimeError("memmove failed")
        print(res.hex())
    return
