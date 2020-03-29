from ctypes import *
import os
import logging
import hkws.model.login as login
import hkws.model.preview as preview
import hkws.model.model as model_1

from hkws.callback import hikFunc, alarm_stracture

from hkws.callback import g_real_data_call_back, face_alarm_call_back


class HKAdapter:
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
        if user_id == -1:  # -1表示失败，其他值表示返回的用户ID值。
            self.print_error("NET_DVR_Login_V40 用户登录失败: the error code is ")
        return user_id

    def start_preview(self, cbFunc: hikFunc, userId=0):
        req = preview.NET_DVR_PREVIEWINFO()
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
    def callback_real_data(self, lRealPlayHandle: c_long, cbFunc: g_real_data_call_back, dwUser: c_uint):
        result = self.call_cpp("NET_DVR_SetStandardDataCallBack", lRealPlayHandle, cbFunc, dwUser)
        if result is False:
            self.print_error("NET_DVR_SetStandardDataCallBack 注册捕获实时流码回调函数失败: the error code is ")

    def setup_alarm_chan_v31(self, cbFunc: face_alarm_call_back):
        result = self.call_cpp("NET_DVR_SetDVRMessageCallBack_V31", cbFunc, None)
        if result == -1:
            self.print_error("NET_DVR_SetDVRMessageCallBack_V31 设置报警回调函数失败: the error code is ")
        return result

    def setup_alarm_chan_v41(self, user_id=0):
        structure_l = model_1.NET_DVR_SETUPALARM_PARAM()
        structure_l.byFaceAlarmDetection = 0
        structure_l_ref = byref(structure_l)
        result = self.call_cpp("NET_DVR_SetupAlarmChan_V41", user_id, structure_l_ref)
        if result == -1:
            self.print_error("NET_DVR_SetupAlarmChan_V41 报警布放失败: the error code is ")
        return result

    def close_alarm(self, alarm_result):
        return self.call_cpp("NET_DVR_CloseAlarmChan_V30", alarm_result)

    # 设置设备的配置信息
    def set_dvr_config(self, user_id=0):
        stru_pic_param = model_1.NET_DVR_JPEGPARA()
        stru_pic_param.wPicSize = 5
        stru_pic_param.wPicQuality = 1

        struc_rect = model_1.NET_VCA_RECT()
        struc_rect.fX = 0
        struc_rect.fY = 0
        struc_rect.fWidth = 0
        struc_rect.fHeight = 0

        size_filter = model_1.NET_VCA_SIZE_FILTER()
        size_filter.byActive = 0
        size_filter.byMode = 0
        size_filter.struMiniRect = struc_rect
        size_filter.struMaxRect = struc_rect

        point_1 = model_1.NET_VCA_POINT()
        point_1.fX = 0.01
        point_1.fY = 0.005

        point_2 = model_1.NET_VCA_POINT()
        point_2.fX = 0.01
        point_2.fY = 0.995

        point_3 = model_1.NET_VCA_POINT()
        point_3.fX = 0.99
        point_3.fY = 0.995

        point_4 = model_1.NET_VCA_POINT()
        point_4.fX = 0.99
        point_4.fY = 0.005

        polygon = model_1.NET_VCA_POLYGON()
        polygon.dwPointNum = 4
        polygon.struPos[0] = point_1
        polygon.struPos[1] = point_2
        polygon.struPos[2] = point_3
        polygon.struPos[3] = point_4

        single_face = model_1.NET_VCA_SINGLE_FACESNAPCFG()
        single_face.byActive = 0
        single_face.byAutoROIEnable = 0
        single_face.struSizeFilter = size_filter
        single_face.struVcaPolygon = polygon

        lpInBuffer = model_1.NET_VCA_FACESNAPCFG()
        size = sizeof(lpInBuffer)
        lpInBuffer.dwSize = size
        lpInBuffer.bySnapTime = 1
        lpInBuffer.bySnapInterval = 5
        lpInBuffer.bySnapThreshold = 70
        lpInBuffer.byGenerateRate = 5
        lpInBuffer.bySensitive = 4
        lpInBuffer.byReferenceBright = 40
        lpInBuffer.byMatchType = 1
        lpInBuffer.byMatchThreshold = 50

        lpInBuffer.struPictureParam = stru_pic_param
        lpInBuffer.struRule[0] = single_face

        lpInBuffer.wFaceExposureMinDuration = 1
        lpInBuffer.byFaceExposureMode = 0
        lpInBuffer.byBackgroundPic = 0
        lpInBuffer.dwValidFaceTime = 1
        lpInBuffer.dwUploadInterval = 800
        lpInBuffer.dwFaceFilteringTime = 5
        lpInBuffer_ref = byref(lpInBuffer)
        print(lpInBuffer)
        print("size", size)
        print(lpInBuffer_ref)

        set_dvr_result = self.call_cpp("NET_DVR_SetDVRConfig", user_id, 5002, 1, lpInBuffer_ref, size)
        if not set_dvr_result:
            error_info = self.call_cpp("NET_DVR_GetLastError")
            logging.error("设置设备的配置信息错误为：" + str(error_info))

        return set_dvr_result
