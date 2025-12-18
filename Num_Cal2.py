import numpy as np
import plot_package as pp

class Num_Cal:
    # class variables for default settings
    _default_tol = 1e-6 

    def __init__(self, tol=None):
        if tol is not None:
            self.tol = tol
        else:
            self.tol = self._default_tol

    # Internal helper to calculate derivative (slope)
    def _deriv(self, fun, x):
        h = 1e-6
        # Central difference formula
        return (fun(x + h) - fun(x-h)) / (2*h)

    # Core Solver: Find a single root using Newton-Raphson method
    # Note: This function focuses on calculation only, no plotting logic here
    def fsolve(self, fun, x0, max_iter=100):
        x = float(x0)
        
        # Main iteration loop
        for i in range(max_iter):
            y = fun(x)
            
            # Check convergence (if y is close enough to 0)
            if abs(y) < self.tol:
                return x, True # Success
            
            # Calculate derivative
            d = self._deriv(fun, x)
            
            # Avoid division by zero
            if abs(d) < 1e-10:
                return x, False # Failed (slope is too flat)
            
            # Update x using Newton's formula
            x = x - y / d
            
        return x, False # Failed (exceeded max iterations)

    # Advanced Solver: Find multiple roots within a specific range
    def fsolve_all(self, fun, search_range, step=1.0, plot=False):
        """
        fun: The target function
        search_range: [start, end], e.g., [-10, 10]
        step: Gap between initial guesses (smaller step = more accurate but slower)
        plot: Whether to visualize the results
        """
        start, end = search_range
        
        guesses = np.arange(start, end, step)
        
        found_roots = []
        
        for x0 in guesses:
            root, success = self.fsolve(fun, x0)
            
            if success:
                is_new = True
                for r in found_roots:
                    if abs(root - r) < 1e-4:
                        is_new = False
                        break
                
                if is_new and start <= root <= end:
                    found_roots.append(root)
        
        # Sort roots for better readability
        found_roots.sort()

        # --- Visualization Section ---
        if plot:
            pp.figure()
            pp.hold('on') # Allow multiple plots on one figure
            
            # Plot the function curve
            x_vals = np.linspace(start, end, 200)
            y_vals = [fun(x) for x in x_vals]
            pp.plot(x_vals, y_vals, 'b-', label='Function')
            
            # Plot reference line at y=0
            pp.plot([start, end], [0, 0], 'k--')
            
            # Mark all found roots with red circles
            if len(found_roots) > 0:
                # Create a list of zeros [0, 0, ...] for plotting
                zeros_y = [0] * len(found_roots)
                pp.plot(found_roots, zeros_y, 'ro', label='Roots')
                print(f"Roots found: {found_roots}")
            else:
                print("No roots found.")

            pp.title(f"Found {len(found_roots)} roots")
            pp.legend()
            pp.grid(True)
            pp.show()
            
        return found_roots

    #Calculate integral using Trapezoidal rule
    def integral(self, fun, a, b, n=1000, plot=False):
        """
        Calculate definite integral using Composite Trapezoidal Rule.
        
        Parameters:
        -----------
        fun : function
            Target function f(x) to integrate
        a : float
            Lower limit of integration
        b : float
            Upper limit of integration
        n : int
            Number of sub-intervals (higher n = better precision)
        plot : bool
            If True, visualize the area under the curve
            
        Returns:
        --------
        total_area : float
            Approximated area under the curve
        """
        width = (b - a) / n
        total_area = 0
        
        #Store points for plotting
        x_points = []
        y_points = []
        
        for i in range(n):
            x1 = a + i * width
            x2 = a + (i + 1) * width
            y1 = fun(x1)
            y2 = fun(x2)
            
            #Trapezoid area calculation
            area = (y1 + y2) * width / 2
            total_area += area
            
            if plot:
                x_points.append(x1)
                y_points.append(y1)

        #Visualize integration area
        if plot:
            pp.figure()
            pp.hold('on')
            
            pp.plot(x_points, y_points, 'b-', label='f(x)')
            
            #Draw vertical lines to represent area
            for i in range(0, len(x_points), 20): #Sample points to avoid clutter
                xi = x_points[i]
                yi = y_points[i]
                pp.plot([xi, xi], [0, yi], 'g--', linewidth=0.5)
                
            pp.title(f"Calculated Area = {total_area:.4f}")
            pp.xlabel("x axis")
            pp.ylabel("y axis")
            pp.show()
            
        return total_area

    #Solve ODE using RK4 (Fixed step size)
    def RK4(self, fun, tspan, y0, h=0.01, plot=False):
        """
        Solve ODE using Runge-Kutta 4th order method.
        
        Parameters:
        -----------
        fun : function
            ODE function dy/dt = fun(t, y)
        tspan : list or array
            Time span [a, b] for integration
        y0 : float
            Initial condition y(a)
        h : float
            Step size (smaller h = more accurate but slower)
        plot : bool
            If True, visualize the solution
            
        Returns:
        --------
        t_values : array
            Time points where solution is computed
        y_values : array
            Corresponding solution values y(t)
        """
        t_start, t_end = tspan    #tspan=[a,b]
        t_values = np.arange(t_start, t_end, h)
        y_values = [y0]
        y = y0
        
        #Runge-Kutta 4th order steps
        for t in t_values[:-1]:
            k1 = fun(t, y)
            k2 = fun(t + 0.5 * h, y + 0.5 * h * k1)
            k3 = fun(t + 0.5 * h, y + 0.5 * h * k2)
            k4 = fun(t + h, y + h * k3)
            
            slope = (k1 + 2*k2 + 2*k3 + k4) / 6
            y = y + h * slope
            
            y_values.append(y)
            
        if plot:
            pp.figure()
            pp.plot(t_values, y_values, 'r-', label='y(t)')
            pp.title("ODE Solution")
            pp.xlabel("Time")
            pp.ylabel("Value")
            pp.grid(True)
            pp.legend()
            pp.show()
            
        return np.array(t_values), np.array(y_values)

#Testing block
if __name__ == "__main__":
    nc = Num_Cal()
    
    #Test fsolve
    print("Testing fsolve...")
    f1 = lambda x: np.sin(x)
    nc.fsolve_all(f1,[-5, 5], step=0.5, plot=True)
    
    #Test integral
    print("Testing integral...")
    f2 = lambda x: np.sin(x)
    nc.integral(f2, 0, np.pi, plot=True)

    #Test RK4
    print("Testing RK4...")
    f3 = lambda t, y: -y + t      #dy/dt = -y + t
    nc.RK4(f3, [0, 5], 1, plot=True)    
