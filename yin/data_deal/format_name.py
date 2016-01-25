# coding:utf-8

import os
import codecs
import jieba
import pickle


path = os.path.dirname(__file__)
file_path_read = path + '/data_files/'
file_path_write = path + '/data_files/'

expand_file = codecs.open(file_path_read + 'expand_word.pkl', 'r')
posi_file = codecs.open(file_path_read + 'position_dict.pkl', 'r')
position_dict_file = codecs.open(file_path_read + 'all_posi_dict.pkl', 'r')
expand_file_2 = codecs.open(file_path_read + 'expand_word_1.pkl', 'r')
zhuanyuan_file = codecs.open(file_path_read + 'zhuanyuan_set.pkl', 'r')
jingli_file = codecs.open(file_path_read + 'jingli_set.pkl', 'r')
zongjian_file = codecs.open(file_path_read + 'zongjian_set.pkl', 'r')
posi_file1 = codecs.open(file_path_read + 'position_set.pkl', 'r')
posi_file2 = codecs.open(file_path_read + 'position_set1.pkl', 'r')
sp_posi_file = codecs.open(file_path_read + 'special_dict.pkl', 'r')

jieba.load_userdict(file_path_read + 'position_dict_new.txt')

position_dict = pickle.load(posi_file)  # 职位对应的扩充词
posi_set = pickle.load(position_dict_file)  # 职位中最直接的匹配词
expand_dict = pickle.load(expand_file)  # 经理、总监、专员的扩充词字典
jingli_set = pickle.load(jingli_file)  # 经理扩充词
zongjian_set = pickle.load(zongjian_file)  # 总监扩充词
zhuanyuan_set = pickle.load(zhuanyuan_file)  # 专员扩充词
expand_word_dict = pickle.load(expand_file_2)  # 匹配后是其他对应的大分类字典
position_set1 = pickle.load(posi_file1)  # 第一个职位字典扩充词
position_set2 = pickle.load(posi_file2)  # 第二个职位字典扩充词
special_posi_dict = pickle.load(sp_posi_file)


def format_name(position):
    global each_position_name
    global position_name
    if position in special_posi_dict:
        position_name = special_posi_dict[position]
        return position_name
    else:
        position_list = list(jieba.cut(position.upper()))
        position_cut_set = set(position_list)
    i = 0
    for position_key, position_value in position_dict.items():
        inter_word = posi_set & position_cut_set
        if not inter_word:
            inter_position = position_value & position_cut_set
            if not inter_position:
                i += 1
                if i < len(position_dict):
                    continue
            if len(inter_position) != 0:
                each_position_name = position_key
                break
            if len(inter_position) == 0:
                each_position_name = u'其他'
                position_name = each_position_name
        if inter_word and not inter_word & position_value:
            continue
        if inter_word and inter_word & position_value:
            each_position_name = position_key
    if each_position_name in position_set1:
        position_name = each_position_name
    if each_position_name in position_set2:
        if (each_position_name != u'客服' and each_position_name != u'后勤' and
                each_position_name != u'人力资源' and each_position_name != u'采购'):
            position_name = withzongjian(position_cut_set)
        if each_position_name == u'采购':
            position_name = withoutzhuanyuan(position_cut_set)
        if each_position_name == u'客服':
            position_name = withoutzongjian_and_zhuanyuan(position_cut_set)
        if each_position_name == u'后勤':
            position_name = withzhuguan(position_cut_set)
        if each_position_name == u'人力资源':
            position_name = withoutzongjian(position_cut_set)
    if position_name == u'其他':
        position_name = deal_others(position)
    return position_name


def withzongjian(position_cut_set):
    global position_name
    j = 0
    for expand_key, expand_value in expand_dict.items():
        inter_expand = expand_value & position_cut_set
        if not inter_expand:
            j += 1
            if j < len(expand_dict):
                continue
        if inter_expand & zhuanyuan_set:
            each_position_post_name = expand_key
            position_name = each_position_name + each_position_post_name
            break
        if inter_expand & jingli_set:
            if position_cut_set & zhuanyuan_set:
                continue
            each_position_post_name = expand_key
            position_name = each_position_name + each_position_post_name
            break
        if inter_expand & zongjian_set:
            if position_cut_set & zhuanyuan_set:
                continue
            each_position_post_name = expand_key
            position_name = each_position_name + each_position_post_name
            break
        if len(inter_expand) == 0:
            position_name = each_position_name + u'专员'
    return position_name


def withoutzhuanyuan(position_cut_set):
    global position_name
    p = 0
    for expand_key, expand_value in expand_dict.items():
        inter_expand = expand_value & position_cut_set
        if not inter_expand:
            p += 1
            if p < len(expand_dict):
                continue
        if inter_expand & zhuanyuan_set:
            position_name = each_position_name + u'助理'
            break
        if inter_expand & jingli_set:
            if position_cut_set & zhuanyuan_set:
                continue
            each_position_post_name = expand_key
            position_name = each_position_name + each_position_post_name
            break
        if inter_expand & zongjian_set:
            if position_cut_set & zhuanyuan_set:
                continue
            each_position_post_name = expand_key
            position_name = each_position_name + each_position_post_name
            break
        if len(inter_expand) == 0:
            position_name = each_position_name + u'助理'
    return position_name


def withoutzongjian_and_zhuanyuan(position_cut_set):
    global position_name
    m = 0
    for expand_key, expand_value in expand_dict.items():
        inter_expand = expand_value & position_cut_set
        if not inter_expand:
            m += 1
            if m < len(expand_dict):
                continue
        if inter_expand & zhuanyuan_set:
            position_name = each_position_name
            break
        if inter_expand & jingli_set or inter_expand & zongjian_set:
            if position_cut_set & zhuanyuan_set:
                continue
            position_name = each_position_name + u'经理'
            break
        if len(inter_expand) == 0:
            position_name = each_position_name
    return position_name


def withzhuguan(position_cut_set):
    global position_name
    n = 0
    for expand_key, expand_value in expand_dict.items():
        inter_expand = expand_value & position_cut_set
        if not inter_expand:
            n += 1
            if n < len(expand_dict):
                continue
        if inter_expand & zhuanyuan_set:
            each_position_post_name = expand_key
            position_name = each_position_name + each_position_post_name
            break
        if inter_expand & jingli_set or inter_expand & zongjian_set:
            if position_cut_set & zhuanyuan_set:
                continue
            position_name = each_position_name + u'主管'
            break
        if len(inter_expand) == 0:
            position_name = each_position_name + u'专员'
    return position_name


def withoutzongjian(position_cut_set):
    global position_name
    l = 0
    for expand_key, expand_value in expand_dict.items():
        inter_expand = expand_value & position_cut_set
        if not inter_expand:
            l += 1
            if l < len(expand_dict):
                continue
        if inter_expand & zhuanyuan_set:
            each_position_post_name = expand_key
            position_name = each_position_name + each_position_post_name
            break
        if inter_expand & jingli_set or inter_expand & zongjian_set:
            if position_cut_set & zhuanyuan_set:
                continue
            position_name = each_position_name + u'经理'
            break
        if len(inter_expand) == 0:
            position_name = each_position_name + u'专员'
    return position_name


def deal_others(position_cut_set):
    global position_name
    i = 0
    for word_key, word_value in expand_word_dict.items():
        inter_position = word_value & position_cut_set
        if not inter_position:
            i += 1
            if i < len(expand_word_dict):
                continue
        if expand_word_dict[u'助理类'] & inter_position:
            position_name = u'助理类'
            pass
        elif len(inter_position) != 0:
            if expand_word_dict[u'助理类'] & inter_position:
                position_name = u'助理类'
                break
            position_name = word_key
            pass
        elif len(inter_position) == 0:
            position_name = u'其他'
            pass
    return position_name

# 输出全部工作
# def main():
#     for doc in sheet.find():
#         workExper = doc['workExperienceList']
#         posi_list = [work['position_name'] for work in workExper]
#         for posi in posi_list:
#             position_name = format_name(posi)
#             out_file.write(position_name + '\t')
#         out_file.write('\n')
#     out_file.close()

# 输出第二份工作
# def main():
#     for doc in sheet.find():
#         workExper = doc['workExperienceList']
#         posi_list = [work['position_name'] for work in workExper]
#         position_name = format_name(posi_list[1])
#         out_file.write(position_name + '\t')
#         out_file.write('\n')
#     out_file.close()


#
# if __name__ == '__main__':
#     main()
