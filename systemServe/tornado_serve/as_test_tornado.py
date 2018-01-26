
from orm import *
# stuList=['150410218','150410219']
# print(MyBaseModel.returnList(stu_basic_info.select(stu_basic_info.stuName).where(stu_basic_info.stuID.in_(stuList))))

# from tornado_serve.common.get_class_or_stu_by_user import getClassOrStuByUser
import pandas as pd
# drop(['winter'],axis=1,inplace=True)
# odata.drop(odata.index[[16,17]],inplace=True)

# from tornado_serve.office.stu_data_filter.get_exam_result import GetExamResult
# request={   "userId":"wangjianting",
#     "returnKind":'stuRecord',
#     'stuRange':{'rangeKind':'useClassId','rangeData':['1504102','1504103']}, #若按班级，参数为列表；按其余两个，参数为字符串
#     'courseRange':'all',    #若未选择，值设为 'all'
# }
# print(GetExamResult().entry(request))
# df=pd.DataFrame(MyBaseModel.returnList(exam_results.select(exam_results.stuID,exam_results.stuName)))
# df.dropna(axis=1,inplace=True)    #删除值为空的列
# print(df)
# with db.execution_context():
#     s=exam_results.select()
#     for line in s:
#         line.stuClass=line.stuClass.replace('.0','')
#         print(line.stuClass)
#         line.save()


# df.drop(['a','b'],axis=1,inplace=True)
# print(df)
# scoreCountResult = pd.DataFrame(MyBaseModel.returnList(stu_score_count.select(stu_score_count.scoreCountInfo).where(
#     stu_score_count.stuID == '150410218')))
# scoreCountResult = scoreCountResult['scoreCountInfo'].to_dict()
# print(scoreCountResult)

# from tornado_serve.office.stu_data_filter.get_stu_by_score_free import GetStuByScoreFree
# request={  "userId":"wangjianting",
#     "returnKind":'stuList',   #若为成绩查询，此值强制设为'stuRecord'
#     'stuRange':{'rangeKind':'useStuName','rangeData':'刘鹏飞'}, #若按班级，参数为列表；按其余两个，参数为字符串
#     'courseRange':{'rangeKind':'courseNum','rangeData':'GN06000101'},    #若未选择，值设为 'all'
#     'countKind':'failCourse',    #若上面不是选择全部课程，这个强制设为failCourse，，min与max设为1！！！！！
#     'countRange':{'min':0,'max':11}
# }
# print(GetStuByScoreFree().entry(request))

# from tornado_serve.common.deal_data_by_redis import saveData
# from tornado_serve.office.stu_data_filter.get_stu_by_score_fixed import GetStuByScoreFixed
# saveData('123','wangjianting')
# request={
#     "userId":"wangjianting",
#     "returnKind":'stuList',   #若为成绩查询，此值强制设为'stuRecord'
#     "sessionId":'123',   #sessionId为登录的时候返回给前端的那个字符串
#     'queryKind':'fixed1',    #int型
#
# }
# print(GetStuByScoreFixed().entry(request))
# import time
# s=time.time()
# sleepCountResult=pd.DataFrame(MyBaseModel.returnList(stu_sleep_count.select(stu_sleep_count.stuID,stu_sleep_count.freeQueryCountInfo).where(
#                             stu_sleep_count.stuID.in_(['150410218','150410219']))))
# sleepCountResult.index = sleepCountResult['stuID']
# sleepCountResult = sleepCountResult['freeQueryCountInfo'].to_dict()
# for key in sleepCountResult.keys():
#     sleepCountResult[key]=eval(sleepCountResult[key])
#     print(sleepCountResult[key][1])
# # resultDf = pd.DataFrame([eval(line) for line in sleepCountResult.values()], index=sleepCountResult.keys())
# print(time.time()-s)

# from tornado_serve.office.stu_data_filter.get_stu_by_sleep_free import GetStuBySleepFree
# request={   "userId":"wangjianting",
#     "returnKind":'stuRecord',
#     'stuRange':{'rangeKind':'useClassId','rangeData':['1504102','1504101','1504102']}, #若按班级，参数为列表；按其余两个，参数为字符串
#     'dateRange':{'startDate':'2017-10-01','endDate':'2018-01-18'},  #若用户未选择，则设为默认值，startDate=endDate='threeMonth'/startDate和endDate=具体的间隔3个月的日期，看你方便哪种，不过记得跟我说
#     'countKind':'laterReturn',
#     'appearTimes':{'minTimes':1,'maxTimes':100},  #若用户未选择，令appearTimes=1
# }
# s=GetStuBySleepFree().entry(request)
# s=pd.DataFrame(s['tableData'])
# print(s)
# print(s[s['stuID']=='150410218'])

#
# from tornado_serve.common.deal_data_by_redis import saveData
# saveData('123','wangjianting')
# from tornado_serve.office.stu_data_filter.get_stu_by_sleep_fixed import GetStuBySleepFixed
# request={
#     "userId":"wangjianting",
#     "returnKind":'stuRecord',   #若为成绩查询，此值强制设为'stuRecord'
#     "sessionId":'123',   #sessionId为登录的时候返回给前端的那个字符串
#     'queryKind':'fixed3',    #int型
#
# }
# s=GetStuBySleepFixed().entry(request)
# s=pd.DataFrame(s['tableData'])
# print(s)
# print(s[s['stuID']=='150410218'])

# from tornado_serve.office.stu_data_filter.get_stu_by_cost_free import GetStuByCostFree
# requestData={
#     "userId":"wangjianting",
#     "returnKind":'stuRecord',
#     'stuRange':{'rangeKind':'useClassId','rangeData':['1504102','1504103']}, #若按班级，参数为列表；按其余两个，参数为字符串
#     'dateRange':{'startDate':'2017-11-01','endDate':'2018-01-17'},  #若用户未选择，则设为默认值，startDate=endDate='threeMonth'/startDate和endDate=具体的间隔3个月的日期，看你方便哪种，不过记得跟我说
#     'moneyRange':{'minMoney':50,'maxMoney':100},
#     'countKind':'single'
# }
# s=GetStuByCostFree().entry(requestData)
# print(pd.DataFrame(s['tableData']))
#
# from tornado_serve.office.stu_data_filter.get_stu_by_cost_fixed import GetStuByCostFixed
# from tornado_serve.common.deal_data_by_redis import saveData
# saveData('123','wangjianting')
# requestData={
#     "userId":'wangjianting',
#     "returnKind":'stuRecord',   #若为成绩查询，此值强制设为'stuRecord'
#     "sessionId":'123',   #sessionId为登录的时候返回给前端的那个字符串
#     'queryKind':'fixed2',
# }
# s=GetStuByCostFixed().entry(requestData)
# s=pd.DataFrame(s['tableData'])
# print(s)
# print(s[s['stuID']=='150410219'])
a=pd.DataFrame([{'id':3,'flag':0},{'id':5,'flag':1}])
a=a[a['flag']==2]
print(len(a))
print(sum(a['flag']))
