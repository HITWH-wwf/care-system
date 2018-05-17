from tornado_serve.orm import MyBaseModel,stu_all_aspect_info,stu_some_state,db
from tornado_serve.common.deal_dateortime_func import intChangeToDateTimeStr
from tornado_serve.common.deal_data_by_redis import getValue
from tornado_serve.common.judge_permission import judgeIfPermiss
from tornado_serve.common.get_class_or_stu_by_user import getClassOrStuByUser
from tornado_serve.common.deal_dateortime_func import dateTimeChangeToIntWithTime
from datetime import datetime
import pandas as pd
class GetPersonStudyCareInfo(object):
    def entry(self,receiveRequest):
        self.requestData = eval(receiveRequest.request.body)
        userName = getValue(self.requestData['sessionId'])
        # self.requestData = receiveRequest
        stuId=self.requestData['stuId']
        # userName='wangjianting'
        if userName == None:
            return {'status': 0, 'errorInfo': '登陆状态已过期，请重新登录'}
        elif judgeIfPermiss(user_id=userName, mode=1, page="personStudyInfo") == False:
            return {"status": 0, "errorInfo": "用户没有操作此页面的权限"}
        elif judgeIfPermiss(user_id = userName, stuid = stuId, mode = 0) == False:
            return {"status":0, "errorInfo":"用户没有操作该学生的权限"}
        else:
            thisStu=MyBaseModel.returnList(stu_all_aspect_info.select().where(stu_all_aspect_info.stuID==stuId))
            if len(thisStu)==0:
                thisStu=self.createOneNewRecord(stuId)
            else:
                thisStu = thisStu[0]

            inRoleStu = getClassOrStuByUser(userName, 1)
            self.inRoleStuDf = pd.DataFrame(inRoleStu)
            thisStuBasicInfo=self.inRoleStuDf[self.inRoleStuDf['stuID'] == stuId].to_dict('record')
            if len(thisStuBasicInfo)==0:
                return {'status': 0, 'errorInfo': '该学生不存在或您无权限查看'}

            stuStateInfo=['正常','学情关注','修改未提交','取消未通过','关注未通过','取消待审核','关注待审核']
            thisStu['stuState']=stuStateInfo[thisStu['stuState']]
            thisStu['latelyEditTime']=intChangeToDateTimeStr(thisStu['latelyEditTime'])
            thisStuBasicInfo=thisStuBasicInfo[0]
            fudaoyuanActions=eval(thisStu['fudaoyuan'])
            fushujiToExamines=eval(thisStu['fushuji'])

            if len(fudaoyuanActions)==0:    #若没有记录，传什么？？？？？
                pass
            else:
                thisStu['fudaoyuan']=fudaoyuanActions[0]

            if len(fushujiToExamines)==0:
                pass
            else:
                thisStu['fushuji']=fushujiToExamines[0]


            for k,v in thisStuBasicInfo.items():
                thisStu[k]=v

            thisStu['earlyWarningHistory']=self.getEarlyWarningCount(stuId)

            return {
                'status': 1, 'info': '操作成功', 'data': thisStu
            }




    def getEarlyWarningCount(self,stuId):
        warningKind = {
            'costWarning': '消费预警', 'sleepWarning': '住宿预警', 'scoreWarning': '学业预警', 'aboveOne': '综合预警'
        }
        oneStu=MyBaseModel.returnList(stu_some_state.select(stu_some_state.warningHistory).where(stu_some_state.stuID==stuId))
        if len(oneStu)==0:
            return {'status':0,'errorInfo':'未查询到该学生'}

        stuWarningHistory=oneStu[0]['warningHistory']
        stuWarningHistory=eval(stuWarningHistory)
        stuWarningHistoryDf=pd.DataFrame(stuWarningHistory)
        earlyWarningCount={}
        for k,v in warningKind.items():
            earlyWarningCount[v]=len(stuWarningHistoryDf[stuWarningHistoryDf['warningKind']==k])

        earlyWarningCountStr='发生预警情况的统计结果为：'
        for k,v in earlyWarningCount.items():
            earlyWarningCountStr=earlyWarningCountStr+k+'：'+str(v)+'次 '

        return earlyWarningCountStr

    def createOneNewRecord(self,stuId):
        oneStu={
            'stuID':stuId,
            'studyInfo':{'type':[],'remarks':''},
            'thoughtInfo':{'type':[],'remarks':''},
            'economyInfo':{'type':'','nowState':'','remarks':''},
            'bodyInfo':{'type':'','remarks':''},
            'networkInfo':{'type':'','remarks':''},
            'sleepInfo':{'type':'','liveWithInfo':'','remarks':''},
            'burstInfo':{'type':[],'remarks':''},
            'peopleInfo':{'type':'','remarks':''},
            'mentalityInfo':{'type':'','remarks':''},
            'gayInfo':{'type':'','remarks':''},
            'familyInfo':{'type':'','remarks':''},
            'otherInfo':{'type':'','remarks':''},
            'fudaoyuan':'[]',  # 初始化为[]
            'fushuji':'[]',  # 初始化为[]
            'stuState':0,
            'latelyEditTime': dateTimeChangeToIntWithTime(datetime.now())
            }
        with db.execution_context():
            stu_all_aspect_info.create(**oneStu)

        return oneStu