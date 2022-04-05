import logging
from ctypes import *

from hkws.base_adapter import BaseAdapter
from hkws.core.type_map import h_HWND, h_LONG, h_DWORD


class PlayM4(BaseAdapter):
    Source_Buf_Min = 1024 * 50
    Source_Buf_Max = 1024 * 100000
    __port = h_LONG(0)
    __hwnd = h_HWND(0)
    __ready = False

    def set_hwnd(self, hwnd):
        self.__hwnd = hwnd

    def ready(self):
        if not self.__ready:
            logging.error("port 没准备好，不可执行该操作")
        return self.__ready

    # 获取未使用的通道号
    def get_port(self):
        port = byref(self.__port)
        res = self.call_cpp("PlayM4_GetPort", port)
        if res == 0:
            self.print_error("PlayM4_SetStreamOpenMode 设置流播放模式失败: the error code is ")
        else:
            self.__ready = True
        return res

    # 设置流播放模式
    # nmode: 流播放模式  0:会尽量保证实时性，防止数据阻塞;而且数据检查严格   1:按时间戳播放
    def set_stream_open_mode(self, nmode: h_DWORD):
        if not self.ready():
            return -1
        res = self.call_cpp("PlayM4_SetStreamOpenMode", self.__port, nmode)
        if res == 0:
            self.print_error("PlayM4_SetStreamOpenMode 设置流播放模式失败: the error code is ")
        return res

    # 打开流
    # pFileHeadBuf： 文件头数据
    # nSize：文件头长度
    # nBufPoolSize： 设置播放器中存放数据流的缓冲区大小  范围为SOURCE_BUF_MIN ~ SOURCE_BUF_MAX
    def open_stream(self, pFileHeadBuf, nSize, nBufPoolSize):
        if not self.ready():
            return -1
        res = self.call_cpp(
            "PlayM4_OpenStream", self.__port, pFileHeadBuf, nSize, nBufPoolSize
        )
        if res == 0:
            self.print_error("PlayM4_OpenStream 设置流播放模式失败: the error code is ")
        return res

    # 开启播放
    # hwnd 播放视频的窗口句柄
    def playM4_play(self):
        if not self.ready():
            return -1
        res = self.call_cpp("PlayM4_Play", self.__port, self.__hwnd)
        if res == 0:
            self.print_error("PlayM4_Play 开启播放失败: the error code is ")
        return res

    # 输入流数据
    # pBuf: 流数据缓冲区地址
    # nSize: 流数据缓冲区大小
    def playM4_inputData(self, pBuf, nSize):
        if not self.ready():
            return -1
        res = self.call_cpp("PlayM4_InputData", self.__port, pBuf, nSize)
        if res == 0:
            self.print_error("PlayM4_InputData 输入流数据失败: the error code is ")
        return res

    def playM4_setHLogFlag(self, switch):
        if not self.ready():
            return -1
        res = self.call_cpp("PlayM4_SetHLogFlag", self.__port, switch, None)
        if res == 0:
            self.print_error("PlayM4_SetHLogFlag 输入流数据失败: the error code is ")
        return res
