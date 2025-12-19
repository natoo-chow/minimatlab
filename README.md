# About Minimatlab 
Minimatlab is a simplified version of matlab, with function calls almost as the same as matlab.
We aim to make this project useful for us student, helping us learn maths， physics and of course CS.
The developers of this programme are new to python, so please be tolerant of the bugs of the programme.

# Setup: How to install ?

copy our project from github https://github.com/natoo-chow/minimatlab or ask me to send you the .zip
In the terminal paste:
```bash
pip install -r requirements.txt
```

create a setup.py in the same root of minimatlab
copy and paste the following code:
```python
from setuptools import setup, find_packages
setup(
    name="minimatlab",
    version="1.0.0",
    author="Nathan",
    packages=find_packages(),
)
```

after that in the terminal type:
```bash
cd minimatlab
pip -e install 
```
-e means editing mode. If you want to make adjustments in this project, just do whatever you want!
check whether your file name is straight minimatlab, if it is minimatlab-master it's because you directly copy the code. Change it into minimatlab

if something else goes wrong, ask ai for help.

# usage 1 Mini-MATLAB 

This guide is going to lead you through the basic usage of plot_package, which is a powerful tool for function plotting. Note that if you put your mouse on the function name, you can see its docstring for more information.

0. cheat sheet
| Category   | Function                  | Example Usage                              |
| :--------- | :------------------------ | :----------------------------------------- |
| Control    | figure(), figure3()       | figure(1), figure3()                       |
|            | hold()                    | hold('on'), hold('off')                    |
|            | subplot()                 | subplot(2, 1, 1)                           |
| 2D Plot    | plot()                    | plot(x, y, 'r--o', label='Data')           |
|            | switch()                  | switch('polar') (Toggles polar mode)       |
|            | polar()                   | polar(theta, r, 'g-')                      |
| 3D Plot    | plot3()                   | plot3(x, y, z, 'b-', linewidth=2)          |
|            | surf()                    | surf(X, Y, Z, cmap=cm.plasma)              |
|            | mesh()                    | mesh(X, Y, Z, color='red')                 |
| Labels     | title(), xlabel(), ylabel() | title('My Plot'), xlabel('Time')           |
|            | zlabel()                  | zlabel('Height') (3D only)                 |
| Math       | pi, sin, cos, exp, linspace | x = linspace(0, 2*pi, 100)                 |
| Display    | grid(), legend(), show()  | grid(True), legend(), show()               |
1. Let's start!

first import our package 
```python
from minimatlab import *
```
In this way we can directly use whatever function calls shown above in the cheat sheet.

2. create figure

The `plot` function mimics MATLAB's syntax, including the ability to pass a single argument (interpreted as Y-values) and shorthand format strings.

```python
x = linspace(0, 10, 100)
y = sin(x)

figure(1)
plot(x, y, 'b-', label='Sine')
title('Harmonic Motion')
xlabel('Time (s)')
ylabel('Amplitude')
grid(True)
legend()
show()
```
*Note*: Do not forget to use `show()` at the end to display the plot.

3. The hold() Machanism
Every time you type `hold()`,you change the hold stage of the working environment just like matlab.The default value is "False"
When hold is "on", you'll be able to layer multiple plots on the same canvas(or "axes")
When hold is "False", the next plot will be in a different window.
You can use `hold('True')` or `hold('on')` to specifically manage the hold state.

4. About switch()
Similarly as `hold()`,`switch()`manages the current coordinate that you're working on.The default value is "cartesian"
Every time you type `switch()`,you change the coordinate system of the working environment.
When switch is "polar",you can use `polar()` to plot polar functions.
When switch is "cartesian",you can use `plot()` to plot cartesian functions.
You can use `switch('polar')` or `switch('cartesian')` to specifically manage the coordinate system.

5. subplot() function
The `subplot()` function allows you to create multiple plots in a single figure.subplot(m, n, p) divides the figure into an m-by-n grid and creates axes in the position specified by p. 
'p' means left to right, top to bottom the p th plot.

6. Figure()
Handle multiple figures using the `figure()` function is recommanded when you want to create a lot of plots in one file.
Even if you don't use `figure()`, the package will automatically create figures for you, but using `figure()` gives you more control over which figure you're working on.
not specify working figure would cause some issues sometimes.

7. 3D Plotting
In this part, there're some advanced features inherited from matplotlib for 3D plotting. We have to import `cm` from `matplotlib` for colormaps and some other functionalities you may need.
To create 3D plots, you can use the `plot3()`, `surf()`, and `mesh()` functions. Here's an example of a 3D surface plot:
```python
# Example 1: 3D curve (plot3)
close('all') # Close all figure (not necessary)

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
X, Y = meshgrid(X, Y)
R = sqrt(X**2 + Y**2)
Z = sin(R) / R # Mexican hat function

# surf 绘制曲面图 
s = surf(X, Y, Z, cmap=cm.coolwarm, alpha=0.7) # return Surface object
title('3D Surface Plot (surf)')
zlabel('Z')

# Advanced function: Use the returned surface object to add colorbar
fig = figure3(2) # get current Figure
fig.colorbar(s, shrink=0.5, aspect=5)
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
```

8. Decoration 
You can use `title()`, `xlabel()`, `ylabel()`, and `zlabel()` to add titles and axis labels to your plots. The `grid()` function adds a grid to the plot for better readability, and `legend()` displays the legend for labeled plots.
Following format of line is supported in 2D and 3D plot:

| Type         | Symbol                          | Description                  |
| :----------- | :------------------------------ | :--------------------------- |
| **Colors**   | b                               | blue（蓝色）                 |
|              | g                               | green（绿色）                |
|              | r                               | red（红色）                  |
|              | c                               | cyan（青色）                 |
|              | m                               | magenta（品红）              |
|              | y                               | yellow（黄色）               |
|              | k                               | black（黑色）                |
|              | w                               | white（白色）                |
| **Markers**  | .                               | point（点）                  |
|              | o                               | circle（圆形）               |
|              | x                               | x-mark（叉号）               |
|              | +                               | plus（加号）                 |
|              | *                               | star（星号）                 |
|              | s                               | square（正方形）             |
|              | d                               | diamond（菱形）              |
|              | ^                               | triangle（三角形，向上）     |
| **Line Styles** | -                              | solid（实线）                |
|              | --                              | dashed（虚线）               |
|              | -.                              | dash-dot（点划线）           |
|              | :                               | dotted（点线）               |
