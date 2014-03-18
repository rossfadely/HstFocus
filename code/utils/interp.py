#
# Interpolate temperature data onto Focus data grid,
# right now for WFC3 UVIS only.
#

import numpy as np
from scipy.interpolate import interp1d

# Focus data
f = open('../../data/focus/UVIS1FocusHistory.txt')
raw1 = f.readlines()[1:]
f.close()
f = open('../../data/focus/UVIS2FocusHistory.txt')
raw2 = f.readlines()[1:]
f.close()

# mjds of focus data
focus_mjds1 = np.array([np.float(l.split()[3]) for l in raw1])
focus_mjds2 = np.array([np.float(l.split()[3]) for l in raw2])

# thermal data
raw = []
for i in range(9, 15):
    f = open('../../data/temps/thermalData20%s.dat' % str(i).zfill(2))
    raw.extend(f.readlines()[1:])
    f.close()

# mjds, temps
temp_mjds = np.array([np.float(l.split()[1]) for l in raw])
temp_temps = np.array([l.split()[2:] for l in raw]).astype(np.float)

# crappy interpolation, using linear for now - bbq throws 
# memory error for cubic... can parse if need cubic.
focus_temps1 = np.zeros((focus_mjds1.size, temp_temps.shape[1]))
focus_temps2 = np.zeros((focus_mjds2.size, temp_temps.shape[1]))
for i in range(temp_temps.shape[1]):
    f = interp1d(temp_mjds, temp_temps[:, i], kind='linear')
    focus_temps1[:, i] = f(focus_mjds1)
    focus_temps2[:, i] = f(focus_mjds2)

# dump into single array
uvis1 = np.zeros((focus_mjds1.size, focus_temps1.shape[1] + 1))
uvis2 = np.zeros((focus_mjds2.size, focus_temps2.shape[1] + 1))
uvis1[:, 0] = focus_mjds1
uvis2[:, 0] = focus_mjds2
uvis1[:, 1:] = focus_temps1
uvis2[:, 1:] = focus_temps2

# save it
h = 'date and temperatures (in mystery units)\n'
h += 'mjd Aft Light Shield, Axial Truss, Truss Diameter, Aft Shroud, '
h += 'Forward Shell, and Light Shield'
np.savetxt('../../data/temps/UVIS1_linear.dat', uvis1, header=h)
np.savetxt('../../data/temps/UVIS2_linear.dat', uvis2, header=h)
