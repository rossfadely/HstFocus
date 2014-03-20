#
# Pull out pieces from UVIS2 data, to develop models
#

from matplotlib import use
from astropy.time import Time

use('Agg')
import numpy as np
import matplotlib.pyplot as pl

t1a = '2010-11-08 00:00:00'
t2a = '2010-11-22 00:00:00'
t1b = '2010-11-08 20:00:00'
t2b = '2010-11-22 20:00:00'

mjds1 = Time([t1a, t1b], format='iso', scale='utc').mjd
mjds2 = Time([t2a, t2b], format='iso', scale='utc').mjd

f = open('../../data/focus/UVIS2FocusHistory.txt')
raw = f.readlines()[1:]
f.close()
mjds = np.array([np.float(l.split()[3]) for l in raw])
focii = np.array([np.float(l.split()[4]) for l in raw])

temps = np.loadtxt('../../data/temps/UVIS2_linear.dat')

ind1 = np.where((mjds >= mjds1[0]) & (mjds <= mjds1[1]))[0]
ind2 = np.where((mjds >= mjds2[0]) & (mjds <= mjds2[1]))[0]

# magic number set by UVIS1 data
thresh = 1.69999999e-03
ind = [0, -1]
idx = []
for i in range(1, mjds.size - 1):
    if ((mjds[i + 1] - mjds[i] > thresh) & (mjds[i] - mjds[i - 1] > thresh)):
        ind.append(i)
    else:
        idx.append(i)
ind = np.array(ind)
idx = np.array(idx)

# save it
h = 'date and temperatures (in mystery units)\n'
h += 'mjd Aft Light Shield, Axial Truss, Truss Diameter, Aft Shroud, '
h += 'Forward Shell, and Light Shield'
np.savetxt('../../data/temps/UVIS2_linear_noshort.dat', temps[ind], header=h)
np.savetxt('../../data/temps/UVIS2_linear_short.dat', temps[idx], header=h)
np.savetxt('../../data/temps/UVIS2_linear_isr1.dat', temps[ind1], header=h)
np.savetxt('../../data/temps/UVIS2_linear_isr2.dat', temps[ind2], header=h)

h = 'file camera date mjd focus error\n'
f = open('../../data/focus/UVIS2FocusHistory_noshort.txt', 'w')
f.write(h)
for i in ind:
    f.write(raw[i])
f.close()
f = open('../../data/focus/UVIS2FocusHistory_short.txt', 'w')
f.write(h)
for i in idx:
    f.write(raw[i])
f.close()
f = open('../../data/focus/UVIS2FocusHistory_isr1.txt', 'w')
f.write(h)
for i in ind1:
    f.write(raw[i])
f.close()
f = open('../../data/focus/UVIS2FocusHistory_isr2.txt', 'w')
f.write(h)
for i in ind2:
    f.write(raw[i])
f.close()

f = open('../../data/focus/UVIS2FocusHistory_noshort.txt')
raw = f.readlines()[1:]
f.close()
mjds = np.array([np.float(l.split()[3]) for l in raw])
focii = np.array([np.float(l.split()[4]) for l in raw])

pl.plot(mjds, focii, 'o', alpha=0.3)
pl.savefig('../../plots/foo.png')

