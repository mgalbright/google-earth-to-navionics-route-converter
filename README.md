# Google Earth path to Navionics route converter

## About

### TLDR 
A simple python script to convert a travel route saved with the
[Google Earth Pro on Desktop app](https://www.google.com/earth/about/versions/)
into the file format used by the 
[Navionics Boating App](https://www.navionics.com/usa/apps/navionics-boating). 
This allows you to load the route in the Navionics app.

### Background

With the Google Earth Desktop app, you can create travel routes (which consist 
of sequences of gps coordinates) by clicking points on the map using the "Path" 
tool. You can then save your routes as .kml files. If you want to load those routes into the Navionics app, you need to 
convert the kml file into the Navionics file format.

The Navionics App uses a customized version of the .gpx file format for routes. 
Hence, if  you use an off-the-shelf program (like an online converter, or 
 [gpsbabel](https://www.gpsbabel.org/)) to convert the .kml file to .gpx, 
 Navionics will fail to import the file, since Navionics expects its custom 
 .gpx format.  (This was explained in a Youtube video by 
[The Outdoor News with Rex](https://www.youtube.com/watch?v=OotuLHvwBCc). 
Interestingly, the ActiveCaptain app - also owned by Garmin - can import 
standard .gpx files.) Hence, you need to write the data to a file using the 
Navionics format.

The python script in this repo can do the conversion through a two step process:
1. Use the gpsbabel program (free) to convert the .kml file to a geojson 
(temporary) file. (This makes it trivially easy to read the gps coordinates.)
1. Write the gps coordinates into a Navionics-formatted .gpx route file.

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
(Tested on mac only, but I expect it should work on any *nix distro.)
1. Save your google earth path as a kml file.
1. Convert the kml file to a Navionics file using this script:
    ```shell
    python convert_to_nav.py -i googleearthroute.kml -o navionicsroute.gpx
    ```
1. Email the .gpx file to your device with the Navionics app and open the .gpx 
file with the Navionics app.  This will load the route.

You can also convert a whole folder ./data of route files like this:
```shell
for f in data/*.kml; do python convert_to_nav.py -i "$f" -o "${f%.kml}.gpx"; done
```

### Sample files
The [samples](samples) folder contains a sample .kml file with a path exported from google earth, along with the converted gpx file. You can use these for testing.

### Testing (optional)
You can unit test the script on your system if you install pytest and xmldiff:
```shell
pip install pytest xmldiff
```

Run the test to convert the sample .kml file and make sure it matches the 
sample .gpx file:
```shell
pytest test.py
```

## References
1. Instructions for importing routes into Navionics:   
[How to Export and Import GPX Files withe Navionics Boating App](https://www.youtube.com/watch?v=FEUY-VJNZ_A)
1. Documented problem with importing GPX files in navionics:  
[Navionics Boating App GPX Track File Corrupted or Invalid](https://www.youtube.com/watch?v=OotuLHvwBCc)
