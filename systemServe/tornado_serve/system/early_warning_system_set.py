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
        if judgeIfPermiss(user_id = userId, mode = 1, page = "earlyWarningSet") == False:
            return {"status":0, "errorInfo":"用户没有操作此页面的权限"}

        earlyWarningState = self.requestData['earlyWarningState']
        costWarningSetting=self.requestData['costWarning']
        sleepWarningSetting=self.requestData['sleepWarning']
        scoreWarningSetting=self.requestData['scoreWarning']

        systemSetting=getDictDataFromFile()
        systemSetting['isOpen']=earlyWarningState
        systemSetting['costWarning']=costWarningSetting
        systemSetting['sleepWarning']=sleepWarningSetting
        systemSetting['scoreWarning']=scoreWarningSetting

        setDataInFile(str(systemSetting))
        return {'status':1,'info':'操作成功'}
