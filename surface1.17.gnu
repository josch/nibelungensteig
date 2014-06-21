# set terminal png transparent nocrop enhanced font arial 8 size 420,320 
# set output 'surface1.17.png'
set dummy u,v
set parametric
set view 70, 20, 1, 1
set samples 51, 51
set isosamples 30, 33
set hidden3d offset 1 trianglepattern 3 undefined 1 altdiagonal bentover
sinc(u,v) = sin(sqrt(u**2+v**2)) / sqrt(u**2+v**2)
xx = 6.08888888888889
dx = 1.11
x0 = -5
x1 = -3.89111111111111
x2 = -2.78222222222222
x3 = -1.67333333333333
x4 = -0.564444444444444
x5 = 0.544444444444445
x6 = 1.65333333333333
x7 = 2.76222222222222
x8 = 3.87111111111111
x9 = 4.98
xmin = -4.99
xmax = 5
n = 10
zbase = -1
splot [u=.5:3*n-.5][v=-4.99:4.99] 	 xmin+floor(u/3)*dx, v, ((floor(u)%3)==0) ? zbase : 			 (((floor(u)%3)==1) ? sinc(xmin+u/3.*dx,v) : 1/0) notitle
