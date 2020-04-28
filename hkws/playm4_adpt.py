import logging

from hkws.base_adapter import BaseAdapter
from ctypes import *


class PlayM4(BaseAdapter):
    Source_Buf_Min = 1024 * 50
    Source_Buf_Max = 1024 * 100000
    __port = 0
    __ready = False

    def ready(self):
        if not self.__ready:
            logging.error("port 没准备好，不可执行该操作")
        return self.__ready

    # 获取未使用的通道号
    def get_port(self):
        p = byref(self.__port)
        res = self.call_cpp("PlayM4_GetPort", p)
        if res == 0:
            self.print_error("PlayM4_SetStreamOpenMode 设置流播放模式失败: the error code is ")
        else:
            self.__port = p
            self.__ready = True
        return res

    # 设置流播放模式
    # nport: 播放通道号
    # nmode: 流播放模式  0:会尽量保证实时性，防止数据阻塞;而且数据检查严格   1:按时间戳播放
    def set_stream_open_mode(self, nmode):
        if not self.ready():
            return -1
        res = self.call_cpp("PlayM4_SetStreamOpenMode", self.__port, nmode)
        if res == 0:
            self.print_error("PlayM4_SetStreamOpenMode 设置流播放模式失败: the error code is ")
        return res

    # 打开流
    # nport: 播放通道号
    # pFileHeadBuf： 文件头数据
    # nSize：文件头长度
    # nBufPoolSize： 设置播放器中存放数据流的缓冲区大小  范围为SOURCE_BUF_MIN ~ SOURCE_BUF_MAX
    def open_stream(self, nport, pFileHeadBuf, nSize, nBufPoolSize):
        if not self.ready():
            return -1
        res = self.call_cpp("PlayM4_OpenStream", nport, pFileHeadBuf, nSize, nBufPoolSize)
        if res == 0:
            self.print_error("PlayM4_SetStreamOpenMode 设置流播放模式失败: the error code is ")
        return res
