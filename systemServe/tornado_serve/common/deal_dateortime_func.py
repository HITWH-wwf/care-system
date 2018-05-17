from datetime import datetime,timedelta

oneDay=timedelta(days=1)

def strChangeToDateTime(strDate,strTime=None):     #strDate格式：'2010-01-01',strTime格式：'23:00:00'
    dateList = strDate.split('-')
    if strTime==None:
        resultDateTime = datetime(int(dateList[0]), int(dateList[1]), int(dateList[2]))
    else:
        timeList=strTime.split(':')
        resultDateTime = datetime(int(dateList[0]), int(dateList[1]), int(dateList[2]),int(timeList[0]),
                                  int(timeList[1]),int(timeList[2]))
    return resultDateTime


def intChangeToDateTime(inputInt):
    resultDateTime=datetime(inputInt//10000,(inputInt%10000)//100,inputInt%100)
    return resultDateTime

def intChangeToDateStr(inputInt):
    inputInt=int(inputInt)
    resultDateTime=datetime(inputInt//10000,(inputInt%10000)//100,inputInt%100)
    return str(resultDateTime.date())

def strDateTimeChangeToInt(inputStr):
    dateList = inputStr.split('-')
    resultInt = int(dateList[0]) * 10000 + int(dateList[1]) * 100 + int(dateList[2])
    return resultInt


def getBeforeDateTime(distanceDay,nowDate=None):     #默认是求今天的前几天的日期
    if nowDate==None:
        nowDate=strChangeToDateTime(str(datetime.today().date()))
    else:
        nowDate=strChangeToDateTime(nowDate)

    resultDate=nowDate-distanceDay*oneDay
    return resultDate

def getNextDateTime(distanceDay,nowDate=None):     #默认是求今天的后几天的日期
    if nowDate==None:
        nowDate=strChangeToDateTime(str(datetime.today().date()))
    else:
        nowDate=strChangeToDateTime(nowDate)

    resultDate=nowDate+distanceDay*oneDay
    return resultDate

def getDistanceDay(strStartDate,strEndDate=None,frontDay=0):   #默认enddate是今天，通过frontDay可以使enddate往前推
    startDate=strChangeToDateTime(strStartDate)
    if strEndDate==None:
        enbDate=datetime.today()-frontDay*oneDay
    else:
        enbDate=strChangeToDateTime(strEndDate)-frontDay*oneDay

    return (enbDate.date()-startDate.date()).days


def compareTime(waitCompareDateTime,intTime):   #只比较时间部分，第一个参数为datetime类型，第二个参数为整数
    waitCompareTime=waitCompareDateTime.time()
    intWaitCompareTime=int(waitCompareTime.strftime("%H%M%S"))
    if intWaitCompareTime>intTime:
        return 1     #大于返回1
    else:
        return 0    #小于返回0

def intChangeToDateTimeStr(inputInt):   #20180910 00:30
    strInt=str(inputInt).zfill(12)
    dateTimeStr=strInt[0:4]+'-'+strInt[4:6]+'-'+strInt[6:8]+' '+strInt[8:10]+':'+strInt[10:12]
    return dateTimeStr

def dateTimeChangeToInt(inputDateTime):
    strDate=str(inputDateTime.date())
    dateList=strDate.split('-')
    resultInt=int(dateList[0])*10000+int(dateList[1])*100+int(dateList[2])
    return resultInt

def dateTimeChangeToIntWithTime(inputDateTime): #不包含秒
    dateInt=dateTimeChangeToInt(inputDateTime)
    timeInt=int(inputDateTime.time().strftime("%H%M"))
    return int(dateInt*1e4+timeInt)

def getGradeByYear():   #此处默认9.8号是开学日期
    dateInt=dateTimeChangeToInt(datetime.now())
    yearInt=dateInt//10000
    if (yearInt*10000+908)>dateInt:   #当前时间小于同年的9月8号，认为当年学生还未入学
        oneGradeYear=yearInt%100-1
    else:
        oneGradeYear=yearInt%100

    gradeDict={}
    for i in range(4):
        gradeDict[str(oneGradeYear-i)]=i+1

    return gradeDict

