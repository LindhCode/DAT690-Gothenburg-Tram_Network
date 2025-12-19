
# imports added in Lab 3 version
import math
import os
import sys
from django.conf import settings, time


sys.path.append("../lab1-group-2/")
import tramdata as td

from .graphs import WeightedGraph
import sys
import json

TRAM_FILE = os.path.join(settings.BASE_DIR, "../lab1-group-2/tramnetwork.json")

class TramNetwork(WeightedGraph):
    def __init__(self, lines, stops, times):
        super().__init__()
        self._linedict = lines
        self._stopdict = stops
        self._timedict = times

        for stop in self.all_stops():
            self.add_vertex(stop)

        for i in self.all_lines():
            stops = self.line_stops(i)
            for j in range(len(stops) - 1):
                self.add_edge(stops[j], stops[j + 1])
                self.set_weight(
                    stops[j], stops[j + 1], self.transition_time(stops[j], stops[j + 1])
                )

    def all_lines(self):
        return list(self._linedict.keys())

    def all_stops(self):
        return list(self._stopdict.keys())

    def extreme_positions(self):
        pos = sorted([tuple(list(a.values())) for a in self._stopdict.values()])
        # return {"min": pos[0], "max": pos[-1]}
        return pos[0][0], pos[0][1], pos[-1][0], pos[-1][1]

    def geo_distance(self, a, b):
        return td.distance_between_stops(self._stopdict, a, b)

    def line_stops(self, line):
        return self._linedict[line] if line in self._linedict else None

    def stop_lines(self, a):
        return td.lines_via_stop(self._linedict, a)
    
    def stop_position(self, a):
        return self._stopdict[a]

    def transition_time(self, a, b):
        alpha_sorted = sorted([a, b])
        return self._timedict[alpha_sorted[0]][alpha_sorted[1]]


# TODO: your own trams.readTramNetwork()
def readTramNetwork(tramfile=TRAM_FILE):
    with open(tramfile, "r", encoding="utf-8") as f:
        data = json.load(f)
        stops, lines, times = data["stops"], data["lines"], data["times"]
        return TramNetwork(lines, stops, times)


def specialize_stops_to_lines(network):
    # Converting to a list due to edges being changed below
    origin_edges = list(network.edges())

    for stop in network.all_stops():
        network.remove_vertex(stop)
        for line in network.stop_lines(stop):
            network.add_vertex(tuple([stop, line]))
        same_stop = [vertex for vertex in network.vertices() if vertex[0] == stop]
        for vertex in same_stop:
            comp_same_stop = same_stop
            comp_same_stop.remove(vertex)
            for comp_vertex in comp_same_stop:
                network.add_edge(vertex, comp_vertex)

    for s1, s2 in origin_edges:
        for line in network.all_lines():
            if (
                tuple([s1, line]) in network.vertices()
                and tuple([s2, line]) in network.vertices()
            ):
                network.add_edge(tuple([s1, line]), tuple([s2, line]))

    return network

def specialized_transition_time(spec_network, a, b, changetime=10):
    return changetime if a[0] == b[0] else spec_network.transition_time(a[0],b[0])

def specialized_geo_distance(spec_network, a, b, changedistance=0.02):
    return changedistance if a[0] == b[0] else spec_network.geo_distance(a[0],b[0])
