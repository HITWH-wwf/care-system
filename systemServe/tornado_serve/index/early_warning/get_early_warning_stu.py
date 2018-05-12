from tornado_serve.orm import *
from tornado_serve.common.judge_permission import judgeIfPermiss
from tornado_serve.common.get_class_or_stu_by_user import getClassOrStuByUser
import pandas as pd
from tornado_serve.common.deal_data_by_redis import getFlagValue
'''
{
'sessionId':....,
"userId":用户名
}

响应：
{
    "status":1,
    "colName": [
            列名的value，如：
             学号，姓名，专业,统计日期,预警类型
        ],
    "propName": [
            列名对应的key值，如：
            "stuId","stuName","major",'countDate','earlyWarningKind'

        ],
    "tableData": [{....,,'rank':'red/blue/yellow/orange'},{},....],
    "info":'请求成功'
    }

'''

class GetEarlyWarningStu():
    def entry(self,receiveRequest):
        # self.requestData = receiveRequest
        self.requestData = eval(receiveRequest.request.body)
        userId = self.requestData['userId']
        if judgeIfPermiss(user_id=userId, mode=1, page="earlyWarning") == False:
            return {"status": 0, "errorInfo": "用户没有操作此页面的权限"}
        else:
            inRoleStu = getClassOrStuByUser(self.requestData['userId'], 1)
            self.inRoleStuDf = pd.DataFrame(inRoleStu)
            self.selectStuIds = list(self.inRoleStuDf['stuID'])
            self.someStateResultDf = pd.DataFrame(MyBaseModel.returnList(
                stu_some_state.select(stu_some_state.stuID,stu_some_state.lastTimeCountDate,stu_some_state.earlyWarningInfo).where(
                    stu_some_state.stuID.in_(self.selectStuIds))))

            self.someStateResultDf.dropna(axis=1, inplace=True)
            return self.getResultData()

    def getResultData(self):
        self.inRoleStuDf.index=self.inRoleStuDf['stuID']
        self.someStateResultDf.index=self.someStateResultDf['stuID']
        stuBasicInfo=self.inRoleStuDf.to_dict('index')
        stuStateInfo=self.someStateResultDf.to_dict('index')
        for stuId in stuStateInfo.keys():
            stuStateInfo[stuId]['earlyWarningInfo']=eval(stuStateInfo[stuId]['earlyWarningInfo'])
        warningKind = {
            'costWarning': '消费预警', 'sleepWarning': '住宿预警', 'scoreWarning': '学业预警', 'have': '综合预警','no':'正常'
        }
        warningLevel={'costWarning':1, 'sleepWarning':1, 'scoreWarning':1, 'have':2,'no':0}
        warningColorKeys={'costWarning': 'costColor', 'sleepWarning': 'sleepColor', 'scoreWarning': 'scoreColor', 'have': 'aboveOneColor','no':'aboveOneColor'}
        tableData=[]
        for stuId in self.selectStuIds:
            oneStu=stuBasicInfo[stuId]
            oneStu['countDate']=stuStateInfo[stuId]['lastTimeCountDate']
            stuStateInfo[stuId]=stuStateInfo[stuId]['earlyWarningInfo']
            oneStu['earlyWarningKind']=warningKind[stuStateInfo[stuId]['aboveOneWarning']]
            colorKey=warningColorKeys[stuStateInfo[stuId]['aboveOneWarning']]
            oneStu['rank']=stuStateInfo[stuId][colorKey]
            oneStu['warningLevel']=warningLevel[stuStateInfo[stuId]['aboveOneWarning']]
            tableData.append(oneStu)

        tableDataDf=pd.DataFrame(tableData)
        tableDataDf.sort_values(['warningLevel'],ascending=False,inplace=True)
        tableData=tableDataDf.to_dict('record')
        if getFlagValue('isUpdateStateFlag')=='2':
            resultData = {
                "status": 2,
                "colName": ['学号', '姓名', '专业', '统计日期', '预警类型'],
                "propName": ["stuID", "stuName", "major", 'countDate', 'earlyWarningKind'],
                "tableData": tableData,
                "info": '最新的预警名单更新失败，请联系管理员'
            }
        else:
            resultData={
                "status":1,
                "colName": ['学号','姓名','专业','统计日期','预警类型'],
                "propName": ["stuID","stuName","major",'countDate','earlyWarningKind'],
                "tableData": tableData,
                "info":'请求成功'
                }
        return resultData