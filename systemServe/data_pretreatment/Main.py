import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_pretreatment.data_handle.update_all_count import updateAllCount
from data_pretreatment.update_mysql import updateMysql
from data_pretreatment.logConfig import logger,errorMessage

if __name__=='__main__':
    try:
        logger.info('开始第一次初始化数据统计')
        updateAllCount()    #若当天数据库数据不完全，导致统计失败，则等到明天才会重新尝试进行数据统计
        logger.info('第一次初始化数据统计完成')
        updateMysql()
    except Exception as e:
        logger.critical(errorMessage(e))
