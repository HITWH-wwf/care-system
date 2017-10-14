#coding=utf8

import sys
sys.path.append("..")

from api_define import update_score
from orm import *
from common.data_clean import DataClean
import json
import datetime

class UpdateScore(update_score):
    """分数更新"""

    def entry(self, file):
        returndata = {}
        allData = DataClean().updateScore(file)
        if allData["status"] == 0:
            returndata["status"] = 0
            returndata["errorInfo"] = allData["errorInfo"]
            return json.dumps(returndata, ensure_ascii=False)
        else:
            #增量更新方法如下：
            #for循环遍历allData["data"],当select发现不存在该学号时，执行insert，否则update
            #每一次执行insert或者update都有try catch，将所有不符合的数据存入到列表内，随后返回给前端，前端直接将其下载成excel递交给用户，让用户自己决定该怎么做
            res = []
            success_create_count = 0
            success_update_count = 0
            with db.execution_context():
                for data in allData["data"]:
                    judge = exam_results.select().where(exam_results.courseIndex == data["courseIndex"], exam_results.courseID == data["courseID"]).aggregate(fn.Count(exam_results.courseID))
                    try:
                        if judge >= 1:
                            exam_results.update(**data).where(exam_results.courseIndex == data["courseIndex"], exam_results.courseID == data["courseID"]).execute()
                            success_update_count += 1
                        else:
                            exam_results.create(**data)
                            success_create_count += 1
                    except:
                        res.append([data["courseID"], data["courseIndex"]])
            if len(res) == 0:
                #表示本次全部都导入成功了
                returndata["status"] = 1
                returndata["errorInfo"] = "系统本次总共接收到%d条数据\n未发现无法导入的情况\n导入操作完成后,数据库中新增了%d条数据,覆盖了%d条数据"%(len(allData["data"]), success_create_count, success_update_count)
            else:
                #表示本次部分或者全部导入不成功
                returndata["status"] = 2
                returndata["errorInfo"] = "系统本次总共接收到%d个数据\n未成功导入的数据数量为%d个\n导入动作完成后,新增了%d条数据,覆盖了%d条数据"%(len(allData["data"]), len(res), success_create_count, success_update_count)
                returndata["file"] = res

            return json.dumps(returndata, ensure_ascii=False)
