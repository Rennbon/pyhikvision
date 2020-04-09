import fcntl
import os
import time
from hkws.core.type_map import *
from hkws.model import alarm, camera


@CFUNCTYPE(h_BOOL, h_LONG, POINTER(alarm.NET_DVR_ALARMER), POINTER(h_CHAR), h_DWORD, h_VOID_P)
def face_alarm_call_back(lCommand: h_LONG,
                         pAlarmer: POINTER(alarm.NET_DVR_ALARMER),
                         pAlarmInfo: POINTER(h_CHAR),
                         dwBufLen: h_DWORD,
                         pUser: h_VOID_P):
    if lCommand == 0x1112:
        temperature = 36.20
        print(lCommand)
        alarm_info = camera.NET_VCA_FACESNAP_RESULT()
        memmove(pointer(alarm_info), pAlarmInfo, sizeof(alarm_info))
        print(alarm_info.byAddInfo)
        print(alarm_info.dwFacePicLen)
        if alarm_info.byAddInfo:
            face_addinfo_buff = camera.NET_VCA_FACESNAP_ADDINFO()
            memmove(pointer(face_addinfo_buff), alarm_info.pAddInfoBuffer, sizeof(camera.NET_VCA_FACESNAP_ADDINFO))
            temperature = face_addinfo_buff.fFaceTemperature
            print(temperature)
        if alarm_info.dwFacePicLen:
            a = string_at(alarm_info.pBuffer1, alarm_info.dwFacePicLen)
            with open((os.environ.get("HKSVR_DIR") + "/media/temp_pic/.temp_file.lock"), "wb") as lock_file:
                lock_file.write(b'lock')
                lock_file.close()
            current_milli_time = lambda: int(round(time.time() * 1000))
            with open("%s/media/temp_pic/temp%d-%.2f.jpeg" % (
                    os.environ.get("HKSVR_DIR"), current_milli_time(), temperature), "wb") as p_file:
                fcntl.flock(p_file.fileno(), fcntl.LOCK_EX)
                p_file.write(a)
                p_file.close()
            os.remove((os.environ.get("HKSVR_DIR") + "/media/temp_pic/.temp_file.lock"))

    return True
