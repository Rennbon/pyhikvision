import logging
import os
import time
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
PathProject = os.path.split(rootPath)[0]
sys.path.append(rootPath)
sys.path.append(PathProject)

from hkws import base_adapter, config

# 初始化配置文件
cnf = config.Config()
path = os.path.join('../local_config.ini')
cnf.InitConfig(path)

# 初始化SDK适配器
adapter = base_adapter.BaseAdapter()
userId = adapter.common_start(cnf)
if userId < 0:
    logging.error("初始化Adapter失败")
    os._exit(0)

print("Login successful,the userId is ", userId)
v = adapter.get_sdk_version()
print("version:", v)
bv = adapter.get_sdk_build_version()
print("build version", bv)
res, state = adapter.get_sdk_state()
if res:
    print(state.dwTotalLoginNum)

res2, abl = adapter.get_sdk_abl()
if res2:
    print(abl.dwMaxLoginNum)
adapter.logout(userId)
adapter.sdk_clean()
