## 项目概况
### 分析目的
本项目通过对2019年科技区发布的所有视频进行分析，在RFM模型的基础上，尝试使用更符合b站特性的IFL模型，挑选出视频质量高，值得关注的up主。
### 数据来源
分析数据均基于bilibili 网站上的公开信息，主要有以下数据维度：  
2019年度，科技区播放量超过5w视频的**分区名称、作者名称、作者id、发布时间、播放数、硬币数、弹幕数、收藏数、点赞数、分享数、评论数**，共计50130行。

## 数据概览
### 数据表
![数据概况](https://github.com/faat17/fantian/blob/master/image/shuju.jpg) 
**关键指标解释**  
coins：投硬币数  
danmu：弹幕数  
favorite：收藏数  
like：点赞数  
comment：评论数  
share：分享数  
view：播放量  

### 各字段数量统计
![字段统计](https://github.com/faat17/fantian/blob/master/image/字段统计.jpg) 

### 缺失值统计
![缺失值](https://github.com/faat17/fantian/blob/master/image/缺失值.jpg) 

## 数据清洗
### 删除空值和重复值

```python
table_view = table_view.dropna() #删除空值
table_view = table_view.drop_duplicates() #删除重复值
```

![删除重复值](https://github.com/faat17/fantian/blob/master/image/删除重复值.jpg)  
共删除1330行数据，剩余数据量**48799**行

### 提取构建模型所需的指标
```python
table_view = table_view[['partition','author','datetime','view','danmu','comment','like','coins','favorite','share']] #提取指标
```

## 数据建模
RFM模型是衡量客户价值和客户创利能力的重要工具和手段。在众多的客户关系管理(CRM)的分析模式中，RFM模型是被广泛提到的。通过一个客户近期购买行为、购买的总体频率以及消费金额三项指标来描述客户的价值状况。  
R：最近一次消费时间（最近一次消费到参考时间的间隔）  
F：消费的频率(消费了多少次）  
M：消费的金额 （总消费金额）  
但RFM模型并不能评价视频的质量，所以在这里针对up主的视频信息构建了IFL模型，以评估视频的质量。  

**I(Interaction_rate)：**
I值反映的是平均每个视频的互动率，互动率越高，表明其视频更能产生用户的共鸣，使其有话题感。  
**I = （总弹幕数+总评论数） / 总播放量 / 统计范围内视频数量**  

**F(Frequence)：**
F值表示的是每个视频的平均发布周期，每个视频之间的发布周期越短，说明内容生产者创作视频的时间也就越短，创作时间太长，不是忠实粉丝的用户可能将其遗忘。
**F = （统计时间内最晚发布视频时间-最早发布视频时间）/ 发布视频数量**  

**L(Like_rate)：**
L值表示的是统计时间内发布视频的平均点赞率，越大表示视频质量越稳定，用户对up主的认可度也就越高。
**L = （点赞数*1+投币数*2+收藏数*3+分享数*4）/ 播放量 / 发布视频数**

### 对科技区进行分区
根据不同的分区进行IFL打分，这里以数据量最多的**社科人文**为例
![分区](https://github.com/faat17/fantian/blob/master/image/分区.jpg)
```python
table_sc = table_view.loc[table_view['partition']=='科学科普']
table_la = table_view.loc[table_view['partition']=='社科人文']
table_ma = table_view.loc[table_view['partition']=='机械']
table_tec = table_view.loc[table_view['partition']=='野生技术协会']
table_mi = table_view.loc[table_view['partition']=='星海'] # 一般发布军事内容
table_car = table_view.loc[table_view['partition']=='汽车']
```
