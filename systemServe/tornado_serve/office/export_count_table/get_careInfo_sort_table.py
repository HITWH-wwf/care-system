from tornado_serve.office.export_count_table.generate_count_df import GenerateCountDf
from tornado_serve.office.export_count_table.some_setting_info import getJudgeState,getCollegesName,getCareKindList
from tornado_serve.common.judge_permission import judgeIfPermiss
from tornado_serve.common.deal_data_by_redis import getValue

class GetCareInfoSortTable():
    def entry(self,receiveRequest):
        self.requestData = eval(receiveRequest.request.body)
        userName = getValue(self.requestData['sessionId'])
        if userName == None:
            return {'status': 0, 'errorInfo': '登陆状态已过期，请重新登录'}
        elif judgeIfPermiss(user_id=userName, mode=1, page="getCountTable") == False:
            return {"status": 0, "errorInfo": "该用户没有此项操作的权限"}
        else:
            self.stuDf=GenerateCountDf().entry(userName)
            self.judgeState=getJudgeState()
            self.careKindList=getCareKindList()

    def getSortTable(self):
        countResult = []
        collegesName = getCollegesName()
        grades=['大一','大二','大三','大四']
        gradeLineKey=[]
        gradeLineValue=[]
        for i in range(len(grades)):
            oneRecord={grades[i]:len(self.stuDf[self.stuDf['grade']==(i+1)])}
            self.adjustPosition(gradeLineKey,gradeLineValue,oneRecord)
        countResult.append(self.getLastLineResult(gradeLineKey,gradeLineValue))

        collegeLineKey=[]
        collegeLineValue=[]
        for college in collegesName:
            oneRecord={college:len(self.stuDf[self.stuDf['college']==college])}
            self.adjustPosition(collegeLineKey,collegeLineValue,oneRecord)
        countResult.append(self.getLastLineResult(collegeLineKey,collegeLineValue))

        countResult.append(['','','',''])

        for kind in self.careKindList:
            careKindStuDf=self.stuDf[self.stuDf[kind]>0]
            oneLineKey=[]
            oneLineValue=[]
            for college in collegesName:
                oneRecord = {college: len(careKindStuDf[careKindStuDf['college'] == college])}
                self.adjustPosition(oneLineKey, oneLineValue, oneRecord)
            countResult.append(self.getLastLineResult(oneLineKey, oneLineValue))

        countResult.append(['', '', '', ''])

        for oneLevelkind in self.careKindList:  #一级指标进去
            for twoLevelkindState in self.judgeState[oneLevelkind]: #一级指标下各种二级指标对应的state值
                careKindStuDf = self.stuDf[self.stuDf[oneLevelkind].isin(twoLevelkindState)]    #获取符合条件的全部学生
                oneLineKey=[]
                oneLineValue=[]
                for college in collegesName:    #按学院进行统计
                    oneRecord = {college: len(careKindStuDf[careKindStuDf['college'] == college])}
                    self.adjustPosition(oneLineKey, oneLineValue, oneRecord)
                countResult.append(self.getLastLineResult(oneLineKey, oneLineValue))    #一种二级指标为一行

        return countResult


    def adjustPosition(self,oneLineKey,oneLineValue,oneRecord):
        judgeFlag=0
        for k,v in oneRecord.items():
            for i in range(len(oneLineValue)):
                judgeFlag=1
                if oneLineValue[i]<v:
                    oneLineValue.insert(i,v)
                    oneLineKey.insert(i,k)
                    break
            else:
                if judgeFlag==0:
                    oneLineKey.append(k)
                    oneLineValue.append(v)
                else:
                    oneLineValue.insert(i+1, v)
                    oneLineKey.insert(i+1, k)

    def getLastLineResult(self,oneLineKey,oneLineValue):
        oneLine=[]
        for i in range(4):
            oneCol=oneLineKey[i]+str(oneLineValue[i])+'人'
            oneLine.append(oneCol)
        return oneLine

