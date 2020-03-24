from ctypes import *


# 设置sdk加载路劲
class NET_DVR_LOCAL_SDK_PATH(Structure):
    _fields_ = [
        ("sPath", c_byte*256),
        ("byRes", c_byte*128)
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
