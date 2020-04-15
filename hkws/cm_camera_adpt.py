from hkws.model import camera, callbacks
from hkws.base_adapter import BaseAdapter
from hkws.core.type_map import *


# 摄像器适配器
class CameraAdapter(BaseAdapter):
    # 启动预览
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
            self.print_error("NET_DVR_RealPlay_V40 启动预览失败: the error code is ")
            self.logout(userId)
            self.sdk_clean()
        return lRealPlayHandle

    # 停止预览
    def stop_preview(self, lRealPlayHandle):
        self.call_cpp("NET_DVR_StopRealPlay", lRealPlayHandle)

    # def callback_real_data(self, lRealPlayHandle: c_long, cbFunc: g_real_data_call_back, dwUser: c_ulong):
    #     return self.call_cpp("NET_DVR_SetRealDataCallBack", lRealPlayHandle, cbFunc, dwUser)
    # 根据lRealPlayHandle订阅视频流
    def callback_real_data(self, lRealPlayHandle, cbFunc, dwUser):
        result = self.call_cpp("NET_DVR_SetRealDataCallBack", lRealPlayHandle, cbFunc, dwUser)
        if not result:
            self.print_error("NET_DVR_SetRealDataCallBack 注册回调函数，捕获实时码流数据失败: the error code is ")
        return result

    def callback_standard_data(self, lRealPlayHandle, cbFunc, dwUser):
        result = self.call_cpp("NET_DVR_SetStandardDataCallBack", lRealPlayHandle, cbFunc, dwUser)
        if not result:
            self.print_error("NET_DVR_SetStandardDataCallBack 注册回调函数，捕获实时码流数据(标准流码)失败: the error code is ")
        return result

    # 设置设备的配置信息
    def set_dvr_config(self, user_id=0):
        stru_pic_param = camera.NET_DVR_JPEGPARA()
        stru_pic_param.wPicSize = 5
        stru_pic_param.wPicQuality = 1

        struc_rect = camera.NET_VCA_RECT()
        struc_rect.fX = 0
        struc_rect.fY = 0
        struc_rect.fWidth = 0
        struc_rect.fHeight = 0

        size_filter = camera.NET_VCA_SIZE_FILTER()
        size_filter.byActive = 0
        size_filter.byMode = 0
        size_filter.struMiniRect = struc_rect
        size_filter.struMaxRect = struc_rect

        point_1 = camera.NET_VCA_POINT()
        point_1.fX = 0.01
        point_1.fY = 0.005

        point_2 = camera.NET_VCA_POINT()
        point_2.fX = 0.01
        point_2.fY = 0.995

        point_3 = camera.NET_VCA_POINT()
        point_3.fX = 0.99
        point_3.fY = 0.995

        point_4 = camera.NET_VCA_POINT()
        point_4.fX = 0.99
        point_4.fY = 0.005

        polygon = camera.NET_VCA_POLYGON()
        polygon.dwPointNum = 4
        polygon.struPos[0] = point_1
        polygon.struPos[1] = point_2
        polygon.struPos[2] = point_3
        polygon.struPos[3] = point_4

        single_face = camera.NET_VCA_SINGLE_FACESNAPCFG()
        single_face.byActive = 0
        single_face.byAutoROIEnable = 0
        single_face.struSizeFilter = size_filter
        single_face.struVcaPolygon = polygon

        lpInBuffer = camera.NET_VCA_FACESNAPCFG()
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
            self.print_error("NET_DVR_SetDVRConfig 启动预览失败: the error code is ")
        return set_dvr_result
