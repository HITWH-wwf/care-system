
def sleepModel(returnKind,queryKind,resultDate):
    if returnKind=='stuList':
        endColName={'laterReturn':'晚归次数','noReturn':'晚归次数','fixed1':'23：30前未归次数',
                    'fixed2':'24小时内无出入记录次数','fixed3':'23:30-5：00归寝次数'}
        colName=['学号','姓名','专业']
        colName.append(endColName[queryKind])
        resultModel={
            'status':1,
            'colName':colName,
            "propName": ['stuID', 'stuName', 'major', 'times'],
            "tableData":resultDate,
            'info':'请求成功'
        }
        return resultModel
    else:
        if queryKind=='fixed2':
            resultModel={
                "status":1,
                "colName": ['学号','姓名','专业','24小时内无出入记录的日期'],
                "propName":['stuID','stuName','major','happenDate'],
                "tableData": resultDate,
                "info":'请求成功'
            }
            return resultModel
        else:
            resultModel={
                "status": 1,
                "colName": ['学号', '姓名', '公寓', '外出时间', '归寝时间'],
                "propName": ['stuID', 'stuName', 'apartment', 'outTime', 'inTime'],
                "tableData": resultDate,
                "info": '请求成功'
            }
            return resultModel


def costModel(returnKind,queryKind,resultData):
    if returnKind=='stuList':
        resultModel={
                "status":1,
                "colName": ['学号','姓名','专业','出现次数'],
                "propName":['stuID','stuName','major','times'],
                "tableData": resultData,
                "info":'请求成功'
        }
        return resultModel
    else:
        if queryKind=='single':
            resultModel={
                "status": 1,
                "colName": ['学号', '姓名',  '专业', '日期', '符合条件的交易笔数'],
                "propName": ['stuID', 'stuName','major','date', 'times'],
                "tableData":resultData,
                "info": '请求成功'
            }
            return resultModel
        elif  queryKind=='total':
            resultModel = {
                "status": 1,
                "colName": ['学号', '姓名', '专业', '日期', '当日消费总额'],
                "propName": ['stuID', 'stuName', 'major', 'date', 'todayCostSum'],
                "tableData": resultData,
                "info": '请求成功'
            }
            return resultModel
        elif queryKind=='fixed1':
            resultModel={
                "status": 1,
                "colName": ['学号', '姓名', '专业', '现象出现日期'],
                "propName": ['stuID', 'stuName', 'major', 'happenDate'],
                "tableData": resultData,
                "info": '请求成功'
            }
            return resultModel
        else:
            resultModel={
                "status": 1,
                "colName": ['学号', '姓名', '交易时间', '交易金额', '消费场所'],
                "propName": ['stuID', 'stuName', 'tradingTime', 'turnover', 'tradingPlace'],
                "tableData":resultData,
                "info": '请求成功'
            }
            return resultModel

def scoreModel(returnKind,queryKind,resultData):
    if returnKind=='stuList':
        colName=['学号', '姓名', '专业']
        propName=['stuID', 'stuName', 'major']
        endColName = {'failCourse': '不及格科目数', 'totalCredit': '已获得的总学分', 'failCredit': '不及格科目累计学分',
                      'fixed1':'不及格科目数','fixed2':'不及格科目累计学分', 'fixed3': '不及格科目累计学分'}
        endPropName={'failCourse': 'number', 'totalCredit': 'gainTotalCredit', 'failCredit': 'failTotalCredit',
                      'fixed1':'number','fixed2':'failTotalCredit', 'fixed3': 'failTotalCredit'}
        colName.append(endColName[queryKind])
        propName.append(endPropName[queryKind])
        resultModel={
            "status": 1,
            "colName": colName,
            "propName": propName,
            "tableData": resultData,
            "info": '请求成功'
        }
        return resultModel
    else:
        resultModel={
            "status": 1,
            "colName": ['学号', '姓名', '课程名', '成绩', '学分', '考试类型'],
            "propName": ['stuID', 'stuName', 'courseName', 'examScore', 'credit', 'examKind'],
            "tableData": resultData,
            "info": '请求成功'
        }
        return resultModel