# 硬件产品人像相关
from hkws.core.type_map import *


# 人体属性参数结构体。
class NET_VCA_HUMAN_FEATURE(Structure):
    _fields_ = [
        ("byAgeGroup", h_BYTE),
        ("bySex", h_BYTE),
        ("byEyeGlass", h_BYTE),
        ("byAge", h_BYTE),
        ("byAgeDeviation", h_BYTE),
        ("byEthnic", h_BYTE),
        ("byMask", h_BYTE),
        ("bySmile", h_BYTE),
        ("byFaceExpression", h_BYTE),
        ("byBeard", h_BYTE),
        ("byRace", h_BYTE),
        ("byHat", h_BYTE),
        ("byRes", h_BYTE * 4)
    ]


# 点坐标参数结构体
class NET_VCA_POINT(Structure):
    _fields_ = [
        ("fX", h_FLOAT),
        ("fY", h_FLOAT)
    ]


# 多边形结构体
class NET_VCA_POLYGON(Structure):
    _fields_ = [
        ("dwPointNum", h_DWORD),
        ("struPos", NET_VCA_POINT * 4)
    ]


# 区域框参数结构体。
class NET_VCA_RECT(Structure):
    _fields_ = [
        ("fX", h_FLOAT),
        ("fY", h_FLOAT),
        ("fWidth", h_FLOAT),
        ("fHeight", h_FLOAT)
    ]


# 尺寸过滤器参数结构体
class NET_VCA_SIZE_FILTER(Structure):
    _fields_ = [
        ("byActive", h_BYTE),
        ("byMode", h_BYTE),
        ("byRes", h_BYTE * 2),
        ("struMiniRect", NET_VCA_RECT),
        ("struMaxRect", NET_VCA_RECT)
    ]


# JPEG图像信息结构体。
class NET_DVR_JPEGPARA(Structure):
    _fields_ = [
        ("wPicSize", h_WORD),
        ("wPicQuality", h_WORD),
    ]


# 人脸抓拍规则参数（单条）结构体
class NET_VCA_SINGLE_FACESNAPCFG(Structure):
    _fields_ = [
        ("byActive", h_BYTE),
        ("byAutoROIEnable", h_BYTE),
        ("byRes", h_BYTE * 2),
        ("struSizeFilter", NET_VCA_SIZE_FILTER),
        ("struVcaPolygon", NET_VCA_POLYGON),
    ]


# 人脸抓拍规则参数结构体
class NET_VCA_FACESNAPCFG(Structure):
    _fields_ = [
        ("dwSize", h_DWORD),
        ("bySnapTime", h_BYTE),
        ("bySnapInterval", h_BYTE),
        ("bySnapThreshold", h_BYTE),
        ("byGenerateRate", h_BYTE),
        ("bySensitive", h_BYTE),
        ("byReferenceBright", h_BYTE),
        ("byMatchType", h_BYTE),
        ("byMatchThreshold", h_BYTE),
        ("struPictureParam", NET_DVR_JPEGPARA),
        ("struRule", NET_VCA_SINGLE_FACESNAPCFG * 1),
        ("wFaceExposureMinDuration", h_WORD),
        ("byFaceExposureMode", h_BYTE),
        ("byBackgroundPic", h_BYTE),
        ("dwValidFaceTime", h_DWORD),
        ("dwUploadInterval", h_DWORD),
        ("dwFaceFilteringTime", h_DWORD),
        ("byRes2", h_BYTE * 84)
    ]


# 报警目标信息结构体。
class NET_VCA_TARGET_INFO(Structure):
    _fields_ = [
        ("dwID", h_DWORD),
        ("struRect", NET_VCA_RECT),
        ("byRes", h_BYTE * 4)
    ]


# IP地址结构体。
class NET_DVR_IPADDR(Structure):
    _fields_ = [
        ("sIpV4", h_CHAR * 16),
        ("sIpV6", h_BYTE * 128)
    ]


# 前端设备信息结构体。
class NET_VCA_DEV_INFO(Structure):
    _fields_ = [
        ("struDevIP", NET_DVR_IPADDR),
        ("wPort", h_WORD),
        ("byChannel", h_BYTE),
        ("byIvmsChannel", h_BYTE)
    ]


# 时间参数结构体
class NET_DVR_TIME_EX(Structure):
    _fields_ = [
        ("wYear", h_WORD),
        ("byMonth", h_BYTE),
        ("byDay", h_BYTE),
        ("byHour", h_BYTE),
        ("byMinute", h_BYTE),
        ("bySecond", h_BYTE),
        ("byRes", h_BYTE),
    ]


# 人脸抓拍附加信息结构体
class NET_VCA_FACESNAP_ADDINFO(Structure):
    _fields_ = [
        ("struFacePicRect", NET_VCA_RECT),
        ("iSwingAngle", h_INT),
        ("iTiltAngle", h_INT),
        ("dwPupilDistance", h_DWORD),
        ("byBlockingState", h_BYTE),

        ("byFaceSnapThermometryEnabled", h_BYTE),
        ("byIsAbnomalTemperature", h_BYTE),
        ("byThermometryUnit", h_BYTE),
        ("struEnterTime", NET_DVR_TIME_EX),
        ("struExitTime", NET_DVR_TIME_EX),

        ("fFaceTemperature", h_FLOAT),
        ("fAlarmTemperature", h_FLOAT),
        ("byRes", h_BYTE * 472),
    ]


# 人脸抓拍结果结构体。
class NET_VCA_FACESNAP_RESULT(Structure):
    _fields_ = [
        ("dwSize", h_DWORD),
        ("dwRelativeTime", h_DWORD),
        ("dwAbsTime", h_DWORD),
        ("dwFacePicID", h_DWORD),
        ("dwFaceScore", h_DWORD),

        ("struTargetInfo", NET_VCA_TARGET_INFO),
        ("struRect", NET_VCA_RECT),
        ("struDevInfo", NET_VCA_DEV_INFO),
        ("dwFacePicLen", h_DWORD),
        ("dwBackgroundPicLen", h_DWORD),

        ("bySmart", h_BYTE),
        ("byAlarmEndMark", h_BYTE),
        ("byRepeatTimes", h_BYTE),
        ("byUploadEventDataType", h_BYTE),
        ("struFeature", NET_VCA_HUMAN_FEATURE),

        ("fStayDuration", h_FLOAT),
        ("sStorageIP", h_CHAR * 16),
        ("wStoragePort", h_WORD),
        ("wDevInfoIvmsChannelEx", h_WORD),
        ("byFacePicQuality", h_BYTE),

        ("byUIDLen", h_BYTE),
        ("byLivenessDetectionStatus", h_BYTE),
        ("byAddInfo", h_BYTE),
        ("pUIDBuffer", POINTER(h_BYTE_P)),
        ("pAddInfoBuffer", POINTER(NET_VCA_FACESNAP_ADDINFO)),

        ("byTimeDiffFlag", h_BYTE),
        ("cTimeDifferenceH", h_CHAR),
        ("cTimeDifferenceM", h_CHAR),
        ("byBrokenNetHttp", h_BYTE),
        ("pBuffer1", POINTER(h_BYTE_P)),
        ("pBuffer2", POINTER(h_BYTE_P))
    ]


# 预览参数结构体
class NET_DVR_PREVIEWINFO(Structure):
    _fields_ = [
        # 通道号，目前设备模拟通道号从1开始，数字通道的起始通道号通过
        # NET_DVR_GetDVRConfig(配置命令NET_DVR_GET_IPPARACFG_V40)获取（dwStartDChan）
        ('lChannel', h_LONG),
        # 码流类型：0-主码流，1-子码流，2-三码流，3-虚拟码流，以此类推
        ('dwStreamType', h_DWORD),
        # 连接方式：0-TCP方式，1-UDP方式，2-多播方式，3-RTP方式，4-RTP/RTSP，5-RTP/HTTP,6-HRUDP（可靠传输）
        ('dwLinkMode', h_DWORD),
        # 播放窗口的句柄，为NULL表示不解码显示
        ('hPlayWnd', h_HWND),
        # 0-非阻塞取流，1- 阻塞取流
        # 若设为不阻塞，表示发起与设备的连接就认为连接成功，如果发生码流接收失败、播放失败等
        # 情况以预览异常的方式通知上层。在循环播放的时候可以减短停顿的时间，与NET_DVR_RealPlay
        # 处理一致。
        # 若设为阻塞，表示直到播放操作完成才返回成功与否，网络异常时SDK内部connect失败将会有5s
        # 的超时才能够返回，不适合于轮询取流操作。
        ('bBlocked', h_BOOL),
        # 是否启用录像回传： 0-不启用录像回传，1-启用录像回传。ANR断网补录功能，
        # 客户端和设备之间网络异常恢复之后自动将前端数据同步过来，需要设备支持。
        ('bPassbackRecord', h_BOOL),
        # 延迟预览模式：0-正常预览，1-延迟预览
        ('byPreviewMode', h_BYTE),
        # 流ID，为字母、数字和"_"的组合，IChannel为0xffffffff时启用此参数
        ('byStreamID', h_BYTE * 32),
        # 应用层取流协议：0-私有协议，1-RTSP协议。
        # 主子码流支持的取流协议通过登录返回结构参数NET_DVR_DEVICEINFO_V30的byMainProto、bySubProto值得知。
        # 设备同时支持私协议和RTSP协议时，该参数才有效，默认使用私有协议，可选RTSP协议。
        ('byProtoType', h_BYTE),
        # 保留，置为0
        ('byRes1', h_BYTE),
        # 码流数据编解码类型：0-通用编码数据，1-热成像探测器产生的原始数据
        # （温度数据的加密信息，通过去加密运算，将原始数据算出真实的温度值）
        ('byVideoCodingType', h_BYTE),
        # 播放库播放缓冲区最大缓冲帧数，取值范围：1、6（默认，自适应播放模式）   15:置0时默认为1
        ('dwDisplayBufNum', h_DWORD),
        # NPQ模式：0- 直连模式，1-过流媒体模式
        ('byNPQMode', h_BYTE),
        # 保留，置为0
        ('byRes', h_BYTE * 215),
    ]
