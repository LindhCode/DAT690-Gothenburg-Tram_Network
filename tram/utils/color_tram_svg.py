"""
Path visualization with direct colouring of SVG file.
Colours SVG directly, specialized to SVG produced by graphviz.
"""

import xml.etree.ElementTree as et

def color_svg_network(
        infile,
        outfile,
        colormap=lambda v: 'red'
    ):
    tree = et.parse(infile)
    root = tree.getroot()
    ns = '{http://www.w3.org/2000/svg}'
    lns = len(ns)
    rg = root.find(ns+'g')
    for g in rg.iter(ns+'g'):
        if g.get('class') == 'node':
            stop = g.find(ns+'title').text
            for p in g.iter():
                if p.tag[-7:] == 'polygon':
                    p.set('fill', colormap(stop))
    xns = '{http://www.w3.org/1999/xlink}'
    lxns = len(xns)
    for elem in root.iter():
        elem.tag = elem.tag[lns:]
        for k, v in elem.items():
            if k[:lxns] == xns:
                elem.set(k[lxns:], v)
                # del elem[k]

    tree.write(outfile)
