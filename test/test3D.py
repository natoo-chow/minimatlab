from minimatlab import *
from matplotlib import cm
# Now the question is why the fuck should I import plot3_function again after I had written import *? what the ******* 12.10.20.30
# The above annoying problem has been fixed. It was due to silly issues (not saving the file after modifying it)
# Example 1: 3D curve (plot3)
close('all') # Close all figure (not necessary)
# Note when plotting punch of figures, it is recommended to use 'figure(your figure number or name)' to specify what figure you're currently working on. figure3 is to create a 3D figure
figure3(1) # Create a 3D figure
t = linspace(0, 10 * pi, 500)
x = sin(t)
y = cos(t)
z = t
plot3(x, y, z, 'r-', linewidth=2, label='Helix') # Draw 3D helix(螺旋线)

hold('on')# Add a second 3D curve on the same figure

plot3(x * 0.5, y * 0.5, z, 'b--', linewidth=1)

title('3D Helix Plot')
xlabel('X-axis')
ylabel('Y-axis')
zlabel('Z-axis (Time)')
show()


# Example 2: 3D surf(曲面图) 和 mesh (网格图)
close('all')

figure3(2)
X = linspace(-5, 5, 50)
Y = linspace(-5, 5, 50)
X, Y = meshgrid(X, Y) # Every possible combination of x, y values.
R = sqrt(X**2 + Y**2)
Z = sin(R) / R # Mexican hat function

# surf 绘制曲面图 
s = surf(X, Y, Z, cmap=cm.coolwarm, alpha=0.7) # return Surface object. coolwarm:color alpha:transparency
title('3D Surface Plot (surf)')
zlabel('Z')

show()

# Example 3: 3D Wireframe Plot (mesh)
close('all')

figure3(3)
mesh(X, Y, Z, color='black') 
title('3D Wireframe Plot (mesh)')
show()


# 3D line plot with format string
hold('off')
figure3(4)
x = linspace(0, 10, 100)
y = sin(x)
z = cos(x)
plot3(x, y, z, 'b-o', label='3D curve')
title('3D Line Plot with Format String')
show()

# 3D surface
X = linspace(-5, 5, 50)
Y = linspace(-5, 5, 50)
[X, Y] = meshgrid(X, Y)
Z = X**2 + Y**2
figure3(5)
surf(X, Y, Z)
show()

# T=linspace(0,273,500)
# P=linspace(0,101325,500)
# V=linspace(0,1,500)
# plot3(T, P, V, 'r-', linewidth=2, label='PV Diagram')
# show()

#Example of meshgrid
'''
x = np.array([1, 2, 3])  # 长度m=3
y = np.array([4, 5])     # 长度n=2

X, Y = np.meshgrid(x, y)

print("X =", X)
print("Y =", Y)

Output:
X = [[1 2 3]
     [1 2 3]]  
Y = [[4 4 4]
     [5 5 5]]
Z = X + Y
Z = .....(every possible combination of X + Y)
     
'''