# autoSafe_BJFU

## 1、简介

​	根据BJFU师生报平安网站设计的自动报平安脚本，参考了[k652大佬](https://github.com/k652)写的[daily_fudan](https://github.com/k652/daily_fudan)。

##### WARNING：

**“师生报平安”是学校决策的重要参考之一，务必认真对待。**

##### 	Features：

- [x] 自动报平安脚本开发
- [ ] 支持自动获取表单json
- [ ] 云函数部署，定时执行

## 2、操作步骤

### （1）进行报平安表单数据的手动抓包

​		1）登录账号后进入报平安界面

​		2）F12后进入网络模块

​		3）开启低速3G模式

​		4）点击提交按钮

​		5）当第二个报文出现后，立刻将低速3G模式切换为离线模式

​		6）第一个报文内容如下

​			![image-20220611121425067](https://github.com/2001renhaoyu/autoSafe_BJFU/blob/master/img/image-20220611121425067.png)

​		7）将请求荷载内容复制到jsonData.json中

​		8）利用ide将jsonData.json转换为双引号模式（复制过去会报错，自动解决错误即完成双引号转换）

### （2）在config.json中填写账号、密码、dataStores_id

​		dataStores_id在抓包数据中可以找到

​			![image-20220611112018186](https://github.com/2001renhaoyu/autoSafe_BJFU/blob/master/img/image-20220611112018186.png)

### （3）运行autoSafe.py

## 3、实现原理

### （1）登录

​		经过抓包分析，bjfu登录的流程如下：

​			![image-20220611123405727.png](https://github.com/2001renhaoyu/autoSafe_BJFU/blob/master/img/image-20220611123405727.png)

​		其中需要解决的问题以及解决的方法：

​			1）lt口令、excutioon、_eventId的获取

​				利用lxml中的etree，根据html构建树，拿出lt、excutioon、_eventId

​			2）des加密，bjfu用的三密钥des是自行编写的，没有调库

​				a. 	抓包，获得bjfu的des.js

​				b.	利用execjs在python中执行des.js,获取rsa

​				

### （2）报平安表单提交

​		经过抓包分析，bjfu表单提交只需要向下面的url发送携带jsonData的POST的请求即可。

https://s.bjfu.edu.cn/tp_fp/formParser?status=update&formid=7394b770-ba93-4041-91b7-80198a68&workflowAction=startProcess&seqId=&unitId=&applyCode=&workitemid=&process=bae380db-7db4-4c7c-9458-d79188fa359a

​		1）status=update表示更新表格

​		2）formid=7394b770-ba93-4041-91b7-80198a68表示报平安表单，每个人的都一样

​		3）process=bae380db-7db4-4c7c-9458-d79188fa359a表示执行更新表格的进程id，每个人的都一样 

​		4）bjfu对发送的jsonData没有校验，程序每次提交都修改了提交日期

​		5）提交后会返回相应信息

成功时会返回SYS_PK、SYS_FK

​			![image-20220611121649919](https://github.com/2001renhaoyu/autoSafe_BJFU/blob/master/img/image-20220611121649919.png)
