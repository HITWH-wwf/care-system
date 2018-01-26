from tornado_serve.orm import *
from tornado_serve.common.get_class_or_stu_by_user import getClassOrStuByUser
from tornado_serve.office.stu_data_filter.return_model import scoreModel
import pandas as pd
from tornado_serve.common.deal_data_by_redis import getValue
class GetStuByScoreFixed():
    def entry(self,receiveRequest):
        self.requestData = eval(receiveRequest.request.body)
        self.failNum=3
        self.failCreditMin=16
        self.failCreditMax=20
        #3,16,20
        # self.requestData = receiveRequest
        self.resultDf = None
        userName=getValue(self.requestData['sessionId'])
        if userName==None:
            return {'status':0,'errorInfo':'登陆状态已过期，请重新登录'}

        self.getStuResultByQueryKind(self.requestData['queryKind'])

        if len(self.resultDf)==0:
            return {'status': 0, 'errorInfo': '未查询到相关学生'}
        return self.getLastResultByReturnKind(self.requestData['returnKind'],self.requestData['queryKind'])

    def getStuResultByQueryKind(self,queryKind):
        inRoleStu = getClassOrStuByUser(self.requestData['userId'], 1)
        inRoleStuDf = pd.DataFrame(inRoleStu)
        inRoleStuId = list(inRoleStuDf['stuID'])
        scoreCountResult = pd.DataFrame(MyBaseModel.returnList(
            stu_score_count.select(stu_score_count.stuID, stu_score_count.scoreCountInfo).where(
                stu_score_count.stuID.in_(inRoleStuId))))
        scoreCountResult.index = scoreCountResult['stuID']
        scoreCountResult = scoreCountResult['scoreCountInfo'].to_dict()
        self.resultDf = pd.DataFrame([eval(line) for line in scoreCountResult.values()], index=scoreCountResult.keys())

        if queryKind=='fixed1':
            self.resultDf=self.resultDf[self.resultDf['failNum']>self.failNum]
        elif queryKind=='fixed2':
            self.resultDf=self.resultDf[(self.resultDf['failCredit']>=self.failCreditMin)&(self.resultDf['failCredit']<=self.failCreditMax)]
        else:
            self.resultDf = self.resultDf[self.resultDf['failCredit']>self.failCreditMax]

    def getLastResultByReturnKind(self,returnKind,queryKind):
        if len(self.resultDf) == 0:
            return scoreModel(returnKind, queryKind, [])
        if returnKind=='stuRecord':
            allFailIdList = list(self.resultDf['failId'])
            allFailId = []
            for line in allFailIdList:
                allFailId = allFailId + line

            self.resultDf = pd.DataFrame(MyBaseModel.returnList(
                    exam_results.select(exam_results.stuID, exam_results.stuName, exam_results.courseName,
                    exam_results.credit, exam_results.examKind, exam_results.examScore,
                    exam_results.courseID).where(exam_results.id.in_(allFailId))))

            self.resultDf.dropna(axis=1, inplace=True)
            resultData = self.resultDf.to_dict("report")
            return scoreModel('stuRecord', 'queryScore', resultData)

        else:
            inRoleStu = getClassOrStuByUser(self.requestData['userId'], 1)
            inRoleStuDf = pd.DataFrame(inRoleStu)
            inRoleStuDf.index=inRoleStuDf['stuID']
            inRoleStuList=inRoleStuDf.to_dict('index')
            # self.resultDf.index = self.resultDf['stuID']
            if queryKind=='fixed1':
                tempResult = self.resultDf['failNum'].to_dict()
                resultData = []
                for stu in tempResult.keys():
                    oneStu = inRoleStuList[stu]
                    oneStu['failNum'] = int(tempResult[stu])
                    resultData.append(oneStu)
            else:
                tempResult = self.resultDf['failCredit'].to_dict()
                resultData = []
                for stu in tempResult.keys():
                    oneStu = inRoleStuList[stu]
                    oneStu['failCredit'] = float(tempResult[stu])
                    resultData.append(oneStu)

            return scoreModel('stuList', queryKind, resultData)
