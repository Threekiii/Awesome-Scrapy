# Windows + 夜神模拟器 + Appium 移动端模拟器

##### 转载请注明出处

## 安装依赖

##### Nodejs

- 点击进入下载页面https://nodejs.org/zh-cn/。
- 下载安装包并安装。

![1](https://github.com/Threekiii/Scrapy-Spiders/blob/master/Notes/Windows+%E5%A4%9C%E7%A5%9E+Appium%E6%A8%A1%E6%8B%9F%E5%99%A8%E6%96%87%E6%A1%A3.assets/1-1591754209098.PNG?raw=true)

- 安装完成后，在CMD中输入`node -v`，显示版本号则表示安装成功。

  ```
  C:\Users\xbei>node -v
  v12.16.3
  ```

##### java SDK

- 点击进入下载页面https://www.oracle.com/java/technologies/javase/javase-jdk8-downloads.html。
- 注册Oracle账号，下载windows ×86安装包并安装，默认安装位置为：`C:\Program Files (x86)\Java`。

![2](https://github.com/Threekiii/Scrapy-Spiders/blob/master/Notes/Windows+%E5%A4%9C%E7%A5%9E+Appium%E6%A8%A1%E6%8B%9F%E5%99%A8%E6%96%87%E6%A1%A3.assets/2.PNG?raw=true)

- 添加环境变量。

  - JAVA_HOME

    `C:\Program Files (x86)\Java\jdk1.8.0_251`

  - CLASSPATH

    `.;%JAVA_HOME%\lib\dt.jar;%JAVA_HOME%\lib\tools.jar;`

  - Path

    `%JAVA_HOME%\bin`

    `%JAVA_HOME%\jre\bin`

- 安装完成后，在CMD中输入命令，显示版本号则表示安装成功。

  ```
  C:\Users\xbei>java -version
  java version "1.8.0_251"
  Java(TM) SE Runtime Environment (build 1.8.0_251-b08)
  Java HotSpot(TM) Client VM (build 25.251-b08, mixed mode, sharing)
  
  C:\Users\xbei>javac -version
  javac 1.8.0_251
  ```

##### Android SDK

- 点击进入下载页面 https://www.androiddevtools.cn/。
- 点击AndroidSDK工具，选择SDK Tools，下载安装包并安装。

![3](https://github.com/Threekiii/Scrapy-Spiders/blob/master/Notes/Windows+%E5%A4%9C%E7%A5%9E+Appium%E6%A8%A1%E6%8B%9F%E5%99%A8%E6%96%87%E6%A1%A3.assets/3.png?raw=True)

- 添加环境变量。

  - ANDROID_HOME

    `C:\Users\xbei\AppData\Local\Android\android-sdk`

  - Path

    `%ANDROID_HOME%\tools`

    `%ANDROID_HOME%\platform-tools`

##### Appium

- 科学上网，点击进入下载页面http://appium.io/。
- 下载最新版本并安装，安装路径为：`C:\Users\xbei\AppData\Local\Programs\Appium`。

##### 夜神模拟器

- 点击进入下载页面 https://www.yeshen.com/。
- 下载最新版本并安装，安装路径为：`D:\Spider\Nox\bin`。

## 配置环境

##### mitmproxy证书安装

- 安装Anaconda3，在python环境下安装mitmproxy：`pip install mitmproxy`，安装完成后，目录`$PYTHON_HOME/Scripts/`下将有以下三个文件：

  - mitmproxy：具有SSL/TLS功能的交互式拦截代理。
  - mitmdump：mitmproxy基于命令行的版本。
  - mitmweb：mitmproxxy基于web的界面。

- 在目录`$PYTHON_HOME/Scripts/`下运行mitmdump，将在用户目录`C:\Users\xbei`下生成.mitmproxy文件夹，包含以下证书：

  ```
  mitmproxy-ca.p12----PKCS12格式证书私钥
  
  mitmproxy-ca.pem----PEM格式证书私钥
  
  mitmproxy-ca-cert.cer----PEM格式证书，与mitmproxy-ca-cert.pem相同仅改变了后辍，适用于部分Android
  
  mitmproxy-ca-cert.p12----PKCS12格式证书，适用于Windows
  
  mitmproxy-ca-cert.pem----PEM格式证书，适用于大多数非Windows平台
  
  mitmproxy-dhparam.pem----PEM格式秘钥文件，用于增强SSL安全性
  
  Windows安装证书：双击mitmproxy-ca-cert.p12----全部默认直接点“下一步”直到安装完成。
  
  Android安装证书：
  * mitmproxy-ca-cert.cer复制到手机上----点击使用证书安装器安装证书
  * 手机访问mitm.it，选择安卓操作系统安装。
  ```

##### 夜神模拟器设置

- 将Android SDK目录下`C:\Users\xbei\AppData\Local\Android\android-sdk\platform-tools`中的`adb.exe`复制两份，其中一份改名为`nox_adb.exe`。
- 将复制的`adb.exe`和改名的`nox_adb.exe`复制到夜神模拟器目录`D:\Spider\Nox\bin`下，覆盖原文件。

![4](https://github.com/Threekiii/Scrapy-Spiders/blob/master/Notes/Windows+%E5%A4%9C%E7%A5%9E+Appium%E6%A8%A1%E6%8B%9F%E5%99%A8%E6%96%87%E6%A1%A3.assets/4-1591756541628.PNG?raw=True)

- 进入夜神模拟器，打开`设置`，连点五次`关于平板电脑`中的`版本号`，将出现`开发者选项`，进入`开发者选项`，勾选`USB调试`。

##### mitmproxy与夜神模拟器建立连接

- 确保已经在模拟器和电脑上安装了mitmproxy证书。
- 设置网络代理，打开设置，选择`无线网络`，点击`WLAN`，左键长按当前网络，点击`修改网络`，将代理服务器主机名设置为当前电脑IP，如`172.27.149.173`，代理服务器端口设置为`8080`。
- 设置好代理后，如果没有运行mitmdump，模拟器无法连接网络；运行mitmdump，模拟器能够连接网络，并且CMD能够看到POST/GET输出，则配置成功。

##### adb与夜神模拟器建立连接

- 确保已经复制adb.exe并覆盖。

- 进入夜神模拟器安装目录`D:\Spider\Nox\bin`。

- 输入`adb devices`后，出现提示：

  ```
  List of devices attached
  * daemon not running; starting now at tcp:5037
  * daemon started successfully
  ```

  此时，没有连接模拟器。

- 在输入`nox_adb.exe connect 127.0.0.1:62001`，出现提示：

  ```
  connected to 127.0.0.1:62001
  ```

  再次输入`adb devices`后，出现提示：

  ```
  List of devices attached
  127.0.0.1:62001 device
  ```

  此时，已经成功连接模拟器。

##### Appium与夜神模拟器建立连接

- 打开Appium，使用默认Host+Port，点击`Start Server`。

![5](https://github.com/Threekiii/Scrapy-Spiders/blob/master/Notes/Windows+%E5%A4%9C%E7%A5%9E+Appium%E6%A8%A1%E6%8B%9F%E5%99%A8%E6%96%87%E6%A1%A3.assets/5.PNG?raw=True)

- 点击右上角的放大镜进行配置。

![6](https://github.com/Threekiii/Scrapy-Spiders/blob/master/Notes/Windows+%E5%A4%9C%E7%A5%9E+Appium%E6%A8%A1%E6%8B%9F%E5%99%A8%E6%96%87%E6%A1%A3.assets/6.PNG?raw=True)

- Appium的配置参数包括以下内容：
  - `platformName`：系统
  - `platformVersion`：系统版本
  - `deviceName`：手机型号
  - `appPackage`：app包名
  - `appActivity`：app进程名
  - `noReset`：设置为True，每次打开app时不进行重置

  获取系统、系统版本及手机型号：

  - 进入夜神模拟器，点击`关于平板电脑`即可获取。

  获取app包名、进程名（网易新闻为例）：

  - 进入夜神模拟器，打开“网易新闻”app。

  - 进入夜神模拟器安装目录`D:\Spider\Nox\bin`，输入adb shell。进入adb shell后，输入`dumpsys activity | grep mFocusedActivity`。

    ```
    D:\Spider\Nox\bin>adb shell
    root@shamu:/ # dumpsys activity | grep mFocusedActivity
      mFocusedActivity: ActivityRecord{3542dc1c u0 com.hxzk.android.hxzksyjg_xj/.ui.activity.QueryActivity t3}
    ```

  - `com.hxzk.android.hxzksyjg_xj`即为app包名。

  - `.ui.activity.QueryActivity`即为app进程名。

- 在Desired Capabilities处填写参数，点击`Start Session`。

![7](https://github.com/Threekiii/Scrapy-Spiders/blob/master/Notes/Windows+%E5%A4%9C%E7%A5%9E+Appium%E6%A8%A1%E6%8B%9F%E5%99%A8%E6%96%87%E6%A1%A3.assets/7-1591758717236.PNG?raw=True)

- 可在Appium中进行元素定位，找到需要操作（点击、传参等）的元素，进行自动化操作。

![8](https://github.com/Threekiii/Scrapy-Spiders/blob/master/Notes/Windows+%E5%A4%9C%E7%A5%9E+Appium%E6%A8%A1%E6%8B%9F%E5%99%A8%E6%96%87%E6%A1%A3.assets/8-1591758865585.PNG?raw=True)

## 编写数据处理+自动化程序

##### mitmproxy数据处理

- 通过命令`mitmdump.exe -s extract.py`启动mitmproxy，所有发出的请求数据包、响应数据包都会被`extract.py`中定义的方法所处理。

```
# 请求数据包
def request(flow):
    # 获取请求对象
    request = flow.request
    # 实例化输出类
    info = ctx.log.info
    # 打印请求的url
    info(request.url)
    # 打印请求方法
    info(request.method)
    # 打印host头
    info(request.host)
    # 打印请求端口
    info(str(request.port))
    # 打印所有请求头部
    info(str(request.headers))
    # 打印cookie头
    info(str(request.cookies))

# 响应数据包，同上，也可定义数据库存储相关操作
def response(flow):
    # 数据库存储相关操作
    ...
```

##### Appium自动化

- 通过Appium-Python-Client建立模拟器与Appium的联系，实现自动化控制。安装命令`pip install Appium-Python-Client`。

```
def slide_app(page):
    # 初始化配置，设置Desired Capabilities参数
    desired_caps = {
        'udid': '127.0.0.1:62001', # 模拟器id，通过adb devices获取
        'platformName': 'Android',
        'platformVersion': '5.1.1',
        'deviceName': 'MI 9',
        'appPackage': 'com.netease.newsreader.activity',
        'appActivity': 'com.netease.nr.phone.main.MainActivity',
        'noReset': 'True',
        'unicodeKeyboard': 'True'
    }

    # 指定Appium Server
    server = 'http://localhost:4730/wd/hub'

    # 新建一个driver
    driver = webdriver.Remote(server, desired_caps)

    # 自动化操作
    # 点击
    driver.find_elements_by_id().click()
    # 滑动
    driver.swipe()
    # 截屏
    driver.save_screenshot()
    ...
```

## 并发执行

##### mitmproxy监听不同端口

- 在配置夜神模拟器的网络代理时，指定不同端口（如8080/8081）。

![9](https://github.com/Threekiii/Scrapy-Spiders/blob/master/Notes/Windows+%E5%A4%9C%E7%A5%9E+Appium%E6%A8%A1%E6%8B%9F%E5%99%A8%E6%96%87%E6%A1%A3.assets/9.PNG?raw=True)

- 在启动mitmproxy时，指定不同端口和不同数据处理程序`extract.py`。

  ```
  模拟器1：mitmdump -p 8080 -s extract.py
  模拟器2：mitmdump -p 8081 -s extract.py
  ```

##### 安装Appium Server

- https://bitbucket.org/appium/appium.app/downloads/

##### Appium Server端口

- 启动Appium时在Advanced中配置`Server Port`，指定不同端口。

![捕获](https://github.com/Threekiii/Scrapy-Spiders/blob/master/Notes/Windows+%E5%A4%9C%E7%A5%9E+Appium%E6%A8%A1%E6%8B%9F%E5%99%A8%E6%96%87%E6%A1%A3.assets/捕获.PNG?raw=True)

- 在Appium自动化程序中指定不同`模拟器id`和`Appium Server`。

```
desired_caps = {
    'udid': '127.0.0.1:62001', # 指定不同模拟器id
    'platformName': 'Android',
    'platformVersion': '5.1.1',
    'deviceName': 'MI 9',
    'appPackage': 'com.netease.newsreader.activity',
    'appActivity': 'com.netease.nr.phone.main.MainActivity',
    'noReset': 'True',
    'unicodeKeyboard': 'True'
}

# 指定Appium Server
模拟器1：server = 'http://localhost:4730/wd/hub'
模拟器2：server = 'http://localhost:4731/wd/hub'
```
