from tornado_serve.office.export_count_table.generate_count_df import GenerateCountDf
from tornado_serve.office.export_count_table.some_setting_info import getJudgeState,getCollegesName,getCareKindList
from tornado_serve.common.judge_permission import judgeIfPermiss
from tornado_serve.common.deal_data_by_redis import getValue
import pandas as pd
class GetCareInfoCountTable():
    def entry(self,receiveRequest):
        self.requestData = eval(receiveRequest.request.body)
        userName = getValue(self.requestData['sessionId'])
        tableKind=self.requestData['tableKind']

        # self.requestData=receiveRequest
        # userName='wangjianting'
        if userName == None:
            return {'status': 0, 'errorInfo': '登陆状态已过期，请重新登录'}
        elif judgeIfPermiss(user_id=userName, mode=1, page="getCountTable") == False:
            return {"status": 0, "errorInfo": "该用户没有此项操作的权限"}
        else:
            self.stuDf=GenerateCountDf().entry(userName)
            self.judgeState=getJudgeState()
            self.careKindList=getCareKindList()
            if tableKind=='countByGrade':
                return self.countTableByGrade()
            elif tableKind=='countByCollege':
                return self.countTableByCollege()
            else:
                return {"status": 0, "errorInfo": "参数错误"}

    def countTableByGrade(self):
        countResult=[]
        for i in range(1,5):
            oneLine=[]
            gradeStuDf=self.stuDf[self.stuDf['grade']==i]
            for kind in self.careKindList:
                for oneCol in self.judgeState[kind]:
                    oneLine.append(len(gradeStuDf[gradeStuDf[kind].isin(oneCol)]))

        return countResult


    def countTableByCollege(self):
        collegesName=getCollegesName()
        countResult=[]
        for college in collegesName:
            oneLine = []
            collegeStuDf = self.stuDf[self.stuDf['college'] == college]
            for kind in self.careKindList:
                for oneCol in self.judgeState[kind]:
                    oneLine.append(len(collegeStuDf[collegeStuDf[kind].isin(oneCol)]))

        return countResult


