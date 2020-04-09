from ctypes import *
import os
import logging
from hkws.config import Config
from hkws.model import base, alarm, callbacks


# 海康威视基础类，AI摄像机，通用摄像机，门禁产品，出入口产品通用
class BaseAdapter:
    # 动态sdk文件 .so .dll
    so_list = []

    # 常规启动，初始化SDK到用户注册设备
    def common_start(self, cnf: Config):
        userId = -1
        self.add_lib(cnf.SDKPath, cnf.Suffix)
        if len(self.so_list) == 0:
            return userId
        if not self.init_sdk():
            return userId
        userId = self.login(cnf.IP, cnf.Port, cnf.User, cnf.Password)
        if userId < 0:
            self.print_error("common_start 失败: the error code is")
        return userId

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
            self.print_error("NET_DVR_GetLastError 初始化SDK失败: the error code is")
            return False

    # 设置sdk初始化参数
    def set_sdk_config(self, enumType, sdkPath):
        req = base.NET_DVR_LOCAL_SDK_PATH()
        sPath = bytes(sdkPath, "ascii")
        i = 0
        for o in sPath:
            req.sPath[i] = o
            i += 1

        ptr = byref(req)
        res = self.call_cpp("NET_DVR_SetSDKInitCfg", enumType, ptr)
        if res < 0:
            self.print_error("NET_DVR_SetSDKInitCfg 启动预览失败: the error code is")
        return res

    # 释放sdk
    def sdk_clean(self):
        result = self.call_cpp("NET_DVR_Cleanup")
        logging.info("释放资源", result)

    # 设备登录
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

        # 设备登出

    def logout(self, userId=0):
        result = self.call_cpp("NET_DVR_Logout", userId)
        logging.info("登出", result)

    # 设置报警回调函数
    def setup_alarm_chan_v31(self, cbFunc, user_id):
        result = self.call_cpp("NET_DVR_SetDVRMessageCallBack_V31", cbFunc, user_id)
        if result == -1:
            self.print_error("NET_DVR_SetDVRMessageCallBack_V31 初始化SDK失败: the error code is")
        return result

    # 设置报警布防
    def setup_alarm_chan_v41(self, user_id=0):
        structure_l = alarm.NET_DVR_SETUPALARM_PARAM()
        structure_l.dwSize = sizeof(structure_l)
        structure_l.byFaceAlarmDetection = 0
        structure_l_ref = byref(structure_l)
        result = self.call_cpp("NET_DVR_SetupAlarmChan_V41", user_id, structure_l_ref)
        if result == -1:
            self.print_error("NET_DVR_SetupAlarmChan_V41 报警布防: the error code is")
        return result

    # 报警撤防
    def close_alarm(self, alarm_result):
        return self.call_cpp("NET_DVR_CloseAlarmChan_V30", alarm_result)

    # msg 描述前缀
    def print_error(self, msg=""):
        error_info = self.call_cpp("NET_DVR_GetLastError")
        logging.error(msg + str(error_info))
