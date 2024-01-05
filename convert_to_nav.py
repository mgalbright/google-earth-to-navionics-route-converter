"""Convert google earth kml file to navionics boating app route file"""

import os
import argparse
import json
import time
import jinja2
import subprocess

TMP_FILE = 'tmp.json'

NAV_FILE_TEMPLATE = \
    """<?xml version="1.0" encoding="UTF-8" ?><gpx xmlns="http://www.topografix.com/GPX/1/1" version="1.1" creator="Navionics Boating App"><metadata><link href="http://www.navionics.com" /></metadata><rte><name>{{ROUTE_NAME}}</name><time>{{TIME_STAMP}}</time>{% for COORD in COORDS2D %}<rtept lat="{{'%0.6f'|format(COORD[1])}}" lon="{{'%0.6f'|format(COORD[0])}}" />{% endfor %}</rte></gpx>"""

def convert_kml_to_geojson(input_file, temp_file):
  result = subprocess.run(['gpsbabel', '-r', '-i', 'kml', '-f', input_file, '-o', 
                           'geojson', '-F', temp_file], capture_output=True, 
                           text=True)
  print(result.stdout)
  print(result.stderr)

def convert_kml_file(input_file, output_file, temp_file):
  print("Calling program gpsbabel to process google earth kml file ...")

  convert_kml_to_geojson(input_file, temp_file)

  print("Loading processed data ...")
  with open(TMP_FILE) as f1:
    data = json.load(f1)
    data = data['features'][0]
    coordinates = data['geometry']['coordinates']
    route_name = data['properties']['name']
    
    current_time = str(int(time.time()))
    
    environment = jinja2.Environment()
    template = environment.from_string(NAV_FILE_TEMPLATE)
    outstring = template.render(ROUTE_NAME=route_name, TIME_STAMP=current_time, 
                                COORDS2D=coordinates)

  with open(output_file, mode='w') as f2:
    f2.write(outstring)
    print(f"Finished writing file {output_file}")
    
  print("cleaning up ...")
  os.remove(temp_file)

  print("done") 


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert google earth kml file (storing a single path) into a route file for navionics boating app.')
    parser.add_argument('-i', '--infile', 
      help='Name of google earth kml file to convert', required=True)
    parser.add_argument('-o', '--outfile', 
      help='Name of navionics file generated. Make sure to save it as .gpx format', required=True)
    parser.add_argument('-t', '--tmpfile', 
      help='Name of temporary file generated during processing', required=False, default=TMP_FILE)
    args = parser.parse_args()

    if not os.path.isfile(args.infile):
      raise ValueError("Input file files does not exist")
    if not args.outfile.endswith(".gpx"):
      raise ValueError("Output file must end with .gpx")

    convert_kml_file(args.infile, args.outfile, args.tmpfile)