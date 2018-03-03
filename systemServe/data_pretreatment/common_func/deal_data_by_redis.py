import redis
'''
使用redis连接池
'''
redisPool=redis.ConnectionPool(host='127.0.0.1',port=6379)
r = redis.StrictRedis(connection_pool=redisPool)

def saveData(key,value):
    r.set(key,value)
    return True

def getValue(key):
    result=r.get(key)
    if result!=None:
        # r.expire(key,1800)
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

def getFlagValueInt(key):
    result = r.get(key)
    if result != None:
        result = result.decode('utf-8')
    else:
        result='0'
    return int(result)

