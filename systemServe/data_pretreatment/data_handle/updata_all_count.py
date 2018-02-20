from data_pretreatment.logConfig import logger,errorMessage
from data_pretreatment.data_handle.updata_stu_cost_count import updataStuCostCount
from data_pretreatment.data_handle.updata_stu_score_count import updataStuScoreCount
from data_pretreatment.data_handle.updata_stu_sleep_count import updataStuSleepCount
from data_pretreatment.common_func.deal_dateortime_func import *
from data_pretreatment.data_orm import *
from data_pretreatment.common_func.deal_data_by_redis import saveData,getValue
saveDataDays=94
def updataAllCount():
    try:
        saveDateStartDate=getBeforeDateTime(saveDataDays)
        logger.info('start updata all count table')
        try:
            saveData('isDeleteFlag', 1)  # 设置开始删除数据标识
            logger.info('start delete data')
            querySleep = entry_and_exit.delete().where(
               (entry_and_exit.exitDate < saveDateStartDate) | (entry_and_exit.entryDate < saveDateStartDate))
            querySleep.execute()
            queryCost = stu_transaction_record.delete().where(stu_transaction_record.tradingTime < saveDateStartDate)
            queryCost.execute()
            saveData('isDeleteFlag', 0)
            logger.info('finish delete data')
        except  Exception as e:
            saveData('isDeleteFlag', 0)
            logger.critical(errorMessage(e))

        try:
            saveData('isUpdataSleepFlag',1)   #开始更新
            updataStuSleepCount()
            saveData('isUpdataSleepFlag',0)   #结束更新
        except Exception as e:
            logger.info('updata stu_sleep_count fail')
            logger.critical(errorMessage(e))

        try:
            saveData('isUpdataCostFlag',1)
            updataStuCostCount()
            saveData('isUpdataCostFlag',0)
        except Exception as e:
            logger.info('updata stu_cost_count fail')
            logger.critical(errorMessage(e))

        try:
            saveData('isUpdataScoreFlag',1)
            updataStuScoreCount()
            saveData('isUpdataScoreFlag',0)
        except Exception as e:
            logger.info('updata stu_score_count fail')
            logger.critical(errorMessage(e))

        logger.info('finish updata all count table')

    except Exception as e:
        logger.info('updata all count table fail')
        logger.critical(errorMessage(e))



