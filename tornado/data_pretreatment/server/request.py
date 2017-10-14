from tornado import web
import json
from server.handler.abnormal_stu import AbnormalStu
import time
from logConfig import logger,errorMessage

def isClose(request_self):
    request_self.finish({'status': 0, 'errorInfo': "功能关闭时间00：30-05：30", 'data': ''})


def judgeIsOpen(func):      #用于检测服务器是否关闭
    def is_open(self_request):
        now=int(time.strftime("%H%M%S"))
        if now>=3000 and now<=53000:    #服务关闭
            return isClose(self_request)
        else:
            return func(self_request)
    return is_open


def getErrorMessage(post):
    def diyPost(self_request):
        try:
            post(self_request)
        except Exception as e:
            # _, reason, exc_tb = sys.exc_info()
            # error = traceback.extract_tb(exc_tb)
            # result = error[len(error) - 1]
            # message=("file: %s--line: %s--errorfunc: %s()--reason: %s" % (result[0], result[1], result[2], reason))
            logger.error(errorMessage(e))
            self_request.finish({"status":0, "errorInfo":"服务器出错，请稍后再试"})
    return diyPost


class BaseHandler(web.RequestHandler):  #每个请求的基类
    def initialize(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET,POST')


class GetAbnormalStu(BaseHandler):
    @getErrorMessage
    @judgeIsOpen
    def post(self):
        startdate=self.get_argument('startdate','2017-01-01')
        enddate=self.get_argument('enddate','2017-01-01')
        sleepdays=self.get_argument('sleepdays',0)  #0表示没有选择此项异常筛选
        moneydays=self.get_argument('moneydays',0)
        maxmoney=self.get_argument('maxmoney',100)
        failnum=self.get_argument('failnum',0)
        allstuid=self.get_argument('allstuid')
        allstuid=eval(allstuid)
        result=AbnormalStu().entry(startdate,enddate,int(sleepdays),int(moneydays),int(failnum),float(maxmoney),allstuid)
        result=json.dumps(result,ensure_ascii=False)
        self.write(result)

