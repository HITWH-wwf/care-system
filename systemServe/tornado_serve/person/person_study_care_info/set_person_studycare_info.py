from tornado_serve.orm import MyBaseModel,stu_all_aspect_info,db,stu_basic_info
from tornado_serve.common.deal_dateortime_func import dateTimeChangeToIntWithTime
from tornado_serve.common.deal_data_by_redis import getValue
from tornado_serve.common.judge_permission import judgeIfPermiss
from datetime import datetime

class SetPersonStudyCareInfo(object):
    def entry(self,receiveRequest):
        self.requestData = eval(receiveRequest.request.body)
        # self.requestData=receiveRequest
        userName = getValue(self.requestData['sessionId'])
        stuId=self.requestData['stuId']
        # userName='wangjianting'
        if userName == None:
            return {'status': 0, 'errorInfo': '登陆状态已过期，请重新登录'}
        elif judgeIfPermiss(user_id = userName, stuid = stuId, mode = 0) == False:
            return {"status":0, "errorInfo":"用户没有操作该学生的权限"}
        else:
            operate=self.requestData['operate']
            judgeFlag=self.judgeOperateRole(userName,operate)
            if judgeFlag['status']==0:
                return judgeFlag
            return self.setStudyCareInfo(stuId,operate)

    def judgeOperateRole(self,userName,operate):
        studyInfoEditRole=['save','submitAdd','submitCancel']
        toExamineEdit=['checkPass','checkRefuse']
        if operate in studyInfoEditRole:
            if judgeIfPermiss(user_id=userName, mode=1, page="studyInfoEdit") == False:
                return {"status": 0, "errorInfo": "当前用户没有进行此项操作的权限"}
            else:
                return {'status':1}
        elif operate in toExamineEdit:
            if judgeIfPermiss(user_id=userName, mode=1, page="toExamineEdit") == False:
                return {"status": 0, "errorInfo": "当前用户没有进行此项操作的权限"}
            else:
                return {'status':1}

    def setStudyCareInfo(self,stuId,operate):
        thisStu=MyBaseModel.returnList(stu_all_aspect_info.select(stu_all_aspect_info.stuID,stu_all_aspect_info.stuState).where(stu_all_aspect_info.stuID==stuId))
        newStudyCareInfo={
            'studyInfo' : self.requestData['studyInfo'],
            'thoughtInfo' :self.requestData['thoughtInfo'],
            'economyInfo' : self.requestData['economyInfo'],
            'bodyInfo' :self.requestData['bodyInfo'],
            'networkInfo' :self.requestData['networkInfo'],
            'sleepInfo' : self.requestData['sleepInfo'],
            'burstInfo' : self.requestData['burstInfo'],
            'peopleInfo' : self.requestData['peopleInfo'],
            'mentalityInfo' : self.requestData['mentalityInfo'],
            'gayInfo' :self.requestData['gayInfo'],
            'familyInfo' : self.requestData['familyInfo'],
            'otherInfo' : self.requestData['otherInfo'],
            'latelyEditTime':dateTimeChangeToIntWithTime(datetime.now())
            }

        thisStu = thisStu[0]
        thisStuBasic=MyBaseModel.returnList(stu_basic_info.select(stu_basic_info.state).where(stu_basic_info.stuID==stuId))
        thisStuBasic=thisStuBasic[0]
        stuData = {"state": thisStuBasic["state"]} #'focusColor': 'blue'
        operateFlag=0
        if operate == 'submitAdd':
            if stuData['state'] == 0:
                newStudyCareInfo['stuState'] = 6  # 关注待审核
            elif stuData['state'] == 1:
                operateFlag=1
            else:
                operateFlag = 2

        elif operate == 'submitCancel':
            if stuData['state'] == 1:
                newStudyCareInfo['stuState'] = 5  # 取消待审核
            else:
                operateFlag = 3 #未处于关注状态，发起取消关注


        elif operate == 'checkPass':
            if thisStu['stuState'] == 6:
                stuData['focusColor']='yellow'
                stuData['state']=1
                newStudyCareInfo['stuState'] = 1  # 关注  学情关注对应的学生基本表中state值等于1

            elif thisStu['stuState'] == 5:
                stuData['state']=0
                stuData['focusColor'] = 'blue'
                newStudyCareInfo['stuState'] = 0  # 取消关注
            else:
                operateFlag=4   #当前没有任何审核申请

        elif operate == 'checkRefuse':
            if thisStu['stuState'] == 6:
                newStudyCareInfo['stuState'] = 4  # 关注未通过

            elif thisStu['stuState'] == 5:
                newStudyCareInfo['stuState'] = 3  # 取消未通过
            else:
                operateFlag = 4

        with db.execution_context():
            stu_all_aspect_info.update(**newStudyCareInfo).where(stu_all_aspect_info.stuID == stuId).execute()
            stu_basic_info.update(**stuData).where(stu_basic_info.stuID == stuId).execute()

        if operateFlag==2:
            return {'status':0,'errorInfo':'操作失败，该学生已经处于其他的关注状态，无法发起添加为学情关注申请'}
        elif operateFlag==3:
            return {'status': 0, 'errorInfo': '操作失败，该学生未处于学情关注状态，无法发起取消关注申请'}
        elif operateFlag==4:
            return {'status': 0, 'errorInfo': '操作失败，该学生无任何审核申请'}
        elif operateFlag==1:
            return {'status': 0, 'errorInfo': '操作失败，该学生已经处于学情关注状态，请勿重复申请'}
        else:
            return {'status':1,'info':'操作成功'}
