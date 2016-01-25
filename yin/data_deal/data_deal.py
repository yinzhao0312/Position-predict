# coding:utf-8

import re
import codecs
import os
import pickle

path = os.path.dirname(__file__)

major_pickle = file(path + '/data_files/major_class.pkl', 'r')
major_class = pickle.load(major_pickle)
major_pickle = file(path + '/data_files/majorRankedDic.pkl', 'r')
major_num = pickle.load(major_pickle)

model_file = codecs.open(path + '/data_files/ModelPosition.txt', 'r', 'utf-8')
model_lines = [line.strip() for line in model_file.readlines()]
industry_file = codecs.open(path + '/data_files/industry_classify.txt', 'r', 'utf-8')
industry_dic = {}
industryLines = [line.strip() for line in industry_file.readlines()]
for i in range(len(industryLines)):
    for item in industryLines[i].split('\t'):
        industry_dic[item] = i

'''
返回性别flag
'''


def get_gender(tem_gender):
    gender = True
    if tem_gender == u'男' or tem_gender == u'Male':
        return gender
    if tem_gender == u'女' or tem_gender == u'Female':
        gender = False
    return gender


'''
返回两个时间点之间的月数
'''


def time_deal(s_time, e_time):
    if e_time == u'至今' or e_time == u'今' or e_time == u'Present':
        e_time = u'2015-11'
    if s_time == u'至今' or s_time == u'今' or s_time == u'Present':
        s_time = u'2015-11'
    try:
        s_year, s_month = s_time.split('-')
        s_month_num = int(s_year) * 12 + int(s_month)
        e_year, e_month = e_time.split('-')
        e_month_num = int(e_year) * 12 + int(e_month)
    except:
        print(s_time, e_time)
        e_month_num, s_month_num = 0, 0
    m_time = e_month_num - s_month_num
    if m_time < 0:
        m_time = 0
    return m_time


'''
返回年龄
'''


def age_deal(age_str):
    age = 0
    if age_str is None:
        return age
    match = re.search(u"^\d+", age_str)
    if match:
        age = int(match.group())
    else:
        return age
    return age


'''
返回输入的年份
'''


def get_year(year_str):
    year = 0
    if year_str == u'至今' or year_str == u'今':
        year_str = u'2015-11'
    if year_str is None:
        return year
    year, month = int(year_str.split('-')[0]), int(year_str.split('-')[1])
    if month > 7 and year != 2015:
        year += 1
    return year


'''
返回首次工作的年龄
'''


def get_first_age(age, year):
    time = 2015 - year
    if time > 50 or time > age:
        return -1
    return age - time


'''
获得职位字典
'''


def get_model_position_dict():
    posi_num_dict = {}
    n = 0
    for line1 in model_lines:
        posi_num_dict[line1] = n
        n += 1
    return posi_num_dict


'''
获得position_num
'''


def get_position_num(posi_list_model):
    posi_dict = get_model_position_dict()
    for key in posi_dict:
        if key == posi_list_model:
            return posi_dict[key]
        else:
            continue


'''
由职位编号变回职位名称
'''


def get_num_position(num):
    num_posi_dict = {}
    n = 0
    for line2 in model_lines:
        num_posi_dict[n] = line2
        n += 1
    return num_posi_dict[num]


def get_industry_num(industry_str):
    if industryLines in industry_dic.keys():
        return industry_dic[industry_str]
    return -1


'''
输出专业的类别
'''


def get_major_calss(major_str):
    major_str = major_str.strip()
    if major_str in major_class:
        return major_class[major_str]
    else:
        return 2


'''
输出专业的编号
'''


def get_major_num(major_str):
    major_str = major_str.strip()
    if major_str in major_num:
        return major_num[major_str]
    else:
        return -1
