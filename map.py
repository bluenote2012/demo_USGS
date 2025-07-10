import folium
import requests
import json
from datetime import datetime
from folium.plugins import MarkerCluster
from folium.plugins import TimestampedGeoJson

class MapInteractive:
    """
    Create an interactive mpa class centered on coordinates input by the user.
    Add markers to the map with the following parameters:
        location: tuplet pair containing the latitude and longitude of the earthquake
            lat, long: float
        tooltip: str
        popup_text: str
        icon: str

    
       TODO Parameters
    """

    def __init__(self, long=32.7157, lat=-117.1611):
        # Corvallis: long=45.5236, lat=-122.6750
        # San Francisco: '37.7749', 'longitude' : '-122.4194'
        # Initialize map based on long, lat coordinates supplied by user.

        # TODO: Create mechanism to allow map to be interactive and allow user input.
        self.m = folium.Map(location=(long, lat))
        self.m.save("maptest.html")

    def color(self, magnitude):
        if magnitude > 6:
            color = 'red'
        elif magnitude > 4 and magnitude < 6:
            color = 'orange'
        elif magnitude >= 2.5:
            color = 'yellow'
        else:
            color = 'green'
        return color

    def add_marker(self, lat, long, depth, magnitude, tooltip='Click me', popup_text='magnitude'):
        """
        Color and radius of marker are set by the reported magnitude of the earthquake."""
        folium.CircleMarker(
            location=[long, lat],
            tooltip=tooltip,
            popup=f'magnitude = {str(magnitude)}',
            # icon=folium.Icon(icon="cloud"),
            color = self.color(magnitude),
            fill=True,
            fill_color = self.color(magnitude),
            fill_opacity = 1,
            opacity = 1,
            radius = magnitude * 5
        ).add_to(self.m)
        self.m.save("maptest.html")


def generate_location_list():
    """
    TODO: add documentation
    
    """
    # San Francisco
    # payload = {'starttime' : '2025-01-01' , 'endtime': '2025-06-26', 'format' : 'geojson', 'latitude': '37.7749', 'longitude' : '-122.4194', 'minmagnitude' : '1.0', 'maxradiuskm' : '100'}
    # # Corvallis
    # payload = {'starttime' : '2025-04-01' , 'endtime': '2025-06-26', 'format' : 'geojson', 'latitude': '44.5646', 'longitude' : '-123.2620', 'minmagnitude' : '1.0', 'maxradiuskm' : '100', 'limit' : '15'}
    # San Diego
    payload = {'starttime' : '2025-04-01' , 'endtime': '2025-04-27', 'format' : 'geojson', 'latitude': '32.7157', 'longitude' : '-117.1611', 'minmagnitude' : '1.0', 'maxradiuskm' : '100'}
    r = requests.get('https://earthquake.usgs.gov/fdsnws/event/1/query', params=payload)
    json_output =json.loads(r.text)

    features_list = json_output['features']
    earthquake_list = []
    for item in features_list:
        magnitude = item['properties']['mag']
        if item['properties']['type'] == 'earthquake' and magnitude > 2:
            lat, long, depth = item['geometry']['coordinates']
            time = item['properties']['time']
            dt = datetime.fromtimestamp(time / 1000)
            dt_fmt = dt.strftime('%Y-%m-%d %H:%M:%S')
            print(dt_fmt, magnitude)
            earthquake_list.append((long, lat, depth, magnitude, dt))
    earthquake_sorted_by_mag = sorted(earthquake_list, key=lambda item: item[3], reverse=True)
    # print(earthquake_sorted_by_mag)
    
    return earthquake_sorted_by_mag[0:30]

mymap = MapInteractive()
for element in generate_location_list():
    mymap.add_marker(long=element[0],lat=element[1], depth=element[2], magnitude=element[3])


"""
Parameters:
format: String          Default = quakeml
    format=geojson      Response format is GeoJSON. Mime-type is “application/json”.
starttime: String       Default NOW - 30 days All times use ISO8601 Date/Time format. 
                        Unless a timezone is specfified, UTC is assumed.
endtime: String         Default present time

Circle:
    latitude: Decimal [-90, 90] degrees  Default: null - Specify the latitude to be used for a radius search.
    longitude: Decimal [-180, 180] degrees   Default: null - Specify the longitude to be used for a radius search.
    maxradius: Decimal[0,180] degrees    Default - Limit to events within the specified maximum number of degrees 
                                         from the geographic point defined by the latitude and longitude parameters
    maxradiuskm: Decimal [1, 20001.6] km   Default - 20001.6 - Limit to events within the specified maximum number 
                                         of kilometers from the geographic point defined by the latitude and longitude 
                                         parameters.
limit: Integer          Default: null - Limit the resultsto the specified number of events.
mindepth: Decimal       Default: -100 - Limit to events with depth less than the specified amount.
maxdepth: Decimal       Default: null Limit to events with depth less than the specified maximum
minmagnitude: Decimal   Default null - Limit to events with a magnitude larger than the specified minimum
maxmagnitude: Decimal   Default null - Limit to events with a magnitude smaller thant he specified maximum
orderby: String         Default time
                            orderby=time - order by origin descending time
                            orderby=time-asc  - order by origin ascending time
                            orderby=magnitude - order by descending magnitude
                            orderby=magnitude-asc - order by ascending magnitude
eventtype: String       Default: null = Limit to events of a specific type. NOTE: “earthquake” will filter non-earthquake events.
nodata: Integer (204|404)   Default 204 - Define the error code that will be returned when no data is found.

"""

# TODO - add attributes to MapInteractive class ?
# m.start = start
# m.end = end
# m.latitude = latitude
# m.longitude = longitude
# m.minmag = minmag
# m.magradkm = maxradkm
# m.limit = limit