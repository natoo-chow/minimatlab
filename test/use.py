from minimatlab import *
x = linspace(-1/4*pi,-0.000001, 800)
y =tan(x)/x
plot(x,y)
x1= linspace(-100,-0.001,800)
y1= sin(1/x1)
plot(x1,y1)
hold()
x2= linspace(0.0001,100,800)
y2= sin(1/x2)
plot(x2,y2)
show()