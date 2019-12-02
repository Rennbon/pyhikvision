from ctypes import *
import os
import logging
import hkws.model.login as login


class HKAdapter:
    so_list = []

    # 加载目录下所有so文件
    def add_so(self, path):
        files = os.listdir(path)
        for file in files:
            if not os.path.isdir(path + file):
                if file.endswith(".so"):
                    self.so_list.append(path + file)
            else:
                self.add_so(path + file + "/")

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

    # 用户登录指定摄像机设备
    def login(self, address="192.168.1.1", port=8000, user="admin", pwd="admin"):
        # 设置连接时间
        set_overtime = self.call_cpp("NET_DVR_SetConnectTime", 5000, 4)  # 设置超时
        if set_overtime:
            logging.info(address + ", 设置超时时间成功")
        else:
            error_info = self.call_cpp("NET_DVR_GetLastError")
            logging.error(address + ", 设置超时错误信息：" + str(error_info))
            return False
        # 设置重连
        self.call_cpp("NET_DVR_SetReconnect", 10000, True)

        b_address = bytes(address, "ascii")
        b_user = bytes(user, "ascii")
        b_pwd = bytes(pwd, "ascii")

        struLoginInfo = login.NET_DVR_USER_LOGIN_INFO()
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

        device_info = login.NET_DVR_DEVICEINFO_V40()
        loginInfo1 = byref(struLoginInfo)
        loginInfo2 = byref(device_info)
        user_id = self.call_cpp("NET_DVR_Login_V40", loginInfo1, loginInfo2)
        logging.info(address + ", 登录结果：" + str(user_id))
        if user_id == -1:  # -1表示失败，其他值表示返回的用户ID值。
            error_info = self.call_cpp("NET_DVR_GetLastError")
            logging.error(address + ", 登录错误信息：" + str(error_info))

        return user_id
