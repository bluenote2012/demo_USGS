import folium

class MapInteractive:
    """Input coordinates to create a map.
    
       TODO Parameter"""

    def __init__(self, long=45.5236, lat=-122.6750):
        self.m = folium.Map(location=(long, lat))
        self.m.save("maptest.html")

    def add_marker(self, long, lat, tooltip='Click me', popup_text='Corvallis'):
        folium.Marker(
            location=[long, lat],
            tooltip=tooltip,
            popup=popup_text,
            icon=folium.Icon(icon="cloud"),
        ).add_to(self.m)




