"""
Baseline tram visualization for Lab 3

Creates an SVG image usable on the home page.
This image is then coloured by tramviz.py depending on the route.
You only need to run this file once, to change the URLs of the vertices.
"""

from .trams import readTramNetwork
import graphviz
import json

MY_GBG_SVG = './tram/templates/tram/images/my_gbg_tramnet.svg'  # the output SVG file
MY_TRAMNETWORK_JSON = '../lab1-group-2/tramnetwork.json'  # JSON file from lab1
TRAM_URL_FILE = 'tram/utils/stop_urls.json'  # given in lab3/files, replace with your own stop URL file

# assign colors to lines, indexed by line number; not quite accurate
gbg_linecolors = {
    1: 'gray',
    2: 'yellow',
    3: 'blue',
    4: 'green',
    5: 'red',
    6: 'orange',
    7: 'brown',
    8: 'purple',
    9: 'cyan',
    10: 'lightgreen',
    11: 'black',
    13: 'pink'
}

# Return a function which scales positions, based on scale of entire network.
def position_scaler(network):
    minlat, minlon, maxlat, maxlon = network.extreme_positions()
    size_x = maxlon - minlon
    size_y = maxlat - minlat
    scalefactor = len(network)/4  # heuristic
    x_factor = scalefactor/size_x
    y_factor = scalefactor/size_y

    return lambda lon, lat: (x_factor*(lon-minlon), y_factor*(lat-minlat))

def network_graphviz(network, outfile=MY_GBG_SVG):
    with open(TRAM_URL_FILE) as file:
        stop_urls = json.loads(file.read())

    dot = graphviz.Graph(
        engine='fdp',
        graph_attr={
            'size': '12,12'  # max image size (in inches!)
        }
    )
    scaler = position_scaler(network)

    for stop in network.all_stops():
        pos = network.stop_position(stop)
        lat = pos["lat"]
        lon = pos["lon"]

        pos_x, pos_y = scaler(lon, lat)
        dot.node(
            stop,
            label=stop,
            shape='rectangle',
            pos=f'{pos_x},{pos_y}!',
            fontsize='8pt',
            width='0.4',
            height='0.05',
            URL=stop_urls.get(stop, '.'),
            fillcolor='white',
            style='filled'
        )

    for line in network.all_lines():
        stops = network.line_stops(line)
        for i in range(len(stops)-1):
            dot.edge(
                stops[i],
                stops[i+1],
                color=gbg_linecolors[int(line)],
                penwidth=str(2)
            )

    dot.format = 'svg'
    s = dot.pipe().decode('utf-8')
    with open(outfile, 'w', encoding="utf-8") as file:
        file.write(s)

if __name__ == '__main__':
    network = readTramNetwork(tramfile=MY_TRAMNETWORK_JSON)
    network_graphviz(network)
