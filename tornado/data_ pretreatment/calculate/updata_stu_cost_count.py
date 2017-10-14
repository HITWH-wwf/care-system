from calculate.orm import *
from datetime import datetime,timedelta
import numpy as np
from logConfig import logger,errorMessage

def updataStuCostCount():
    logger.info('updata stu_cost_count')
    print('updata stu_cost_count')
    day = timedelta(days=1)
    nowdate = datetime.today()-day  #昨天
    with db_data.execution_context():
        old_count = stu_cost_count.select()
    restart = 0  # 用于判断是否要重新更新表
    if len(old_count) > 0:
        if nowdate.date() != old_count[0].countDate.date():  # 判断表里的数据是否是最新的
            with db_data.execution_context():
                query = stu_cost_count.delete().where(stu_cost_count.countDate != nowdate)#清空表
                query.execute()
            restart = 1  # 要重新更新
    if len(old_count) == 0 or restart == 1:  # 第一次运行或者新的一天
        with db_data.execution_context():
            allStuId = stu_basic_info.select(stu_basic_info.stuID)
            allstu=[]
            for i in range(len(allStuId)):
                stu=countCostDays(allStuId[i].stuID)
                allstu.append(stu)
            with db_data.atomic():
                stu_cost_count.insert_many(allstu).execute()
    logger.info('updata stu_cost_count is ok')
    print('updata stu_cost_count is ok')
    return {'status': 1}

def countCostDays(stuId):
    nowStuRecord = MyBaseModel.returnList2(stu_transaction_record.select().where(stu_transaction_record.stuID == stuId))
    disdays=365                 #只统计最近180天的消费
    day=timedelta(days=1)
    endDate = datetime.today()-day  #今天的前一天
    startDate= endDate-day*disdays
    record=np.zeros(disdays)

    addr=0  #这边初始化一次，下面不用在初始化了
    for i in range(disdays):
        nowdate = startDate + day * i
        todayMoney = 0.0
        while addr != len(nowStuRecord):
            if nowStuRecord[addr].tradingTime.date() == nowdate.date():
                if nowStuRecord[addr].turnover < 0: #消费
                    todayMoney = todayMoney + nowStuRecord[addr].turnover
                nowStuRecord.pop(addr)
                continue
            if (nowStuRecord[addr].tradingTime.date() - nowdate.date()).days >0:
                break   #到了另一天的刷卡记录，跳出循环,下次进入循环仍然从当前位置开始
            addr = addr + 1

        dis=(nowdate.date() - startDate.date()).days
        record[dis]=abs(todayMoney)


    countdays=''
    for i in range(disdays):
        countdays = countdays + str(record[i]) + '-'
    nowstu={'stuID':stuId,'everyDayCost':countdays,'countDate':endDate}
    return nowstu
    # stu_cost_count.create(stuID=stuId,everyDayCost=countdays,countDate=endDate)



