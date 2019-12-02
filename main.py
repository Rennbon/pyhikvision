import config
import hkws.soadapter as sdk
import os
import getopt, sys

# 启动函数  python3 main.py -c xxx/xxx
cnfPath = ''
opts, args = getopt.getopt(sys.argv[1:], '-c:')
for opt_name, opt_val in opts:
    if opt_name in ('-c'):
        cnfPath = opt_val

if cnfPath == '':
    print('Please enter the config path.')

# loadconfig
cnf = config.Config()
path = os.path.join(cnfPath, 'config.ini')
cnf.InitConfig(path)

# new adpter
adapter = sdk.HKAdapter()
adapter.add_so(cnf.SDKPath)
# init hkws linux sdk
initRes = adapter.init_sdk()
if initRes == False:
    os._exit(0)

# user login
loginRes = adapter.login(cnf.IP, cnf.Port, cnf.User, cnf.Password)
if loginRes < 0:
    adapter.NET_DVR_Cleanup()
