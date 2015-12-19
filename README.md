# pyorcnews------>基于scrapy框架的爬虫

##项目


##部署
###scrapyd
方便部署爬虫到服务器，可以远程调控服务器中爬虫的运行、暂停等操作
文档地址：http://scrapyd.readthedocs.org/en/latest/
安装完成后需要配置文件
接下来需要上传爬虫到服务器
首先修改爬虫项目下的scrapy.cfg文件
```
[deploy:pyorcnews]
url = http://localhost:6800/
project = pyorcnews
url 表示爬虫服务器地址
```
进到爬虫项目中
scrapyd-deploy -l 查看项目列表
scrapyd-deploy pyorcnews 上传项目
项目上传成功后就可以操作爬虫工作了


###supervisor
Supervisor --> Python写的进程管理器。
安装好后修改配置文件(linux下默认目录/etc/supervisor/supervisord.conf)
如下图，配置后可以在浏览器中查看和管理进程

supervisor监控的进程配置在
做一个最简单的配置如下

完成后启动

启动成功可以打开浏览器可以看到

###crontab
