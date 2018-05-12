from data_pretreatment.logConfig import logger,errorMessage
from data_pretreatment.data_handle.update_stu_cost_count import updateStuCostCount
from data_pretreatment.data_handle.update_stu_score_count import updateStuScoreCount
from data_pretreatment.data_handle.update_stu_sleep_count import updateStuSleepCount
from data_pretreatment.data_handle.update_stu_some_state import initializeTable,updateState
from data_pretreatment.common_func.deal_dateortime_func import *
from data_pretreatment.data_orm import *
from data_pretreatment.common_func.deal_data_by_redis import saveData,getValue,getFlagValueInt
saveDataDays=131
def updateAllCount():
    try:
        saveDateStartDate=getBeforeDateTime(saveDataDays)
        logger.info('start update all count table')
        try:
            saveData('isDeleteFlag', 1)  # 设置开始删除数据标识
            logger.info('start delete data')
            with db_data.execution_context():
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
            saveData('isUpdateSleepFlag',1)   #开始更新
            updateStuSleepCount()
            saveData('isUpdateSleepFlag',0)   #结束更新
        except Exception as e:
            logger.info('update stu_sleep_count fail')
            logger.critical(errorMessage(e))

        try:
            saveData('isUpdateCostFlag',1)
            updateStuCostCount()
            saveData('isUpdateCostFlag',0)
        except Exception as e:
            logger.info('update stu_cost_count fail')
            logger.critical(errorMessage(e))

        try:
            saveData('isUpdateScoreFlag',1)
            updateStuScoreCount()
            saveData('isUpdateScoreFlag',0)
        except Exception as e:
            logger.info('update stu_score_count fail')
            logger.critical(errorMessage(e))

        try:
            isUpdateSleepFlagInt = getFlagValueInt('isUpdateSleepFlag')
            isUpdateCostFlagInt=getFlagValueInt('isUpdateCostFlag')
            isUpdateScoreFlagInt=getFlagValueInt('isUpdateScoreFlag')
            sumFlagInt=isUpdateCostFlagInt+isUpdateScoreFlagInt+isUpdateSleepFlagInt
            if sumFlagInt!=0:
                saveData('isUpdateStateFlag',2)     #前面的数据统计阶段出错，跳过今天的预警统计
                b=int('a')
            saveData('isUpdateStateFlag',1)   #开始更新
            initializeTable()
            updateState()
            saveData('isUpdateStateFlag',0)   #结束更新
        except Exception as e:
            logger.info('update stu_some_state fail')
            logger.critical(errorMessage(e))

        logger.info('finish update all count table')

    except Exception as e:
        logger.info('update all count table fail')
        logger.critical(errorMessage(e))



