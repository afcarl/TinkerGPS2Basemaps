# TinkerGPS2Basemaps

## Wofür?

Liest die Position von [Tinkerforge GPS Bricklets](http://www.tinkerforge.com/en/doc/Hardware/Bricklets/GPS.html#gps-bricklet) ein und stellt die Punkte auf [Basemaps](http://matplotlib.org/basemap/index.html) dar.

![GPS Koordinate Europa](https://raw.github.com/balzer82/TinkerGPS2Basemaps/master/basemap-europa.png)


## Wie benutzt man es?

``` python tinkerGPS2Basemaps.py ```


## Was tut es?

1. Initialisiert das GPS Bricklet (UID ändern!)
2. wartet bis GPS genug Satelliten gefunden hat
3. Rendert Karte von Europa (je nach Zoom)
4. zeichnet GPS Punkte ein (alle 1 Sekunde)
5. schreibt gpsdump.csv Datei mit Rohdaten

### Karte

![Detail View](https://raw.github.com/balzer82/TinkerGPS2Basemaps/master/basemap-detail.png)

### GPSDUMP.CSV

```
Date , Time     , North   , N, East    , E, PDOP, HDOP, VDOP, EPE 
61213, 124736100, 51040055, N, 13792814, E, 3012, 2826, 1044, 2236
```

PDOP, HDOP and VDOP are the dilution of precision [DOP](http://en.wikipedia.org/wiki/Dilution_of_precision_(GPS)) values. They specify the additional multiplicative effect of GPS satellite geometry on GPS precision. The values are give in hundredths.

[EPE](http://www.nps.gov/gis/gps/WhatisEPE.html) is the "Estimated Position Error". The EPE is given in cm. This is not the absolute maximum error, it is the error with a specific confidence.


## Dependencies

1. Matplotlib (for Rendering)
2. Basemap (for Map)
3. numpy (for array)
4. Tinkerforge Egg (for Tinkerforge Brick Communication)