from minimatlab import*
x=linspace(-10,10,800)
# y=x+1/x**2 # Note here the matplotlib will handle 0 dividion 
 
# hold()
y=1/3*x-sin(2*x)/3
y1=x**2/6+1/12*cos(2*x)
plot(x,y)
hold()
plot(x,y1)
show()
