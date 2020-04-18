from hkws.core.type_map import *
from hkws.model import alarm

msg_callback_v31 = CFUNCTYPE(h_BOOL, h_LONG, POINTER(alarm.NET_DVR_ALARMER), POINTER(h_CHAR), h_DWORD, h_VOID_P)

# 码流数据回调函数
real_data_callback = CFUNCTYPE(None, h_LONG, h_DWORD, POINTER(h_BYTE), h_DWORD, h_DWORD)

