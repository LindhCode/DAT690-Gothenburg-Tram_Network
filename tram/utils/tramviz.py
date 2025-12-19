# visualization of shortest path in Lab 3, modified to work with Django

from haversine import Unit
from .color_tram_svg import color_svg_network
from .graphs import dijkstra
from .trams import (readTramNetwork, specialize_stops_to_lines,
                    specialized_geo_distance, specialized_transition_time)

import os

from django.conf import settings
from django.core.files.storage import default_storage

from .color_tram_svg import color_svg_network
from .graphs import dijkstra
from .trams import (readTramNetwork, specialize_stops_to_lines,
                    specialized_geo_distance, specialized_transition_time)

def show_shortest(dep, dest):
    def get_path(dif):
        result = []
        last_line = None
        last_stop = None

        for stop, line in dif[0]:
            if line != last_line:
                if stop in result:
                    result.pop()
            
                result.append(f"{line} {stop}")
        
            elif stop != last_stop:
                result.append(stop)
        
            last_line = line
            last_stop = stop
        
        return  result , dif[1]
    
    network = readTramNetwork()
    special_network = specialize_stops_to_lines(readTramNetwork())

    shortest_dif, quickest_dif = (), ()
    dep_lines, dest_lines = network.stop_lines(dep), network.stop_lines(dest)
    for dep_line in dep_lines:
        for dest_line in dest_lines:
            dep_inp = tuple([dep, dep_line])
            dest_inp = tuple([dest, dest_line])
            temp_shortest = dijkstra(
                special_network,
                dep_inp,
                cost=lambda u, v: specialized_geo_distance(special_network, u, v),
            )[dest_inp]
            temp_quickest = dijkstra(
                special_network,
                dep_inp,
                cost=lambda u, v: specialized_transition_time(special_network, u, v),
            )[dest_inp]
            time = sum([
                specialized_transition_time(
                    special_network, temp_quickest[i], temp_quickest[i + 1]
                )
                for i in range(len(temp_quickest) - 1)
            ])
            distance = sum([
                specialized_geo_distance(
                    special_network, temp_shortest[i], temp_shortest[i + 1]
                )
                for i in range(len(temp_shortest) - 1)
            ])
            if not shortest_dif or distance < shortest_dif[1]:
                shortest_dif = tuple([temp_shortest, distance])
            if not quickest_dif or time < quickest_dif[1]:
                quickest_dif = tuple([temp_quickest, time])

    shortest = [stop[0] for stop in shortest_dif[0]]
    quickest = [stop[0] for stop in quickest_dif[0]]

    shortest_path, shortest_value = get_path(shortest_dif)
    geopath = " - ".join(shortest_path) + " " + str(round(shortest_value,3))
    quickest_path, quickest_value = get_path(quickest_dif)
    timepath = " - ".join(quickest_path) + " " + str(quickest_value)

    def colors(v):
        if v in shortest and v in quickest:
            return 'cyan'
        elif v in shortest:
            return "green"
        elif v in quickest:
            return "orange"
        else:
            return "white"

    dep_safe = default_storage.get_valid_name(dep)
    dest_safe = default_storage.get_valid_name(dest)
    outfile_unique_name = f"shortest_path_{dep_safe}_{dest_safe}.svg"

    infile = os.path.join(
        settings.BASE_DIR, "tram/templates/tram/images/my_gbg_tramnet.svg"
    )
    outfile = os.path.join(
        settings.BASE_DIR, f"tram/templates/tram/images/generated/{outfile_unique_name}"
    )
    color_svg_network(infile, outfile, colormap=colors)
    return timepath, geopath, outfile