import xml.etree.ElementTree as ET
import pygal.maps
import yaml



# Load the countries from your YAML file
#with open(r'C:\Users\rishi\Google Drive\GitHub\personal-blog\data\countries.yaml') as yaml_file:
with open("data/countries.yaml", "r") as yaml_file:
    countries_yaml = yaml.load(yaml_file, Loader=yaml.FullLoader)


# Create a world map
worldmap = pygal.maps.world.World(width=300, height=100)  # Set the width and height here
worldmap.title = 'My Traveled Countries'

# Parse the SVG file
#tree = ET.parse(r'C:\Users\rishi\Google Drive\GitHub\personal-blog\static\images\worldmap_base.svg')
tree = ET.parse("static/images/worldmap_base.svg")


root = tree.getroot()

# Iterate through the SVG paths and update their fill attribute
for path in root.findall('.//svg:path', namespaces=ns):
    country_code = path.get('id')
    if country_code in countries_yaml:
        print(country_code)
        path.set('fill', 'orange')  # You can change the fill color to orange or any color you prefer

# Save the updated SVG file
#tree.write(r'C:\Users\rishi\Google Drive\GitHub\personal-blog\static\images\worldmap.svg', encoding="utf-8")
tree.write("static/images/worldmap.svg", encoding="utf-8")


