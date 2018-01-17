#coding=utf8

from orm import *

if __name__ == "__main__":

    middleList = MyBaseModel.returnList(stu_focus.select(stu_focus.stuID, stu_focus.style))
    print(len(middleList), middleList[0])
    for index,middle in enumerate(middleList):
        # if len(middle["stuID"]) == 9 and len(middle["stuClassNumber"]) == 7:
        # print(middle["stuClassNumber"][2:4])
        stu_basic_info.update(**{"state": 1}).where(stu_basic_info.stuID == middle["stuID"]).execute()
        print(middle["stuID"], index)
    pass
