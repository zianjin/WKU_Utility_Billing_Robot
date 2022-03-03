# WKU水电费小助手
一个用于定期记录WKU水电费的脚本

[Looking for English Readme?](README_EN.md)

## 背景

由于WKU校园内的水电账单系统时常存在扣费延迟的现象，而补扣的费用缺乏令人信服的证明。不少学生为费用摸不着头脑，但也没有申诉的依据。为了更好地掌握水电费使用情况，留下一手证据，我开源了这个自动化脚本。配合定时任务，它可以根据设定的时间间隔，自动查询当前的剩余的水电费情况，并形成记录。

## 安装以及部署

### 步骤#1: 捕获必要的验证信息

在获取水电费数据过程中，Cookie是通过身份认证的必要元素。为了抓取用于认证的数据包，我从微信公众号 ”温州肯恩大学校园卡 “下的“一卡通充值”服务入手。

> 提示：在本篇教程中，我使用Fiddler作为抓包工具。

#### 步骤#1.1: 启用对HTTPS流量的捕获功能

由于我们获取Cookie所需的参数是通过HTTPS通信的，所以我们必须确保在开始之前，抓包软件已经启用了这个功能。

<img src="img/fiddler_https.png" alt="fiddler_https" width="60%" height="60%" />

#### 步骤#1.2: 抓取微信公众号下H5网页的HTTPS请求

在抓包软件开始正常抓包后，我们打开微信公众号 ”温州肯恩大学校园卡 “并依次点击 "校园服务"、"一卡通充值"、"缴水费"。

#### 步骤#1.3: 获得验证数据

最后一步! 我们从抓包软件中找到请求头为 "POST /app/login/getThirdUserAuthorize HTTP/1.1"的请求。在文本视图中复制*ymToken*和*ymUserId*备用。

![fiddler_data](img/fiddler_data.png)

> 提示：如果文本包含特殊符号，你需要将其转换为ASCII码。例如，"="需要转换为"%3D"。



### 步骤#2：安装Python脚本的依赖包

这个项目使用了Python3以及相关的依赖包，请确保你已经安装了它们。

```sh
pip install -r requirements.txt
```



### 步骤#3: 获取你寝室的areaCode

#### 步骤#3.1: 填入验证数据

还记得我们在第一步获取的*ymToken*和*ymUserId*嘛？将它们复制到我所提供的两个脚本中。

![example_ym](img/example_ym.png)

#### 步骤#3.2: 执行firstRun.py

在firstRun脚本中，你需要按照提示依次选择所属楼栋、所在楼层以及寝室号。

```sh
python firstRun.py
```

#### Step#3.3: 获取areaCode

复制脚本提供的*areaCode*，以便之后部署水电费记录机器人。

![example_firstRun](img/example_firstRun.png)

> 提示：如果显示的水电费与微信公众号不一样，请通过问题板块告诉我（或者见面告诉我）



### 第4步：部署水电费记录机器人

#### 步骤#4.1: 执行logRobot.py

```sh
python logRobot.py "your_area_code"
```

![example_logRobot](img/example_logRobot.png)
> 提示：*areaCode*参数需要用引号括起来，否则记录机器人会报错。

执行后，在当前目录下会产生一个以*areaCode*为名称的txt文件。时间和对应的水电费会被记录在其中。

![example_logFile](img/example_logFile.png)



#### 步骤#4.2: 将机器人部署在你想要部署的地方

该脚本目前部署在我的私人NAS上，并通过crontab定期进行记录。下面是我设置的crontab任务。
```sh
0 */4 * * * cd /data/fee && /usr/bin/python3 logRobot.py [areaCode]
```



## 拓展

这个脚本在轻量改写后可以在钉钉中实现缴费预警的功能。代码会在以后公布（可能会吧 老鸽子了orz）

<img src="img/example_dingReport.png" alt="example_dingReport" width="40%" height="40%" />
