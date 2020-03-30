### local_config.ini配置（主目录下config.ini修改为local_config.ini即可）
```
[DEFAULT]
SDKPath: .dll或.so的根目录，会遍历加载，填根SDK目录即可
User: 摄像头访问用户名，需要在海康威视图形界面上自己配置
Password: 摄像头访问密码，需要在海康威视图形界面上自己配置
Port: 摄像头端口
IP: 摄像头ip
Plat: 枚举值 0:linux    1:windows
```

### 启动方式
```
python3 main.py -c "配置文件目录，不需要带config.ini"
```
### Linux SDK加载107问题解决方案
1. 将SDK动态库路径加入到LD_LIBRARY_PATH环境变量
```
# 修改系统预加载项,增加一行export
vim ~/.bashrc
export  LD_LIBRARY_PATH=$LD_LIBRARY_PATH:{pyhikvsion/hkws/lib/在Linux中的绝对路径}:{pyhikvsion/hkws/lib/HCNetSDKCom/在Linux中的绝对路径}
source ~/.bashrc

vim /etc/profile
export  LD_LIBRARY_PATH=$LD_LIBRARY_PATH:{pyhikvsion/hkws/lib/在Linux中的绝对路径}:{pyhikvsion/hkws/lib/HCNetSDKCom/在Linux中的绝对路径}
source /etc/profile
```
2. 在/etc/ld.so/conf下增加sdk路径
```
//查看配置信息
cat /etc/ld.so.conf
//如果有以下Include，建议在ld.so.conf.d下新建文件设置，这样隔离比较干净
include ld.so.conf.d/*.conf
//切换到指定目录
cd /etc/ld.so.conf.d

vim hikvsdk.conf
#加入以下2个路径
{pyhikvsion/hkws/lib/HCNetSDKCom/在Linux中的绝对路径}
{pyhikvsion/hkws/lib/在Linux中的绝对路径}

//保存完后执行以下命令重新加载系统.so配置
ldconfig

```

### 注意：
{pyhikvsion/hkws/lib/HCNetSDKCom/在Linux中的绝对路径}
{pyhikvsion/hkws/lib/在Linux中的绝对路径}
相对应的系统路径需要加最后需要加"/",因为该库Python的加载逻辑中没有拼接"/"
如： 
```
/opt/hkws/lib/
/opt/hkws/lib/HCNetSDKCom/
```

### 维护及联系：
1. 该库我们将会以社区化的方式维护，欢迎提交pull request
2. 本库配有QQ群（901635269）

![QQ群](./doc/qq-qr.jpg)
<img src="./doc/qq-qr.jpg" width="100px" >
3. 以下是支付宝捐赠入口，我们将用于设备采集，完善开源库。

![捐赠](./doc/donate.jpg)
