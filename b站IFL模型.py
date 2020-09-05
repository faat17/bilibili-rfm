# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 14:41:31 2020

@author: Administrator
"""

import os
import pandas as pd



os.chdir(r'C:\Users\A\Desktop\项目')
table_view=pd.read_excel('b站科技区2019数据.xlsx',encoding='utf-8',sep=',',header =0,sheet_name=0) #打开文件

#-----数据概况-----
table_view.shape #统计格式
table_view.info() #各字段数量
    
table_null = table_view.isnull().sum()
print(table_null) #缺失值数量
    
#-----数据清洗-----
table_view = table_view.dropna() #删除空值
table_view = table_view.drop_duplicates() #删除重复值
            
    
table_view = table_view[['partition','author','datetime','view','danmu','comment','like','coins','favorite','share']] #提取关键词
table_view.head(5)
    
#-----构建模型-----
print(table_view.groupby('partition')['datetime'].count())
#-------分区-------
table_sc = table_view.loc[table_view['partition']=='科学科普']
table_la = table_view.loc[table_view['partition']=='社科人文']
table_ma = table_view.loc[table_view['partition']=='机械']
table_tec = table_view.loc[table_view['partition']=='野生技术协会']
table_mi = table_view.loc[table_view['partition']=='星海'] # 一般发布军事内容
table_car = table_view.loc[table_view['partition']=='汽车']

#---------社科人文分区 IFL模型构建
#-------F值------

la_count = round(table_la.groupby('author')['datetime'].count()).reset_index() #计算发布视频的次数
la_count.columns = ['author','times'] 

la_count_5 = la_count[la_count['times']>5] #剔除掉发布视频数小于5的up主
la_count_5.info()

la_datetime_last = table_la.groupby('author')['datetime'].max()
la_datetime_late = table_la.groupby('author')['datetime'].min()
# F值 =(最晚发布日期 - 最早发布日期)/发布次数，保留整数
la_F = round((la_datetime_last-la_datetime_late).dt.days/table_la.groupby('author')['datetime'].count()).reset_index()
la_F.columns = ['author','F']
la_F = pd.merge(la_count_5,la_F,on = 'author',how = 'inner')

la_F = la_F.loc[la_F['F']>0] #剔除一天发布很多视频的up主
la_F.describe

#------I值------

la_danmu = table_la.groupby('author')['danmu'].sum()
la_comment = table_la.groupby('author')['comment'].sum()
la_view = table_la.groupby('author')['view'].sum()
la_count = table_la.groupby('author')['datetime'].count()

# I值 = (总弹幕数+总评论数)/总播放量/统计范围内视频数量
la_I = round((la_danmu+la_comment)/la_view/la_count*100,2).reset_index()
la_I.columns = ['author','I']
la_F_I = pd.merge(la_F,la_I,on = 'author',how = 'inner')
la_F_I.head(5)
la_F_I.describe

#------L值------

# L值 = (点赞数 * 1 + 投币数 * 2 + 收藏数 * 3 + 分享数 * 4)/播放量/发布视频数
#计算每个视频的L值
table_la['L'] = (table_la['like']+table_la['coins']*2+table_la['favorite']*3+table_la['share']*4)/table_la['view']*100

la_L = (table_la.groupby('author')['L'].sum()/table_la.groupby('author')['datetime'].count()).reset_index()
la_L.columns = ['author','L']
la_L = round(la_L,2)

la_IFL = pd.merge(la_F_I,la_L,on = 'author',how = 'inner')
la_IFL['partition'] = '社科人文'
la_IFL = la_IFL[['partition','author','I','F','L']]

la_IFL.head()




#---------科学科普分区 IFL模型构建
#-------F值------

sc_count = round(table_sc.groupby('author')['datetime'].count()).reset_index() #计算发布视频的次数
sc_count.columns = ['author','times'] 

sc_count_5 = sc_count[sc_count['times']>5] #剔除掉发布视频数小于5的up主
sc_count_5.info()

sc_datetime_last = table_sc.groupby('author')['datetime'].max()
sc_datetime_late = table_sc.groupby('author')['datetime'].min()
# F值 =(最晚发布日期 - 最早发布日期)/发布次数，保留整数
sc_F = round((sc_datetime_last-sc_datetime_late).dt.days/table_sc.groupby('author')['datetime'].count()).reset_index()
sc_F.columns = ['author','F']
sc_F = pd.merge(sc_count_5,sc_F,on = 'author',how = 'inner')

sc_F = sc_F.loc[sc_F['F']>0]
sc_F.describe

#------I值------

sc_danmu = table_sc.groupby('author')['danmu'].sum()
sc_comment = table_sc.groupby('author')['comment'].sum()
sc_view = table_sc.groupby('author')['view'].sum()
sc_count = table_sc.groupby('author')['datetime'].count()

# I值 = (总弹幕数+总评论数)/总播放量/统计范围内视频数量
sc_I = round((sc_danmu+sc_comment)/sc_view/sc_count*100,2).reset_index()
sc_I.columns = ['author','I']
sc_F_I = pd.merge(sc_F,sc_I,on = 'author',how = 'inner')
sc_F_I.head(5)
sc_F_I.describe

#------L值------

# L值 = (点赞数 * 1 + 投币数 * 2 + 收藏数 * 3 + 分享数 * 4)/播放量/发布视频数
#计算每个视频的L值
table_sc['L'] = (table_sc['like']+table_sc['coins']*2+table_sc['favorite']*3+table_sc['share']*4)/table_sc['view']*100

sc_L = (table_sc.groupby('author')['L'].sum()/table_sc.groupby('author')['datetime'].count()).reset_index()
sc_L.columns = ['author','L']
sc_L = round(sc_L,2)

sc_IFL = pd.merge(sc_F_I,sc_L,on = 'author',how = 'inner')
sc_IFL['partition'] = '科学科普'
sc_IFL = sc_IFL[['partition','author','I','F','L']]

sc_IFL.head()



#---------机械分区IFL模型构建
#-------F值------

ma_count = round(table_ma.groupby('author')['datetime'].count()).reset_index() #计算发布视频的次数
ma_count.columns = ['author','times'] 

ma_count_5 = ma_count[ma_count['times']>5] #剔除掉发布视频数小于5的up主
ma_count_5.info()

ma_datetime_last = table_ma.groupby('author')['datetime'].max()
ma_datetime_late = table_ma.groupby('author')['datetime'].min()
# F值 =(最晚发布日期 - 最早发布日期)/发布次数，保留整数
ma_F = round((ma_datetime_last-ma_datetime_late).dt.days/table_ma.groupby('author')['datetime'].count()).reset_index()
ma_F.columns = ['author','F']
ma_F = pd.merge(ma_count_5,ma_F,on = 'author',how = 'inner')

ma_F = ma_F.loc[ma_F['F']>0]
ma_F.describe

#------I值------

ma_danmu = table_ma.groupby('author')['danmu'].sum()
ma_comment = table_ma.groupby('author')['comment'].sum()
ma_view = table_ma.groupby('author')['view'].sum()
ma_count = table_ma.groupby('author')['datetime'].count()

# I值 = (总弹幕数+总评论数)/总播放量/统计范围内视频数量
ma_I = round((ma_danmu+ma_comment)/ma_view/ma_count*100,2).reset_index()
ma_I.columns = ['author','I']
ma_F_I = pd.merge(ma_F,ma_I,on = 'author',how = 'inner')
ma_F_I.head(5)
ma_F_I.describe

#------L值------

# L值 = (点赞数 * 1 + 投币数 * 2 + 收藏数 * 3 + 分享数 * 4)/播放量/发布视频数
#计算每个视频的L值
table_ma['L'] = (table_ma['like']+table_ma['coins']*2+table_ma['favorite']*3+table_ma['share']*4)/table_ma['view']*100

ma_L = (table_ma.groupby('author')['L'].sum()/table_ma.groupby('author')['datetime'].count()).reset_index()
ma_L.columns = ['author','L']
ma_L = round(ma_L,2)

ma_IFL = pd.merge(ma_F_I,ma_L,on = 'author',how = 'inner')
ma_IFL['partition'] = '机械'
ma_IFL = ma_IFL[['partition','author','I','F','L']]

ma_IFL.head()

            
        
            
 
#---------野生技术协会分区 IFL模型构建
#-------F值------

tec_count = round(table_tec.groupby('author')['datetime'].count()).reset_index() #计算发布视频的次数
tec_count.columns = ['author','times'] 

tec_count_5 = tec_count[tec_count['times']>5] #剔除掉发布视频数小于5的up主
tec_count_5.info()

tec_datetime_last = table_tec.groupby('author')['datetime'].max()
tec_datetime_late = table_tec.groupby('author')['datetime'].min()
# F值 =(最晚发布日期 - 最早发布日期)/发布次数，保留整数
tec_F = round((tec_datetime_last-tec_datetime_late).dt.days/table_tec.groupby('author')['datetime'].count()).reset_index()
tec_F.columns = ['author','F']
tec_F = pd.merge(tec_count_5,tec_F,on = 'author',how = 'inner')

tec_F = tec_F.loc[tec_F['F']>0]
tec_F.describe

#------I值------

tec_danmu = table_tec.groupby('author')['danmu'].sum()
tec_comment = table_tec.groupby('author')['comment'].sum()
tec_view = table_tec.groupby('author')['view'].sum()
tec_count = table_tec.groupby('author')['datetime'].count()

# I值 = (总弹幕数+总评论数)/总播放量/统计范围内视频数量
tec_I = round((tec_danmu+tec_comment)/tec_view/tec_count*100,2).reset_index()
tec_I.columns = ['author','I']
tec_F_I = pd.merge(tec_F,tec_I,on = 'author',how = 'inner')
tec_F_I.head(5)
tec_F_I.describe

#------L值------

# L值 = (点赞数 * 1 + 投币数 * 2 + 收藏数 * 3 + 分享数 * 4)/播放量/发布视频数
#计算每个视频的L值
table_tec['L'] = (table_tec['like']+table_tec['coins']*2+table_tec['favorite']*3+table_tec['share']*4)/table_tec['view']*100

tec_L = (table_tec.groupby('author')['L'].sum()/table_tec.groupby('author')['datetime'].count()).reset_index()
tec_L.columns = ['author','L']
tec_L = round(tec_L,2)

tec_IFL = pd.merge(tec_F_I,tec_L,on = 'author',how = 'inner')
tec_IFL['partition'] = '野生技术协会'
tec_IFL = tec_IFL[['partition','author','I','F','L']]

tec_IFL.head()

       


#---------星海分区 IFL模型构建
#-------F值------

mi_count = round(table_mi.groupby('author')['datetime'].count()).reset_index() #计算发布视频的次数
mi_count.columns = ['author','times'] 

mi_count_5 = mi_count[mi_count['times']>5] #剔除掉发布视频数小于5的up主
mi_count_5.info()

mi_datetime_last = table_mi.groupby('author')['datetime'].max()
mi_datetime_late = table_mi.groupby('author')['datetime'].min()
# F值 =(最晚发布日期 - 最早发布日期)/发布次数，保留整数
mi_F = round((mi_datetime_last-mi_datetime_late).dt.days/table_mi.groupby('author')['datetime'].count()).reset_index()
mi_F.columns = ['author','F']
mi_F = pd.merge(mi_count_5,mi_F,on = 'author',how = 'inner')

mi_F = mi_F.loc[mi_F['F']>0] #剔除一天发布很多视频的up主
mi_F.describe

#------I值------

mi_danmu = table_mi.groupby('author')['danmu'].sum()
mi_comment = table_mi.groupby('author')['comment'].sum()
mi_view = table_mi.groupby('author')['view'].sum()
mi_count = table_mi.groupby('author')['datetime'].count()

# I值 = (总弹幕数+总评论数)/总播放量/统计范围内视频数量
mi_I = round((mi_danmu+mi_comment)/mi_view/mi_count*100,2).reset_index()
mi_I.columns = ['author','I']
mi_F_I = pd.merge(mi_F,mi_I,on = 'author',how = 'inner')
mi_F_I.head(5)
mi_F_I.describe

#------L值------

# L值 = (点赞数 * 1 + 投币数 * 2 + 收藏数 * 3 + 分享数 * 4)/播放量/发布视频数
#计算每个视频的L值
table_mi['L'] = (table_mi['like']+table_mi['coins']*2+table_mi['favorite']*3+table_mi['share']*4)/table_mi['view']*100

mi_L = (table_mi.groupby('author')['L'].sum()/table_mi.groupby('author')['datetime'].count()).reset_index()
mi_L.columns = ['author','L']
mi_L = round(mi_L,2)

mi_IFL = pd.merge(mi_F_I,mi_L,on = 'author',how = 'inner')
mi_IFL['partition'] = '星海'
mi_IFL = mi_IFL[['partition','author','I','F','L']]

mi_IFL.head()




#---------汽车分区IFL模型构建
#-------F值------

car_count = round(table_car.groupby('author')['datetime'].count()).reset_index() #计算发布视频的次数
car_count.columns = ['author','times'] 

car_count_5 = car_count[car_count['times']>5] #剔除掉发布视频数小于5的up主
car_count_5.info()

car_datetime_last = table_car.groupby('author')['datetime'].max()
car_datetime_late = table_car.groupby('author')['datetime'].min()
# F值 =(最晚发布日期 - 最早发布日期)/发布次数，保留整数
car_F = round((car_datetime_last-car_datetime_late).dt.days/table_car.groupby('author')['datetime'].count()).reset_index()
car_F.columns = ['author','F']
car_F = pd.merge(car_count_5,car_F,on = 'author',how = 'inner')

car_F = car_F.loc[car_F['F']>0]
car_F.describe

#------I值------

car_danmu = table_car.groupby('author')['danmu'].sum()
car_comment = table_car.groupby('author')['comment'].sum()
car_view = table_car.groupby('author')['view'].sum()
car_count = table_car.groupby('author')['datetime'].count()

# I值 = (总弹幕数+总评论数)/总播放量/统计范围内视频数量
car_I = round((car_danmu+car_comment)/car_view/car_count*100,2).reset_index()
car_I.columns = ['author','I']
car_F_I = pd.merge(car_F,car_I,on = 'author',how = 'inner')
car_F_I.head(5)
car_F_I.describe

#------L值------

# L值 = (点赞数 * 1 + 投币数 * 2 + 收藏数 * 3 + 分享数 * 4)/播放量/发布视频数
#计算每个视频的L值
table_car['L'] = (table_car['like']+table_car['coins']*2+table_car['favorite']*3+table_car['share']*4)/table_car['view']*100

car_L = (table_car.groupby('author')['L'].sum()/table_car.groupby('author')['datetime'].count()).reset_index()
car_L.columns = ['author','L']
car_L = round(car_L,2)

car_IFL = pd.merge(car_F_I,car_L,on = 'author',how = 'inner')
car_IFL['partition'] = '汽车'
car_IFL = car_IFL[['partition','author','I','F','L']]

car_IFL.head()


#---------整合所有分区的IFL模型------------
IFL = pd.concat([la_IFL,sc_IFL,ma_IFL,tec_IFL,mi_IFL,car_IFL],ignore_index=True)
print(IFL)



#-----------维度打分------------
IFL.describe()

# bins参数代表我们按照什么区间进行分组
# labels和bins切分的数组前后呼应,给每个分组打标签
# right表示了右侧区间是开还是闭，即包不包括右边的数值，如果设置成False，就代表[0,30)

IFL['I_SCORE'] = pd.cut(IFL['I'], bins=[0,0.03,0.06,0.11,1000],labels=[1,2,3,4], right=False).astype(float)
IFL['F_SCORE'] = pd.cut(IFL['F'], bins=[0,7,15,30,90,1000],labels=[5,4,3,2,1], right=False).astype(float)
IFL['L_SCORE'] = pd.cut(IFL['L'], bins=[0,3.62,7.56,15.85,1000],labels=[1,2,3,4], right=False).astype(float)

IFL.head()


#判断用户的分值是否大于平均值

IFL['I是否大于平均值'] =(IFL['I_SCORE'] > IFL['I_SCORE'].mean()) *1
IFL['F是否大于平均值'] =(IFL['F_SCORE'] > IFL['F_SCORE'].mean()) *1
IFL['L是否大于平均值'] =(IFL['L_SCORE'] > IFL['L_SCORE'].mean()) *1

IFL.head()


#客户分层（RFM经典的分层会按照R/F/M每一项指标是否高于平均值，把用户划分为8类）
#引入人群数值的辅助列，把之前判断的I\F\S是否大于均值的三个值串联起来

IFL['人群数值'] =(IFL['I是否大于平均值'] *100) +(IFL['F是否大于平均值'] *10) +(IFL['L是否大于平均值'] *1)
IFL.head()


#构建判断函数，通过判断人群数值的值，来返回对应标签
def transform_label(x):
    if x == 111:
        label = '高价值up主'
    elif x == 101:
        label = '高价值拖更up主'
    elif x == 11:
        label = '高质量内容高深up主'
    elif x == 1:
        label = '高质量内容高深拖更up主'
    elif x == 110:
        label = '接地气活跃up主'
    elif x == 10:
        label = '活跃up主'
    elif x == 100:
        label = '接地气up主'
    elif x == 0:
        label = '还在成长的up主'
    return label

#将标签分类函数应用到人群数值列

IFL['人群类型'] = IFL['人群数值'].apply(transform_label) 
IFL.head()
        

#各类用户占比
account = IFL['人群类型'].value_counts().reset_index()
account['人数占比'] = account['人群类型'] / account['人群类型'].sum()
account



#导出结果表
os.chdir(r'C:\Users\A\Desktop\项目')
writer= pd.ExcelWriter('科技区IFL模型.xlsx')
IFL.to_excel(excel_writer = writer,index=False,header=True,sheet_name='科技区IFL模型')
writer.save()