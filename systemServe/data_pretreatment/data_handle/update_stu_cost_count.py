from data_pretreatment.data_orm import *
from data_pretreatment.common_func.deal_dateortime_func import *
from data_pretreatment.logConfig import logger,errorMessage
from data_pretreatment.data_handle.cost_count import costCountAll,costCountOneDay

def updateStuCostCount():
    logger.info('start update stu_cost_count')
    print('start update stu_cost_count')
    yesterday = getBeforeDateTime(1)
    beforeTowDay=getBeforeDateTime(2)
    allStuId = MyBaseModel.returnList2(stu_basic_info.select(stu_basic_info.stuID))
    costAllStuId=MyBaseModel.returnList2(stu_cost_count.select(stu_cost_count.stuID))

    lastTimeCountDate=MyBaseModel.returnList2(stu_cost_count.select(stu_cost_count.lastTimeCountDate).distinct())

    restart = 0  # 用于判断是否要重新更新表

    if len(allStuId)!=len(costAllStuId):   #初次运行或数据不完整 len(allStuId)
        restart=1

    elif len(lastTimeCountDate) > 1:  #数据存在错误
        restart=1

    elif len(lastTimeCountDate)>0:  #数据库中的统计信息是一天内完成的
        lastCountDate=strChangeToDateTime(lastTimeCountDate[0].lastTimeCountDate).date()
        if yesterday.date() != lastCountDate:  # 判断表里的数据不是最新的
            if beforeTowDay.date()== lastCountDate:
                restart = 2     #是前天的统计信息，只需增加昨天的数据统计
            else:
                restart = 1     #是更早之前的统计信息，需重新更新

# 此部分不用修改，如果出现学生名单更新，直接清空表就好
# 如果是从头开始，全部进行更新，则预警状态的需改等到全部更新完成后，再进行修改
# 如果是只更新最近的，则一次性进行全部更新，减少对数据库的IO操作，更新完成后，再对预警状态进行修改

    if restart == 1:  # 需要重新更新
        with db_data.execution_context():
            query = stu_cost_count.delete()  # 清空表
            query.execute()
        allstu=[]
        for i in range(len(allStuId)):    #len(allStuId)
            stu=costCountAll(allStuId[i].stuID)
            allstu.append(stu)
            if i%500 ==0 or i==(len(allStuId)-1):  #len(allStuId)-1
                logger.info(str(i))
                with db_data.execution_context():
                    with db_data.atomic():
                        stu_cost_count.insert_many(allstu).execute()
                    allstu=[]

    elif restart==2:
        for i in range(len(allStuId)):
            costCountOneDay(allStuId[i].stuID)
            if i%500 ==0 or i==(len(allStuId)-1):  #len(allStuId)-1
                logger.info(str(i))

    print('update stu_cost_count is ok')
    logger.info('update stu_cost_count is ok')
    return {'status': 1}




