# coding:utf-8

# import pymongo
import codecs
import os
# import format_name

__author__ = '123'

path = os.path.abspath(os.path.join(os.path.dirname("__file__"), os.path.pardir))
file_path_read = path + '/data_deal/data_files/'
file_path_write = path + '/data_deal/data_files/'

# out_file = codecs.open(file_path_write+'featur_num.txt', 'w', 'utf-8')
model_file = codecs.open(file_path_read + 'ModelPosition.txt', 'r', 'utf-8')

# host, port = '10.0.0.54', 27017
# conn = pymongo.MongoClient(host, port)
# sheet = conn['xunying_match']['resume-train']


mode_list = model_file.readlines()
model_lines = [line.strip() for line in mode_list]


def get_feature(line_list, model_line):
    global num
    if line_list[0] != model_line and line_list[1] != model_line:
        try:
            if line_list[2] != model_line:
                num = 0
            if line_list[2] == model_line:
                num = 1
        except:
            num = 0
    if line_list[0] == model_line and line_list[1] != model_line:
        try:
            if line_list[2] != model_line:
                num = 2
            if line_list[2] == model_line:
                num = 5
        except:
            num = 2
    if line_list[0] != model_line and line_list[1] == model_line:
        try:
            if line_list[2] != model_line:
                num = 4
            if line_list[2] == model_line:
                num = 6
        except:
            num = 4
    if line_list[0] == model_line and line_list[1] == model_line:
        try:
            if line_list[2] != model_line:
                num = 3
            if line_list[2] == model_line:
                num = 7
        except:
            num = 3
    return num


def get_matrix(line_list):
    num_matrix = []
    for model_line in model_lines:
        model_line = model_line.strip()
        num1 = get_feature(line_list, model_line)
        num_matrix.append(num1)
    return num_matrix


# def main():
#     lines = [line.strip() for line in position_file.readlines()]
#     for line in lines:
#         line_list = line.split('\t')
#         line_list.pop(1)
#         num_matrix = get_matrix(line_list)
#         for num in num_matrix:
#         # for model_line in model_lines:
#         #     model_line = model_line.strip()
#         #     num = get_feature(line_list, model_line)
#         #     out_file.write(str(num) + '\t')
#             out_file.write(str(num) + '\t')
#         out_file.write('\n')
#     out_file.close()
#     a = 0
#
#
# if __name__ == '__main__':
#     main()
