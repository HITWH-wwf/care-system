# coding=utf8

import io
import pandas as pd


class DataClean():
    """
    用以作为数据清洗入口，从前端传递回来的
    """

    def set_bad_ans(self, dict_temp, error_info):
        """添加一条失败的原因"""
        if type(dict_temp) != dict:
            dict_temp = {}
        dict_temp["status"] = 0
        dict_temp["errorInfo"] = str(error_info)
        return dict_temp

    def updateBasic(self, file):
        """
        针对用户上传的学生基础数据进行数据清洗和检错.
        在tornado接收到request后，调用本函数，传入 self.request.files['file'][0]
        函数返回值ans为字典：{"status":0, "errorInfo":"", "data":[]}
        当status为0时，data为空列表，errorInfo内的字符串存储了可能的错误原因
        当status为1时，errorInfo为空字符串，data为列表，列表内元素为N个字典，举例如下：
            [
                {
                    "stuID":"110440401",
                    "stuClassNumber":"1104404",
                    "stuName":"张三",
                    "sex":"男"，
                    "nationality":"汉族",
                    "politicalLandscape":"政治面貌",
                    "stuEducation":"学历",
                    "idNumber":"61011211122052132",
                    "apartmentNumber":"6",
                    "dormitoryNumber":"404",
                    "graduatedHighSchool":"XX高中",
                    "stuMobileNumber":"183631211223",
                    "homeAddress":"XX省XX市",
                    "fatherName":"张三爸",
                    "fatherWorkUnit":"张三爸工作单位",
                    "fatherMobileNumber":"186548945121",
                    "motherName":"张三妈",
                    "motherWorkUnit":"张三妈工作单位",
                    "motherMobileNumber":"18451587222",
                    "state":0,#state均为0
                    "ifSingleParent":0，#ifSingleParent均为0
                    "ifPoor":0，//ifPoor均为0
                    "specialitiesid":"04",
                    "collegeid":"020",
                    "grade":13,
                    "schoolStatus":学籍状态
                    "sleepInOrOut":校外住宿
                    "turnProfessional":转专业
                    "turnInProfessional":转入专业
                    "downgrade":降级
                },
                {……},
                {……},
                …
            ]
        """
        ans = {"status": 1, "errorInfo": "", "data": []}
        #myfile = self.request.files['file'][0]
        myfile = file
        content = myfile["body"]
        try:
            # 文件类型、完整性检测
            pd_data = pd.read_excel(io.BytesIO(content), engine='xlrd')

        except Exception as e:
            # print(e)
            # raise Exception("文件无法识别，系统只接受excel文件，只录取第一个sheet，且不接受任何合并单元格的操作。请严格按照模板的格式填充")
            return self.set_bad_ans(ans, "文件无法识别，系统只接受excel文件，只录取第一个sheet，且不接受任何合并单元格的操作。请严格按照模板的格式填充")

        # 文件列名检测
        pd_data.rename(index=str, columns={"学号": "stuID", "班号": "stuClassNumber", "姓名": "stuName", "性别": "sex", "民族": "nationality", "政治面貌": "politicalLandscape", "学历": "stuEducation", "身份证号": "idNumber", "公寓号": "apartmentNumber", "寝室号": "dormitoryNumber",
                                           "毕业高中": "graduatedHighSchool", "学生手机号": "stuMobileNumber", "家庭地址": "homeAddress", "父亲姓名": "fatherName", "父亲工作单位": "fatherWorkUnit", "父亲联系方式": "fatherMobileNumber", "母亲姓名": "motherName", "母亲工作单位": "motherWorkUnit", "母亲联系方式": "motherMobileNumber",
                                           "学籍状态":"schoolStatus","校外住宿":"sleepInOrOut","转专业":"turnProfessional","转入专业":"turnInProfessional","降级":"downgrade"}, inplace=True)
        cols = pd_data.columns.tolist()
        if set(['apartmentNumber', 'dormitoryNumber', 'fatherMobileNumber', 'fatherName', 'fatherWorkUnit', 'graduatedHighSchool', 'homeAddress', 'idNumber', 'motherMobileNumber', 'motherName', 'motherWorkUnit', 'nationality', 'politicalLandscape', 'sex', 'stuClassNumber', 'stuEducation', 'stuID', 'stuMobileNumber', 'stuName'
                ,"schoolStatus","sleepInOrOut","turnProfessional","turnInProfessional","downgrade"]) != set(cols):
            return self.set_bad_ans(ans, "文件的列名或列数量与模板不同，请核对")

        pd_data.fillna("", inplace=True)
        pd_data["state"] = 0
        pd_data["ifSingleParent"] = 0
        pd_data["ifPoor"] = 0
        pd_data["specialitiesid"] = pd_data["stuClassNumber"].apply(lambda x: str(x)[2:5])
        pd_data["collegeid"] = pd_data["stuClassNumber"].apply(lambda x: str(x)[2:4])
        pd_data["grade"] = pd_data["stuClassNumber"].apply(lambda x: str(x)[0:2])
        ans["data"] = pd_data.to_dict("report")
        return ans

    def updateFocus(self,file):
        ans = {"status": 1, "errorInfo": "", "data": []}
        # myfile = self.request.files['file'][0]
        myfile = file
        content = myfile["body"]
        try:
            # 文件类型、完整性检测
            pd_data = pd.read_excel(io.BytesIO(content), engine='xlrd')

        except Exception as e:
            # print(e)
            # raise Exception("文件无法识别，系统只接受excel文件，只录取第一个sheet，且不接受任何合并单元格的操作。请严格按照模板的格式填充")
            return self.set_bad_ans(ans, "文件无法识别，系统只接受excel文件，只录取第一个sheet，且不接受任何合并单元格的操作。请严格按照模板的格式填充")

        # 文件列名检测
        pd_data.rename(index=str, columns={"学号":"stuID","重点关注原因":"reason","被关注日期":"createDate","关注级别":"level","校外住宿":"sleepInOrOut","家长陪读":"studyWithParent"}, inplace=True)
        cols = pd_data.columns.tolist()
        if set(["stuID","reason","createDate","level","sleepInOrOut","studyWithParent"]) != set(cols):
            return self.set_bad_ans(ans, "文件的列名或列数量与模板不同，请核对")
        pd_data.fillna("", inplace=True)
        pd_data["style"] = 0
        ans["data"] = pd_data.to_dict("report")
        return ans

    def updateScore(self, file):
        """
        针对用户上传的学生成绩数据进行数据清洗和检错.
        在tornado接收到request后，调用本函数，传入 self.request.files['file'][0]
        函数返回值ans为字典：{"status":0, "errorInfo":"", "data":[]}
        当status为0时，data为空列表，errorInfo内的字符串存储了可能的错误原因
        当status为1时，errorInfo为空字符串，data为列表，列表内元素为N个字典，举例如下：
            [
                {
                    "courseID":"",#课程号
                    "courseIndex":"",#课序号
                    "stuID":"",#学号
                    "initialScore":0，#初试成绩
                    "makeUpScore":0, #补考成绩(没有不填写)
                    "examDate":"2017-01-01",#考试时间(格式如:2017-01-01)
                    "repairOrNot":0, #是否重修(是或者否)，是为1，否为0
                    "adoptOrNot":0  #是否通过。是为1，否为0
                },
                {……},
                {……},
                …
            ]
        """
        ans = {"status": 1, "errorInfo": "", "data": []}
        #myfile = self.request.files['file'][0]
        myfile = file
        content = myfile["body"]
        try:
            # 文件类型、完整性检测
            pd_data = pd.read_excel(io.BytesIO(content), engine='xlrd')
        except:
            return self.set_bad_ans(ans, "文件无法识别，系统只接受excel文件，只录取第一个sheet，且不接受任何合并单元格的操作。请严格按照模板的格式填充")
            # raise Exception("文件无法识别，系统只接受excel文件，只录取第一个sheet，且不接受任何合并单元格的操作。请严格按照模板的格式填充")
        # 文件列名检测
        pd_data.rename(index=str, columns={"学号": "stuID", "姓名":"stuName","班级":"stuClass","考试学期":"examSemester","课程号": "courseID", "课序号": "courseIndex", "课程名": "courseName",
                                           "学分": "credit", "课程属性": "courseKind", "总成绩": "examScore","备注":"remarks","考试时间":"examDate","考查/考试":"examKind"}, inplace=True)
        cols = pd_data.columns.tolist()
        if set(["stuID", "stuName","stuClass","examSemester", "courseID",  "courseIndex", "courseName","credit", "courseKind","examScore","remarks","examDate","examKind"]) != set(cols):
            return self.set_bad_ans(ans, "文件的列名或列数量与模板不同，请核对")

        try:
            pd_data["examScore"] = pd_data["examScore"].astype(float)
        except:
            # raise Exception("考试成绩无法转为数字，存在非法符号，请核对")
            return self.set_bad_ans(ans, "考试成绩无法转为数字，存在非法符号，请核对")

        # try:
        #     pd_data["makeUpScore"] = pd_data["makeUpScore"].fillna(
        #         0).astype(float)
        # except:
        #     return self.set_bad_ans(ans, "补考成绩无法转为数字，存在非法符号，请核对")

        try:
            pd_data["examDate"] = pd_data["examDate"].astype(
                str).apply(pd.to_datetime)
            pd_data["examDate"] = pd_data["examDate"].apply(
                lambda x: str(x.date()))
        except:
            # raise Exception("考试时间格式错误，存在非法符号或空，请核对")
            return self.set_bad_ans(ans, "考试时间格式错误，存在非法符号或空，请核对")

        # pd_data["repairOrNot"] = pd_data["repairOrNot"].apply(lambda x: str(x).strip())
        # reset = set(pd_data["repairOrNot"].tolist())
        # reset.add("是")
        # reset.add("否")
        # if reset != set({"是", "否"}):
        #     return self.set_bad_ans(ans, "重修列(是或者否)中，出现了其他字符")
        # else:
        #     pd_data["repairOrNot"] = pd_data["repairOrNot"].replace("是", "1").replace("否", "0")
        # pd_data["adoptOrNot"] = (pd_data["initialScore"] >= 60) | (
        #     pd_data["makeUpScore"] >= 60)
        # pd_data["adoptOrNot"] = pd_data["adoptOrNot"].astype(int)

        pd_data.fillna("", inplace=True)
        ans["data"] = pd_data.to_dict("report")
        return ans
