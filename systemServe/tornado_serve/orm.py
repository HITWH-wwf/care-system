# coding=utf8

from peewee import SelectQuery, CharField, IntegerField, fn, Model, FloatField, MySQLDatabase, TextField,\
    DateTimeField,TextField,BigIntegerField
from playhouse.shortcuts import model_to_dict as to_dict
import playhouse as ph
from tornado_serve.api_define import users
from playhouse.pool import PooledMySQLDatabase
from tornado_serve.logConfig import logger

for user in users:
  try:
      db = PooledMySQLDatabase(
      database='school',
      max_connections=4,
      stale_timeout=3600,  # 1 hour
      timeout=0,
      user=user['name'],
      host='127.0.0.1',
      passwd=user['pwd'],
      )
      with db.execution_context():
          pass
      break
  except:
      logger.warning("this mysql username is not "+user['name'])
      print("this mysql username is not "+user['name'])


def applyConnect(func):
    def applyFunc(cls, *args, **kwargs):
      with db.execution_context():
        # print('lian jie is ok')
        return func(cls, *args, **kwargs)
    return applyFunc

# Model是peewee的基类
class MyBaseModel(Model):
    class Meta:
        database = db

    @classmethod
    @applyConnect
    def getOne(cls, *query, **kwargs):

        """
        为了方便使用，新增此接口，查询不到返回None，而不抛出异常
        """

        try:
            return cls.get(*query, **kwargs)
        except:
            raise

    @classmethod
    @applyConnect
    def returnList(cls, Model=None, key=None):
        """
        将结果返回成一个列表嵌套字典的结构返回
        """
        if not type(Model) == SelectQuery:
            return None
        list = []
        for con in Model:
            if type(con) == dict:
                if not key == None:
                    list.append(con[key])
                else:
                    list.append(con)
            else:
                list.append(to_dict(con))
        return list

    @classmethod
    @applyConnect
    def returnList2(cls, Model=None, key=None):
        """
        将结果返回成一个列表嵌套字典的结构返回
        """
        if not type(Model) == SelectQuery:
            return None
        list = []
        for con in Model:
            if type(con) == dict:
                if not key == None:
                    list.append(con[key])
                else:
                    list.append(con)
            else:
                list.append(con)
        return list


class course_data(MyBaseModel):
    courseID = CharField()
    courseIndex = IntegerField()
    courseName = CharField(null=True)
    courseStyle = CharField(null=True)
    courseWeek = CharField(null=True)
    requiredOrElectiveCourse = CharField(null=True)
    credit = FloatField(null=True)
    teacherName = CharField(null=True)


class exam_results(MyBaseModel):
    courseID = CharField()
    courseName = CharField()
    courseIndex = IntegerField(null=True)
    stuID = CharField()
    stuName=CharField()
    stuClass=CharField()
    examScore = FloatField(null=True)
    credit = FloatField(null=True)
    examSemester = CharField(null=True) #考试学期
    examDate=DateTimeField(null=True)   #考试时间
    courseKind = CharField(null=True)       #课程属性
    examKind=CharField(null=True)       #考试类型
    remarks=CharField(null=True)



class school_college_info(MyBaseModel):
    collegeid = CharField(primary_key=True)
    college = CharField()


class school_specialities_info(MyBaseModel):
    specialitiesid = CharField(primary_key=True)
    specialities = CharField()
    collegeid = CharField()


class school_class_info(MyBaseModel):
    stuClassNumber = CharField()
    specialitiesid = CharField()
    grade = IntegerField()


class stu_basic_info(MyBaseModel):
    stuID = CharField(primary_key=True)
    stuClassNumber = CharField(null=True)
    stuName = CharField(null=True)
    sex = CharField(null=True)
    nationality = CharField(null=True)
    politicalLandscape = CharField(null=True)
    stuCreed = CharField(null=True)
    stuEducation = CharField(null=True)
    idNumber = CharField(null=True)
    apartmentNumber = CharField(null=True)
    dormitoryNumber = CharField(null=True)
    grade = IntegerField(null=True)
    specialitiesid = CharField(null=True)
    collegeid = CharField(null=True)
    graduatedHighSchool = CharField(null=True)
    stuMobileNumber = CharField(null=True)
    homeAddress = CharField(null=True)
    homeMobileNumber = CharField(null=True)
    fatherName = CharField(null=True)
    fatherWorkUnit = CharField(null=True)
    fatherMobileNumber = CharField(null=True)
    motherName = CharField(null=True)
    motherWorkUnit = CharField(null=True)
    motherMobileNumber = CharField(null=True)
    state = IntegerField(null=True)     #是否被关注，及关注类型
    ifSingleParent = IntegerField()
    ifPoor = IntegerField()
    updateDate = DateTimeField(null=True)
    classNumberId = IntegerField(null=True)
    schoolStatus=CharField(null=True)   #学籍状态
    sleepInOrOut=CharField(null=True)   #校外住宿
    turnProfessional=CharField(null=True)   #转专业
    turnInProfessional=CharField(null=True) #转入专业
    downgrade=CharField(null=True)  #降级
    studyWithParent = CharField(null=True)  # 是否家长陪读
    focusColor = CharField(null=True)


class stu_scholarship_and_grant(MyBaseModel):
    stuID = CharField()
    dataOfGrant = DateTimeField(null=True)
    resonOfGrant = CharField()
    amountOfGrant = FloatField()


class psychology_data(MyBaseModel):
    stuID = CharField()
    testQuesNumber = CharField()
    testQuesResult = TextField()
    score = FloatField()


class merchant_date(MyBaseModel):  # 应该是data
    merchantAccount = CharField()
    merchantName = CharField(null=True)
    department = CharField(null=True)


class stu_transaction_record(MyBaseModel):
    stuID = CharField()
    turnover = FloatField(null=True)
    cardBalance = FloatField(null=True)
    cardUseNumber = IntegerField(null=True)
    tradingTime = DateTimeField(null=True)
    merchantAccount = CharField(null=True)
    operationType = CharField(null=True)


class entry_and_exit(MyBaseModel):
    stuID = CharField()
    entryDate = DateTimeField(null=True)
    exitDate = DateTimeField(null=True)
    apartmentNumber = CharField()


class stu_focus(MyBaseModel):
    stuID = CharField()
    style = IntegerField(null=True)
    reason = TextField(null=True)
    level = IntegerField(null=True)
    createDate = DateTimeField(null=True)


class new_users(MyBaseModel):
    username = CharField(null=True)  # 用户名，varchar
    userpass = CharField(null=True)  # 用户密码，varchar
    description = CharField()
    userteamname = CharField(null=True)  # 该用户对应用户组名
    userrolename = CharField(null=True)  # 该用户对应角色组名


class new_user_role(MyBaseModel):
    userrolename = CharField(null=True)
    description = CharField()
    permission = TextField(null=True)  # 角色组权限，varchar


class new_user_team(MyBaseModel):
    userteamname = CharField(null=True)
    description = CharField()
    permission = TextField(null=True)  # 用户组权限，text


class new_feedback(MyBaseModel):
    createDate = DateTimeField(null=True)
    info = CharField(null=True)
    start = FloatField(null=True)
    userId = CharField(null=True)


class new_event_message(MyBaseModel):  # 新建事件表
    createDate = DateTimeField(null=True)
    fromUserId = CharField(null=True)
    messContent = TextField(null=True)
    messTitle = CharField(null=True)
    stuId = CharField(null=True)


class stu_cost_count(MyBaseModel):
    stuID = CharField(null=True)
    everyDayDetailRecord = TextField(null=True)
    everyDayCount=TextField(null=True)
    lastTimeCountDate = CharField(null=True)
    class Meta:
        db_table = 'stu_cost_count'
        primary_key = False



class stu_sleep_count(MyBaseModel):
    stuID = CharField(null=True)
    freeQueryCountInfo=TextField(null=True)
    fixedQueryCountInfo= TextField(null=True)
    lastTimeCountDate = CharField(null=True)
    class Meta:
        db_table = 'stu_sleep_count'
        primary_key = False

class stu_score_count(MyBaseModel):
    stuID = CharField(null=True)
    scoreCountInfo=TextField(null=True)
    lastTimeCountDate = CharField(null=True)
    class Meta:
        db_table = 'stu_score_count'
        primary_key = False

class stu_some_state(MyBaseModel):
    stuID = CharField(null=False, primary_key=True)
    lastTimeCountDate = CharField(null=True)
    earlyWarningInfo=TextField(null=True)
    vacationStayflag=CharField(null=True)
    stayDate=TextField(null=True)
    stayRemarks=CharField(null=True)
    warningHistory = TextField(null=True)
    scoreWarningLevel=IntegerField(null=True)

class stu_all_aspect_info(MyBaseModel):
    stuID=CharField(null=False,primary_key=True)
    studyInfo=TextField(null=True)
    thoughtInfo=TextField(null=True)
    economyInfo=TextField(null=True)
    bodyInfo=TextField(null=True)  # 身体
    networkInfo=TextField(null=True)  # 网络
    sleepInfo=TextField(null=True)  # 公寓
    burstInfo=TextField(null=True)  # 突发
    peopleInfo=TextField(null=True)  # 人际
    mentalityInfo=TextField(null=True)  # 心理
    gayInfo=TextField(null=True)    # 同性恋
    familyInfo=TextField(null=True) # 单亲/孤儿
    otherInfo=TextField(null=True)  # 其他问题
    fudaoyuan=TextField(null=True)  #初始化为[]
    fushuji=TextField(null=True)    #初始化为[]
    stuState=IntegerField(null=True)    #初始化为0
    latelyEditTime=BigIntegerField(null=True)
    class Meta:
        db_table = 'stu_all_aspect_info'

'''
关于stu_all_aspect_info表中stuState字段的值说明
0：取消关注状态    1：学情关注
2：修改未提交      3：取消未通过
4：关注未通过      5：取消待审核
6：关注待审核
'''
db.create_tables([stu_all_aspect_info,stu_some_state,exam_results,stu_focus,stu_cost_count,stu_score_count,stu_sleep_count], safe=True)

