# bzip2 -d -c germany.osm.bz2 | osmosis --read-xml enableDateParsing=no file=/dev/stdin --bounding-box top=49.761 left=8.589 bottom=49.564 right=9.352 --write-xml file=- | gzip -9 -c > odenwald.osm
import xml.parsers.expat
import sys
import cairo
from math import pi, log, tan

WIDTH = 300
HEIGHT = 300

lat = 0;
lon = 0;
name = "";
shop = "";

entries = list()

# 3 handler functions
def start_element(elem, attrs):
    global lat, lon, name, shop
    if elem == "node":
        lat = attrs["lat"]
        lon = attrs["lon"]
    elif elem == "tag":
        if attrs["k"] == "name":
            name = attrs["v"]
        elif attrs["k"] == "shop":
            shop = attrs["v"]

def end_element(elem):
    global lat, lon, name, shop, entries
    if elem == "node" and name \
        and shop in ["supermarket", "bakery", "butcher", "beverages"]:
        #entries.append((lat, lon, shop, name))
        print "\t".join([lat, lon, shop, name]).encode("utf8")
        lat = 0
        lon = 0
        name = ""
        shop = ""

def char_data(data):
    pass

p = xml.parsers.expat.ParserCreate()

p.StartElementHandler = start_element
p.EndElementHandler = end_element
p.CharacterDataHandler = char_data

p.ParseFile(sys.stdin)

exit()

fo = open("test2.svg", "w")
surface = cairo.SVGSurface (fo, WIDTH, HEIGHT)
ctx = cairo.Context (surface)
ctx.scale (WIDTH/1.0, HEIGHT/1.0)

for lat, lon, shop, name in entries:
    lat = float(lat)
    lon = float(lon)
    if shop == "beverages":
        ctx.move_to(lon, -180/pi*log(tan(pi/4 + lat*(pi/180)/2.0)))
        ctx.arc(lon, -180/pi*log(tan(pi/4 + lat*(pi/180)/2.0)), 0.0005, 0.0, 2.0*pi)
        ctx.close_path()
        #ctx.set_source_rgb(1.0, 1.0, 0.0)
        #ctx.set_source_rgb(1.0, 0.0, 1.0)
        #ctx.set_source_rgb(1.0, 0.5, 0.0)
        ctx.set_source_rgb(1.0, 0.0, 0.5)
        ctx.fill_preserve()

surface.finish()
