import numpy as np
from minimatlab import *

def lorenz(t, state, sigma=10.0, rho=28.0, beta=8.0/3.0):
    x, y, z = state
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return [dx, dy, dz]

def integrate_lorenz(y0, t0, t1, npts=10000):
    t = linspace(t0, t1, npts) #time span
    #try part is an advanced way to solve lorenz system, but for now we use RK4 which has been covered in my partner's work, but here I extend it into 3 dimensional.
    #-----------------------------------------------
    # try:
        # from scipy.integrate import solve_ivp
        # sol = solve_ivp(lambda tt, yy: lorenz(tt, yy), (t0, t1), y0, t_eval=t, rtol=1e-8)
        # X, Y, Z = sol.y[0], sol.y[1], sol.y[2]
        # return t, X, Y, Z
    # except Exception:
    #-----------------------------------------------
    y = np.empty((npts, 3)) # a two dimensional matrix where the first row is time steps, each has a column of x,y,z values
    y[0] = y0
    for i in range(npts - 1):
        dt = t[i+1] - t[i]
        k1 = np.array(lorenz(t[i], y[i])) # array is to inforce coordinate calculation
        k2 = np.array(lorenz(t[i] + dt/2.0, y[i] + dt * k1 / 2.0))
        k3 = np.array(lorenz(t[i] + dt/2.0, y[i] + dt * k2 / 2.0))
        k4 = np.array(lorenz(t[i] + dt, y[i] + dt * k3))
        y[i+1] = y[i] + dt * (k1 + 2*k2 + 2*k3 + k4) / 6.0
    return t, y[:,0], y[:,1], y[:,2]
# above is just math way to generate punch of (x,y,z) do this by researching online or ask ai, below is the very easy part you can write yourself.

def main():
    y0 = [1.0, 1.0, 1.0]
    t, X, Y, Z = integrate_lorenz(y0, 0.0, 50.0, npts=10000)

    figure3()
    plot3(X, Y, Z, fmt='-', color='purple', linewidth=0.6)
    title('Lorenz attractor')
    xlabel('x')
    ylabel('y')
    zlabel('z')
    hold('on')
    y1 = [1.0, 1.0, 1.05]
    t, X1, Y1, Z1 = integrate_lorenz(y1, 0.0, 50.0, npts=10000)
    plot3(X1, Y1, Z1, fmt='-', color='orange', linewidth=0.6)
    title('Lorenz attractor with different initial conditions')
    show()
#the same as previous ones.
if __name__ == '__main__':
    main()
