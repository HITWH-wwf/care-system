from data_pretreatment.data_orm import *
from datetime import datetime
import os

def getAbnormalStuSleep(startdate,enddate,days):
    try:
        # allStuId, stuRecord_sleep,
        # allStuId = stu_basic_info.select(stu_basic_info.stuID)
        # abnormalStu = []
        # stuRecord_sleep,
        result = judgeStuAbnormalSleep(startdate, enddate, days)
        return {'status': 1, 'data': result}
    except (Exception) as e:
        raise e
        # print(e)
        # return {'status': 0, 'errorInfo': "操作出错，请稍候再试", 'data': ''}


def judgeStuAbnormalSleep(startdate,enddate,days):
    with db_data.execution_context():
        stuRecord=stu_sleep_count.select()
    result=[]
    totaldays=365
    startdates = startdate.split('-')
    enddates = enddate.split('-')
    startDate = datetime(int(startdates[0]), int(startdates[1]), int(startdates[2]))
    endDate = datetime(int(enddates[0]), int(enddates[1]), int(enddates[2]))
    disdays=(endDate.date()-startDate.date()).days
    disdays2=(stuRecord[0].countDate.date()-endDate.date()).days
    if disdays2<0:
        disdays2=0
    startat=totaldays-disdays-disdays2-1
    endat=totaldays-disdays2     #这个不用减1
    for stu in stuRecord:
        everydays=stu.everyDaySleep.split('-')
        counts=0
        for i in range(startat,endat):
            if everydays[i]=='1':
                counts=counts+1
            if counts>=days:
                result.append(stu.stuID)
                break
    return result

def getStuInformation(stu):
    #获取该学生的信息，用于返回给前端
    nowStuInfo={"specialitiesid":stu.specialitiesid,"collegeid":stu.collegeid,
                "state":stu.state,"stuID":stu.stuID,"stuName":stu.stuName,"sex":stu.sex}
    return nowStuInfo
