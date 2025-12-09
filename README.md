# About Minimatlab 
Minimatlab is a simplified version of matlab, with function calls almost as the same as matlab.
We aim to make this project useful for us student, helping us learn maths， physics and of course CS.
The developers of this programme are new to python, so please be tolerant of the bugs of the programme.

# usage

Mini-MATLAB 绘图库使用教程

本教程将指导你如何使用 plot_package 模块。该模块封装了 Python 的 Matplotlib，使其语法和行为（如 hold on/off，格式字符串 'r--' 等）高度模仿 MATLAB。

0. 准备工作

假设你已经将提供的代码保存为 plot_package.py。
在你的主脚本中，你需要引入所有内容：

code
Python
download
content_copy
expand_less
# 推荐这样引入，可以直接使用 sin, cos, pi 等变量，完全模拟 MATLAB 环境
from plot_package import *
1. 基础 2D 绘图 (Cartesian)

最基本的绘图功能，支持 MATLAB 风格的简写格式字符串。

code
Python
download
content_copy
expand_less
# 准备数据 (使用库内集成的 numpy 函数)
x = linspace(0, 2*pi, 100)
y = sin(x)

# 1. 创建图形并绘图
figure(1)           # 创建或激活 Figure 1
plot(x, y, 'r--')   # 红色虚线
title('Sine Wave')
xlabel('Time (s)')
ylabel('Amplitude')
grid(True)          # 打开网格

show()              # 显示图像

支持的格式字符串 (fmt):

颜色: r (红), g (绿), b (蓝), k (黑), w (白), y (黄), m (洋红), c (青)

线型: - (实线), -- (虚线), -. (点划线), : (点线)

标记: o (圆点), * (星号), . (点), x (叉号), s (方块) 等

示例: plot(x, y, 'bo-') (蓝色实线带圆点标记)

2. Hold 机制 (叠加绘图)

这是该库的核心功能之一，模拟了 MATLAB 的状态机绘图模式。

code
Python
download
content_copy
expand_less
x = linspace(0, 10, 100)
y1 = sin(x)
y2 = cos(x)

figure(2)

# 绘制第一条线
plot(x, y1, 'b-', label='Sin', linewidth=2) 

# 开启 Hold on，之后的绘图将叠加在当前坐标轴上
hold('on') 

# 绘制第二条线
plot(x, y2, 'r--', label='Cos')

legend() # 显示图例
title('Hold On Demo')

# 养成好习惯，画完后关闭 hold，以免影响后续绘图
hold('off') 

show()
3. 极坐标绘图 (Polar)

该库提供了两种方式进行极坐标绘图：状态切换法和直接调用法。

方法 A：使用 switch 切换坐标系 (推荐)

这种方式更像状态机，适合连续画多张极坐标图。

expand_less
theta = linspace(0, 2*pi, 100)
r = 1 - sin(theta)  # 心形线

# 切换到极坐标模式
switch('polar') 

figure(3)
plot(theta, r, 'm-', linewidth=2)
title('Cardioid (Polar Switch)')

# 记得切换回直角坐标系，否则后续 plot 都会是极坐标
switch('cartesian') 

show()
方法 B：使用 polar 函数

直接在极坐标下绘图。

theta = linspace(0, 4*pi, 200)
r = theta 

figure(4)
polar(theta, r, 'g--')
title('Spiral (Direct Polar Function)')
show()
4. 3D 绘图

该库封装了 Axes3D，并通过 figure3 自动管理 3D 上下文。

3D 曲线 (plot3)
code
Python
download
content_copy
expand_less
# 生成 3D 螺旋线数据
t = linspace(0, 20, 200)
x = sin(t)
y = cos(t)
z = t

# 使用 figure3 强制初始化 3D 环境
figure3(5) 

plot3(x, y, z, 'r-', linewidth=1)
title('3D Helix')
zlabel('Height')
show()
3D 曲面 (surf) 与 网格 (mesh)
code
Python
download
content_copy
expand_less
# 生成网格数据
X = linspace(-5, 5, 50)
Y = linspace(-5, 5, 50)
X, Y = np.meshgrid(X, Y) # 这里的 np 需要保证你导入了 numpy 或者使用库里的别名
R = sqrt(X**2 + Y**2)
Z = sin(R)

figure3(6)
# 绘制曲面
surf(X, Y, Z, cmap=cm.coolwarm) 
title('Sinc Function Surface')

figure3(7)
# 绘制网格
mesh(X, Y, Z, color='b')
title('Sinc Function Mesh')

show()
5. 子图 (Subplot)

支持标准的行列索引方式。

code
Python
download
content_copy
expand_less
x = linspace(0, 10, 100)

figure(8)

# 左上角
subplot(2, 2, 1)
plot(x, sin(x), 'r')
title('Subplot 1')

# 右上角
subplot(2, 2, 2)
plot(x, cos(x), 'b')
title('Subplot 2')

# 左下角 (演示在 subplot 中使用极坐标)
switch('polar') # 切换状态
subplot(2, 2, 3) # 这个 subplot 会变成极坐标
theta = linspace(0, 2*pi, 50)
plot(theta, np.ones_like(theta), 'g-')
switch('cartesian') # 切回来

# 右下角
subplot(2, 2, 4)
plot(x, tan(x), 'k')
axis_limit = [-10, 10] # 注意：库里没封装 ylim，这里仅演示
plt.ylim(-5, 5) # 混合使用 matplotlib 原生命令也是可以的
title('Subplot 4')

show()
6. 内置数学工具

为了让体验更像 MATLAB，代码底部封装了常用的 Numpy 函数。你可以直接使用：

pi

sin, cos, tan

exp, log (自然对数), log10

sqrt

linspace

min, max, mean

示例:

y = exp(-0.5 * linspace(0, 10, 100)) * sin(2 * pi * linspace(0, 10, 100))
7. 综合示例：蒙特卡洛圆周率模拟

这是一个将上述功能结合在一起的完整脚本示例。

from plot_package import *
import numpy as np # 用于生成随机数

# 1. 准备数据
N = 1000
x = np.random.rand(N)
y = np.random.rand(N)
d = sqrt(x**2 + y**2)

inside_idx = d <= 1
x_in, y_in = x[inside_idx], y[inside_idx]
x_out, y_out = x[~inside_idx], y[~inside_idx]

# 2. 开始绘图
figure(10)
hold('on') # 开启叠加模式

# 画圆弧 (1/4圆)
theta = linspace(0, pi/2, 100)
plot(cos(theta), sin(theta), 'k-', linewidth=2, label='Circle Boundary')

# 画点
plot(x_in, y_in, 'b.', label='Inside')
plot(x_out, y_out, 'r.', label='Outside')

# 装饰
title(f'Monte Carlo PI Simulation (N={N})')
xlabel('X')
ylabel('Y')
legend()
grid(True)
axis_equal = plt.axis('equal') # 调用 matplotlib 原生命令让比例尺一致

hold('off')
show()
总结

figure(n) / figure3(n): 控制窗口。

hold('on'/'off'): 控制是否覆盖。

plot(..., 'fmt'): 核心绘图，支持字符串样式。

switch('polar'): 开启极坐标模式。

show(): 记得最后调用这个来显示窗口。


    
