#将系统设置保留在本地文件中 systemServe.conf中
from tornado_serve.common.deal_data_by_file import getDictDataFromFile,setDataInFile
'''
{
'sessionId':....,
"userId":用户名,
'earlyWarningState':'allOpen'/'halfOpen'/'close'
}
'''
class EarlyWarningSystemSet():
    def entry(self):
        pass
