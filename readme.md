### 系统差异
./hkws/core/type_map.py
```
# line 11  DWORD会根据操作系统的不同，被定义成了不同的长度,如果是32位的请自行修改下
h_DWORD = c_ulong  # 64bit:c_ulong    32bit:c_uint32  
```
### 理念
- 如果帮助到了您，希望能够获得您的star
- 海康威视摄像头等硬件官方提供有SDK动态库，另外Python社区的AI库是最强的，所以Python对应的开发环境也是有一定场景的，尤其是基于图像功能的二次开发。
- 海康威视SDK偏函数式编程，且直接基于动态SDK二次开发较为复杂，实现一个接口的调用要查阅很多资料，还要对比官方的其他语言的Demo库，很不方便。

所以这里打算维护迭代海康威视动态SDK基于Python3的开源库以减轻二次开发的难度。

### Python 版本
python 3.6

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

### example启动方式
- 将根目录下config.ini 改为local_config.ini
```
cd example
python3 xxx.py
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
//查看配置信息
cat /etc/ld.so.conf
//如果有以下Include，建议在ld.so.conf.d下新建文件设置，这样隔离比较干净
include ld.so.conf.d/*.conf
//切换到指定目录
cd /etc/ld.so.conf.d

vim hikvsdk.conf
#加入以下2个路径
{官方动态库MakeAll所对应的Linux中的绝对路径}
{官方动态库MakeAll/HCNetSDKCom/在Linux中的绝对路径}

//保存完后执行以下命令重新加载系统.so配置
ldconfig

```

### 注意：
{官方动态库MakeAll所对应的Linux中的绝对路径}
{官方动态库MakeAll/HCNetSDKCom/在Linux中的绝对路径}
相对应的系统路径需要加最后需要加"/",因为该库Python的加载逻辑中没有拼接"/"
如： 
```
/opt/hkws/lib/
/opt/hkws/lib/HCNetSDKCom/
```

### 维护及联系：
1. 该库我们将会以社区化的方式维护，欢迎提交pull request
2. 本库配有QQ群（901635269）

<img src="./doc/qq-qr.jpg" width="100px" >

