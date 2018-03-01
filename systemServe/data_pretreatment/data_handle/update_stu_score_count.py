from data_pretreatment.data_orm import *
from data_pretreatment.common_func.deal_dateortime_func import *
from data_pretreatment.logConfig import logger,errorMessage

def scoreCount(stuId):
    nowStuRecord = MyBaseModel.returnList2(exam_results.select(exam_results.id,exam_results.examScore,exam_results.credit).where(exam_results.stuID==stuId))
    yesterday = getBeforeDateTime(1)
    strYesterday=str(yesterday.date())
    failNum=0
    failCredit=0
    gainTotalCredit=0
    failId=[]
    successId=[]
    for record in nowStuRecord:
        if record.examScore<60:
            failNum=failNum+1
            failCredit=failCredit+record.credit
            failId.append(record.id)
        else:
            successId.append(record.id)
            gainTotalCredit=gainTotalCredit+record.credit

    stu={'stuID':stuId,'scoreCountInfo':{'failNum':failNum,'failId':failId,'failCredit':failCredit,'gainTotalCredit':gainTotalCredit,'successId':successId},'lastTimeCountDate':strYesterday}
    return stu


def updateStuScoreCount():
    logger.info('start update stu_score_count')
    print('update stu_score_count')
    yesterday = getBeforeDateTime(1)
    allStuId = MyBaseModel.returnList2(stu_basic_info.select(stu_basic_info.stuID))
    scoreAllStuId=MyBaseModel.returnList2(stu_score_count.select(stu_score_count.stuID))

    lastTimeCountDate=MyBaseModel.returnList2(stu_score_count.select(stu_score_count.lastTimeCountDate).distinct())

    restart = 0  # 用于判断是否要重新更新表

    if len(allStuId)!=len(scoreAllStuId):   #初次运行或数据不完整
        restart=1
    elif len(lastTimeCountDate) > 1:  #数据存在错误
        restart=1

    elif len(lastTimeCountDate)>0:
        if yesterday.date() != strChangeToDateTime(lastTimeCountDate[0].lastTimeCountDate).date():  # 判断表里的数据不是最新的
            restart = 1     #要重新更新
    if restart == 1:  # 第一次运行或者新的一天
        with db_data.execution_context():
            query = stu_score_count.delete()  # 清空表
            query.execute()
        allstu = []
        for i in range(len(allStuId)):
            allstu.append(scoreCount(allStuId[i].stuID))
            if i%1000 ==0 or i==(len(allStuId)-1):
                logger.info(str(i))
                with db_data.execution_context():
                    with db_data.atomic():
                        stu_score_count.insert_many(allstu).execute()
                    allstu=[]

    logger.info('update stu_score_count is ok')
    print('update stu_score_count is ok')
    return {'status': 1}

