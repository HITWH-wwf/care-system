from calculate.orm import *
from datetime import datetime,timedelta
import numpy as np
from logConfig import logger,errorMessage
# from test_orm import *
def updataStuSleepCount():
    logger.info('updata stu_sleep_count')
    print('updata stu_sleep_count')
    day = timedelta(days=1)
    nowdate = datetime.today()-day
    with db_data.execution_context():
        old_count = stu_sleep_count.select()
    restart = 0  # 用于判断是否要重新更新表

    if len(old_count) > 0:
        if nowdate.date() != old_count[0].countDate.date():  # 新的一天
            with db_data.execution_context():
                query = stu_sleep_count.delete().where(stu_sleep_count.countDate != nowdate)#清空表
                query.execute()
            restart = 1  # 要重新更新
    if len(old_count) == 0 or restart == 1:  # 第一次运行或者新的一天
        with db_data.execution_context():
            allStuId = stu_basic_info.select(stu_basic_info.stuID)
            allstu=[]
            for i in range(len(allStuId)):
                stu=countSleepDays(allStuId[i].stuID)
                allstu.append(stu)
            with db_data.atomic():
                stu_sleep_count.insert_many(allstu).execute()
    print('updata stu_sleep_count is ok')
    logger.info('updata stu_sleep_count is ok')
    return {'status': 1}

def countSleepDays(stuId):
    with db_data.execution_context():
        nowStuRecord = entry_and_exit.select().where(entry_and_exit.stuID == stuId)
    disdays=365                 #只统计最近180天的归寝记录
    day=timedelta(days=1)
    endDate = datetime.today()-day  #今天的前一天
    startDate= endDate-day*disdays
    record=np.zeros(disdays)
    size=len(nowStuRecord)
    startFlag=0
    for i in range(size):
        if nowStuRecord[i].entryDate != None and startFlag == 0:
            if (nowStuRecord[i].entryDate.date() - startDate.date()).days >= 0:
                startFlag = 1
        if startFlag == 1:
            if nowStuRecord[i].exitDate != None:  # 出去的时间不为null
                if i < len(nowStuRecord) - 1 and nowStuRecord[i + 1].entryDate != None:  # 进来的时间不为null且还不是最后一个记录
                    if nowStuRecord[i].exitDate.date() != nowStuRecord[i + 1].entryDate.date():  # 外出跟回来不是同一天
                        dis=(nowStuRecord[i].exitDate.date() - startDate.date()).days
                        record[dis]=1   #表示该天异常
    countdays=''
    for i in range(disdays):
        if record[i]==0:
            countdays=countdays+str(0)+'-'
        else:
            countdays = countdays + str(1) + '-'
    nowstu={'stuID':stuId,'everyDaySleep':countdays,'countDate':endDate}
    return nowstu
    # stu_sleep_count.create(stuID=stuId,everyDaySleep=countdays,countDate=endDate)



