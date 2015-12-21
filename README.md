
# pyorcnews------>基于scrapy框架的爬虫


##项目说明
此项目是功能时爬取新闻网站的新闻信息存入数据库mysql中,项目中使用了[DjangoItem](https://github.com/scrapy/scrapy/blob/0.24/docs/topics/djangoitem.rst),所以需要依赖django项目[Pyorc](https://github.com/pyorc/pyorc)

##部署
### [scrapyd](http://scrapyd.readthedocs.org/en/latest/)
方便部署爬虫到服务器，可以远程调控爬虫的运行、暂停等操作
安装完成后需要配置文件
![scrapyd配置文件](http://img.blog.csdn.net/20151221103635312)
首先修改爬虫项目下的scrapy.cfg文件
```
[deploy:pyorcnews]
url = http://localhost:6800/
project = pyorcnews
url 表示爬虫服务器地址
```
接下来执行命令【scrapyd】 启动服务
scrapyd-deploy -l 查看项目列表
scrapyd-deploy pyorcnews 上传项目
![上传全部爬虫](http://img.blog.csdn.net/20151221105712220)
上传成功显示状态为OK
项目上传成功后就可以操作爬虫工作了
![部分功能](http://img.blog.csdn.net/20151221105701924)

###supervisor
Supervisor --> Python写的进程管理器。
安装好后修改配置文件(linux下默认目录/etc/supervisor/supervisord.conf)
如下图，配置后可以在浏览器中查看和管理进程
![supervisor简单配置](http://img.blog.csdn.net/20151221110124841)
supervisor监控的进程配置在
做一个最简单的配置如下
![scrapyd进程配置](http://img.blog.csdn.net/20151221110343598)
完成后启动
![启动scrapyd](http://img.blog.csdn.net/20151221110351916)
启动成功可以打开浏览器可以看到
![这里写图片描述](http://img.blog.csdn.net/20151221110117111)
###crontab
编写shell脚本
![shell脚本](http://img.blog.csdn.net/20151221110639648)
编辑crontab
crontab -e
    * */6 * * * /home/zmy/shell-sh/scrapyd.sh #表示每6个小时执行一次
执行cron~~
sudo service cron start

至此部署完成，爬虫可以每六小时执行一此
