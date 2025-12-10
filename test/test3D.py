from minimatlab import *
import numpy as np
from matplotlib import cm
from minimatlab.plot_package import plot3_function 
# Now the queation is why the fuck should I import ploy_package again after I had written import *? what the ******* 12.10.20.30
# 示例 1: 3D 曲线图 (plot3)
close('all') # 关闭所有 Figure

figure3(1) # 创建 Figure 1，强制为 3D
t = linspace(0, 10 * pi, 500)
x = sin(t)
y = cos(t)
z = t

plot3(x, y, z, 'r-', linewidth=2, label='Helix') # 绘制 3D 螺旋线
hold('on')

# 添加第二个 3D 曲线
plot3(x * 0.5, y * 0.5, z, 'b--', linewidth=1)

title('3D Helix Plot')
xlabel('X-axis')
ylabel('Y-axis')
zlabel('Z-axis (Time)')
show()


# 示例 2: 3D 曲面图 (surf) 和网格图 (mesh)
close('all')

figure3(2)
X = linspace(-5, 5, 50)
Y = linspace(-5, 5, 50)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = sin(R) / R # Mexican hat function

# 绘制曲面图
s = surf(X, Y, Z, cmap=cm.coolwarm, alpha=0.7) # 返回 Surface 对象
title('3D Surface Plot (surf)')
zlabel('Z')

# 高级功能：利用返回的 Surface 对象添加 Colorbar
fig = plot3_function._current_figure # 获取当前 Figure
fig.colorbar(s, shrink=0.5, aspect=5)
show()

# 示例 3: 3D 网格图 (mesh)
close('all')

figure3(3)
mesh(X, Y, Z, color='black') # 绘制网格图
title('3D Wireframe Plot (mesh)')
show()


# 3D line plot with format string
x = linspace(0, 10, 100)
y = sin(x)
z = cos(x)
plot3(x, y, z, 'b-o', label='3D curve')
show()

# 3D surface
X = linspace(-5, 5, 50)
Y = linspace(-5, 5, 50)
[X, Y] = np.meshgrid(X, Y)
Z = X**2 + Y**2
figure3()
surf(X, Y, Z)
show()