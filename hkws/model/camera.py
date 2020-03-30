# 硬件产品人像相关
from ctypes import *


# 人体属性参数结构体。
class NET_VCA_HUMAN_FEATURE(Structure):
    _fields_ = [
        ("byAgeGroup", c_byte),
        ("bySex", c_byte),
        ("byEyeGlass", c_byte),
        ("byAge", c_byte),
        ("byAgeDeviation", c_byte),
        ("byEthnic", c_byte),
        ("byMask", c_byte),
        ("bySmile", c_byte),
        ("byFaceExpression", c_byte),
        ("byBeard", c_byte),
        ("byRace", c_byte),
        ("byHat", c_byte),
        ("byRes", c_byte * 4)
    ]


# 点坐标参数结构体
class NET_VCA_POINT(Structure):
    _fields_ = [
        ("fX", c_float),
        ("fY", c_float)
    ]


# 多边形结构体
class NET_VCA_POLYGON(Structure):
    _fields_ = [
        ("dwPointNum", c_uint32),
        ("struPos", NET_VCA_POINT * 4)
    ]


# 区域框参数结构体。
class NET_VCA_RECT(Structure):
    _fields_ = [
        ("fX", c_float),
        ("fY", c_float),
        ("fWidth", c_float),
        ("fHeight", c_float)
    ]


# 尺寸过滤器参数结构体
class NET_VCA_SIZE_FILTER(Structure):
    _fields_ = [
        ("byActive", c_byte),
        ("byMode", c_byte),
        ("byRes", c_byte * 2),
        ("struMiniRect", NET_VCA_RECT),
        ("struMaxRect", NET_VCA_RECT)
    ]


# JPEG图像信息结构体。
class NET_DVR_JPEGPARA(Structure):
    _fields_ = [
        ("wPicSize", c_uint16),
        ("wPicQuality", c_uint16),
    ]


# 人脸抓拍规则参数（单条）结构体
class NET_VCA_SINGLE_FACESNAPCFG(Structure):
    _fields_ = [
        ("byActive", c_byte),
        ("byAutoROIEnable", c_byte),
        ("byRes", c_byte * 2),
        ("struSizeFilter", NET_VCA_SIZE_FILTER),
        ("struVcaPolygon", NET_VCA_POLYGON),
    ]


# 人脸抓拍规则参数结构体
class NET_VCA_FACESNAPCFG(Structure):
    _fields_ = [
        ("dwSize", c_uint32),
        ("bySnapTime", c_byte),
        ("bySnapInterval", c_byte),
        ("bySnapThreshold", c_byte),
        ("byGenerateRate", c_byte),
        ("bySensitive", c_byte),
        ("byReferenceBright", c_byte),
        ("byMatchType", c_byte),
        ("byMatchThreshold", c_byte),
        ("struPictureParam", NET_DVR_JPEGPARA),
        ("struRule", NET_VCA_SINGLE_FACESNAPCFG * 1),
        ("wFaceExposureMinDuration", c_uint16),
        ("byFaceExposureMode", c_byte),
        ("byBackgroundPic", c_byte),
        ("dwValidFaceTime", c_uint32),
        ("dwUploadInterval", c_uint32),
        ("dwFaceFilteringTime", c_uint32),
        ("byRes2", c_byte * 84)
    ]


# 报警目标信息结构体。
class NET_VCA_TARGET_INFO(Structure):
    _fields_ = [
        ("dwID", c_uint32),
        ("struRect", NET_VCA_RECT),
        ("byRes", c_byte * 4)
    ]


# IP地址结构体。
class NET_DVR_IPADDR(Structure):
    _fields_ = [
        ("sIpV4", c_char * 16),
        ("sIpV6", c_byte * 128)
    ]


# 前端设备信息结构体。
class NET_VCA_DEV_INFO(Structure):
    _fields_ = [
        ("struDevIP", NET_DVR_IPADDR),
        ("wPort", c_uint16),
        ("byChannel", c_byte),
        ("byIvmsChannel", c_byte)
    ]


# 人脸抓拍结果结构体。
class NET_VCA_FACESNAP_RESULT(Structure):
    _fields_ = [
        ("dwSize", c_uint32),
        ("dwRelativeTime", c_uint32),
        ("dwAbsTime", c_uint32),
        ("dwFacePicID", c_uint32),
        ("dwFaceScore", c_uint32),
        ("struTargetInfo", NET_VCA_TARGET_INFO),
        ("struRect", NET_VCA_RECT),
        ("struDevInfo", NET_VCA_DEV_INFO),
        ("dwFacePicLen", c_uint32),
        ("dwBackgroundPicLen", c_uint32),
        ("bySmart", c_byte),
        ("byAlarmEndMark", c_byte),
        ("byRepeatTimes", c_byte),
        ("byUploadEventDataType", c_byte),
        ("struFeature", NET_VCA_HUMAN_FEATURE),
        ("fStayDuration", c_float),
        ("sStorageIP", c_char * 16),
        ("wStoragePort", c_uint16),
        ("wDevInfoIvmsChannelEx", c_uint16),

        ("byFacePicQuality", c_byte),
        ("byUIDLen", c_byte),
        ("byLivenessDetectionStatus", c_byte),
        ("byAddInfo", c_byte),
        ("byTimeDiffFlag", c_byte),
        ("cTimeDifferenceH", c_char),
        ("cTimeDifferenceM", c_char),

        ("byBrokenNetHttp", c_byte),
        ("pBuffer1", c_void_p),
        ("pBuffer2", c_void_p)
    ]


# 预览参数结构体
class NET_DVR_PREVIEWINFO(Structure):
    _fields_ = [
        # 通道号，目前设备模拟通道号从1开始，数字通道的起始通道号通过
        # NET_DVR_GetDVRConfig(配置命令NET_DVR_GET_IPPARACFG_V40)获取（dwStartDChan）
        ('lChannel', c_long),
        # 码流类型：0-主码流，1-子码流，2-三码流，3-虚拟码流，以此类推
        ('dwStreamType', c_ulong),
        # 连接方式：0-TCP方式，1-UDP方式，2-多播方式，3-RTP方式，4-RTP/RTSP，5-RTP/HTTP,6-HRUDP（可靠传输）
        ('dwLinkMode', c_ulong),
        # 播放窗口的句柄，为NULL表示不解码显示
        ('hPlayWnd', c_void_p),
        # 0-非阻塞取流，1- 阻塞取流
        # 若设为不阻塞，表示发起与设备的连接就认为连接成功，如果发生码流接收失败、播放失败等
        # 情况以预览异常的方式通知上层。在循环播放的时候可以减短停顿的时间，与NET_DVR_RealPlay
        # 处理一致。
        # 若设为阻塞，表示直到播放操作完成才返回成功与否，网络异常时SDK内部connect失败将会有5s
        # 的超时才能够返回，不适合于轮询取流操作。
        ('bBlocked', c_bool),
        # 是否启用录像回传： 0-不启用录像回传，1-启用录像回传。ANR断网补录功能，
        # 客户端和设备之间网络异常恢复之后自动将前端数据同步过来，需要设备支持。
        ('bPassbackRecord', c_bool),
        # 延迟预览模式：0-正常预览，1-延迟预览
        ('byPreviewMode', c_byte),
        # 流ID，为字母、数字和"_"的组合，IChannel为0xffffffff时启用此参数
        ('byStreamID', c_byte * 32),
        # 应用层取流协议：0-私有协议，1-RTSP协议。
        # 主子码流支持的取流协议通过登录返回结构参数NET_DVR_DEVICEINFO_V30的byMainProto、bySubProto值得知。
        # 设备同时支持私协议和RTSP协议时，该参数才有效，默认使用私有协议，可选RTSP协议。
        ('byProtoType', c_byte),
        # 保留，置为0
        ('byRes1', c_byte),
        # 码流数据编解码类型：0-通用编码数据，1-热成像探测器产生的原始数据
        # （温度数据的加密信息，通过去加密运算，将原始数据算出真实的温度值）
        ('byVideoCodingType', c_byte),
        # 播放库播放缓冲区最大缓冲帧数，取值范围：1、6（默认，自适应播放模式）   15:置0时默认为1
        ('dwDisplayBufNum', c_ulong),
        # 保留，置为0
        ('byRes', c_byte * 216),
    ]
