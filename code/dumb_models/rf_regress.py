#
# Trial for RF regression
#
from matplotlib import use
use('Agg')
import numpy as np
import matplotlib.pyplot as pl

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.decomposition import FactorAnalysis, KernelPCA, FastICA, PCA

def run_rf(xtrain, xtest, ytrain, Nest):
    """
    Run RF and return predictions
    """
    rf = RandomForestRegressor(Nest)
    rf.fit(xtrain, ytrain)
    return rf.predict(xtest)

def cv_loop(x, y, Nfolds=10, Nest=10, cv_fraction=0.1):
    """
    Run Nfold CV
    """
    scores = np.zeros(Nfolds)
    for i in range(Nfolds):
        inds = np.random.permutation(y.size)
        Ntest = np.ceil(y.size * cv_fraction)
        trninds = inds[Ntest:]
        tstinds = inds[:Ntest]
        xtest = x[tstinds]
        ytest = y[tstinds]
        xtrain = x[trninds]
        ytrain = y[trninds]
        ypred = run_rf(xtrain, xtest, ytrain, Nest)
        s = np.sort(np.sqrt((ypred - ytest) ** 2))
        pl.plot(ytest, ypred-ytest, 'o', alpha=0.3)
        scores[i] = s[np.ceil(ytest.size * 0.8)]
    return scores

if __name__ == '__main__':

    np.random.seed(100)

    temps = np.loadtxt('../../data/temps/UVIS1_linear.dat')
    f = open('../../data/focus/UVIS1FocusHistory.txt')
    raw = f.readlines()[2:]
    f.close()
    focii = np.array([np.float(l.split()[4]) for l in raw])

    kpca = KernelPCA(n_components=3, kernel='linear')
    x = kpca.fit_transform(temps)
    x = np.hstack((temps, x))

    scores = cv_loop(x[:, :], focii, Nfolds=20, cv_fraction=0.1)
    print scores, np.mean(scores), np.std(scores)
    pl.savefig('../../plots/foo.png')
