# Docker + Appium 移动端模拟器

##### 【注意】由于安卓模拟器响应过慢，并且不支持x86架构app安装，此方案暂时中断。问题总结如下：

- 安卓模拟器仅支持X86架构的app安装包，不支持arm架构。
- 重启Docker后，包括网络代理在内等信息需要重新配置。
- mitmproxy证书安装后，转为CA证书时，受到SD卡访问限制。

## Docker

来源：Github - Docker Android

链接：https://github.com/budtmo/docker-android

##### 注意事项

- Linux OS请使用包含“X86”的镜像名称。
- OSX和Windows OS请使用支持Ubuntu OS虚拟化的虚拟机。

##### 可用镜像列表

| OS    | Android | API  | Browser | Browser version | Chromedriver | Image                             |
| ----- | ------- | ---- | ------- | --------------- | ------------ | --------------------------------- |
| Linux | 5.0.1   | 21   | browser | 37.0            | 2.21         | budtmo/docker-android-x86-5.0.1   |
| Linux | 5.1.1   | 22   | browser | 39.0            | 2.13         | budtmo/docker-android-x86-5.1.1   |
| Linux | 6.0     | 23   | browser | 44.0            | 2.18         | budtmo/docker-android-x86-6.0     |
| Linux | 7.0     | 24   | chrome  | 51.0            | 2.23         | budtmo/docker-android-x86-7.0     |
| Linux | 7.1.1   | 25   | chrome  | 55.0            | 2.28         | budtmo/docker-android-x86-7.1.1   |
| Linux | 8.0     | 26   | chrome  | 58.0            | 2.31         | budtmo/docker-android-x86-8.0     |
| Linux | 8.1     | 27   | chrome  | 61.0            | 2.33         | budtmo/docker-android-x86-8.1     |
| Linux | 9.0     | 28   | chrome  | 66.0            | 2.40         | budtmo/docker-android-x86-9.0     |
| Linux | 10.0    | 29   | chrome  | 74.0            | 74.0.3729.6  | budtmo/docker-android-x86-10.0    |
| All   | -       | -    | -       | -               | -            | budtmo/docker-android-real-device |
| All   | All     | All  | All     | All             | All          | budtmo/docker-android-genymotion  |

##### 可用设备列表

| Type   | Device Name            |
| ------ | ---------------------- |
| Phone  | Samsung Galaxy S10     |
| Phone  | Samsung Galaxy S9      |
| Phone  | Samsung Galaxy S8      |
| Phone  | Samsung Galaxy S7 Edge |
| Phone  | Samsung Galaxy S7      |
| Phone  | Samsung Galaxy S6      |
| Phone  | Nexus 4                |
| Phone  | Nexus 5                |
| Phone  | Nexus One              |
| Phone  | Nexus S                |
| Tablet | Nexus 7                |

##### Docker-android镜像准备

- 拉取镜像，此处设备为Nexus 5，容器名为android-container，安卓版本为android-x86-7.1.1。

  ```
  docker run --privileged -d -p 6080:6080 -p 5554:5554 -p 5555:5555 -e DEVICE="Nexus 5" --name android-container butomo1989/docker-android-x86-7.1.1
  （此处7安装证书有问题，改为安卓6，待更新）
  ```

- 查看正在运行的容器，android-container的状态应该为healthy，如果状态为unhealthy，请开启虚拟化。

  ```
  docker ps -a 
  ```

- 通过docker-host-ip-address+6080端口访问安卓模拟器图形化界面：

  ```
  http://172.27.128.72:6080/
  ```

  <img src=".\Docker App文档.assets\image-20200526105859196.png" alt="image-20200526105859196" style="zoom:50%;" />

  

##### Android-container内部工具及依赖准备

- 进入容器内部中的命令行：

  ```
  docker exec -i -t android-container /bin/bash
  ```

- 查看python、Appium、Java、Adb版本：

  ```
  # python版本
  root@a3b4a552f85c:~# python3
  Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
  
  # Appium版本
  root@a3b4a552f85c:~# appium -v
  1.10.1
  
  # Java版本
  root@a3b4a552f85c:~# java -version
  openjdk version "1.8.0_191"
  OpenJDK Runtime Environment (build 1.8.0_191-8u191-b12-0ubuntu0.18.04.1-b12)
  OpenJDK 64-Bit Server VM (build 25.191-b12, mixed mode)
  
  # Adb版本
  root@a3b4a552f85c:~# adb version
  Android Debug Bridge version 1.0.40
  Version 4986621
  Installed as /root/platform-tools/adb
  ```

- 安装pip及各项依赖：

  ```
  # 升级apt
  apt-get update
  
  # 安装vim
  apt-get install vim
  
  # 安装pip
  apt-get install python-pip
  apt-get install python3-pip
  ```

- 显示连接设备：

  ```
  root@a3b4a552f85c:~# adb devices
  List of devices attached
  emulator-5554	device
  ```

##### 服务器外部环境准备

- 使用virtualenv创建python3虚拟环境。启动虚拟环境进行后续操作：

  ```
  # 启动虚拟环境
  source app_env/bin/activate
  # 关闭虚拟环境
  deactivate
  ```

- 安装mitmproxy工具（mitmproxy文档：https://docs.mitmproxy.org/stable/）：

  ```
  # 安装mitmproxy
  pip install mitmproxy
  
  # mitmdump是mitmproxy的命令行版本
  # 执行mitmdump后将在root根目录下的.mitmproxy文件夹生成证书
  (app_env) [liurui@m7-model-test01 ~]$ mitmdump
  Proxy server listening at http://*:8080
  
  # 将.mitmrproxy中的证书拷贝并重命名为mitmproxy（需要root权限）
  sudo -s
  cp /root/.mitmproxy mitmproxy目录/
  mv .mitmproxy mitmproxy
  ```

##### 安卓模拟器图形化界面环境准备

- 通过http://172.27.128.72:6080/访问安卓模拟器图形化界面。mitmproxy监听端口为8080，为了使mitmproxy获取中间流量，需要在模拟器的网络设置（Settings->Wi-Fi->Modify Network）中手动设置代理：

  ```
  Proxy hostname: 172.27.128.72
  Proxy port: 8080
  ```

  <img src=".\Docker App文档.assets\image-20200526113127182.png" alt="image-20200526113127182" style="zoom:50%;" />

- 此时由于mitmproxy证书还未传入手机，虽然在mitmdump界面能够看到流量，到那时https流量无法被解析：

  <img src=".\Docker App文档.assets\image-20200526113528917.png" alt="image-20200526113528917" style="zoom:50%;" />
  =======
  ![image-20200526113528917](.\Docker App文档.assets\image-20200526113528917.png)
##### 安装证书

- centos安装根证书：

  ```
  # 复制证书
  cp /root/.mitmproxy/mitmproxy-ca-cert.cer /etc/pki/ca-trust/source/anchors/
  
  # 建立软连接
  ln -s /etc/pki/ca-trust/source/anchors/mitmproxy-ca-cert.cer  /etc/ssl/certs/mitmproxy-ca-cert.cer
  
  # 更新系统证书
  update-ca-trust
  ```

- 将证书复制到安卓模拟器：

  ```
  docker cp mitmproxy/mitmproxy-ca-cert.pem android-container-2:/root
  ```

- 添加mitmproxy证书为系统证书：

  ```
  # 进入容器命令行
  docker exec -i -t android-container /bin/bash
  
  # 获取有效的系统证书文件名
  openssl x509 -inform PEM -subject_hash_old -in mitmproxy-ca-cert.pem -noout  
  
  # 转换证书格式为PEM格式，并重命名证书为有效的系统证书名。
  openssl x509 -inform PEM -in mitmproxy-ca-cert.pem -out c8750f0d.0 
  
  # 上传证书到设备
  adb push c8750f0d.0 /system/etc/security/cacerts  
  ```

  