from hkws import cm_camera_adpt,config
import os
from example.instant_preview_cb import *
import time

# 启动函数  python3 main2.py -c xxx/xxx

cnf = config.Config()
path = os.path.join('./local_config.ini')
cnf.InitConfig(path)

# new adpter
adapter = cm_camera_adpt.CameraAdapter()
adapter.add_lib(cnf.SDKPath, cnf.Suffix)
adapter.init_sdk()
# user login
userId = adapter.login(cnf.IP, cnf.Port, cnf.User, cnf.Password)
if userId < 0:
    adapter.NET_DVR_Cleanup()

print("Login successful,the userId is ", userId)

lRealPlayHandle = adapter.start_preview(None, userId)
if lRealPlayHandle < 0:
    os._exit(2)

print("Start preview successful,the lRealPlayHandle is ", lRealPlayHandle)
callback = adapter.callback_real_data(lRealPlayHandle, f_real_data_call_back , userId)
print('callback_real_data result is ', callback)
time.sleep(20)
adapter.stop_preview(lRealPlayHandle)
adapter.logout(userId)
adapter.sdk_clean()
