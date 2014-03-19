#
# Trial for RF regression
#

import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.decomposition import FactorAnalysis

def run_rf(xtrain, xtest, ytrain, Nest):
    """
    Run RF and return predictions
    """
    rf = RandomForestRegressor(Nest)
    rf.fit(xtrain, ytrain)
    return rf.predict(xtest)

def cv_loop(x, y, Nfolds=10, Nest=10):
    """
    Run Nfold CV leaving out 1./Nfolds fraction
    """
    scores = np.zeros(Nfolds)
    for i in range(Nfolds):
        inds = np.random.permutation(y.size)
        Ntest = np.ceil(y.size / Nfolds)
        trninds = inds[Ntest:]
        tstinds = inds[:Ntest]
        xtest = x[tstinds]
        ytest = y[tstinds]
        xtrain = x[trninds]
        ytrain = y[trninds]
        ypred = run_rf(xtrain, xtest, ytrain, Nest)
        scores[i] = np.sqrt(np.median((ypred - ytest) ** 2))
    return scores

if __name__ == '__main__':

    temps = np.loadtxt('../../data/temps/UVIS2_linear_trim-1.dat')

    f = open('../../data/focus/UVIS2FocusHistory_trim-1.txt')
    raw = f.readlines()[2:]
    f.close()
    focii = np.array([np.float(l.split()[4]) for l in raw])

    scores = cv_loop(temps, focii, Nfolds=10)
    print scores, np.mean(scores), np.std(scores)
