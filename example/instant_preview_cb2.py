from hkws import playm4_adpt
from hkws.core.type_map import h_DWORD, h_HWND
from hkws.model import callbacks

NET_DVR_SYSHEAD = 1  # 系统头数据
NET_DVR_STREAMDATA = 2  # 流数据
NET_DVR_AUDIOSTRAMDATA = 3  # 音频数据
NET_DVR_PRIVATE_DATA = 112  # 私有数据，包括智能信息

playm4_instance = playm4_adpt.PlayM4()


def set_playM4_adpt(so_list: [], hwnd: h_HWND):
    playm4_instance.set_lib(so_list)
    playm4_instance.set_hwnd(hwnd)

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
    if dwDataType is NET_DVR_SYSHEAD:  # 系统头数据
        if playm4_instance.get_port() != 1:
            return
        print("get_port success")
        if dwBufSize == 0:
            return
        if playm4_instance.set_stream_open_mode(h_DWORD(0)) != 1:
            return
        print("set_stream_open_mode success")
        if playm4_instance.open_stream(pBuffer, dwBufSize, h_DWORD(1024 * 1024)) != 1:
            return
        print("open_stream success")


        if playm4_instance.playM4_play() != 1:
            return
        print("playM4_play success")
    elif dwDataType is NET_DVR_STREAMDATA:  # 流数据
        if dwBufSize > 0 and playm4_instance.ready():
            playm4_instance.playM4_inputData(pBuffer, dwBufSize)
    elif dwDataType is NET_DVR_AUDIOSTRAMDATA:  # 音频数据
        print("音频数据")
    elif dwDataType is NET_DVR_PRIVATE_DATA:  # 私有数据
        print("私有数据")

    return
