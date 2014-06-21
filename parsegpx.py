import sys, string
from xml.dom import minidom, Node
from datetime import datetime

from math import log, tan, pi

import cairo
import rsvg

class GPXParser:
  def __init__(self, filename):
    self.tracks = {}
    try:
      doc = minidom.parse(filename)
      doc.normalize()
    except:
      return # handle this properly later
    gpx = doc.documentElement
    for node in gpx.getElementsByTagName('trk'):
      self.parseTrack(node)

  def parseTrack(self, trk):
    name = trk.getElementsByTagName('name')[0].firstChild.data
    if not name in self.tracks:
      self.tracks[name] = []
    for trkseg in trk.getElementsByTagName('trkseg'):
      for trkpt in trkseg.getElementsByTagName('trkpt'):
        lat = float(trkpt.getAttribute('lat'))
        lon = float(trkpt.getAttribute('lon'))
        ele = float(trkpt.getElementsByTagName('ele')[0].firstChild.data)
        rfc3339 = trkpt.getElementsByTagName('time')[0].firstChild.data
        rfc3339 = datetime.strptime(rfc3339, '%Y-%m-%dT%H:%M:%SZ')
        self.tracks[name].append((lat, lon, ele, rfc3339))

def main():
    WIDTH, HEIGHT = (300, 300)
    parser = GPXParser("steig.gpx")

    fo = open("test.svg", "w")
    gp = open("gnuplot.dat", "w")
    surface = cairo.SVGSurface (fo, WIDTH, HEIGHT)
    ctx = cairo.Context (surface)
    ctx.scale (WIDTH/1.0, HEIGHT/1.0)

    for lat, lon, ele, time in parser.tracks["Nibelungensteig on GPSies.com"]:
        ctx.line_to(lon, -180/pi*log(tan(pi/4 + lat*(pi/180)/2.0)))
        gp.write("%f %f %f\n"%(lat, lon, ele))

    ctx.set_source_rgb(0.3, 0.2, 0.5) # Solid color
    ctx.set_line_width(0.02)
    ctx.stroke()
    ctx.close_path()

    f = open("start.txt", "r")
    f.readline()

    for line in f:
        if line == '\r\n':
            break
        lat, lon = map(float, line.split('\t')[:2])
        ctx.move_to(lon, -180/pi*log(tan(pi/4 + lat*(pi/180)/2.0)))
        ctx.arc(lon, -180/pi*log(tan(pi/4 + lat*(pi/180)/2.0)), 0.0005, 0.0, 2.0*pi)
        ctx.set_source_rgb(1.0, 0.0, 0.0)
        ctx.fill_preserve()
        ctx.close_path()

    surface.finish()

if __name__ == "__main__":
    main()
