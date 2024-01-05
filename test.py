import os
import subprocess
import pytest
from xmldiff import main

@pytest.fixture()
def files():
  """Define file paths. Use a fixture to ensure the testing output file is 
  deleted after the test"""
  files = {}
  files['ge_file'] = "samples/google-earth-route.kml"
  files['expected_nav_file'] = "samples/expected-nav-route.gpx"
  files['out_nav_file'] = "samples/out.gpx"

  yield files

  if os.path.isfile(files['out_nav_file']):
    os.remove(files['out_nav_file'])

def test_file_conversion(files):
  """Convert the test kml and make sure it matches the expected result"""

  input_file = files['ge_file']
  output_file = files['out_nav_file']
  expected_result_file = files['expected_nav_file']

  assert os.path.isfile(input_file), "Sample .kml file does not exist, re-download it from the repo"
  assert os.path.isfile(expected_result_file), "Sample .gpx file does not exist, re-download it from the repo"

  result = subprocess.run(['python', 'convert_to_nav.py', '-i', input_file, '-o', 
                           output_file], capture_output=True, 
                           text=True, check=True)
  assert os.path.isfile(output_file), "No converted file was generated"

  #check for differences in file content. You can't simply check if files are
  #equal because the <time> fields will differ. Hence, do an xml diff and verify
  #only <time> fields differ
  differences = main.diff_files(expected_result_file, output_file)
  assert len(differences) == 1, "Output file does not match the expected form, too many differences"
  assert differences[0].node == '/*/*[2]/*[2]', "Output file does not match the expected form, differences in unexpected locations"


  