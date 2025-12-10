
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # 3D 绘图所必需的
from matplotlib import cm # 用于 colormap
class plot_function:
    """
    -------------------------------
    MATLAB-style plotting interface
    -------------------------------
    """
    # class variables
    _current_figure = None  # Remembers which window we're currently working with
    _current_axis = None    # Remembers which plotting area inside the window we're using
    _figure_count = 0       # Counts how many windows we've created
    _hold_state = False     # Determines if new plots go in the same window or create new ones
    _current_coord_system = 'cartesian'  # 'cartesian' or 'polar'

    #class method is used to manage variables that can be used across instances
    @classmethod
    def figure(cls,num=None):
        if num is not None :
            plt.figure(num) #plt built in function. If already exist draw on this figure, if not create a figure of num
        else:
            cls._figure_count += 1
            plt.figure(cls._figure_count)
        
        #cls._hold_state = False
        cls._current_figure = plt.gcf()  # Get Current Figure, return a figure object defined by matplotlib
        cls._current_axis = plt.gca()    # Get Current Axis
        return cls._current_figure       # allow users to use more detailed matplotlib operations
    @classmethod
    def hold(cls, state=None):   #the matlab use of hold decides whether or not to paint on one figure
        if state is None:
            cls._hold_state = not cls._hold_state
        else:
            try :
                state_str = str(state).lower()
                if state_str == 'on':
                    cls._hold_state=True
                else:
                    cls._hold_state=False
            except:
                cls._hold_state = bool(cls._hold_state)
        if cls._hold_state:
            print("Hold: on - subsequent plots will be added to current axis")
        else:
            print("Hold: off - subsequent plots will create new figures")
        
        return cls._hold_state
    
    @classmethod
    def switch(cls, coord_system=None):
        if coord_system is None:
            cls._current_coord_system = 'polar' if cls._current_coord_system == 'cartesian' else 'cartesian' # linear way to simplify ‘if’ argument
        else:
            coord_str = str(coord_system).lower()
            
            if coord_str in ['polar', 'on']:
                cls._current_coord_system = 'polar'
            elif coord_str in ['cartesian', 'cart', 'off']:
                cls._current_coord_system = 'cartesian'
            else:
                print(f"warning: non-exsistent coordinate '{coord_system}', use current coordinate : {cls._current_coord_system}")
        
        # 移除此处的 figure 创建逻辑，避免创建空白 Figure, 解决了空白figure的bug
        # Figure 的创建将完全交给 plot() 函数
        # 在进行接下来的3D绘图时遇到了相似的bug，应该也移除类似的逻辑
        # if cls._current_figure is not None and not cls._hold_state:
        #     cls._create_appropriate_figure() 
        # print _current_coordinate_system:
        status_msg = "on" if cls._current_coord_system == 'polar' else "off"
        print(f"Polar: {status_msg} - subsequent plots will use {cls._current_coord_system} coordinate system")
        return cls._current_coord_system
        
    @classmethod
    def _create_appropriate_figure(cls):
        # Creates a new figure and an appropriate axis (polar or cartesian).
        cls._figure_count += 1
        plt.figure(cls._figure_count)
        
        if cls._current_coord_system == 'polar':
            # 修复：使用 plt.subplot(polar=True) 替代 plt.polar()
            # subplot is more robust and returns the axis object directly
            # in the following '_setup_polar_axes' we will set axes returned by this function.
            plt.subplot(111, polar=True)
        # else: default cartesian axis is created by plt.gca() below
        
        cls._current_figure = plt.gcf()
        cls._current_axis = plt.gca()
        cls._current_axis.grid(True, alpha=0.3)

                
    @classmethod
    def _setup_polar_axes(cls):
        '''for advanced subtle adjustion user can change E to W, 1 to -1 etc, if needed'''
        if cls._current_coord_system == 'polar' and cls._current_axis is not None:
            # 设置theta零点在x正方向（右侧）
            cls._current_axis.set_theta_zero_location('E')  # Eest
            # 设置theta方向为逆时针（数学标准）
            cls._current_axis.set_theta_direction(-1)  # -1表示逆时针

    @classmethod
    def plot(cls, x, y=None, fmt='-', label=None, linewidth=1.5, **kwargs): # ** means dictionary, we will use the keys in the following code
        # Plot data. If only one arg provided, treat it as y and use x=range(len(y)). This is a shortcut for constant functions, similar to matlab
        if y is None:
            y = x
            x = np.arange(len(y))
        
        # 简化/修复 Figure/Axes 检查逻辑：
        # 1. 如果 hold off，或没有当前 Figure，则创建一个新的 Figure 和 Axes。
        if (not cls._hold_state) or (cls._current_figure is None):
            cls._create_appropriate_figure()
        # 2. 如果 hold on，则在当前 Axes 上绘图。
        # 3. 移除之前复杂且可能有 bug 的 Axes 类型不匹配检查。

        # Following is the original code to parse which was designed for cartesian ploting
        # Record which aliases were provided by user so explicit None is respected
        orig_keys = set(kwargs.keys())
        color_provided = ('color' in orig_keys) or ('c' in orig_keys)
        ls_provided = ('linestyle' in orig_keys) or ('ls' in orig_keys)
        marker_provided = 'marker' in orig_keys

        # Pop alias values (if any) to avoid passing duplicates later.This is a major bug I fixed(by vibe coding), the code can't run otherwise.
        user_color = kwargs.pop('color', None) if 'color' in orig_keys else (kwargs.pop('c', None) if 'c' in orig_keys else None)
        user_linestyle = kwargs.pop('linestyle', None) if 'linestyle' in orig_keys else (kwargs.pop('ls', None) if 'ls' in orig_keys else None)
        user_marker = kwargs.pop('marker', None) if 'marker' in orig_keys else None

        parsed_color, parsed_marker, parsed_linestyle = cls._parse_format(fmt)

        # Decide final attributes: user-specified (even None) wins; otherwise parsed fmt
        final_color = user_color if color_provided else parsed_color
        if ls_provided:
            final_linestyle = 'None' if user_linestyle is None else user_linestyle
        else:
            final_linestyle = user_linestyle if user_linestyle is not None else parsed_linestyle
        final_marker = user_marker if marker_provided else parsed_marker

        # Build kwargs to pass to matplotlib — only include keys that are not None
        plot_kwargs = {}
        if final_color is not None:
            plot_kwargs['color'] = final_color
        if final_linestyle is not None:
            plot_kwargs['linestyle'] = final_linestyle
        if final_marker is not None:
            plot_kwargs['marker'] = final_marker
        plot_kwargs['linewidth'] = linewidth
        if label:
            plot_kwargs['label'] = label

        # any remaining kwargs are safe to merge
        plot_kwargs.update(kwargs)

        # Call matplotlib without positional fmt string (avoids duplicate kwargs)
        line = cls._current_axis.plot(x, y, **plot_kwargs)

        # --- 分离 Cartesian 和 Polar 绘图后的设置逻辑 ---
        if cls._current_coord_system == 'polar':
            cls._setup_polar_axes()  # 极坐标特有设置
        
        cls._current_axis.grid(True, alpha=0.3) # 统一设置 grid
        
        if label:
            cls._current_axis.legend()
        return line
        

    @classmethod
    def polar(cls, *args, **kwargs):
        """
        直接使用matplotlib的plot函数在极坐标轴上绘图，并设置theta零点在x正方向。
        用法: 
            polar(theta, r) 
            polar(theta, r, 'r--')
        """
        # 临时切换到极坐标
        original_system = cls._current_coord_system
        cls._current_coord_system = 'polar'
        
        # 确保在极坐标轴上，如果当前不是极坐标轴，则创建一个新的极坐标 figure
        current_is_polar = hasattr(cls._current_axis, 'set_theta_zero_location') if cls._current_axis is not None else False
        
        if (not cls._hold_state) or (cls._current_figure is None) or (not current_is_polar):
            # 新建 Figure (如果 hold off 或 axes 类型不匹配)
            cls._figure_count += 1
            plt.figure(cls._figure_count)
            plt.subplot(111, polar=True)
            cls._current_figure = plt.gcf()
            cls._current_axis = plt.gca()
            cls._setup_polar_axes()
        
        # 使用matplotlib的plot在极坐标轴上绘图
        if args:
            line = cls._current_axis.plot(*args, **kwargs)
        else:
            line = cls._current_axis.plot([], [])
        
        # 确保极坐标设置正确
        cls._setup_polar_axes()
        cls._current_axis.grid(True, alpha=0.3)
        
        # 恢复原始坐标系
        if original_system != 'polar':
            cls._current_coord_system = original_system
            
        return line

    @classmethod
    def _parse_format(cls, fmt):
        """Return (color, marker, linestyle) from a matlab-like fmt string."""
        if fmt is None or fmt == '':
            return None, None, 'solid'
        fmt = str(fmt)

        colors = {'b':'blue','g':'green','r':'red','c':'cyan','m':'magenta','y':'yellow','k':'black','w':'white'}
        markers = {'.':'.','o':'o','x':'x','+':'+','*':'*','s':'s','d':'d','^':'^','v':'v','<':'<','>':'>'}
        linestyles = {'--':'dashed','-.':'dashdot',':':'dotted','-':'solid'}

        color = None
        marker = None
        linestyle = None

        # match multi-char linestyles first
        for key in sorted(linestyles.keys(), key=len, reverse=True):
            if key in fmt:
                linestyle = linestyles[key]
                fmt = fmt.replace(key, '', 1)
                break

        # match color (single char)
        for ch in fmt:
            if ch in colors:
                color = colors[ch]
                fmt = fmt.replace(ch, '', 1)
                break

        # match marker (single char)
        for ch in fmt:
            if ch in markers:
                marker = markers[ch]
                fmt = fmt.replace(ch, '', 1)
                break

        # marker-only means no connecting line
        if (marker is not None) and (linestyle is None):
            linestyle = 'None'

        # fallback default: solid line
        if (linestyle is None) and (marker is None):
            linestyle = 'solid'

        return color, marker, linestyle

    @classmethod
    def title(cls, text):
        if cls._current_axis is None:
            cls.figure()        
            print('No current axes exist. Automatically create a figure.')
        cls._current_axis.set_title(text)
    
    @classmethod
    def xlabel(cls, text):
        """Set x-axis label"""
        # 注意：极坐标轴没有 x/y label
        if cls._current_axis:
            current_is_polar = hasattr(cls._current_axis, 'set_theta_zero_location')
            if not current_is_polar:
                 cls._current_axis.set_xlabel(text)
            else:
                 print("Warning: xlabel is ignored for polar coordinates.")
    
    @classmethod
    def ylabel(cls, text):
        """Set y-axis label"""
        # 注意：极坐标轴没有 x/y label
        if cls._current_axis:
            current_is_polar = hasattr(cls._current_axis, 'set_theta_zero_location')
            if not current_is_polar:
                 cls._current_axis.set_ylabel(text)
            else:
                 print("Warning: ylabel is ignored for polar coordinates.")

    @classmethod
    def grid(cls, state=True):
        """Turn grid on/off"""
        if cls._current_axis:
            cls._current_axis.grid(state, alpha=0.3)
    
    @classmethod
    def legend(cls, *args, **kwargs):
        """Show legend"""
        if cls._current_axis:
            cls._current_axis.legend(*args, **kwargs)
    
    @classmethod
    def show(cls, block=True):
        """
        MATLAB-style show function
        Usage: show() or show(block=False)
        """
        plt.show(block=block)
    
    @classmethod
    def close(cls, num='all'):
        """
        MATLAB-style close function
        Usage: close(), close('all'), close(1)
        """
        if num == 'all':
            plt.close('all')
            cls._current_figure = None
            cls._current_axis = None
        else:
            plt.close(num)
    
    @classmethod
    def subplot(cls, rows, cols, index):
        """
        MATLAB-style subplot
        Usage: subplot(2, 2, 1)
        """
        # Note: If the coordinate system is 'polar', this subplot will be polar.
        if cls._current_coord_system == 'polar':
            cls._current_axis = plt.subplot(rows, cols, index, polar=True)
            cls._setup_polar_axes()
        else:
            cls._current_axis = plt.subplot(rows, cols, index)
            
        cls._current_figure = plt.gcf()
        return cls._current_axis
#-------------------------------------------------------------------------------------------------

class plot3_function:
    """
    MATLAB-style 3D plotting interface with robust format/kwarg handling.
    """
    _current_figure = None
    _current_axis = None
    _figure_count = 0
    _hold_state = False

    @classmethod
    def figure3(cls, num=None):
        """Create or activate a 3D figure."""
        if num is not None:
            plt.figure(num)
        else:
            cls._figure_count += 1
            plt.figure(cls._figure_count)

        fig = plt.gcf()
        ax = fig.gca()
        is_3d_axes = isinstance(ax, Axes3D)
        
        if not fig.axes or not is_3d_axes:
            fig.clf()
            ax = fig.add_subplot(111, projection='3d')

        cls._current_figure = fig
        cls._current_axis = ax
        cls._current_axis.grid(True, alpha=0.3)
        #cls._hold_state = False this is why there always a blank figure when calling figure3
        return cls._current_figure

    @classmethod
    def _ensure_3d_axis(cls, force_new=False):
        """Ensure current axis exists and is 3D projection."""
        current_is_3d = isinstance(cls._current_axis, Axes3D) if cls._current_axis else False
        
        # 简化条件：什么时候需要创建一个新的 Figure/Axes？
        # 1. 强制新建 (force_new)
        # 2. hold off (not cls._hold_state)
        # 3. 当前 Axes 不存在 或 存在但不是 3D
        needs_new_axes = force_new or (not cls._hold_state) or (cls._current_axis is None) or (not current_is_3d)

        if needs_new_axes:
            # 如果 hold off，创建新 Figure；如果 hold on 但 Axes 无效，激活当前 Figure。
            # 由于 figure3 内部有 clf() 逻辑，我们始终调用它，但要确保它激活正确的 Figure。
            
            # 如果是 hold on 状态下 Axes 丢失，我们激活当前的 Figure 编号，否则就创建一个新的。
            fig_num = cls._current_figure.number if cls._hold_state and cls._current_figure else None
            
            # figure3 负责确保创建的 Axes 是 3D 的，并设置 cls._current_axis
            cls.figure3(num=fig_num) 
        
        return cls._current_axis
    
    @classmethod
    def hold(cls, state=None):
        """Toggle or set hold state for 3D plots."""
        if state is None:
            cls._hold_state = not cls._hold_state
        else:
            state_str = str(state).lower()
            cls._hold_state = (state_str == 'on')

        if cls._hold_state:
            print("Hold: on - subsequent 3D plots will be added to current 3D axis")
        else:
            print("Hold: off - subsequent 3D plots will create new 3D figures")
        return cls._hold_state

    @classmethod
    def _parse_format_3d(cls, fmt):
        """
        Parse MATLAB-style format string for 3D plots.
        Returns (color, marker, linestyle) — same as 2D _parse_format.
        """
        if fmt is None or fmt == '':
            return None, None, 'solid'
        fmt = str(fmt)

        colors = {'b':'blue','g':'green','r':'red','c':'cyan','m':'magenta','y':'yellow','k':'black','w':'white'}
        markers = {'.':'.','o':'o','x':'x','+':'+','*':'*','s':'s','d':'d','^':'^','v':'v','<':'<','>':'>'}
        linestyles = {'--':'dashed','-.':'dashdot',':':'dotted','-':'solid'}

        color = None
        marker = None
        linestyle = None

        # match multi-char linestyles first
        for key in sorted(linestyles.keys(), key=len, reverse=True):
            if key in fmt:
                linestyle = linestyles[key]
                fmt = fmt.replace(key, '', 1)
                break

        # match color (single char)
        for ch in fmt:
            if ch in colors:
                color = colors[ch]
                fmt = fmt.replace(ch, '', 1)
                break

        # match marker (single char)
        for ch in fmt:
            if ch in markers:
                marker = markers[ch]
                fmt = fmt.replace(ch, '', 1)
                break

        # marker-only means no connecting line
        if (marker is not None) and (linestyle is None):
            linestyle = 'None'

        # fallback default: solid line
        if (linestyle is None) and (marker is None):
            linestyle = 'solid'

        return color, marker, linestyle

    @classmethod
    def plot3(cls, x, y, z, fmt='-', label=None, linewidth=1.5, **kwargs):
        """
        MATLAB-style plot3(x, y, z, 'fmt', label=..., linewidth=..., **kwargs).
        Supports format strings like 'r--o', with robust alias handling.
        """
        ax = cls._ensure_3d_axis()

        # Record which aliases were provided by user
        orig_keys = set(kwargs.keys())
        color_provided = ('color' in orig_keys) or ('c' in orig_keys)
        ls_provided = ('linestyle' in orig_keys) or ('ls' in orig_keys)
        marker_provided = 'marker' in orig_keys

        # Pop alias values to avoid duplicates
        user_color = kwargs.pop('color', None) if 'color' in orig_keys else (kwargs.pop('c', None) if 'c' in orig_keys else None)
        user_linestyle = kwargs.pop('linestyle', None) if 'linestyle' in orig_keys else (kwargs.pop('ls', None) if 'ls' in orig_keys else None)
        user_marker = kwargs.pop('marker', None) if 'marker' in orig_keys else None

        # Parse format string
        parsed_color, parsed_marker, parsed_linestyle = cls._parse_format_3d(fmt)

        # Decide final attributes: user-specified (even None) wins; otherwise parsed fmt
        final_color = user_color if color_provided else parsed_color
        if ls_provided:
            final_linestyle = 'None' if user_linestyle is None else user_linestyle
        else:
            final_linestyle = user_linestyle if user_linestyle is not None else parsed_linestyle
        final_marker = user_marker if marker_provided else parsed_marker

        # Build kwargs to pass to matplotlib — only include keys that are not None
        plot_kwargs = {}
        if final_color is not None:
            plot_kwargs['color'] = final_color
        if final_linestyle is not None:
            plot_kwargs['linestyle'] = final_linestyle
        if final_marker is not None:
            plot_kwargs['marker'] = final_marker
        plot_kwargs['linewidth'] = linewidth
        if label:
            plot_kwargs['label'] = label

        # any remaining kwargs are safe to merge
        plot_kwargs.update(kwargs)

        # Call matplotlib 3D plot
        line = ax.plot(x, y, z, **plot_kwargs)
        
        ax.grid(True, alpha=0.3)
        if label:
            ax.legend()
        return line

    @classmethod
    def surf(cls, X, Y, Z, fmt=None, cmap=cm.viridis, label=None, **kwargs):
        """
        MATLAB-style surf(X, Y, Z, cmap=..., **kwargs).
        fmt parameter reserved for future use (currently ignored for surface).
        """
        ax = cls._ensure_3d_axis()

        # For surf, we mainly use cmap and other surface-specific kwargs
        # Pop common style aliases if provided (though less relevant for surface)
        kwargs.pop('color', None)
        kwargs.pop('c', None)
        kwargs.pop('linestyle', None)
        kwargs.pop('ls', None)
        kwargs.pop('marker', None)

        # Build surf kwargs
        surf_kwargs = {'cmap': cmap}
        surf_kwargs.update(kwargs)

        surface = ax.plot_surface(X, Y, Z, **surf_kwargs)
        
        if label:
            # Surface doesn't support label in legend, but store as title or annotation
            ax.set_title(label)
        
        ax.grid(True, alpha=0.3)
        return surface

    @classmethod
    def mesh(cls, X, Y, Z, fmt=None, color='blue', label=None, **kwargs):
        """
        MATLAB-style mesh(X, Y, Z, color=..., **kwargs).
        fmt parameter reserved for future use (currently ignored for wireframe).
        """
        ax = cls._ensure_3d_axis()

        # For mesh, pop format-related aliases (less relevant but for consistency)
        kwargs.pop('c', None)
        kwargs.pop('linestyle', None)
        kwargs.pop('ls', None)
        kwargs.pop('marker', None)

        # Build mesh kwargs
        mesh_kwargs = {'color': color}
        mesh_kwargs.update(kwargs)

        mesh_obj = ax.plot_wireframe(X, Y, Z, **mesh_kwargs)
        
        if label:
            ax.set_title(label)
        
        ax.grid(True, alpha=0.3)
        return mesh_obj

    @classmethod
    def zlabel(cls, text):
        """Set z-axis label."""
        ax = cls._ensure_3d_axis()
        ax.set_zlabel(text)
    
    @classmethod
    def xlabel(cls, text):
        """Set x-axis label."""
        ax = cls._ensure_3d_axis()
        ax.set_xlabel(text)
    
    @classmethod
    def ylabel(cls, text):
        """Set y-axis label."""
        ax = cls._ensure_3d_axis()
        ax.set_ylabel(text)

    @classmethod
    def title(cls, text):
        """Set plot title."""
        ax = cls._ensure_3d_axis()
        ax.set_title(text)

    @classmethod
    def grid(cls, state=True):
        """Turn grid on/off."""
        if cls._current_axis:
            cls._current_axis.grid(state, alpha=0.3)
            
    @classmethod
    def show(cls, block=True):
        """Show all 3D figures."""
        plt.show(block=block)
    
    @classmethod
    def close(cls, num='all'):
        """Close 3D figure(s)."""
        if num == 'all':
            plt.close('all')
            cls._current_figure = None
            cls._current_axis = None
        else:
            plt.close(num)
# ...existing code...



# 统一 hold 函数：使其能同时控制 2D 和 3D 的 hold 状态
def hold1(state=None):
    # 调用 2D 类的 hold 方法
    state_2d = plot_function.hold(state)
    # 调用 3D 类的 hold 方法（传入相同状态）
    # 由于 plot3_function.hold 内部有打印信息，这里避免重复打印
    
    # 临时重写 print，确保只打印 2D hold 的结果
    # 实际项目中可以直接修改 plot3_function.hold 方法，使其不打印或返回 bool
    
    # 这里我们直接调用其内部逻辑并更新状态，避免重复提示
    if state is None:
        state_3d = not plot3_function._hold_state
    else:
        state_str = str(state).lower()
        state_3d = (state_str == 'on')
    
    plot3_function._hold_state = state_3d
    
    return state_2d # 返回统一的 hold 状态
hold =hold1


figure = plot_function.figure
figure3 = plot3_function.figure3
plot = plot_function.plot
plot3 = plot3_function.plot3
surf = plot3_function.surf
mesh = plot3_function.mesh
switch = plot_function.switch    #polar plotting
polar = plot_function.polar      #polar plotting
title = plot_function.title
xlabel = plot_function.xlabel
ylabel = plot_function.ylabel
zlabel = plot3_function.zlabel # 3D
grid = plot_function.grid
legend = plot_function.legend
show = plot_function.show
close = plot_function.close
subplot = plot_function.subplot  # subplot has some issue to be settled 

#math tools ---- easier to call
pi = np.pi
linspace = np.linspace
sin = np.sin
cos = np.cos
tan = np.tan
exp = np.exp
log = np.log
log10 = np.log10
sqrt = np.sqrt
min = np.min
mean = np.mean
max = np.max

#同时注释多行：ctrl+/


