
from numpy import *
# load the dataSet from file
# 3.542485  1.977398  -1
def loadDataSet(fileName) :
  dataMat = []; labelMat = []
  file = open(fileName)
  for line in file.readlines() :
    lineaddr = line.strip().split()
    dataMat.append([float(lineaddr[0]), float(lineaddr[1])])
    labelMat.append(float(lineaddr[2]))
  return dataMat, labelMat

# select a int number in 0~m, and j != i
def selectJrand(i, m) :
  j = i;
  while (j == i) :
    j = int(random.uniform(0, m))
  return j

# decide change the alpha or not beween L and H
def clipAlpha(aj, H, L) :
  if aj > H : aj = H
  if aj < L : aj = L
  return aj

# simple SMO
def smoSimple(dataMatin, classLabels, C, toler, maxIter) :
  #change to the matrix for *
  dataMatin = mat(dataMatin)
  labelMat = mat(classLabels).T
  # m->all the data number ; n:columns
  m, n = shape(dataMatin); b =0; alphats = mat(zeros((m, 1)))
  iter1 = 0;b = 0
  while (iter1 < maxIter) :
    alphaChanged = False;
    #modifies results fi
    for i in range(m) :
      fxi = float(multiply(labelMat, alphats).T*(dataMatin*dataMatin[i,:].T)) + b
      Ei = fxi - labelMat[i]
      if ((labelMat[i] * Ei < -toler) and (alphats[i] < C)) or ((labelMat[i] * Ei > toler) and (alphats[i] > 0)) :
          j = selectJrand(i, m)
          fxj = float(multiply(labelMat, alphats).T*(dataMatin*dataMatin[j,:].T)) + b
          Ej = fxj - labelMat[j]
          alphaIOld = alphats[i].copy()
          alphaJOld = alphats[j].copy()
          # calculate H and L
          if (labelMat[i] != labelMat[j]) :
            L =max(0, alphats[j] - alphats[i])
            H = min(C, C + alphats[j] - alphats[i])
          else:
            L =max(0, alphats[j] + alphats[i] - C)
            H = min(C, C + alphats[j] + alphats[i])
          if L == H : continue
          eta = 2.0 * dataMatin[i, :] * dataMatin[j, :].T - dataMatin[i, :] * dataMatin[i, :].T - dataMatin[j, :] * dataMatin[j, :].T
          if eta >= 0 : continue
          alphats[j] -= labelMat[j] * (Ei - Ej) / eta
          alphats[j] = clipAlpha(alphats[j], H, L)
          if (abs(alphats[j] - alphaJOld) < 0.000001) : continue
          alphats[i] += labelMat[j] * labelMat[i] * (alphaJOld - alphats[j])
          b1 = b - Ei - labelMat[i] * (alphats[i] - alphaIOld) * (dataMatin[i, :] * dataMatin[i, :].T) - labelMat[j] * (alphats[j] - alphaJOld) * (dataMatin[i, :] * dataMatin[j, :].T)
          b2 = b - Ej- labelMat[i]*(alphats[i]-alphaIOld)*dataMatin[i,:]*dataMatin[j,:].T - labelMat[j]*(alphats[j]-alphaJOld)*dataMatin[j,:]*dataMatin[j,:].T
          if alphats[i] >= 0 and alphats[i] <= C : b = b1
          elif alphats[j] >= 0 and alphats[j] <= C : b = b2
          else : b = (b1 + b2) / 2.0
          alphaChanged = True
          print "iter : %d i:%d, pairs changed %d"%(iter1,i,alphaChanged)
    if (alphaChanged == False) : iter1 +=1
    else : iter1 = 0
    print "iter : %d"%(iter1)
  return b, alphats

