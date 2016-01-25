# coding:utf-8

import pickle
import codecs
import os
import numpy as np
from yin.data_deal import common_data_deal as dl
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

path = os.path.dirname(__file__)
path2 = os.path.abspath(os.path.join(os.path.dirname("__file__"), os.path.pardir)) + '/predict_code/predictFile/'

infile1 = codecs.open(path + '/predictFile/posi_gbdt.txt', 'r', 'utf-8')
infile2 = codecs.open(path + '/predictFile/posi_rf.txt', 'r', 'utf-8')
pickleFile1 = file(path + '/predictFile/gbdtPosiProb.pkl')
TrfProb = pickle.load(pickleFile1)
pickleFile2 = file(path + '/predictFile/rfPosiProb.pkl')
TgbdtProb = pickle.load(pickleFile2)
outFiles = codecs.open('merged_posi.txt', 'w', 'utf-8')

# Einfile1 = codecs.open(path2+'posi_gbdt.txt', 'r', 'utf-8')
# Einfile2 = codecs.open(path2+'posi_rf.txt', 'r', 'utf-8')

feature = {}
tarList = []

Tlines1 = infile1.readlines()
Tlines2 = infile2.readlines()
# Elines1 = Einfile1.readlines()
# Elines2 = Einfile2.readlines()

idList = []


def get_feature(lines1, lines2, rf_prob, gbdt_prob):
    tmp = 0
    gbdt_po_list, rf_po_list, high_list, dip_list = [], [], [], []

    for p in range(len(lines1) - 3):
        # idStr,idStr = '1','1'
        id_str, gbdt_posi, answer1 = lines1[p].strip().split('\t')
        id_str, rf_posi, answer2 = lines2[p].strip().split('\t')
        gbdt_posi = dl.get_position_num(gbdt_posi)
        rf_posi = dl.get_position_num(rf_posi)
        answer2 = dl.get_position_num(answer2)
        gbdt_po_list.append(gbdt_posi)
        rf_po_list.append(rf_posi)
        high = rf_prob[p, rf_posi] > gbdt_prob[p, gbdt_posi]
        dip = rf_prob[p, rf_posi] - gbdt_prob[p, gbdt_posi]
        high_list.append(high)
        dip_list.append(dip)
        tarList.append(answer2)
        idList.append(id_str)
    feature['high'] = high_list
    feature['dip'] = dip_list
    feature['gbPo'] = gbdt_po_list
    feature['rfPo'] = rf_po_list
    for j in range(rf_prob.shape[1]):
        feature[str(j)] = list(rf_prob[:, j])
    for k in range(gbdt_prob.shape[1]):
        tmp = k + j
        feature[str(tmp)] = list(gbdt_prob[:, t])
    for m in range(gbdt_prob.shape[1]):
        tmp3 = tmp + 1
        feature[str(tmp3)] = list(gbdt_prob[:, m] + rf_prob[:, m])
    m_feature = pd.DataFrame(feature)
    return m_feature


if __name__ == '__main__':
    tFeature = get_feature(Tlines1, Tlines2, TrfProb, TgbdtProb)
    eFeature = get_feature(Tlines1, Tlines2, TrfProb, TgbdtProb)
    target = np.array(tarList)
    idList = np.array(idList)
    tt = []
    for i in range(20000):
        tt.append(i % 15)
    tFeature['is_train'] = tt
    rightAll = 0
    for i in range(15):
        print i
        train, test = tFeature[tFeature['is_train'] != i], tFeature[tFeature['is_train'] == i]
        tmp1 = np.array([t != i for t in tFeature['is_train']])
        tmp2 = np.array([t == i for t in tFeature['is_train']])
        trainTar, testTar = target[tmp1], target[tmp2]
        testId = idList[tmp2]
        clf = RandomForestClassifier(n_estimators=200, min_samples_split=13)  # ,max_depth=35,max_features=0.4)
        features = tFeature.columns[:-1]
        clf.fit(train[features], trainTar)
        preds = clf.predict(test[features])
        right = 0
        for n in range(len(preds)):
            if preds[n] == testTar[n]:
                right += 1.0
                rightAll += 1.0
            outFiles.write(
                testId[n] + '\t' + dl.get_num_position(preds[n]) + '\t' + dl.get_num_position(testTar[n]) + '\n')
        print right / len(preds)
    outFiles.close()
    print rightAll / 20000
