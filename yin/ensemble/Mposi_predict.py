# coding = utf-8

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
import pandas as pd
import numpy as np
import codecs
import os
from yin.data_deal import common_data_deal as dl
import pickle
# import xgboost as xgb

path = os.path.dirname(__file__) + '/predictFile/'

outFile1 = codecs.open(path + 'posi_rf.txt', 'w', 'utf-8')
outFile2 = codecs.open(path + 'posi_gbdt.txt', 'w', 'utf-8')
outPkl1 = file(path + 'rfPosiProb.pkl', 'w')
outPkl2 = file(path + 'gbdtPosiProb.pkl', 'w')
inPklFile = file('feature_pkl.pkl', 'r')
trainFeatureAll, testFeatureAll = pickle.load(inPklFile)
# answer = pickle.load(answerFile)
feature_num = [str(i) for i in range(40)]
feature_str = ['age', 'gender', 'comSize1', 'comSize3', 'comSizeN', 'salary1', 'salary3',
               'time1', 'time2', 'time3', 'time4', 'yearN', 'firstAge', 'posi1List',
               'lengthList', 'lv1', 'lv3', 'aver1', 'aver3', 'year2',
               'industry1Num', 'industry3Num', 'salaryLv1List', 'salaryLv3List',
               'yearSalary1List', 'yearSalary3List'] + feature_num


def merge_feature(all_feature):
    train_feature = {}
    # testFeature = {}
    for string in all_feature:
        train_feature[string] = trainFeatureAll[string]
        # testFeature[str] = testFeatureAll[str]
    train_feature = pd.DataFrame(train_feature)
    # testFeature = pd.DataFrame(testFeature)
    train_id_list = trainFeatureAll['id']
    # testIdList = testFeatureAll['id']
    train_tar_list = trainFeatureAll['posi2List']
    return train_feature, train_id_list, train_tar_list


if __name__ == '__main__':
    trainFeatureR, trainIdListR, trainTarListR = merge_feature(feature_str)
    tmp = [t < 32 for t in trainTarListR]
    tmp = np.array(tmp)
    trainFeatureR = trainFeatureR[tmp]
    targetR = np.array(trainTarListR)
    targetR = targetR[tmp]
    trainIdListR = np.array(trainIdListR)
    trainIdListR = trainIdListR[tmp]
    Cfeature = trainFeatureR.columns[:]

    tt = []
    rfPro, gbPro = [], []
    tmp = []
    for i in range(len(trainFeatureR)):
        tt.append(i % 5)
    i = 4
    tmp1 = np.array([t != i for t in tt])
    tmp2 = np.array([t == i for t in tt])
    trainFeature, testFeature = trainFeatureR[tmp1], trainFeatureR[tmp2]
    trainTar, testTar = targetR[tmp1], targetR[tmp2]
    trainId, testId = trainIdListR[tmp1], trainIdListR[tmp2]
    clf = RandomForestClassifier(n_estimators=200, min_samples_split=17)
    clf.fit(trainFeature[Cfeature], trainTar)
    preds = clf.predict(testFeature)
    predPro = clf.predict_proba(testFeature)
    rfPro = predPro
    right = 0
    for n in range(len(preds)):
        preName = dl.get_num_position(preds[n])
        real = dl.get_num_position(testTar[n])
        if preName == real:
            right += 1.0
        outFile1.write(str(testId[n]) + '\t' + preName + '\t' + real + '\n')
    print right / (len(trainFeatureR) / 5.0)
    pickle.dump(rfPro, outPkl1)

    i = 4
    print i
    tmp1 = np.array([t != i for t in tt])
    tmp2 = np.array([t == i for t in tt])
    trainFeature, testFeature = trainFeatureR[tmp1], trainFeatureR[tmp2]
    trainTar, testTar = targetR[tmp1], targetR[tmp2]
    trainId, testId = trainIdListR[tmp1], trainIdListR[tmp2]
    clf = GradientBoostingClassifier(n_estimators=6, min_samples_split=17)
    clf.fit(trainFeature[Cfeature], trainTar)
    preds = clf.predict(testFeature)
    predPro = clf.predict_proba(testFeature)
    gbPro = predPro
    for n in range(len(preds)):
        preName = dl.get_num_position(preds[n])
        real = dl.get_num_position(testTar[n])
        if preName == real:
            right += 1.0
        outFile2.write(testId[n] + '\t' + preName + '\t' + real + '\n')
    print right / (70000 / 5.0)
    pickle.dump(predPro, outPkl2)
outPkl1.close()
outPkl2.close()
outFile1.close()
outFile2.close()
