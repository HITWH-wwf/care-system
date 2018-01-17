from data_pretreatment.data_orm import *
from data_pretreatment.common_func.deal_dateortime_func import *
from data_pretreatment.logConfig import logger,errorMessage
from data_pretreatment.data_handle.cost_count import costCount

def updataStuCostCount():
    logger.info('start updata stu_cost_count')
    print('start updata stu_cost_count')
    yesterday = getBeforeDateTime(1)
    allStuId = MyBaseModel.returnList2(stu_basic_info.select(stu_basic_info.stuID))
    costAllStuId=MyBaseModel.returnList2(stu_cost_count.select(stu_cost_count.stuID))

    lastTimeCountDate=MyBaseModel.returnList2(stu_cost_count.select(stu_cost_count.lastTimeCountDate).distinct())

    restart = 0  # 用于判断是否要重新更新表

    if len(allStuId)!=len(costAllStuId):   #初次运行或数据不完整 len(allStuId)
        restart=1

    elif len(lastTimeCountDate) > 1:  #数据存在错误
        restart=1

    elif len(lastTimeCountDate)>0:
        if yesterday.date() != strChangeToDateTime(lastTimeCountDate[0].lastTimeCountDate).date():  # 判断表里的数据不是最新的
            restart = 1


    if restart == 1:  # 需要重新更新
        with db_data.execution_context():
            query = stu_cost_count.delete()  # 清空表
            query.execute()
        allstu=[]
        for i in range(len(allStuId)):    #len(allStuId)
            stu=costCount(allStuId[i].stuID)
            allstu.append(stu)
            if i%500 ==0 or i==(len(allStuId)-1):  #len(allStuId)-1
                logger.info(str(i))
                with db_data.atomic():
                    stu_cost_count.insert_many(allstu).execute()
                allstu=[]
    print('updata stu_cost_count is ok')
    logger.info('updata stu_cost_count is ok')
    return {'status': 1}




