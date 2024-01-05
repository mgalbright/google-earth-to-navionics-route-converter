# Convert Google Earth paths to Navionics routes

## About

### TLDR 
This script converts a travel route from the Google Earth Desktop app (saved as a .kml file) into the file format used by the Navionics Boating App. You can then load the route in the Navionics app.

### Background

With the Google Earth Desktop app, you can create travel routes (which consist of sequences of gps coordinates) by clicking points on the map using the "Path" tool. You can then save your routes as .kml files. It would be convenient to load your travel routes into the Navionics Boating App.  To do that, you need to convert the kml file to the Navionics file format.

The Navionics App uses a propriety version of the .gpx file format.  Hence, if you use an off-the-shelf program (like an online converter, or [gpsbabel](https://www.gpsbabel.org/)) to convert the .kml file to .gpx, Navionics will fail to import the file, since Navionics expects its propriety .gpx format.
(This was explained in a Youtube video by [The Outdoor News with Rex](https://www.youtube.com/watch?v=OotuLHvwBCc).)  Hence, you need to get the data into the propietary format for the import to work.

The python script in this repo can do the conversion through a two step process:
1. Use the gpsbabel program (free) to convert the .kml file to a geojson (temporary) file.
1. Load the gps coordinates from the geojson file and write them into a Navionics-formatted file.

## Instructions

### Setup
(Mac only)  
1. Install [gpsbabel](https://www.gpsbabel.org/)
    ```shell
    brew install gpsbabel
    ```
2. Install python and make sure your python distribution has jinja2 installed, e.g
    ```shell
    conda install jinja2
    ```

### Conversion
(Tested on mac only)
1. Save your google earth path as a kml file.
1. Convert the kml file to a Navionics file using this script:
    ```shell
    python convert_to_nav.py -i googleearthroute.kml -o navionicsroute.gpx
    ```
1. Email the .gpx file to your device with the navionics app and open the .gpx file with the navionics app.  This will load the route

## References
1. Instructions for importing routes into Navionics:   
[How to Export and Import GPX Files withe Navionics Boating App](https://www.youtube.com/watch?v=FEUY-VJNZ_A)
1. Documented problem with importing GPX files in navionics:  
[Navionics Boating App GPX Track File Corrupted or Invalid](https://www.youtube.com/watch?v=OotuLHvwBCc)