## pyhikvision [一闪一闪亮晶晶，star一下好心情]
![GitHub](https://img.shields.io/github/license/Rennbon/pyhikvision)
![release](https://img.shields.io/github/v/release/Rennbon/pyhikvision)
![python](https://img.shields.io/badge/python-3.10.4-brightgreen)
![platform](https://img.shields.io/badge/platform-Linux64|Linux32|win64|win32-lightgrey)
官方最新sdk已经有Python示例了
## 新变动
- preview使用tk代替win32gui
- 移除系统类型配置
## 分支 feature/rennbon 有rstp的实现，加了点异步能提升一些性能

## 配套理解sdk二次开发原理
- pyhivision使用指南https://www.jianshu.com/p/c3c4bf3d1ef8
- 海康威视官方音视频技术方案对比 https://open.hikvision.com/docs/docId?productId=612781c8ec4acb28e0e1c0c3&version=%2Fff026cfc47a14e79a6c9acf21d9d8769&curNodeId=2e231666a7854dc4a2dc29b9ed06782a
### 注意

- 海康有些设备的SDK需要跟海康的技术要，官网的版本可能是对不上的，已经有部分开发者遇到这个问题了，请大家注意下，百思不得其解，找官方技术人员了解一下SDK是否对应。
- 支持Centos及Windows系统，不支持ubuntu（官方没有针对ubuntu做优化）
- error code https://open.hikvision.com/hardware/definitions/NET_DVR_GetLastError.html
### 推荐
mac开发虚拟机推荐：
虚拟工具：https://www.parallels.cn/pd/general/
可以直接安装linux和windows，且可以独立到应用级别，非常适合海康威视开发，比云服务器或者docker好用

### 对应海康SDK版本
链接:https://pan.baidu.com/s/1xe3wXH7CYIswPgx59y4XWg 提取码:oqd5
- 设备网络SDK V6.1.9.4_build20220412
- 播放库SDK V7.3.9.50_build20210106
- 密码重置助手 https://www.hikvision.com/cn/password-reset/#download-agreement

### local_config.ini配置（主目录下config.ini修改为local_config.ini即可）

```
[DEFAULT]
SDKPath: .dll或.so的根目录，会遍历加载，填根SDK目录即可
User: 摄像头访问用户名，需要在海康威视图形界面上自己配置
Password: 摄像头访问密码，需要在海康威视图形界面上自己配置
Port: 摄像头端口
IP: 摄像头ip

```

### example启动方式

- 将根目录下config.ini 改为local_config.ini

```
cd example
python xxx.py
```

### Linux SDK加载107问题解决方案

1. 将SDK动态库路径加入到LD_LIBRARY_PATH环境变量

```
# 修改系统预加载项,增加一行export
vim ~/.bashrc
export  LD_LIBRARY_PATH=$LD_LIBRARY_PATH:{官方动态库MakeAll所对应的Linux中的绝对路径}:{官方动态库MakeAll/HCNetSDKCom/在Linux中的绝对路径}
source ~/.bashrc

```

2. 在/etc/ld.so/conf下增加sdk路径

```
# 查看配置信息
cat /etc/ld.so.conf
# 如果有以下Include，建议在ld.so.conf.d下新建文件设置，这样隔离比较干净
include ld.so.conf.d/*.conf
# 切换到指定目录
cd /etc/ld.so.conf.d

vim hikvsdk.conf
# 加入以下2个路径
{官方动态库MakeAll所对应的Linux中的绝对路径}
{官方动态库MakeAll/HCNetSDKCom/在Linux中的绝对路径}

# 保存完后执行以下命令重新加载系统.so配置
ldconfig

```

### 注意：

{官方动态库MakeAll所对应的Linux中的绝对路径} {官方动态库MakeAll/HCNetSDKCom/在Linux中的绝对路径} 相对应的系统路径需要加最后需要加"/",因为该库Python的加载逻辑中没有拼接"/"
如：

```
/opt/hkws/lib/
/opt/hkws/lib/HCNetSDKCom/
```

### 维护及联系：

1. 该库我们将会以社区化的方式维护，欢迎提交pull request

2. 微信群(请加 WB343688972 好友或者扫码加好友，验证回复 pyhikvison 按照指引进群)'

   <img src="./doc/wechat.png" width="200px" >
3. QQ群（901635269）

   <img src="./doc/qq-qr.jpg" width="200px" >

