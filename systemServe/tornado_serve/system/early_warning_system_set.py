#将系统设置保留在本地文件中 systemServe.conf中
from tornado_serve.common.deal_data_by_file import getDictDataFromFile,setDataInFile
from tornado_serve.common.judge_permission import judgeIfPermiss
'''
{
'sessionId':....,
"userId":用户名,
'earlyWarningState':'allOpen'/'halfOpen'/'close'
}
'''
class EarlyWarningSystemSet():
    def entry(self,receiveRequest):
        # self.requestData = receiveRequest
        self.requestData = eval(receiveRequest.request.body)
        userId = self.requestData['userId']
        earlyWarningState = self.requestData['earlyWarningState']

        if judgeIfPermiss(user_id = userId, mode = 1, page = "earlyWarningSet") == False:
            return {"status":0, "errorInfo":"用户没有操作此页面的权限"}

        systemSetting=getDictDataFromFile()
        systemSetting['isOpen']=earlyWarningState
        setDataInFile(str(systemSetting))
        return {'status':1,'info':'操作成功'}
