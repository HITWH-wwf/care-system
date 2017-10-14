# coding=utf8

from peewee import SelectQuery, CharField, IntegerField, fn, Model, FloatField, MySQLDatabase, TextField,\
    DateTimeField,TextField
from playhouse.shortcuts import model_to_dict as to_dict
import playhouse as ph
from api_define import users

from playhouse.pool import PooledMySQLDatabase
from logConfig import logger


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
    state = IntegerField(null=True)
    ifSingleParent = IntegerField()
    ifPoor = IntegerField()
    updateDate = DateTimeField(null=True)
    classNumberId = IntegerField(null=True)
    schoolStatus=CharField(null=True)   #学籍状态
    sleepInOrOut=CharField(null=True)   #校外住宿
    turnProfessional=CharField(null=True)   #转专业
    turnInProfessional=CharField(null=True) #转入专业
    downgrade=CharField(null=True)  #降级


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
    reason = CharField(null=True)
    level = IntegerField(null=True)
    createDate = DateTimeField(null=True)
    sleepInOrOut=CharField(null=True)
    studyWithParent=CharField(null=True)


class new_users(MyBaseModel):
    username = CharField(null=True)  # 用户名，varchar
    userpass = CharField(null=True)  # 用户密码，varchar
    description = CharField()
    userteamname = CharField(null=True)  # 该用户对应用户组名
    userrolename = CharField(null=True)  # 该用户对应角色组名


class new_user_role(MyBaseModel):
    userrolename = CharField(null=True)
    description = CharField()
    permission = CharField(null=True)  # 角色组权限，varchar


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
    messContent = CharField(null=True)
    messTitle = CharField(null=True)
    stuId = CharField(null=True)


class stu_cost_count(MyBaseModel):
    stuID = CharField(null=True)
    everyDayCost = TextField(null=True)
    countDate = DateTimeField(null=True)
    class Meta:
        db_table = 'stu_cost_count'
        primary_key = False


class stu_sleep_count(MyBaseModel):
    stuID = CharField(null=True)
    everyDaySleep = TextField(null=True)
    countDate = DateTimeField(null=True)
    class Meta:
        db_table = 'stu_sleep_count'
        primary_key = False

class stu_score_count(MyBaseModel):
    stuID = CharField(null=True)
    failNum = IntegerField(null=True)
    countDate = DateTimeField(null=True)
    class Meta:
        db_table = 'stu_score_count'
        primary_key = False

db.create_tables([exam_results,stu_focus,stu_cost_count,stu_score_count,stu_sleep_count], safe=True)

