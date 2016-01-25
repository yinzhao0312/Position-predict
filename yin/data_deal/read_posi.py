# coding:utf-8
import codecs

inFile1 = codecs.open('merged_Posi.txt', 'r')
inFile2 = codecs.open('merged_Posi2.txt', 'r')
outFile = codecs.open('aaaa.txt', 'w')

lines1 = inFile1.readlines()
lines2 = inFile2.readlines()

dic = {}
for line in lines1:
    id_str, posi1, posi2 = line.strip().split('\t')
    dic[id_str] = posi1
for line in lines2:
    id_str, posi1, posi2 = line.strip().split('\t')
    dic[id_str] = posi1
for k, v in dic.items():
    outFile.write(k + '\t' + v + '\n')
