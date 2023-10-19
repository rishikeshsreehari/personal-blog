import xml.etree.ElementTree as ET
import pygal.maps
import yaml
import os

# Load the countries from your YAML file
yaml_file_path = os.path.join(os.path.dirname(__file__), 'data', 'countries.yaml')
with open(yaml_file_path, "r") as yaml_file:
    countries_yaml = yaml.load(yaml_file, Loader=yaml.FullLoader)

# Create a world map
worldmap = pygal.maps.world.World(width=300, height=100)  # Set the width and height here
worldmap.title = 'My Traveled Countries'

# Parse the SVG file
svg_file_path = os.path.join(os.path.dirname(__file__), 'static', 'images', 'worldmap_base.svg')
tree = ET.parse(svg_file_path)
root = tree.getroot()

# Find all SVG path elements in the SVG file
paths = root.findall(".//{http://www.w3.org/2000/svg}path")

# Iterate through the found path elements
for path in paths:
    country_code = path.get('id')
    if country_code in countries_yaml:
        print(f"Found country code in YAML: {country_code}")
        path.set('fill', 'orange')
    else:
        print(f"Country code not found in YAML: {country_code}")

# Save the updated SVG file
output_svg_file_path = os.path.join(os.path.dirname(__file__), 'static', 'images', 'worldmap.svg')
tree.write(output_svg_file_path, encoding="utf-8")
