# Windows + mumu模拟器 + Fiddler

## Fiddler配置

1. Tools→Options→HTTPS：

![image-20220214111806577](https://typora-1308934770.cos.ap-beijing.myqcloud.com/202202141118758.png)

2. Tools→Options→Connections：

![image-20220214124532539](https://typora-1308934770.cos.ap-beijing.myqcloud.com/202202141245656.png)

3. 点击Export Root Certificate to Desktop导出证书，点击Trust Root Certificate。

![image-20220214124704554](https://typora-1308934770.cos.ap-beijing.myqcloud.com/202202141247656.png)

4. 设置完成后，保存重启Fiddler。

## mumu模拟器

1. 下载mumu模拟器并安装：https://mumu.163.com/index.html
2. 设置→WLAN→长按已经连接的WLAN→修改网络：

![](https://typora-1308934770.cos.ap-beijing.myqcloud.com/202202141249306.png)

3. 查看本机IP地址：

```
C:\Users\47236>ipconfig
```

![image-20220214125054715](https://typora-1308934770.cos.ap-beijing.myqcloud.com/202202141250784.png)

3. 配置代理为本机IP地址，端口为Fiddler中设置的8888：

![image-20220214124959080](https://typora-1308934770.cos.ap-beijing.myqcloud.com/202202141249189.png)

4. 打开浏览器，访问IP地址:端口号，即192.168.1.40:8888，下载证书。

![image-20220214125233658](https://typora-1308934770.cos.ap-beijing.myqcloud.com/202202141252773.png)

5. 安装证书并设置锁屏密码。

![image-20220214125329281](https://typora-1308934770.cos.ap-beijing.myqcloud.com/202202141253334.png)

6. 通过代理查看HTTP/HTTPS的有关请求和响应。

![image-20220214125427402](https://typora-1308934770.cos.ap-beijing.myqcloud.com/202202141254561.png)

