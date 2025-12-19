from sys import exception
from django.shortcuts import render
from .forms import RouteForm
from django.http import HttpResponseBadRequest
import tram.utils.trams as trams
from .utils.tramviz import show_shortest
from django.http import HttpResponseBadRequest

def tram_net(request):
    return render(request, 'tram/home.html', {})

def find_route(request):
    form = RouteForm()
    if request.method == "POST":
        form = RouteForm(request.POST)
        if form.is_valid():
            route = form.data
            try:
                timepath, geopath, outfile = show_shortest(route['dep'], route['dest'])
            except:
                network = trams.readTramNetwork()
                if route['dep'] not in network.all_stops():
                    stop = route['dep']
                else:
                    stop = route['dest']
                return HttpResponseBadRequest(f'<h2>Unknown stop name: <u>{stop}</u></h2> Return<a href="http://127.0.0.1:8000/route/"> <u><b>HERE</b></u></a>')

            return render(
                request,
                'tram/show_route.html',
                {
                    'route': form.instance.__str__(),
                    'timepath': timepath,
                    'geopath': geopath,
                    'shortest_path_svg': outfile,
                }
            )
        else:
            form = RouteForm()
    return render(request, 'tram/find_route.html', {'form': form})
