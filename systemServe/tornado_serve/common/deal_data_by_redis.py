import redis
from tornado_serve.orm import *
import time
'''
使用redis连接池
所有高频访问数据，均缓存半小时，如果半小时内没有再次被使用，则释放内存
暂时设为高频的数据为：sessionId，成绩统计表，归寝统计表，消费统计表

成绩统计表，归寝统计表，消费统计表三者速度提升效果不明显，暂时不实现
'''
redisPool=redis.ConnectionPool(host='127.0.0.1',port=6379)
r = redis.StrictRedis(connection_pool=redisPool)

def saveData(key,value):
    r.set(key,value,ex=1800)
    return True

def getValue(key):
    result=r.get(key)
    if result!=None:
        r.expire(key,1800)
        result=result.decode('utf-8')
    return result


def delData(key):
    r.delete(key)
    return True

def getFlagValue(key):
    result = r.get(key)
    if result != None:
        result = result.decode('utf-8')
    return result



# import datetime
# s1=time.time()
# result=MyBaseModel.returnList(stu_cost_count.select())
# s2=time.time()
# print('data from mysql cost: ',s2-s1)
# # saveData('costList4',result)
# s3=time.time()
# print('data save cost time ',s3-s2)
# result2=getValue('costList4')
# result2=[eval(line) for line in result2 ]
# print('data from redis cost: ',time.time()-s3)
# print(type(result2[1]))
