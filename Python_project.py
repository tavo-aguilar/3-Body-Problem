# 3 body project

import math
import numpy as np
import pylab as py



# initialization animation function: plot the background of each frame
def init():
    line1.set_data([], [])
    line2.set_data([], [])

    return (line1, line2)


# Force (Earth and Sun) Forces broken up into two components (sin and cos)
def force_es(r):
    F = np.zeros(2)
    Fmag = GG * Me * Ms / (np.linalg.norm(r) + 1e-20) ** 2
    theta = math.atan(np.abs(r[1]) / (np.abs(r[0]) + 1e-20))
    F[0] = Fmag * np.cos(theta)
    F[1] = Fmag * np.sin(theta)
    if r[0] > 0:
        F[0] = -F[0]
    if r[1] > 0:
        F[1] = -F[1]

    return F


# Force (Jupiter and Sun)
def force_js(r):
    F = np.zeros(2)
    Fmag = GG * Mj * Ms / (np.linalg.norm(r) + 1e-20) ** 2
    theta = math.atan(np.abs(r[1]) / (np.abs(r[0]) + 1e-20))
    F[0] = Fmag * np.cos(theta)
    F[1] = Fmag * np.sin(theta)
    if r[0] > 0:
        F[0] = -F[0]
    if r[1] > 0:
        F[1] = -F[1]

    return F


# Force (Earth and Jupiter)
def force_ej(re, rj):
    r = np.zeros(2)
    F = np.zeros(2)
    r[0] = re[0] - rj[0]
    r[1] = re[1] - rj[1]
    Fmag = GG * Me * Mj / (np.linalg.norm(r) + 1e-20) ** 2
    theta = math.atan(np.abs(r[1]) / (np.abs(r[0]) + 1e-20))
    F[0] = Fmag * np.cos(theta)
    F[1] = Fmag * np.sin(theta)
    if r[0] > 0:
        F[0] = -F[0]
    if r[1] > 0:
        F[1] = -F[1]

    return F


def force(r, planet, ro, vo):
    if planet == 'earth':
        return force_es(r) + force_ej(r, ro)
    if planet == 'jupiter':
        return force_js(r) - force_ej(r, ro)


# Velocity
def dr_dt(t, r, v, planet, ro, vo):
    return v


# Acceleration
def dv_dt(t, r, v, planet, ro, vo):
    F = force(r, planet, ro, vo)
    if planet == 'earth':
        y = F / Me
    if planet == 'jupiter':
        y = F / Mj
    return y


# Differential equation solvers

def EulerSolver(t, r, v, h):
    z = np.zeros([2, 2])
    r1 = r + h * dr_dt(t, r, v)
    v1 = v + h * dv_dt(t, r, v)
    z = [r1, v1]
    return z

def EulerCromerSolver(t, r, v, h):
    z = np.zeros([2, 2])
    r = r + h * dr_dt(t, r, v)
    v = v + h * dv_dt(t, r, v)
    z = [r, v]
    return z

def RK4Solver(t, r, v, h, planet, ro, vo):
    k11 = dr_dt(t, r, v, planet, ro, vo)
    k21 = dv_dt(t, r, v, planet, ro, vo)

    k12 = dr_dt(t + 0.5 * h, r + 0.5 * h * k11, v + 0.5 * h * k21, planet, ro, vo)
    k22 = dv_dt(t + 0.5 * h, r + 0.5 * h * k11, v + 0.5 * h * k21, planet, ro, vo)

    k13 = dr_dt(t + 0.5 * h, r + 0.5 * h * k12, v + 0.5 * h * k22, planet, ro, vo)
    k23 = dv_dt(t + 0.5 * h, r + 0.5 * h * k12, v + 0.5 * h * k22, planet, ro, vo)

    k14 = dr_dt(t + h, r + h * k13, v + h * k23, planet, ro, vo)
    k24 = dv_dt(t + h, r + h * k13, v + h * k23, planet, ro, vo)

    y0 = r + h * (k11 + 2. * k12 + 2. * k13 + k14) / 6.
    y1 = v + h * (k21 + 2. * k22 + 2. * k23 + k24) / 6.

    z = np.zeros([2, 2])
    z = [y0, y1]
    return z


def mplot(fign, x, y, xl, yl, clr, lbl):
    py.figure(fign)
    py.xlabel(xl)
    py.ylabel(yl)
    return py.plot(x, y, clr, linewidth=1.0, label=lbl)


Me = 6e24  # Mass of Earth (kg)
Ms = 2e30  # Mass of Sun (kg)
Mj = 1.9e27  # Mass of Jupiter (kg)

G = 6.673e-11  # Gravitational Constant

RR = 1.496e11  # Normalizing distance in km (= 1 AU)
MM = 6e24  # Normalizing mass
TT = 365 * 24 * 60 * 60.0  # Normalizing time (1 year)

FF = (G * MM ** 2) / RR ** 2  # Unit force


GG = (MM * G * TT ** 2) / (RR ** 3)

Me = Me / MM  # Normalized mass of Earth
Ms = Ms / MM  # Normalized mass of Sun

factor = 500  # Size of Jupiter
Mj = factor * Mj / MM  # Normalized mass of Jupiter

ti = 0  # initial time = 0
tf = 12  # final time = # of years years

print(f'Jupiter is {factor}x times its normal size')
print(f'Orbit after {tf} years')

N = 100 * tf  # 100 points per year
t = np.linspace(ti, tf, N)  # time array from ti to tf with N points

h = t[2] - t[1]  # time step (uniform)

# Vectors
r = np.zeros([N, 2])  # position vector of Earth
v = np.zeros([N, 2])  # velocity vector of Earth
rj = np.zeros([N, 2])  # position vector of Jupiter
vj = np.zeros([N, 2])  # velocity vector of Jupiter

ri = [1496e8 / RR, 0]  # initial position of earth (m)
rji = [5.2, 0]  # initial position of Jupiter

vv = np.sqrt(Ms * GG / ri[0])  # Magnitude of Earth's initial velocity

vvj = 13.06e3 * TT / RR  # Magnitude of Jupiter's initial velocity

vi = [0, vv * 1.0]  # Initial velocity vector for Earth.Taken to be along y direction as ri is on x axis.
vji = [0, vvj * 1.0]  # Initial velocity vector for Jupiter

# Initializing the arrays with initial values.
t[0] = ti
r[0, :] = ri
v[0, :] = vi
rj[0, :] = rji
vj[0, :] = vji

for i in range(0, N - 1):
    [r[i + 1, :], v[i + 1, :]] = RK4Solver(t[i], r[i, :], v[i, :], h, 'earth', rj[i, :], vj[i, :])
    [rj[i + 1, :], vj[i + 1, :]] = RK4Solver(t[i], rj[i, :], vj[i, :], h, 'jupiter', r[i, :], v[i, :])


py.plot(0, 0, 'ro', linewidth=7)  # Sun
mplot(1, r[:, 0], r[:, 1], r'$x$ position (AU)', r'$y$ position (AU)', 'blue', 'Earth')  # Earth
mplot(1, rj[:, 0], rj[:, 1], r'$x$ position (AU)', r'$y$ position (AU)', 'orange', 'Jupiter')  # Jupiter
py.title('3 Body Orbit')
py.legend()
py.ylim([-2, 2])
py.xlim([-2, 2])
py.axis('equal')  #Comment this line out to see Earth's orbit closer
py.show()
