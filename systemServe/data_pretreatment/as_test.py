from data_pretreatment.data_orm import *
import pandas as pd
from data_pretreatment.common_func.deal_dateortime_func import *
import numpy as np
import time
from data_pretreatment.common_func.deal_data_by_redis import getValue

# s=[{'name':'wwf','id':{'one':{'w':1,'z':2},'two':2,'three':-3}},{'name':'zyz','id':{'one':31,'two':32,'three':33}},{'name':'sss','id':{'one':11,'two':21,'three':13}}]
# df=pd.DataFrame(s)
# s2=df['id'].to_dict()
# s2=list(s2.values())
# # print(list(s2.values()))
# s3=pd.DataFrame(s2)
# s3['three']=-s3['three']
# print(s3)
# print(list(df.loc[[1,2],'name']))
# print(s3[s3['three']>0]['three'].sum())
# print(list(s3[s3['three']>3]['two']))
#
# print(1234//100)
# print(1234%100)

# print(df)
# s2=s1.idxmin()
# s1=df[df['id']>2]['id']
# print(s1)
# s3=df.loc[s1.idxmin()].to_dict()
# print(s3)
# print(s3['date'])
#
# for i in range(5):
#     if i==3:
#         continue
#     print(i)
