from calculate.get_abnormal_stu import getAbnormalStu

class AbnormalStu(object):
    def entry(self,startdate,enddate,sleepdays,moneydays,failnum,maxmoney,allstuid):
        try:
            return getAbnormalStu(startdate,enddate,sleepdays,moneydays,failnum,maxmoney,allstuid)
        except:
            raise
