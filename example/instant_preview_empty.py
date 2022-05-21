# 空白预览，可以自行拓展，无系统限制
import logging
import os
import sys
import time

from hkws.core import env

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
PathProject = os.path.split(rootPath)[0]
sys.path.append(rootPath)
sys.path.append(PathProject)

from hkws import cm_camera_adpt, config
from example import instant_preview_empty_cb

# 初始化配置文件
cnf = config.Config()
path = os.path.join('../local_config.ini')
cnf.InitConfig(path)
if env.isWindows():
    os.chdir(cnf.SDKPath)

# 初始化SDK适配器
adapter = cm_camera_adpt.CameraAdapter()
userId = adapter.common_start(cnf)
if userId < 0:
    logging.error("初始化Adapter失败")
    os._exit(0)

print("Login successful,the userId is ", userId)

lRealPlayHandle = adapter.start_preview(None, userId)
if lRealPlayHandle < 0:
    adapter.logout(userId)
    adapter.sdk_clean()
    os._exit(2)

print("start preview 成功", lRealPlayHandle)
callback = adapter.callback_real_data(lRealPlayHandle, instant_preview_empty_cb.f_real_data_call_back, userId)
print("callback", callback)

time.sleep(30)
adapter.stop_preview(lRealPlayHandle)
adapter.logout(userId)
adapter.sdk_clean()
