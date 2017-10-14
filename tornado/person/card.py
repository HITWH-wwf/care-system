#coding=utf8

from judge_permission import judgeIfPermiss
from api_define import person_card
from orm import *
import datetime
import json
import traceback

class PersonCard(person_card):

    def entry(self, response_self):
        try:
            body = eval(response_self.request.body)
            print(body)
            user_id = str(body["userId"])
            stu_id = str(body["stuId"])

            if judgeIfPermiss(user_id = user_id, mode = 1, page = "person") == False:
                return {"status":0, "errorInfo":"用户没有权限设置"}
            elif judgeIfPermiss(user_id = user_id, stuid = stu_id, mode = 0) == False:
                return {"status":0, "errorInfo":"用户没有权限设置"}
            else:
                result = self.getData(stu_id)
                result=json.dumps(result,ensure_ascii=False)
                return result
        except:
            error_info = traceback.format_exc()
            print(error_info)
            raise

    def funAccountToName(self, account):

        name = MyBaseModel.returnList(merchant_date.select(merchant_date.merchantName).where(merchant_date.merchantAccount == account).dicts(), key = "merchantName")
        #返回的name是一个列表，列表中的元素是一个字符串，不是字典
        if len(name) == 0:
            return ""
        else:
            return name[0]

    def getData(self, stu_id):
        data_res = {
        "date": [],
        "consume": [],
        "colName": [
            "商户名称",
            "金额",
            "消费时间",
            "消费类型"
        ],
        "propName": [
            "merchantAccount",
            "turnover",
            "tradingTime",
            "operationType"
        ],
        "data": [
        ]}
        #获取近7天的所有数据
        with db.execution_context():
            max_date = stu_transaction_record.select(stu_transaction_record.tradingTime).where(stu_transaction_record.stuID == stu_id).aggregate(fn.Max(stu_transaction_record.tradingTime))
        # print(max_date)
        if max_date == None:
            return {"status":1, "errorInfo":"没有数据", "data": data_res}
        day=datetime.timedelta(days = 1)
        last_days=179
        the_time = (max_date.date() - day*last_days)
        dates=[]
        for i in range((last_days+1)):
            dates.append(str(the_time+day*i))

        data_res['date']=dates
        data_list = MyBaseModel.returnList(stu_transaction_record.select(stu_transaction_record.tradingTime, stu_transaction_record.merchantAccount, stu_transaction_record.turnover, stu_transaction_record.operationType).where(stu_transaction_record.stuID == stu_id, stu_transaction_record.tradingTime >= the_time).dicts())

        sum_money=[]

        for i in range(last_days+1):
            today_sum=0
            for a_deal in data_list:
                if str(a_deal['tradingTime'].date())==dates[i]:
                    if a_deal['turnover']<0:			#这个一会得改成小于号
                        today_sum=today_sum+a_deal['turnover']  #只算消费的，充值不算
            sum_money.append(abs(today_sum))

        for i in range(len(data_list)):
            if data_list[i]['merchantAccount'] == None or len(data_list[i]['merchantAccount']) == 0:
                data_list[i]['merchantAccount'] = ""
            else:
                data_list[i]['merchantAccount'] = self.funAccountToName(data_list[i]['merchantAccount'])
            costTime = str(data_list[i]['tradingTime'])
            data_list[i]['tradingTime'] = costTime

        data_res['consume']=sum_money
        data_res['data']=data_list
        return {"status":1, "errorInfo":"","data": data_res}
