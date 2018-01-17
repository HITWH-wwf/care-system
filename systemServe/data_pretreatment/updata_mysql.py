import time
from datetime import datetime

from data_pretreatment.data_handle.updata_all_count import updataAllCount
from data_pretreatment.logConfig import logger,errorMessage


def updataMysql():
    try:
        nowdate=datetime.today().date()
        while True:
            if nowdate!=datetime.today().date():    #到了新的一天了
                if int(time.strftime("%H%M%S"))>10000:  #凌晨一点开始更新
                    updataAllCount()
                    nowdate=datetime.today().date() #日期更新为今天
            time.sleep(1800)    #每次循环间隔半小时
    except Exception as e:
        # _, reason, exc_tb = sys.exc_info()
        # error = traceback.extract_tb(exc_tb)
        # result = error[len(error) - 1]
        # message = ("file: %s--line: %s--errorfunc: %s()--reason: %s" % (result[0], result[1], result[2], reason))
        logger.critical(errorMessage(e))
