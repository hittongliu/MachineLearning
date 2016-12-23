from numpy import *
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


class optStructk:
  def __init__(self, datMatIn, classLabels, C, toler) :
    self.x = datMatIn
    self.labelMat = classLabels
    self.C = C
    self.tol = toler
    self.m = shape(datMatIn)[0]
    self.alphas = mat(zeros((self.m, 1)))
    self.b = 0
    self.eCache = mat(zeros((self.m, 2)))

def calcEk(oS,k):
     fXk = float(multiply(oS.alphas,oS.labelMat).T*(oS.x*oS.x[k,:].T)) + oS.b
     Ek = fXk - float(oS.labelMat[k])
     return Ek



def selectJ(i, os, Ei) :
  maxk = -1;maxDeltaE = 0; Ej = 0
  os.eCache[i] = [1, Ei]
  validEcacheList = nonzero(os.eCache[i: 0].A)[0]
  if (len(validEcacheList)) > 1 :
    for k in validEcacheList:
      if k == i :continue
      Ek = calcEk(os, k)
      deltaE = abs(Ei - Ek)
      if (deltaE > maxDeltaE) :
        maxk = k; maxDeltaE = deltaE; Ej = Ek
        return maxk, Ej
  else :
    j = selectJrand(i, os.m)
    Ej = calcEk(os, j)
  return j, Ej

def updateEk(os, k) :
  Ek = calcEk(os, k)
  os.eCache[k] = [1, Ek]

def innerL(i, oS):
    Ei = calcEk(oS, i)
    if ((oS.labelMat[i]*Ei < -oS.tol) and (oS.alphas[i] < oS.C)) or ((oS.labelMat[i]*Ei > oS.tol) and (oS.alphas[i] > 0)):
        j,Ej = selectJ(i, oS, Ei) #this has been changed from selectJrand
        alphaIold = oS.alphas[i].copy(); alphaJold = oS.alphas[j].copy();
        if (oS.labelMat[i] != oS.labelMat[j]):
            L = max(0, oS.alphas[j] - oS.alphas[i])
            H = min(oS.C, oS.C + oS.alphas[j] - oS.alphas[i])
        else:
            L = max(0, oS.alphas[j] + oS.alphas[i] - oS.C)
            H = min(oS.C, oS.alphas[j] + oS.alphas[i])
        if L==H: print "L==H"; return 0
        eta = 2.0 * oS.x[i,:]*oS.x[j,:].T - oS.x[i,:]*oS.x[i,:].T - oS.x[j,:]*oS.x[j,:].T
        if eta >= 0: print "eta>=0"; return 0
        oS.alphas[j] -= oS.labelMat[j]*(Ei - Ej)/eta
        oS.alphas[j] = clipAlpha(oS.alphas[j], H, L)
        updateEk(oS, j) #added this for the Ecache
        if (abs(oS.alphas[j] - alphaJold) < 0.00001): print "j not moving enough"; return 0
        oS.alphas[i] += oS.labelMat[j]*oS.labelMat[i]*(alphaJold - oS.alphas[j])#update i by the same amount as j
        updateEk(oS, i) #added this for the Ecache                    #the update is in the oppostie direction
        b1 = oS.b - Ei- oS.labelMat[i]*(oS.alphas[i]-alphaIold)*oS.x[i,:]*oS.x[i,:].T - oS.labelMat[j]*(oS.alphas[j]-alphaJold)*oS.x[i,:]*oS.x[j,:].T
        b2 = oS.b - Ej- oS.labelMat[i]*(oS.alphas[i]-alphaIold)*oS.x[i,:]*oS.x[j,:].T - oS.labelMat[j]*(oS.alphas[j]-alphaJold)*oS.x[j,:]*oS.x[j,:].T
        if (0 < oS.alphas[i]) and (oS.C > oS.alphas[i]): oS.b = b1
        elif (0 < oS.alphas[j]) and (oS.C > oS.alphas[j]): oS.b = b2
        else: oS.b = (b1 + b2)/2.0
        return 1
    else: return 0

def smoP(dataMatin, classLabels, C, toler, maxIter) :
  os = optStructk(mat(dataMatin), mat(classLabels).transpose(), C, toler)
  iter1 = 0
  entireSet = True; alphaChanged = 0
  while ((iter1 < maxIter) and (alphaChanged > 0) or (entireSet)) :
    alphaChanged = 0
    if entireSet :
      for i in range(os.m) :
        alphaChanged += innerL(i, os)
        print "fullSet, iter: %d i:%d, pairs changed %d" % (iter1,i,alphaChanged)
      iter1 += 1
    else :
      nonBounds = nonzero((os.alphas.A > 0) *(os.alphas.A < C))[0]
      for i in nonBounds :
        alphaChanged += innerL(i, os)
        print "nonBounds, iter: %d i:%d, pairs changed %d" % (iter1,i,alphaChanged)
      iter1 += 1
    if entireSet: entireSet = False
    elif (alphaChanged == 0) : entireSet = True
    print "iteration number: %d" % iter1
  return os.b, os.alphas