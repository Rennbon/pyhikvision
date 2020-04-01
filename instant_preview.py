import logging
import os
import time

from hkws import cm_camera_adpt, config
import instant_preview_cb

# 初始化配置文件
cnf = config.Config()
path = os.path.join('local_config.ini')
cnf.InitConfig(path)

# 初始化SDK适配器
adapter = cm_camera_adpt.CameraAdapter()
userId = adapter.common_start(cnf)
if userId < 0:
    logging.error("初始化Adapter失败")
    os._exit(0)

lRealPlayHandle = adapter.start_preview(None, userId)
if lRealPlayHandle < 0:
    adapter.logout(userId)
    adapter.sdk_clean()
    os._exit(2)

callback = adapter.callback_real_data(lRealPlayHandle, instant_preview_cb.g_real_data_call_back, userId)


time.sleep(60)
adapter.stop_preview(lRealPlayHandle)
adapter.logout(userId)
adapter.sdk_clean()
