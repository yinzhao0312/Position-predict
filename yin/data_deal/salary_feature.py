# coding:utf-8

import os
import codecs
import pickle

path = os.path.abspath(os.path.join(os.path.dirname("__file__"), os.path.pardir))
file_path_read = path + '/data_deal/data_files/'
file_path_write = path + '/data_deal/data_files/'

in_file = codecs.open(file_path_read + 'year_sala.pkl', 'r')

year_sala_dict = pickle.load(in_file)


def get_aver_sala(real_posi, real_year):
    n = 0
    aver_sala = 0
    for posi, year_sala in year_sala_dict.items():
        if posi != real_posi:
            n += 1
            if n < len(year_sala_dict):
                continue
        if posi == real_posi:
            n += 1
            if real_year in year_sala.keys():
                sala_list = year_sala_dict[real_posi][real_year]
                sala_list_sort = sorted(sala_list)
                if len(sala_list) % 2 == 1:
                    aver_sala = sala_list_sort[len(sala_list) / 2]
                    break
                else:
                    aver_sala = ((sala_list_sort[len(sala_list) / 2] +
                                  sala_list_sort[len(sala_list) / 2 - 1]) / 2)
                    break
            if real_year not in year_sala.keys():
                real_year_new = year_sala.keys()[0]
                min_value = real_year - real_year_new
                for year in year_sala.keys():
                    chazhi = abs(year - real_year)
                    if chazhi < min_value:
                        min_value = chazhi
                        real_year_new = year
                sala_list = year_sala_dict[real_posi][real_year_new]
                sala_list_sort = sorted(sala_list)
                if len(sala_list) % 2 == 1:
                    aver_sala = sala_list_sort[len(sala_list) / 2]
                else:
                    aver_sala = ((sala_list_sort[len(sala_list) / 2] +
                                  sala_list_sort[len(sala_list) / 2 - 1]) / 2)
    return aver_sala


def get_sala_feature(posi, year, salary):
    aver_sala = get_aver_sala(posi, year)
    shuiping = float(salary) / aver_sala
    return shuiping, aver_sala
