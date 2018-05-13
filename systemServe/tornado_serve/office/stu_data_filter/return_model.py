import json

def sleepModel(returnKind,queryKind,resultData):
    if len(resultData)>3000:
        resultData=resultData[0:3000]
    if returnKind=='stuList':
        endColName={'laterReturn':'晚归次数','noReturn':'未归次数','fixed1':'23：30前未归次数',
                    'fixed2':'24小时内无出入记录次数','fixed3':'23:30-5：00归寝次数'}
        colName=['学号','姓名','专业']
        colName.append(endColName[queryKind])
        resultModel={
            'status':1,
            'colName':colName,
            "propName": ['stuID', 'stuName', 'major', 'times'],
            "tableData":resultData,
            'info':'请求成功'
        }
        return resultModel
    else:
        if queryKind=='fixed2':
            resultModel={
                "status":1,
                "colName": ['学号','姓名','专业','24小时内无出入记录的日期'],
                "propName":['stuID','stuName','major','happenDate'],
                "tableData": resultData,
                "info":'请求成功'
            }
            return resultModel
        else:
            resultModel={
                "status": 1,
                "colName": ['学号', '姓名', '公寓', '外出时间', '归寝时间'],
                "propName": ['stuID', 'stuName', 'apartmentNumber', 'exitDate', 'entryDate'],
                "tableData": resultData,
                "info": '请求成功'
            }
            return resultModel


def costModel(returnKind,queryKind,resultData):
    if len(resultData)>3000:
        resultData=resultData[0:3000]
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
                "propName": ['stuID', 'stuName', 'tradingTime', 'turnover', 'merchantAccount'],
                "tableData":resultData,
                "info": '请求成功'
            }
            return resultModel

def scoreModel(returnKind,queryKind,resultData):
    if len(resultData)>3000:
        resultData=resultData[0:3000]
    if returnKind=='stuList':
        colName=['学号', '姓名', '专业']
        propName=['stuID', 'stuName', 'major']
        endColName = {'failCourse': '不及格科目数', 'totalCredit': '已获得的总学分', 'failCredit': '不及格科目累计学分',
                      'fixed1':'不及格科目数','fixed2':'不及格科目累计学分', 'fixed3': '不及格科目累计学分'}
        endPropName={'failCourse': 'failNum', 'totalCredit': 'gainTotalCredit', 'failCredit': 'failCredit',
                      'fixed1':'failNum','fixed2':'failCredit', 'fixed3': 'failCredit'}
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


def combineModel(resultData):
    resultModel = {
        "status": 1,
        "colName": ['学号', '姓名','班级','专业'],
        "propName": ['stuID', 'stuName', 'stuClassNumber', 'major'],
        "tableData": resultData,
        "info": '请求成功'
    }
    return resultModel

def studyInfoModel(resultData):
    resultModel = {
        "status": 1,
        "colName": ['学号', '姓名','班级','专业','出现所选学情个数'],
        "propName": ['stuID', 'stuName', 'stuClassNumber', 'major','appearKinds'],
        "tableData": resultData,
        "info": '请求成功'
    }
    return resultModel
