# About Minimatlab 
Minimatlab is a simplified version of matlab, with function calls almost as the same as matlab (Maybe even more simplified).
We aim to make this project useful for us student, helping us learn maths， physics and of course CS.
The developers of this programme are new to python, so please be tolerant of the bugs of the programme.

# Setup: How to install ?

Copy our project from github https://github.com/natoo-chow/minimatlab or ask me to send you the .zip

In the terminal paste:
```bash
pip install -r requirements.txt
```

Create a setup.py in the same root of minimatlab, copy and paste the following code:
```python
from setuptools import setup, find_packages
setup(
    name="minimatlab",
    version="1.0.0",
    author="Nathan",
    packages=find_packages(),
)
```

After that in the terminal type:
```bash
cd minimatlab
pip -e install 
```
-e means editing mode. If you want to make adjustments in this project, just do whatever you want!
check whether your file name is straight minimatlab, if it is minimatlab-master it's because you directly copy the code. Change it into minimatlab

If something else goes wrong, ask ai for help.

# usage 1 Function Plotting with plot_package 

This guide is going to lead you through the basic usage of plot_package, which is a powerful tool for function plotting. Note that if you put your mouse on the function name, you can see its docstring for more information.

### 0. cheat sheet

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

### 1. Let's start!

first import our package 
```python
from minimatlab import *
```
In this way we can directly use whatever function calls shown above in the cheat sheet.

### 2. create figure

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

### 3. The hold() Machanism
Every time you type `hold()`,you change the hold stage of the working environment just like matlab.The default value is "False"
When hold is "on", you'll be able to layer multiple plots on the same canvas(or "axes")
When hold is "False", the next plot will be in a different window.
You can use `hold('True')` or `hold('on')` to specifically manage the hold state.

### 4. About switch()
Similarly as `hold()`,`switch()`manages the current coordinate that you're working on.The default value is "cartesian"
Every time you type `switch()`,you change the coordinate system of the working environment.
When switch is "polar",you can use `polar()` to plot polar functions.
When switch is "cartesian",you can use `plot()` to plot cartesian functions.
You can use `switch('polar')` or `switch('cartesian')` to specifically manage the coordinate system.

### 5. subplot() function
The `subplot()` function allows you to create multiple plots in a single figure.subplot(m, n, p) divides the figure into an m-by-n grid and creates axes in the position specified by p. 
'p' means left to right, top to bottom the p th plot.

### 6. Figure()
Handle multiple figures using the `figure()` function is recommanded when you want to create a lot of plots in one file.
Even if you don't use `figure()`, the package will automatically create figures for you, but using `figure()` gives you more control over which figure you're working on.
not specify working figure would cause some issues sometimes.

### 7. 3D Plotting
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

### 8. Decoration 
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

# Usage 2 Numerical Computation with Num_cal
This library provides three specialized tools for solving different types of mathematical problems, and all tools support the **Plot Mode** visualization feature.

## I. Tool A: Root Finder (fsolve_all)
### Function
Solves equations (finds the intersection points between a mathematical curve and the x-axis, i.e., the roots of the equation)

### Conceptual Analogy
It works like a **"metal detector"** for mathematical graphs, scanning the curve to pinpoint where it touches the x-axis.

### Required Parameters (3 Settings to Provide)
1. **The Rule**: The mathematical formula to be solved (e.g., "x squared minus 4")
2. **The Search Zone**: A specified range for the search (e.g., "look between -10 and 10"). The tool will not search outside this boundary.
3. **The Step Size**: The precision level of the search. A smaller step size enables a more thorough search but takes longer; a larger step size is faster but may miss potential solutions.

### Output Result
Returns a **list of all solutions** found within the specified search zone.

## II. Tool B: Area Calculator (integral)
### Function
Calculates definite integrals (computes the total area between a curved line and the coordinate axis below it)

### Conceptual Analogy
It acts as a **"slicer"**, measuring the total area enclosed between the curve and the underlying coordinate axis.

### Required Parameters (4 Settings to Provide)
1. **The Curve**: The mathematical formula representing the shape of the graph
2. **Start Point**: The left boundary where the area measurement begins
3. **End Point**: The right boundary where the area measurement ends
4. **Slice Count**: The number of thin rectangular strips the shape is divided into for calculation (e.g., 1000). A higher number of slices results in a more accurate calculation.

### Output Result
Returns a **single numerical value** representing the total area.

## III. Tool C: Future Predictor (RK4)
### Function
Solves differential equations (predicts the future trajectory of a system based on its change rules and initial state)

### Conceptual Analogy
It functions as a **"simulator"**. If you know the rules governing how an object moves or changes (such as gravity or cooling rate) and its initial state, this tool can predict its future path.

### Required Parameters (4 Settings to Provide)
1. **The Rule of Change**: A formula describing how the value changes over time (e.g., "Speed depends on Height and Time")
2. **The Timeline**: The duration of the simulation (e.g., "from second 0 to second 5")
3. **The Starting Position**: The initial value at the start time of the simulation
4. **The Step Size**: The frequency at which the computer recalculates the position. A smaller step size (e.g., 0.01) generates a smoother, high-definition simulation trajectory.

### Output Result
Generates a complete trajectory dataset (a **list of time points and their corresponding values**).

## IV. Visual Mode (Plot Mode)
All the three tools above come with this special feature, which can be toggled using a boolean value (True/False).

### Plot OFF (False)
The tool runs silently in the background and only returns numerical results.

### Plot ON (True)
The tool will open a pop-up window to plot the results with the following effects:
1. **Root Finder**: Plots the curve and marks the solution points with red dots
2. **Area Calculator**: Fills the measured area with green dashed lines
3. **Future Predictor**: Draws a red line showing the object's trajectory over time

# Usage 3: Interactive Data Analysis Calculator
This guide will walk you through the full functionality of the Interactive Data Analysis Calculator, a user-friendly tool for data loading, cleaning, processing, statistical analysis, and visualization.

## 0. Cheat Sheet

| Category               | Function                          | Example Usage                                  |
| :--------------------- | :-------------------------------- | :--------------------------------------------- |
| Data Loading           | load_data(file_path)              | load_data("data.xlsx"), load_data("data.csv")   |
| Data Cleaning          | clean_data(df)                    | cleaned_df = clean_data(raw_df)                |
| Column Operation       | add_custom_column(df)             | df = add_custom_column(df) (input formula: "col1+col2") |
| Data Filtering         | filter_data_by_condition(df)      | filtered_df = df.query("col>10 and col2<50")    |
| Basic Statistics       | calculate_statistics(df)          | stats_dict, corr_matrix = calculate_statistics(df) |
| Hypothesis Testing     | hypothesis_test(df)               | t-test (col1 vs col2), chi2-test (cat1 vs cat2) |
| Visualization          | visualize_data(df)                | Scatter/Histogram/Fitting Curve                 |
| Data Display           | print(df.head())                  | Show first 5 rows of current data               |

## 1. Let's Start!
First, run the script directly. The program will launch an interactive interface—no additional import statements are required (dependencies are pre-included in the script).
```python
# Run the script in terminal or IDE
python project.py
```
After running, you’ll see the welcome message: `📊 交互式数据分析计算器`

## 2. Data Loading
The tool supports **.xlsx** and **.csv** formats. Enter the full file path when prompted (relative path is supported if the file is in the same folder as the script):
```
请输入文件路径(data.xlsx): data.csv
```
- If the file format is unsupported, the program will prompt: `❌ 仅支持.xlsx或.csv格式`
- If the file is missing or corrupted, it will show the error details: `❌ 加载失败：[error message]`

## 3. Core Function Usage
### 3.1 Automatic Data Cleaning
Select function number `1` to delete all "Unnamed" columns (common redundant columns in Excel/CSV exports):
```
功能菜单：输入功能编号：1
```
- Result prompt: `✅ 已删除X个无用列` (X is the number of deleted columns)
- The cleaned data will be printed automatically for verification.

### 3.2 Add Custom Column
Select function number `2` to add a new column using a custom formula (use existing column names for calculations):
```
功能菜单：输入功能编号：2
请输入新列名：total_score
请输入total_score的计算规则（如x+y、x*2等，用列名表示）：math+english+science
```
- Supported operators: `+` (addition), `-` (subtraction), `*` (multiplication), `/` (division), `**` (power), etc.
- Result prompt: `✅ 已新增列：total_score` (the updated data will be printed)
- Error prompt for invalid formulas: `❌ 公式错误：[error message]` (e.g., typos in column names)

### 3.3 Filter Data by Condition
Select function number `3` to filter data using logical conditions (supports `and`/`or`/`>`/`<`/`==` operators):
```
功能菜单：输入功能编号：3
请输入筛选条件（如x>3 and y<5）：age>18 and income>5000
```
- Result prompt: `✅ 筛选出X行数据` (X is the number of filtered rows)
- The first 5 rows of the filtered data will be printed (use `print(filtered_df)` to view all if needed).

### 3.4 Calculate Basic Statistics
Select function number `4` to compute key statistics for numeric columns and correlation matrix:
```
功能菜单：输入功能编号：4
```
- Output includes:
  - Mean and variance for each numeric column: `📈 统计结果：- col1：均值XX.XXXX，方差XX.XXXX`
  - Correlation matrix (rounded to 4 decimal places): `🔗 相关系数矩阵：[matrix table]`
- Only numeric columns (int/float) are included in calculations (non-numeric columns are automatically skipped).

### 3.5 Hypothesis Testing
Select function number `5` to perform t-test (for numeric data) or chi-square test (for categorical data):
#### Option 1: T-test (Compare two numeric columns)
```
功能菜单：输入功能编号：5
请选择检验类型（1.t检验 2.卡方检验）：1
输入第一列名：group_a_score
输入第二列名：group_b_score
```
- Output: `t统计量：XX.XXXX，p值：XX.XXXX`
- Conclusion: `拒绝原假设` (p<0.05, significant difference) or `接受原假设` (p≥0.05, no significant difference)

#### Option 2: Chi-square Test (Check association between two categorical columns)
```
功能菜单：输入功能编号：5
请选择检验类型（1.t检验 2.卡方检验）：2
输入分类列1：gender
输入分类列2：purchase_status
```
- Output: `卡方统计量：XX.XXXX，p值：XX.XXXX`
- Conclusion: `拒绝原假设（存在关联）` (p<0.05) or `接受原假设（无关联）` (p≥0.05)

### 3.6 Data Visualization
Select function number `6` to generate 2D scatter plots, histograms, or fitting curves (supports 4 model types):
#### Option 1: Scatter Plot (Show relationship between two numeric columns)
```
功能菜单：输入功能编号：6
请选择图表类型（1.散点图 2.直方图 3.拟合曲线）：1
输入X轴列名：study_hours
输入Y轴列名：test_score
```
- The plot will automatically display with title, axis labels, and 60% transparent points.

#### Option 2: Histogram (Show distribution of a single numeric column)
```
功能菜单：输入功能编号：6
请选择图表类型（1.散点图 2.直方图 3.拟合曲线）：2
输入列名：age
```
- Default settings: 10 bins, 70% transparency; the plot shows frequency distribution of the column.

#### Option 3: Fitting Curve (Fit data with linear/quadratic/exponential/power models)
```
功能菜单：输入功能编号：6
请选择图表类型（1.散点图 2.直方图 3.拟合曲线）：3
输入X轴列名：advertising_cost
输入Y轴列名：sales
请选择拟合模型（1.线性 2.二次 3.指数 4.幂函数）：1
```
- Output: A plot with raw data points (scatter) and red fitting curve, plus R² value (shows goodness of fit, closer to 1 = better fit).

### 3.7 Display Current Data
Select function number `7` to preview the current data (first 5 rows by default):
```
功能菜单：输入功能编号：7
```
- Output: `当前数据预览:` + the first 5 rows of the current DataFrame.

### 3.8 Exit Program
Select function number `0` to exit the program:
```
功能菜单：输入功能编号：0
```
- Exit prompt: `👋 程序结束`

## 4. Key Notes
1. **Data Type Requirements**: Numeric columns (int/float) are required for statistics, t-test, and fitting; categorical columns (object/str) are required for chi-square test.
2. **Formula Rules**: When adding columns or filtering, use exact existing column names (case-sensitive); avoid special characters.
3. **Visualization**: Close the current plot window to return to the function menu and continue operations.
4. **Error Handling**: If the input is invalid (e.g., wrong column name, illegal formula), the program will prompt an error and retain the original data state.

## 5. Dependencies
Ensure the following libraries are installed before running (run the command in terminal):
```bash
pip install pandas numpy matplotlib scipy openpyxl
```
- `openpyxl`: Required for reading .xlsx files; omit if only using .csv files.

# Usage 4 : Matrix Operation with Matrix_module