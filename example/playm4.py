import logging
import os
import sys


curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
PathProject = os.path.split(rootPath)[0]
sys.path.append(rootPath)
sys.path.append(PathProject)

from hkws import playm4_adpt, config
from hkws.core.type_map import h_DWORD

# 初始化配置文件
cnf = config.Config()
path = os.path.join('../local_config.ini')
cnf.InitConfig(path)
if cnf.Plat == "1":
    os.chdir(cnf.SDKPath)

# 初始化SDK适配器
adapter = playm4_adpt.PlayM4()
userId = adapter.common_start(cnf)
if userId < 0:
    logging.error("初始化Adapter失败")
    os._exit(0)

res = adapter.get_port()
if res == 0:
    os._exit(0)

res = adapter.set_stream_open_mode(h_DWORD(0))
if res == 0:
    os._exit(0)



