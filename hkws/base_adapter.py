from ctypes import *
import os
import logging
from hkws.model import base,camera
import hkws.model.preview as preview


class BaseAdapter:
    so_list = []

    # 加载目录下所有so文件
    def add_lib(self, path, suffix):
        files = os.listdir(path)
        for file in files:
            if not os.path.isdir(path + file):
                if file.endswith(suffix):
                    self.so_list.append(path + file)
            else:
                self.add_lib(path + file + "/", suffix)

    # python 调用 sdk 指定方法
    def call_cpp(self, func_name, *args):
        for so_lib in self.so_list:
            try:
                lib = cdll.LoadLibrary(so_lib)
                try:
                    value = eval("lib.%s" % func_name)(*args)
                    logging.info("调用的库：" + so_lib)
                    logging.info("执行成功,返回值：" + str(value))
                    return value
                except:
                    continue
            except:
                continue
            # logging.info("库文件载入失败：" + so_lib )

        logging.error("没有找到接口！")
        return False

    # 初始化海康微视 sdk
    def init_sdk(self):
        init_res = self.call_cpp("NET_DVR_Init")  # SDK初始化
        if init_res:
            logging.info("SDK初始化成功")
            return True
        else:
            error_info = self.call_cpp("NET_DVR_GetLastError")
            logging.error("SDK初始化错误：" + str(error_info))
            return False

    # 释放sdk
    def sdk_clean(self):
        result = self.call_cpp("NET_DVR_Cleanup")
        logging.info("释放资源", result)

    def logout(self, userId=0):
        result = self.call_cpp("NET_DVR_Logout", userId)
        logging.info("登出", result)

    # 用户登录指定摄像机设备
    def login(self, address="192.168.1.1", port=8000, user="admin", pwd="admin"):
        # 设置连接时间
        set_overtime = self.call_cpp("NET_DVR_SetConnectTime", 5000, 4)  # 设置超时
        if not set_overtime:
            self.print_error("NET_DVR_SetConnectTime 设置超时错误信息失败：the error code is ")
            return False
        # 设置重连
        self.call_cpp("NET_DVR_SetReconnect", 10000, True)

        b_address = bytes(address, "ascii")
        b_user = bytes(user, "ascii")
        b_pwd = bytes(pwd, "ascii")

        struLoginInfo = base.NET_DVR_USER_LOGIN_INFO()
        struLoginInfo.bUseAsynLogin = 0  # 同步登陆
        i = 0
        for o in b_address:
            struLoginInfo.sDeviceAddress[i] = o
            i += 1

        struLoginInfo.wPort = port
        i = 0
        for o in b_user:
            struLoginInfo.sUserName[i] = o
            i += 1

        i = 0
        for o in b_pwd:
            struLoginInfo.sPassword[i] = o
            i += 1

        device_info = base.NET_DVR_DEVICEINFO_V40()
        loginInfo1 = byref(struLoginInfo)
        loginInfo2 = byref(device_info)
        user_id = self.call_cpp("NET_DVR_Login_V40", loginInfo1, loginInfo2)
        if user_id == -1:  # -1表示失败，其他值表示返回的用户ID值。
            self.print_error("NET_DVR_Login_V40 用户登录失败: the error code is ")
        return user_id

    def start_preview(self, cbFunc, userId=0):
        req = camera.NET_DVR_PREVIEWINFO()
        req.hPlayWnd = None
        req.lChannel = 1  # 预览通道号
        req.dwStreamType = 0  # 码流类型：0-主码流，1-子码流，2-三码流，3-虚拟码流，以此类推
        req.dwLinkMode = 0  # 连接方式：0-TCP方式，1-UDP方式，2-多播方式，3-RTP方式，4-RTP/RTSP，5-RTP/HTTP,6-HRUDP（可靠传输）
        req.bBlocked = 1  # 0-非阻塞 1-阻塞
        struPlayInfo = byref(req)
        # 这个回调函数不适合长时间占用
        # fRealDataCallBack_V30 = preview.REALDATACALLBACK

        lRealPlayHandle = self.call_cpp("NET_DVR_RealPlay_V40", userId, struPlayInfo, cbFunc, None)

        if lRealPlayHandle < 0:
            self.print_error("NET_DVR_RealPlay_V40 启动预览失败: the error code is")
            self.logout(userId)
            self.sdk_clean()
        return lRealPlayHandle

    def set_sdk_config(self, enumType, sdkPath):
        req = preview.NET_DVR_LOCAL_SDK_PATH()
        sPath = bytes(sdkPath, "ascii")
        i = 0
        for o in sPath:
            req.sPath[i] = o
            i += 1

        ndlsp_ptr = byref(req)
        res = self.call_cpp("NET_DVR_SetSDKInitCfg", enumType, ndlsp_ptr)
        logging.warning("call NET_DVR_SetSDKInitCfg result：" + str(res))
        return res

    # msg 描述前缀
    def print_error(self, msg=""):
        error_info = self.call_cpp("NET_DVR_GetLastError")
        logging.error(msg + str(error_info))

    def stop_preview(self, lRealPlayHandle):
        self.call_cpp("NET_DVR_StopRealPlay", lRealPlayHandle)

    # def callback_real_data(self, lRealPlayHandle: c_long, cbFunc: g_real_data_call_back, dwUser: c_ulong):
    #     return self.call_cpp("NET_DVR_SetRealDataCallBack", lRealPlayHandle, cbFunc, dwUser)
    def callback_real_data(self, lRealPlayHandle, cbFunc, dwUser):
        result = self.call_cpp("NET_DVR_SetRealDataCallBack", lRealPlayHandle, cbFunc, dwUser)
        if result is False:
            self.print_error("NET_DVR_SetStandardDataCallBack 注册捕获实时流码回调函数失败: the error code is ")

    def close_alarm(self, alarm_result):
        return self.call_cpp("NET_DVR_CloseAlarmChan_V30", alarm_result)


