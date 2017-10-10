from calculate.get_abnormal_stu_sleep import getAbnormalStuSleep
from calculate.get_abnormal_stu_cost import getAbnormalStuCost
from calculate.get_abnormal_stu_score import getAbnormalStuScore


def getAbnormalStu(startdate,enddate,sleepdays,moneydays,failnum,maxmoney,allStuId):
    result = []
    # allStuId = stu_basic_info.select(stu_basic_info.stuID,stu_basic_info.specialitiesid,stu_basic_info.collegeid,stu_basic_info.sex,
                                     stu_basic_info.stuName,stu_basic_info.state)
    if sleepdays>0:

        result.append(getAbnormalStuSleep(startdate,enddate,sleepdays))

    if moneydays>0:

        result.append(getAbnormalStuCost(startdate,enddate,moneydays,maxmoney))
    if failnum>0:
        result.append(getAbnormalStuScore(failnum))

    # abnormal_stu_temp=[]
    for res in result:
        assert res['status']==1,'数据库搜索出错'
        # abnormal_stu_temp=abnormal_stu_temp+res['data']


    abnormal_stu=[]

    for stu in result[0]['data']:
        flag=1  #用于判断要不要加入
        for i in range(len(result)-1):
            if stu not in result[i+1]['data']:
                flag=0
                break
        if flag==1:
            abnormal_stu.append(stu)


    if len(result)==1:  #只选择了一种模式
        abnormal_stu=abnormal_stu+result[0]['data']

    result_t=[]
    for stu in allStuId:
        if stu['stuID'] in abnormal_stu:
            result_t.append(getStuInformation(stu))

    return {'status': 1, 'data': result_t}

def getStuInformation(stu):
    #获取该学生的信息，用于返回给前端
    nowStuInfo={"specialitiesid":stu['specialitiesid'],"collegeid":stu['collegeid'],
                "state":stu['state'],"stuID":stu['stuID'],"stuName":stu['stuName'],"sex":stu['sex']}
    return nowStuInfo