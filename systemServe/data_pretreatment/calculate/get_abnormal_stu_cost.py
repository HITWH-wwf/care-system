from data_pretreatment.data_orm import *
from datetime import datetime
from data_pretreatment.logConfig import logger,errorMessage
def getAbnormalStuCost(startdate,enddate,days,maxMoney):
    try:
        result = judgeStuAbnormalCost(startdate, enddate,maxMoney,days)
        return {'status': 1, 'data': result}
    except (Exception) as e:
        raise


def judgeStuAbnormalCost(startdate,enddate,maxMoney,days):
    with db_data.execution_context():
        stuRecord = stu_cost_count.select()
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
        everydays=stu.everyDayCost.split('-')
        counts=0
        for i in range(startat,endat):
            if float(everydays[i])>=maxMoney:
                counts = counts + 1
            if counts >= days:
                    result.append(stu.stuID)
                    break
    return result

def getStuInformation(stu):
    #获取该学生的信息，用于返回给前端
    nowStuInfo={"specialitiesid":stu.specialitiesid,"collegeid":stu.collegeid,
                "state":stu.state,"stuID":stu.stuID,"stuName":stu.stuName,"sex":stu.sex}
    return nowStuInfo
