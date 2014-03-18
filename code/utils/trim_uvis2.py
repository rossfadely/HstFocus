#
# Script to trim off short cadence measurements, so that it matches more
# closely to UVIS1 data.
#

import numpy as np
import matplotlib.pyplot as pl

versions = np.arange(10)
np.random.seed(18032014)

# keep percentile
percentile = 0.05

# interpolated temperatures
t1 = np.loadtxt('../../data/temps/UVIS1_linear.dat')
t2 = np.loadtxt('../../data/temps/UVIS2_linear.dat')

# Focus data
f = open('../../data/focus/UVIS2FocusHistory.txt')
raw2 = np.array(f.readlines()[1:])
f.close()

# minimum cadence from shortest UVIS1 measurement
mn = (t1[1:, 0] - t1[:-1, 0]).min()

h1 = 'Trimmed to similar cadence as UVIS1\n'
h1 += 'date and temperatures (in mystery units)\n'
h1 += 'mjd Aft Light Shield, Axial Truss, Truss Diameter, Aft Shroud, '
h1 += 'Forward Shell, and Light Shield'
h2 = 'Trimmed to similar cadence as UVIS1\n'
h2 += 'file camera date mjd focus error\n'
for v in versions:
    inds = []
    for i in range(t2.shape[0] - 1):
        delta = t2[i+1, 0] - t2[i, 0]
        if delta >= mn:
            inds.append(i)
        elif np.random.rand(1) <= percentile:
            inds.append(i)
    inds.append(i + 1)
    inds = np.array(inds)
    np.savetxt('../../data/temps/UVIS2_linear_trim-%d.dat' % v, t2[inds],
               header=h2)
    f = open('../../data/focus/UVIS2FocusHistory_trim-%d.txt' % v, 'w')
    f.write(h2)
    for idx in inds:
        f.write(raw2[idx])
    f.close()
