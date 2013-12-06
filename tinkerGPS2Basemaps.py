#!/usr/bin/env python
# -*- coding: utf-8 -*-  

HOST = "localhost"
PORT = 4223
UID = "f9j" # Change to your UID

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_gps import GPS
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.basemap import Basemap
import os, sys


def writefile(data):
    with open('gpsdatadump.csv', 'a') as the_file:
        the_file.write(str(data))
        the_file.write('\n')


def animate(*args):
    
    # GPS Fix Status überprüfen
    # http://www.tinkerforge.com/en/doc/Software/Bricklets/GPS_Bricklet_Python.html
    if gps.get_status()[0]>1: # also wenn mindestens 2D Fix
        
        # Get current coordinates and time from GPS
        coords = gps.get_coordinates()
        timestamp = gps.get_date_time()
        
        # Dump the Data in file
        data =  ', '.join(map(str,timestamp))
        data += ', '
        data += ', '.join(map(str,coords))
        writefile(data)
        
        # Print the Position
        print('Latitude: ' + str(coords.latitude/1000000.0) + '° ' + coords.ns + \
             '\tLongitude: ' + str(coords.longitude/1000000.0) + '° ' + coords.ew)

        lat=float(coords.latitude/1000000.0)
        lon=float(coords.longitude/1000000.0)

        # Insert to map
        x,y = m(lon, lat)
        m.plot(x, y, 'ro', markersize=10)
        
    else:
        print('Searching for Satellites (maybe you have to go outside)...')
    
def connect():
    ipcon = IPConnection() # Create IP connection
    gps = GPS(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    print('GPS Bricklet connected...')
    return gps, ipcon

def initmap(gps):
    # Generate Map Dimensions
    zoom = 1 # je größer, desto größer der Ausschnitt
    coords = gps.get_coordinates()
    lat0=coords.latitude/1000000.0
    lon0=coords.longitude/1000000.0
    llcrnrlon=lon0-(4.0*zoom) # links
    llcrnrlat=lat0-(2.1*zoom) # unten
    urcrnrlon=lon0+(5.0*zoom) # rechts
    urcrnrlat=lat0+(1.2*zoom) # oben
    
    print('Generating Map...')
    
    # First set up the figure, the axis, and the plot element we want to animate
    fig = plt.figure(figsize=(16,9))
    ax=fig.add_axes([0.01,0.01,0.98,0.98])
    
    
    # Thanks to this great tutorial:
    # http://peak5390.wordpress.com/2012/12/08/mapping-global-earthquake-activity-a-matplotlib-basemap-tutorial/
    m = Basemap(llcrnrlon=llcrnrlon,llcrnrlat=llcrnrlat,urcrnrlon=urcrnrlon,urcrnrlat=urcrnrlat,
               resolution='l',projection='tmerc',lon_0=lon0,lat_0=lat0)

    m.drawcoastlines()
    #m.fillcontinents(color='gray')
    # draw parallels and meridians.
    m.drawparallels(np.arange(-40,61.,2.))
    m.drawmeridians(np.arange(-30.,43.,2.))
    m.drawmapboundary()
    m.drawcountries()
    m.shadedrelief()

    return fig, plt, m


if __name__ == "__main__":
    # Connect the Tinkerforge GPS Bricklet
    gps,ipcon=connect()
    # Set up the Map
    fig, plt, m=initmap(gps)
    
    
    print('\'Ctrl\' + \'C\' will quit logging or\n')
    print('\'Close the Map\' will quit logging.')
    while plt.get_fignums()!=[]:
        try:
            print('Logging Position Data...')
            
            # call the animator.  blit=True means only re-draw the parts that have changed.
            anim = animation.FuncAnimation(fig, animate, interval=1000, blit=False)  
            plt.show()

        except KeyboardInterrupt:
            print('Quit.')
            break

    #Finishing it up
    print('Disconnect...')
    ipcon.disconnect()
    print('Done.')


    