
def getSelectState():
    selectState = {
        'studyInfo': {'濒临降级': 1, '已经降级': 2, '延期毕业': 4},  # [],采用类似linux文件权限去判别一个数字对应的类型
        'thoughtInfo': {'宗教信仰': 1, '专业思想': 2, '过激思想': 4},  # []
        'economyInfo': {'已解决': 1, '未解决': 2},
        'bodyInfo': {'大学之前': 1, '大学之后': 2},
        'networkInfo': {'倾向性': 1, '严重': 2},
        'sleepInfo': {'留学生公寓住宿': 1, '无陪读校外住宿': 2, '家长陪读校外住宿': 3},
        'burstInfo': {'违纪处分': 1, '失踪': 2, '恶性事件': 4},  # []
        'peopleInfo': 1,
        'mentalityInfo': 1,
        'gayInfo': 1,
        'familyInfo': {'单亲': 1, '孤儿': 2},
        'otherInfo': 1,
    }
    return selectState

def getCareKindList():
    kindList = ['studyInfo', 'thoughtInfo', 'economyInfo', 'bodyInfo', 'networkInfo',
                'burstInfo', 'sleepInfo',  'peopleInfo', 'mentalityInfo', 'gayInfo',
                'familyInfo', 'otherInfo']
    return kindList

def getCollegeDict():
    college = {
              '01': '汽车',
              '02':'信电',
              '03':'经管',
              '04':'计算机',
              '05':'语言',
              '06':'理学',
              '07':'海洋',
              '08':'材料',
              '11':'计算机',
              '12':'土木',
              '13':'船舶'
            }
    return college

def getCollegesName():
    return ['船舶','海洋','汽车','信电','计算机','材料','理学','土木','经管','语言']

def getJudgeState():
    judgeState={
        'studyInfo':[(2,3,6,7),(1,3,5,7),(4,5,6,7)],'thoughtInfo':[(1,3,5,7),(2,3,6,7),(4,5,6,7)],
        'economyInfo':[(1,2),(1,),(2,)],'bodyInfo':[(1,),(2,)],'networkInfo':[(1,),(2,)],'burstInfo':[(1,3,5,7),(2,3,6,7),(4,5,6,7)],
                   'sleepInfo':[(1,),(2,3)],'peopleInfo':[(1,)],'mentalityInfo':[(1,)],'gayInfo':[(1,)],
        'familyInfo':[(1,),(2,)],'otherInfo':[(1,)]
    }
    return judgeState