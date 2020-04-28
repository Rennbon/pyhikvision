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
adapter.add_lib(cnf.SDKPath, cnf.Suffix)
adapter.init_sdk()
res = adapter.activate_device(cnf.IP, cnf.Port, cnf.Password)
print(res)