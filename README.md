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
```python```
table_view = table_view.dropna() #删除空值
table_view = table_view.drop_duplicates() #删除重复值
```
![删除重复值](https://github.com/faat17/fantian/blob/master/image/删除重复值.jpg)  
共删除1330行数据，剩余数据量48799行
