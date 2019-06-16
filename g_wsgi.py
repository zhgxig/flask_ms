from gevent import monkey
monkey.patch_all()
import multiprocessing
debug = True
loglevel = 'debug'
bind = '127.0.0.1:8001'
pidfile = './logs/gunicorn.pid'
logfile = './logs/gunicorn.log'
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gevent'
backlog = 2048
worker_connections = 1000
daemon = False
proc_name = 'flask_ms'
errorlog = './logs/gunicorn.log'
