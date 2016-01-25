# coding:utf-8
import pickle
import codecs
import os
import numpy as np
# import common_data_deal
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

path = os.path.dirname(__file__)

infile1 = codecs.open(path + '/datafile/size_predict.txt', 'r', 'utf-8')
infile2 = codecs.open(path + '/datafile/size_predict2.txt', 'r', 'utf-8')
pickleFile1 = file(path + '/datafile/rfSizeProb.pkl')
rfProb = pickle.load(pickleFile1)
pickleFile2 = file(path + '/datafile/gbdtSizeProb.pkl')
gbdtProb = pickle.load(pickleFile2)
outFiles = codecs.open('merged_salary2.txt', 'w', 'utf-8')

feature = {}
tarList = []

lines1 = infile1.readlines()
lines2 = infile2.readlines()

lines1End = lines1[-2:]
lines2End = lines2[-2:]


# idList = []
# def getpreDic(line):
#     outDic = {}
#     sections = line.split('\t')[1:]
#     for section in sections:
#         posiName,pre = section.split(':')
#         posiNum = common_data_deal.get_position_num(posiName)
#         if pre=='nan': pre=0.0
#         else: pre = float(pre)
#         outDic[posiNum] = pre
#     return outDic

def get_feature(feature_dict):
    tmp = 0
    gbdt_po_list, rf_po_list, high_list, dip_list = [], [], [], []

    for j in range(len(lines1) - 4):
        rf_po, answer1 = lines1[j].strip().split('\t')
        gbdt_po, answer2 = lines2[j].strip().split('\t')
        gbdt_po = int(gbdt_po)
        rf_po = int(rf_po)
        high = rfProb[j, rf_po - 1] > gbdtProb[j, gbdt_po - 1]
        dip = rfProb[j, rf_po - 1] - gbdtProb[j, gbdt_po - 1]
        answer2 = int(answer2)
        dip_list.append(dip)
        high_list.append(high)
        gbdt_po_list.append(gbdt_po)
        rf_po_list.append(rf_po)
        tarList.append(answer2)
        # idList.append(idStr)
    feature_dict['high'] = high_list
    feature_dict['gbPo'] = gbdt_po_list
    feature_dict['rfPo'] = rf_po_list
    feature_dict['dip'] = dip_list
    for k in range(rfProb.shape[1]):
        feature[str(k)] = list(rfProb[:, k])
    for n in range(gbdtProb.shape[1]):
        tmp = n + k
        feature[str(tmp)] = list(gbdtProb[:, n])
    for m in range(gbdtProb.shape[1]):
        tmp3 = tmp + 1
        feature[str(tmp3)] = list(gbdtProb[:, m] + rfProb[:, m])
    m_feature = pd.DataFrame(feature_dict)
    return m_feature


if __name__ == '__main__':
    n_feature = get_feature(feature)
    target = np.array(tarList)
    # idList = np.array(idList)
    tt = []
    for i in range(20000):
        tt.append(i % 20)
    n_feature['is_train'] = tt
    rightAll = 0
    for i in range(20):
        train, test = n_feature[n_feature['is_train'] != i], n_feature[n_feature['is_train'] == i]
        tmp1 = np.array([t != i for t in n_feature['is_train']])
        tmp2 = np.array([t == i for t in n_feature['is_train']])
        trainTar, testTar = target[tmp1], target[tmp2]
        # testId = idList[tmp2]
        clf = RandomForestClassifier(n_estimators=100, min_samples_split=17)  # (max_features=0.5)
        features = n_feature.columns[:-1]
        clf.fit(train[features], trainTar)
        preds = clf.predict(test[features])
        right = 0
        for p in range(len(preds)):
            if preds[p] == testTar[p]:
                right += 1.0
                rightAll += 1.0
            outFiles.write(str(preds[p]) + '\t' + str(testTar[p]) + '\n')
        print right / len(preds)
    outFiles.close()
    print rightAll / 20000
