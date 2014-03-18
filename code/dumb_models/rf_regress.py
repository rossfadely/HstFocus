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
    return rf.predict(ytrain)

def cv_loop(x, y, Nfolds=10, Nest=10):
    """
    Run Nfold CV leaving out 1./Nfolds fraction
    """
    scores = np.zeros(Nfolds)
    for i in range(Nfolds):
        inds = np.random.perturbation(y.size)
        frac = 1./Nfolds
        Ntest = np.ciel(y.size * frac)
        xtest = x[:Ntest]
        ytest = y[:Ntest]
        xtrain = x[Ntext:]
        ytrain = y[Ntext:]
        ypred = run_rf()
        scores[i] = np.median((ypred - ytest) ** 2)
    return scores

if __name__ == '__main__':

    temps = np.loadtxt('../../data/temps/UVIS1_linear.dat')

    f = open('UVIS1FocusHistory.txt')
    raw = f.readlines()[1:]
    f.close()
    focii = np.array([l.split()[4] for l in raw])

    scores = cv_loop(temps, focii)
    print scores