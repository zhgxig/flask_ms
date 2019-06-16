### skills

#### web
+ flask

#### request
+ requests
+ httpie


#### 序列化和反序列化
+ msgpack-python
+ pickle
+ cPickle
+ json

#### database
+ mysql/mariadb
    + pymysql
    + mysql.connector
    + mysqldb
+ redis
    + redis
    + wrais
+ memcache
    + libmc
+ mongo
    + pymongo
    + mongoengine
+ elasticsearch
    + elasticsearch


#### deal files
+ python-magic 确定文件类型
+ Pillow 处理图片
+ cropresize2 剪切图片
+ short_url 创建短链接

#### flask package
+ werkzeug(WSGI协议层工具集)
    + DebuggedApplication
    + data structure
        + TypeConversionDict(指定类型dict)
        + ImmutableTypeConversionDict(不可变dict)
        + MultiDict(相同键传入多个值) 
    + special function
        + cached_property(加类的属性上)
        + import_string(获取库的地址)
        + secure_filename(安全文件名，只限英文名)
    + password security
    + middleware
        + SharedDataMiddleware(展示static)
        + ProfilerMiddleware(检测性能)
        + DispatcherMiddleware(调度应用)

+ blinker(解耦复杂逻辑)
+ flask-login(登录管理)
+ flask_script(命令管理)
+ flask_debugtoolbar(debug)
+ flask-migrate(migrate db)
+ flask-wtf(配合模板使用)
+ flask-security(角色管理、权限管理、用户登录、邮箱验证、密码重置、密码加密、跟踪用户登录状态)
+ flask-restful(管理接口)
+ flask-admin(后台管理)
+ flask-assets(前端静态资源管理)

+ gunicorn

+ uwsgi
    