#
# Make a file showing state of secondary during focus measurements
#

from astropy.time import Time

import numpy as np

outfile = '../../data/shifts/UVIS2_shifts_isr2.txt'

f = open('../../data/focus/UVIS2FocusHistory_isr2.txt')
raw = f.readlines()[1:]
f.close()
mjds = np.array([np.float(l.split()[3]) for l in raw])

dates = ['1994-06-29 17:36:00',
         '1995-01-15 23:40:00',
         '1995-08-28 15:16:00',
         '1996-03-14 18:47:00',
         '1996-10-30 17:40:00',
         '1997-03-18 22:55:00',
         '1998-01-12 01:15:00',
         '1998-02-01 16:40:00',
         '1998-06-04 01:01:00',
         '1998-06-28 17:26:00',
         '1999-09-15 15:40:00',
         '2000-01-09 17:42:00',
         '2000-06-15 19:38:00',
         '2002-12-02 20:50:00',
         '2004-12-22 23:12:00',
         '2006-07-31 14:35:00',
         '2009-07-20 09:35:00',
         '2013-01-24 17:58:00',
         '2013-11-11 17:41:00']
ref_mjds = Time(dates, format='iso', scale='utc').mjd

shift = 0.0
moves = np.array([5.0, 5.0, 6.5, 6.0, 5.0, -2.4, 21.0, -18.6, 16.6, -15.2, 3.0,
                  4.2, 3.6, 3.6, 4.16, 5.34, 2.97, 3.60, 2.97])
for i in range(moves.size):
    shift += moves[i]
    moves[i] = shift

shifts = np.zeros_like(mjds)
for i in range(ref_mjds.size - 1):
    ind = np.where((mjds >= ref_mjds[i]) & (mjds < ref_mjds[i + 1]))
    shifts[ind] = moves[i]
ind = np.where(mjds >= ref_mjds[-1])
shifts[ind] = moves[-1]

h = 'shift from zero of secodary mirror\n'
h += 'mjd shift (microns)'
np.savetxt(outfile, np.vstack((mjds, shifts)).T, header=h)
