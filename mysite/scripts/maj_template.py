from bs4 import BeautifulSoup
import folium


# filePath = '/home/followingjude/mysite/log.txt'
# templatePath = '/home/followingjude/mysite/templates/map.html'
no_segment = [(39.88412, 3.32772)]
filePath = '../log.txt'
templatePath = '../templates/map.html'


# 1) Declare variables
# Open log file.
with open(filePath, 'r') as file:
    log = file.read().split('\n')
# Remove first line of log. This one just contains column's titles.
log = log[1:]
# Set lists to store data.
date = []
lon = []
lat = []
# Check if data are exploitable, and store good ones in list : same index for same point's data.
for line in log:
    data = line.split('\t')
    try:
        lon.append(float(data[-1]))
        lat.append(float(data[-2]))
        date.append(data[0])
    except ValueError:
        pass
# Define last know position as tuple. This one will set center of map.
start_coords = (lat[-1], lon[-1])

# 2) Create map template with folium.
folium_map = folium.Map(location=start_coords, zoom_start=9)
# Add points and segment between points on map, except for some points define in no_segment list.
number_of_points = len(lon)
for i in range(1, number_of_points):
    loc = [(lat[i-1], lon[i-1]), (lat[i], lon[i])]
    if (lat[i], lon[i]) not in no_segment:
        folium.PolyLine(loc, color='red', weight=1, opacity=0.8).add_to(folium_map)
    folium.CircleMarker(location=(lat[i-1], lon[i-1]), radius=2, popup=date[i-1], color="#3186cc").add_to(folium_map)
# Add big marker on map at the last know position.
folium.Marker(start_coords, popup=date[-1]).add_to(folium_map)
# Save map as template. This one will we be use with flask.render_template().
folium_map.save(templatePath)

# 3) Adding favicon in the template.
# Define tab icon html with jinja2 arguments.
tab_icon = """<link rel="icon"  href="{{ url_for('static', filename='favicon.ico') }}" type='image/x-icon'/>"""
# Pass map HTML text to BeautifulSoup, returns a soup object (parsed html).
soup = BeautifulSoup(open(templatePath), 'html.parser')
# Find head section and append the 'tab_icon" html. Favicon links must be in the <head> section.
head = soup.find('head')
head.append(BeautifulSoup(tab_icon, 'html.parser'))  # Needs to be parsed as html by BeautifulSoup to work.
# Overwrite the edited html to the MyMap.html file
with open(templatePath, 'w') as html_file:
    html_file.write(str(soup))
