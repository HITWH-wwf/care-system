from data_pretreatment.data_orm import *
from datetime import datetime

def getAbnormalStuScore(nums):
    try:
        # allStuId, stuRecord_sleep,
        # allStuId = stu_basic_info.select(stu_basic_info.stuID)
        # abnormalStu = []
        # stuRecord_sleep,
        result = judgeStuAbnormalScore(nums)
        return {'status': 1, 'data': result}
    except (Exception) as e:
        raise e
        # print(e)
        # return {'status': 0, 'errorInfo': "操作出错，请稍候再试", 'data': ''}


def judgeStuAbnormalScore(nums):
    with db_data.execution_context():
        stuRecord=stu_score_count.select(stu_score_count.stuID,stu_score_count.failNum)
    result=[]

    for stu in stuRecord:
        if stu.failNum>=nums:
            result.append(stu.stuID)

    return result

def getStuInformation(stu):
    #获取该学生的信息，用于返回给前端
    nowStuInfo={"specialitiesid":stu.specialitiesid,"collegeid":stu.collegeid,
                "state":stu.state,"stuID":stu.stuID,"stuName":stu.stuName,"sex":stu.sex}
    return nowStuInfo
