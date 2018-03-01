from data_pretreatment.data_orm import *
from data_pretreatment.common_func.deal_dateortime_func import *
from data_pretreatment.logConfig import logger,errorMessage
from data_pretreatment.data_handle.sleep_count import sleepCount,sleepCountOneDay

def updateStuSleepCount():
    logger.info('start update stu_sleep_count')
    print('start update stu_sleep_count')
    yesterday = getBeforeDateTime(1)
    beforeTowDay = getBeforeDateTime(2)
    allStuId = MyBaseModel.returnList2(stu_basic_info.select(stu_basic_info.stuID))
    sleepAllStuId=MyBaseModel.returnList2(stu_sleep_count.select(stu_sleep_count.stuID))

    lastTimeCountDate=MyBaseModel.returnList2(stu_sleep_count.select(stu_sleep_count.lastTimeCountDate).distinct())

    restart = 0  # 用于判断是否要重新更新表

    if len(allStuId)!=len(sleepAllStuId):   #初次运行或数据不完整 len(allStuId)
        restart=1

    elif len(lastTimeCountDate) > 1:  #数据存在错误
        restart=1


    elif len(lastTimeCountDate) > 0:  # 数据库中的统计信息是一天内完成的
        lastCountDate = strChangeToDateTime(lastTimeCountDate[0].lastTimeCountDate).date()
        if yesterday.date() != lastCountDate:  # 判断表里的数据不是最新的
            if beforeTowDay.date() == lastCountDate:
                #restart = 2  # 是前天的统计信息，只需增加昨天的数据统计
                restart=1
            else:
                restart = 1  # 是更早之前的统计信息，需重新更新


    if restart == 1:  # 需要重新更新
        with db_data.execution_context():
            query = stu_sleep_count.delete()  # 清空表
            query.execute()
        allstu=[]
        for i in range(len(allStuId)):    #len(allStuId)
            stu=sleepCount(allStuId[i].stuID)
            allstu.append(stu)
            if i%500 ==0 or i==(len(allStuId)-1):  #len(allStuId)-1
                logger.info(str(i))
                with db_data.execution_context():
                    with db_data.atomic():
                        stu_sleep_count.insert_many(allstu).execute()
                    allstu=[]

    # elif restart==2:
    #     for i in range(len(allStuId)):
    #         sleepCountOneDay(allStuId[i].stuID)
    #         if i%500 ==0 or i==(len(allStuId)-1):  #len(allStuId)-1
    #             logger.info(str(i))

    print('update stu_sleep_count is ok')
    logger.info('update stu_sleep_count is ok')
    return {'status': 1}




