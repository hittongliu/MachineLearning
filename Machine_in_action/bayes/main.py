#-*- coding: utf-8 -*-

import bayes

postingList,classVec = bayes.loadDataSet()
myVocabList = bayes.createVocabList(postingList)
print(myVocabList)

# 利用所给的六条文档，每个文档生成一个词条向量
trainMat = []
for postline in postingList :
  trainMat.append(bayes.setOfWords2Vec(myVocabList, postline))
p1Vect, p0Vect, pAb = bayes.trainNB0(trainMat, classVec)

testEntry = ['baby', 'hate', 'I']
thisDoc = bayes.setOfWords2Vec(myVocabList, testEntry)
classify = bayes.classifyNB(thisDoc, p0Vect, p1Vect, pAb)
print(classify)


