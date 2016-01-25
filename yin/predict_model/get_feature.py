# coding:utf-8

import json
import os
import numpy as np
import pickle
from yin.data_deal import common_data_deal as dl
from yin.data_deal.format_name import format_name
from yin.data_deal import salary_feature
from yin.data_deal.get_shuiping_aver import get_level_aver
from yin.data_deal import feature as fe

path = os.path.dirname(__file__) + '/data_set/'

trainFile1 = open(path + 'practice.json', 'r')
testFile1 = open(path + 'test.json', 'r')

'''
得到预测时所用的所有feature
以dic形式返回，每个value对就一维特征
'''

idList, genderList, ageList, degreeList = [], [], [], []
name3List, name1List, name2List, nameNList = [], [], [], []
Size3List, Size1List, Size2List, SizeNList, = [], [], [], []
year1, year2, year3, yearN = [], [], [], []
time1, time2, time3, time4 = [], [], [], []
salary1List, salary2List, salary3List, salaryNList = [], [], [], []
lv1List, lv3List, aver1List, aver3List = [], [], [], []
ind0Num, ind2Num = [], []
salaryLv1List, salaryLv3List, yearSalary1List, yearSalary3List = [], [], [], []
industry1Num, industry3Num = [], []
featureMat = []
firstAgeList = []
lengthList = []
majorClassList, majorNumList = [], []
feature = {}


def merge_feature(data_file):
    tmp_n = 0
    # 定义特征list
    # 逐样本提取特征
    for doc in data_file:
        tmp_n += 1
        if tmp_n == 100000:
            break
        doc = json.loads(doc)
        id_str = str(doc['_id']['$oid'])
        idList.append(id_str)
        ageList.append(dl.age_deal(doc['age']))
        genderList.append(dl.get_gender(doc['gender']))
        major_str = doc['major']
        if not major_str or major_str.strip() == u'None':
            major_str = u'0'
        majorClassList.append(dl.get_major_calss(major_str))
        majorNumList.append(dl.get_major_num(major_str))
        work_expList = doc['workExperienceList']
        name1 = format_name(work_expList[0]['position_name'])
        name1List.append(dl.get_position_num(name1))
        name3 = format_name(work_expList[2]['position_name'])
        name3List.append(dl.get_position_num(name3))
        nameNList.append(dl.get_position_num(format_name(work_expList[-1]['position_name'])))
        Size1List.append(int(work_expList[0]['size']))
        Size3List.append(int(work_expList[2]['size']))
        SizeNList.append(int(work_expList[-1]['size']))
        salary1List.append(int(work_expList[0]['salary']))
        salary3List.append(int(work_expList[2]['salary']))
        salaryNList.append(int(work_expList[-1]['salary']))
        ind1_str = work_expList[0]['industry']
        if not ind1_str:
            ind1_str = 'Null'
        ind1_num = dl.get_industry_num(ind1_str.strip())
        industry1Num.append(ind1_num)
        ind3_str = work_expList[2]['industry']
        if not ind3_str:
            ind3_str = 'Null'
        ind3_num = dl.get_industry_num(ind3_str.strip())
        industry3Num.append(ind3_num)
        if work_expList[1]:
            degreeList.append(int(doc['degree']))
            name2List.append(dl.get_position_num(format_name(work_expList[1]['position_name'])))
            Size2List.append(int(work_expList[1]['size']))
            salary2List.append(int(work_expList[1]['salary']))
        else:
            work_expList[1] = {}
            work_expList[1]['position_name'] = 'no name'
        time1.append(dl.time_deal(work_expList[0]['start_date'], work_expList[0]['end_date']))
        time2.append(dl.time_deal(work_expList[2]['end_date'], work_expList[0]['start_date']))
        time3.append(dl.time_deal(work_expList[2]['start_date'], work_expList[2]['end_date']))
        time4.append(dl.time_deal(work_expList[-1]['start_date'], work_expList[0]['end_date']))
        tem_year1 = dl.get_year(work_expList[0]['end_date'])
        tem_year3 = dl.get_year(work_expList[2]['end_date'])
        tem_yearn = dl.get_year(work_expList[-1]['start_date'])
        year1.append(tem_year1)
        year2.append(dl.get_year(work_expList[0]['start_date']))
        year3.append(tem_year3)
        yearN.append(tem_yearn)
        firstAgeList.append(dl.get_frist_age(dl.age_deal(doc['age']), tem_yearn))
        ind0_str = work_expList[0]['industry']
        if not ind0_str:
            ind0_str = 'Null'
        ind0Num.append(dl.get_industry_num(ind0_str.strip()))
        ind2_Str = work_expList[2]['industry']
        if not ind2_Str:
            ind2_Str = 'Null'
        ind2Num.append(dl.get_industry_num(ind2_Str.strip()))
        salary_lv1, year_salary1 = salary_feature.get_sala_feature(name1, tem_year1, int(work_expList[0]['salary']))
        salary_lv3, year_salary3 = salary_feature.get_sala_feature(name3, tem_year3, int(work_expList[2]['salary']))
        salaryLv1List.append(salary_lv1)
        salaryLv3List.append(salary_lv3)
        yearSalary1List.append(year_salary1)
        yearSalary3List.append(year_salary3)

        aver1, lv1 = get_level_aver(tem_year1, int(work_expList[0]['salary']))
        aver3, lv3 = get_level_aver(tem_year3, int(work_expList[2]['salary']))
        lv1List.append(lv1)
        lv3List.append(lv3)
        aver1List.append(aver1)
        aver3List.append(aver3)
        name_list = [format_name(name) for name in [work_expList[i]['position_name'] for i in range(len(work_expList))]]
        name_list.pop(1)
        feature_line = fe.get_matrix(name_list)
        featureMat.append(np.array(feature_line))
        lengthList.append(len(work_expList))
        get_feature_dict(work_expList, feature)


# 将样本放入feature字典
def get_feature_dict(work_expList, my_feature):
    my_feature['id'] = idList
    my_feature['age'] = ageList
    my_feature['gender'] = genderList
    my_feature['majorClass'] = majorClassList
    my_feature['majorNum'] = majorNumList

    my_feature['comSize1'] = Size1List
    my_feature['comSize3'] = Size3List
    my_feature['comSizeN'] = SizeNList

    my_feature['posi1List'] = name1List
    my_feature['posi3List'] = name3List
    my_feature['posiNList'] = nameNList

    my_feature['salary1'] = salary1List
    my_feature['salary3'] = salary3List
    my_feature['salaryN'] = salaryNList
    if work_expList[1]['position_name'] != 'no name':
        my_feature['degree'] = degreeList
        my_feature['comSize2'] = Size2List
        my_feature['posi2List'] = name2List
        my_feature['salary2'] = salary2List

    my_feature['year1'] = year1
    my_feature['year2'] = year2
    my_feature['year3'] = year3
    my_feature['yearN'] = yearN

    my_feature['time1'] = time1
    my_feature['time2'] = time2
    my_feature['time3'] = time3
    my_feature['time4'] = time4

    my_feature['level1'] = lv1List
    my_feature['level3'] = lv3List
    my_feature['aver1'] = aver1List
    my_feature['aver3'] = aver3List

    my_feature['industry1Num'] = industry1Num
    my_feature['industry3Num'] = industry3Num

    my_feature['salaryLv1List'] = salaryLv1List
    my_feature['salaryLv3List'] = salaryLv3List
    my_feature['yearSalary1List'] = yearSalary1List
    my_feature['yearSalary3List'] = yearSalary3List

    feature_mat_list = np.array(featureMat)
    for i in range(feature_mat_list.shape[1]):
        my_feature[str(i)] = list(feature_mat_list[:, i])

    my_feature['firstAge'] = firstAgeList
    my_feature['lengthList'] = lengthList
    return my_feature


if __name__ == '__main__':
    print '将进行训练样本特征的提取'
    trainFeature = merge_feature(trainFile1)
    print '训练样本特征提取完成\n将进行测试样本特征的提取'
    testFeature = merge_feature(testFile1)
    print '测试样本特征提取完成\n将进行特征存储'
    feature_pkl = file('feature_pkl.pkl', 'w')
    pickle.dump((trainFeature, testFeature), feature_pkl)
    feature_pkl.close()
    print '特征存储结束'
