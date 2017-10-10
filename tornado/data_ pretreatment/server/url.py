# -*- coding:utf-8 -*-
import tornado
from server.request import *

class MyApplication(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/getabnormalstu", GetAbnormalStu),

        ]

        settings = {

        }

        tornado.web.Application.__init__(self, handlers, **settings,debug = False)
                #使用多进程的时候，记得设置为false


#MyApplication = tornado.web.Application(handlers = handlers,**settings)
