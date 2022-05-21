# 使用callback处理流，可以将数据转存等操作
import logging
import os
import sys
import tkinter

from hkws.core import env

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
if env.isWindows():
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

win = tkinter.Tk()
win.title("hikvision")
sw = win.winfo_screenwidth()
# 得到屏幕宽度
sh = win.winfo_screenheight()
ww = 600
wh = 400
x = (sw - ww) / 2
y = (sh - wh) / 2
win.geometry("%dx%d+%d+%d" % (ww, wh, x, y))

# 创建一个Canvas，设置其背景色为白色
cv = tkinter.Canvas(win, bg='white', width=ww, height=wh)
cv.pack()

hwnd = cv.winfo_id()

print("start preview 成功", lRealPlayHandle)
instant_preview_cb2.set_playM4_adpt(adapter.get_lib(), hwnd)
callback = adapter.callback_real_data(lRealPlayHandle, instant_preview_cb2.f_real_data_call_back, userId)
print("callback", callback)
# 主窗口循环显示
win.mainloop()
adapter.stop_preview(lRealPlayHandle)
adapter.logout(userId)
adapter.sdk_clean()

