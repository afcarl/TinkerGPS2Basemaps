# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Create Statistics

# <codecell>

from matplotlib import pyplot as plt
from matplotlib.dates import strpdate2num, DateFormatter
import numpy as np
import csv
import time

# <headingcell level=2>

# Read the Dump.csv

# <codecell>

t, N, E, PDOP, HDOP, VDOP, EPE = np.loadtxt('gpsdatadump.csv',
                delimiter=',', unpack=True, usecols = (1,2,4,6,7,8,9),
                converters={1: strpdate2num(' %H%M%S%f')})

# <headingcell level=2>

# Plot the Estimated Position Error

# <codecell>

fig, ax = plt.subplots(figsize=(16,9))
ax.plot_date(t, EPE/100, fmt='g-') # x = array of dates, y = array of numbers        

fig.autofmt_xdate()
ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
plt.ylabel('Estimated Position Error [Meter]')
plt.grid(True)
plt.savefig('gpsdumpEPE.png',dpi=72, bbox_inches='tight')
plt.show()
plt.close()

# <codecell>


