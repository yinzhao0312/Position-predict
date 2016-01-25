# 职位预测大赛 #



## 数据描述 ##

1. 训练集：7w优质简历数，标准json格式 包含字段：id，性别，年龄，专业，学历，工作经验（开始时间，结束时间，公司行业，公司规模，月薪，职位名称，部门，职位类型）
2. 测试集：2w优质简历，标准json格式 包含字段与测试集一样，只是将其中的学历抹去，至今为止的工作经历倒数第二份抹去，之所以抹去是因为这部分数据需要预测。

## 任务描述 ##

先运用训练集数据进行学习、编码与测试，挖掘出并得出职位路径的走向与规律，形成算法模型，再对测试集中置空的信息进行预测。以下为数据详情：
训练集：匿名7万优质简历数据，包含比较完整的字段，
测试集：匿名2万优质简历数据，数据中会隐藏部分信息，需要参赛者预测其中置空的数据项。置空的数据项有：

1. 学历
2. 公司规模
3. 薪水
4. 职位名称
（2-4均是求职者至今从事职位的倒数第二份职位信息，其中第四项只能预测到规定的32种职位名中去，且这32种职位名是出题方自己规整出来的职位名）

##解题思路##

1. 将题目中的问题分解成四个子问题分别进行预测
2. 对于职位名称预测时，先进行职位名规整及语义分析(多数人用的word2vec)
3. 进行特征提取（对于四个子问题进行不同的特征提取）
4. 选取模型（我主要用的rf、gbdt、xgb）
5. 进行模型融合（这个部分不太会，做的很简单）
