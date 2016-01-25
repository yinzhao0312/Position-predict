# coding = utf-8

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
import pandas as pd
import numpy as np
import codecs
import os
from yin.data_deal import common_data_deal as dl
import pickle
import xgboost as xgb

path = os.path.dirname(__file__) + '/predictFile/'

outFile1 = codecs.open(path + 'posi_rf.txt', 'w', 'utf-8')
outFile2 = codecs.open(path + 'posi_gbdt.txt', 'w', 'utf-8')
outFile3 = codecs.open(path + 'posi_all.txt', 'w', 'utf-8')
# outPkl1 = file('rfPosiProb.pkl','w')
# outPkl2 = file('gbdtPosiProb.pkl','w')
inPklFile = file('feature_pkl.pkl', 'r')
trainFeatureAll, testFeatureAll = pickle.load(inPklFile)
feature_num = [str(i) for i in range(40)]
feature_str = ['age', 'gender', 'comSize1', 'comSize3', 'comSizeN', 'salary1', 'salary3',
               'time1', 'time2', 'time3', 'time4', 'yearN', 'firstAge', 'posi1List',
               'lengthList', 'lv1', 'lv3', 'aver1', 'aver3', 'year2',
               'industry1Num', 'industry3Num', 'salaryLv1List', 'salaryLv3List',
               'yearSalary1List', 'yearSalary3List'] + feature_num


def merge_feature(all_feature):
    train_feature = {}
    test_feature = {}
    for word in all_feature:
        train_feature[word] = trainFeatureAll[word]
        test_feature[word] = testFeatureAll[word]
    train_feature = pd.DataFrame(train_feature)
    test_feature = pd.DataFrame(test_feature)
    train_id_list = trainFeatureAll['id']
    test_id_list = testFeatureAll['id']
    train_tar_list = trainFeatureAll['degree']
    return train_feature, test_feature, train_id_list, test_id_list, train_tar_list


def train():
    posi_result = {}
    train_feature, test_feature, train_id_list, test_id_list, train_tar_list = merge_feature(feature_str)
    tmp1 = [m < 32 for m in trainTarList]
    tmp1 = np.array(tmp1)
    # train_feature = train_feature[tmp1]
    target_list = np.array(trainTarList)
    target_list = target_list[tmp1]
    # train_id_list = np.array(train_id_list)
    # train_id_list = train_id_list[tmp1]
    c_feature = trainFeature.columns[:]
    clf1 = RandomForestClassifier(n_estimators=200, min_samples_split=17)
    clf1.fit(trainFeature[c_feature], target_list)
    # rf_preds = clf1.predict(test_feature)
    rf_prob = clf1.predict_proba(test_feature)
    gbdt1 = GradientBoostingClassifier(n_estimators=150, min_samples_split=17)
    gbdt1.fit(trainFeature[c_feature], target_list)
    # gbdt_preds = gbdt1.predict(test_feature)
    gbdt_prob = gbdt1.predict_proba(test_feature)
    all_prob = rf_prob + gbdt_prob
    all_preds = []
    print all_prob.shape
    for k in range(all_prob.shape[0]):
        prob1 = list(allProb[k, :])
        ind1 = prob.index(max(prob1))
        allPreds.append(ind1)
    for j in range(len(all_preds)):
        all_pre_name = dl.get_num_position(all_preds[j])
        posi_result[test_id_list[j]] = all_pre_name
    return posi_result


if __name__ == '__main__':
    trainFeature, testFeature, trainIdList, testIdList, trainTarList = merge_feature()
    tmp = [t < 32 for t in trainTarList]
    tmp = np.array(tmp)
    trainFeature = trainFeature[tmp]
    target = np.array(trainTarList)
    target = target[tmp]
    trainIdList = np.array(trainIdList)
    trainIdList = trainIdList[tmp]
    cFeature = trainFeature.columns[:]
    clf = RandomForestClassifier(n_estimators=200, min_samples_split=17)
    clf.fit(trainFeature[cFeature], target)
    rfPreds = clf.predict(testFeature)
    rfProb = clf.predict_proba(testFeature)
    gbdt = GradientBoostingClassifier(n_estimators=100, min_samples_split=17)
    gbdt.fit(trainFeature[cFeature], target)
    gbdtPreds = gbdt.predict(testFeature)
    gbdtProb = gbdt.predict_proba(testFeature)
    allProb = rfProb + gbdtProb
    allPreds = []
    print allProb.shape
    for tt in range(allProb.shape[0]):
        prob = list(allProb[tt, :])
        ind = prob.index(max(prob))
        allPreds.append(ind)
    rfRight, gbRight, allRight = 0, 0, 0
    for i in range(len(rfPreds)):
        rfPreName = dl.get_num_position(rfPreds[i])
        gbdtPreName = dl.get_num_position(rfPreds[i])
        allPreName = dl.get_num_position(allPreds[i])
        # if rfPreName == real:rfRight+=1.0
        # if rfPreName == real:gbRight+=1.0
        # if allPreName == real:allRight+=1.0
        # outFile1.write(testIdList[i]+'\t'+rfPreName+'\t'+real+'\n')
        # outFile2.write(testIdList[i]+'\t'+gbdtPreName+'\t'+real+'\n')
        # outFile3.write(testIdList[i]+'\t'+allPreName+'\t'+real+'\n')
    print 'rf:' + str(rfRight / 20000) + '\n gbdt:' + str(gbRight / 20000) + '\n all:' + str(allRight / 20000)
    outFile1.write(str(rfRight / 20000))
