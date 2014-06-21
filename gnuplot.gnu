# set terminal png transparent nocrop enhanced font arial 8 size 420,320 
# set output 'surface1.17.png'
splot "gnuplot.dat" with boxes, "" with lines lt 2
