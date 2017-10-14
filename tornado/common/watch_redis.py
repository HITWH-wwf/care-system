# #coding=utf8
#
# import os
# import redis
#
# import logging
# import logging.config
# import logging.handlers
# import configparser
# import traceback
# import time
# import orm
#
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# LOG_DIR = os.path.join(BASE_DIR, "logs")
# if not os.path.exists(LOG_DIR):
#     os.makedirs(LOG_DIR)  # 创建路径
# logging.config.dictConfig({
#     'version': 1,
#     'disable_existing_loggers': True,
#     'formatters': {
#         'verbose': {
#             'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
#             'datefmt': "%Y-%m-%d %H:%M:%S"
#         },
#         'simple': {
#             'format': '%(levelname)s %(message)s'
#         },
#     },
#     'handlers': {
#         'null': {
#             'level': 'DEBUG',
#             'class': 'logging.NullHandler',
#         },
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'verbose'
#         },
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.RotatingFileHandler',
#             # 当达到10MB时分割日志
#             'maxBytes': 1024 * 1024 * 10,
#             # 最多保留10份文件
#             'backupCount': 10,
#             # If delay is true,
#             # then file opening is deferred until the first call to emit().
#             'delay': True,
#             'filename': os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs/watch_redis.log"),
#             'formatter': 'verbose'
#         }
#     },
#     'loggers': {
#         '': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#         },
#     }
# })
#
# logger = logging.getLogger(__file__)
#
# m_redis = None
#
# def init_redis_pool_connect(iflog = True):
#     """创建redis的池化链接"""
#     global m_redis
#     try:
#         pool = redis.ConnectionPool(host='127.0.0.1', port = 6379)
#         m_redis = redis.Redis(connection_pool = pool, decode_responses = True)
#     except:
#         error_info = traceback.format_exc()
#         if iflog == True:
#             logger.error("初次链接redis出错，错误信息为：%s"%error_info)
#             logger.info("程序等待120秒，之后再尝试链接。若失败，程序将退出。")
#         #尝试等待redis服务启动
#         time.sleep(120)
#         pool = redis.ConnectionPool(host='127.0.0.1', port = 6379)
#         m_redis = redis.Redis(connection_pool = pool, decode_responses = True)
#         if iflog == True:
#             logger.info("成功链接redis")
#
# init_redis_pool_connect()
#
# class WatchRedis():
#     """本类维护redis内的数据，常驻运行于后端"""
#     def __init__(self,):
#         """建立与redis的链接"""
#         global m_redis
#         self.m_redis = m_redis
#
#     def watch_class_set(self,):
#         """将数据库中所有班级的集合刷新到redis中"""
#         class_list = orm.MyBaseModel.returnList(orm.stu_basic_info.select(orm.stu_basic_info.classNumberId).distinct(orm.stu_basic_info.classNumberId).dicts(), key = 'stuClassNumber')
#         self.m_redis.set("stu_total_class", str(class_list))
#
#     def watch_page_set(self,):
#         """将配置文件中的页面集合刷新到redis中"""
#         file_path = os.path.dirname(os.path.abspath(__file__)) + "/ini/page.ini"
#         text = configparser.ConfigParser()
#         text.read(file_path, encoding = "GBK")
#         if "page" not in text.sections():
#             raise ("error:page.ini不识别，未查询到page标签")
#
#         page_list = []
#         for con in text["page"]:
#             page_list.append(con)
#         self.m_redis.set("stu_total_page", str(page_list))
#
#     def start(self,):
#         """
#         作为维护redis的运行入口
#         当前维护redis以下两样数据：
#             1.当前设定的所有合法页面名
#             2.当前数据库中所有班级班号的集合
#         """
#         #时间紧张，维护的方法采用比较简单粗暴的一种
#         #每隔10分钟，将数据库中最新的班级集合和最新的页面名覆盖至redis中
#         while True:
#             self.watch_class_set()
#             self.watch_page_set()
#             time.sleep(600)
#
# if __name__ == "__main__":
#     test = WatchRedis()
#     test.start()
