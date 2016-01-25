# coding:utf-8

import pickle
# import re
import os
import codecs

path = os.path.dirname(__file__)
file_path_read = path + '/data_files/'
file_path_write = path + '/data_files/'

in_file = codecs.open(file_path_read + 'year_aver.pkl', 'r')


# out_file = codecs.open(file_path_write + 'shuiping_aver.txt', 'w', 'utf-8')

#
#
# host, port = '192.168.3.150', 27017
# conn = pymongo.MongoClient(host, port)
# # sheet = conn['xunying_match']['resume-train'] #训练集
# sheet = conn['xunying_match']['test4']   #测试集
# sheet1 = conn['xunying_match']['resume-train']


def get_salary(salary_flag):
    salary = 0
    if salary_flag == 0:
        salary = 1000
    if salary_flag == 1:
        salary = 3000
    if salary_flag == 2:
        salary = 5000
    if salary_flag == 3:
        salary = 7000
    if salary_flag == 4:
        salary = 9000
    if salary_flag == 5:
        salary = 15000
    if salary_flag == 6:
        salary = 20000
    return salary


def get_year(year_str):
    year = 0
    if year_str == u'至今' or year_str == u'今' or year_str == u'Present':
        year_str = u'2015-11'
    if year_str is None or not year_str:
        return year
    year, month = int(year_str.split('-')[0]), int(year_str.split('-')[1])
    if month > 7 and year != 2015:
        year += 1
    return year


year_sala_dict = pickle.load(in_file)


def get_level_aver(year, salary):
    aver = year_sala_dict[year]
    shuiping = float(salary) / aver
    return aver, shuiping

# for doc in sheet1.find():
#     workExp_list = doc['workExperienceList']
#     for work in workExp_list:
#         year = get_year(work['end_date'])
#         if year == 0:
#             year = 2012
#         elif year <= 1999:
#             year = 1999
#         # except:
#         #     a= 0
#         salary = get_salary(work['salary'])
#         shuiping = float(salary) / (year_sala_dict[year])
#         out_file.write(str(shuiping) + '\t' + '\t')
#     out_file.write('\n')
# out_file.close()
