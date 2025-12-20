from minimatlab import *
# We can also directly plot in polar coordinates by polar function
theta=linspace(0,2*pi,100)
r=100*[2] #Note r and theta must be the same length(same dimensions)
polar(theta,r,'r--')
show()

