# 使用callback处理流，可以将数据转存等操作
import logging
import os
import sys
import time

import win32con
import win32gui

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
PathProject = os.path.split(rootPath)[0]
sys.path.append(rootPath)
sys.path.append(PathProject)

from example import instant_preview_cb2
from hkws import cm_camera_adpt, config

# 初始化配置文件
cnf = config.Config()
path = os.path.join('../local_config.ini')
cnf.InitConfig(path)
if cnf.Plat == "1":
    os.chdir(cnf.SDKPath)

# 初始化SDK适配器
adapter = cm_camera_adpt.CameraAdapter()
userId = adapter.common_start(cnf)

if userId < 0:
    logging.error("初始化Adapter失败")
    os._exit(0)

print("Login successful,the userId is ", userId)

lRealPlayHandle = adapter.start_preview(None, None, userId)
if lRealPlayHandle < 0:
    adapter.logout(userId)
    adapter.sdk_clean()
    os._exit(2)

# hwnd = win32console.GetConsoleWindow()
# win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 0, 0, 600, 400, win32con.SWP_SHOWWINDOW)
# win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
# win32gui.UpdateWindow(hwnd)

wc = win32gui.WNDCLASS()
wc.lpszClassName = 'instant preview'
wc.style = win32con.CS_GLOBALCLASS | win32con.CS_VREDRAW | win32con.CS_HREDRAW
wc.hbrBackground = win32con.COLOR_WINDOW + 1
class_atom = win32gui.RegisterClass(wc)
hwnd = win32gui.CreateWindowEx(0, class_atom, 'instant preview',
                               win32con.WS_CAPTION | win32con.WS_VISIBLE | win32con.WS_THICKFRAME | win32con.WS_SYSMENU,
                               100, 100, 600, 400, 0, 0, 0, None)

win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
# hwnd = ctypes.windll.kernel32.GetConsoleWindow()
# ctypes.windll.user32.ShowWindow(hwnd, 1)
print("start preview 成功", lRealPlayHandle)
instant_preview_cb2.set_playM4_adpt(adapter.get_lib(), hwnd)
callback = adapter.callback_real_data(lRealPlayHandle, instant_preview_cb2.f_real_data_call_back, userId)
print("callback", callback)

time.sleep(60)
adapter.stop_preview(lRealPlayHandle)
adapter.logout(userId)
adapter.sdk_clean()
win32gui.DestroyWindow(hwnd)
