

import math
from astropy.modeling.blackbody import blackbody_lambda
from tqdm import tqdm
from scipy.interpolate import interp1d

c=3e10 #cm/s
kB= 1.38e-16 #[ergK-1]

# Temperature model [K]
def T(x):
    with open("T.dat", "r") as f:
        T_dat = f.readlines()

    z = []
    Tr = []
    for data in T_dat:
        if data[0] != '#':
            a, b = data.split()
            z.append(float(a))
            Tr.append(float(b))

    f = interp1d(z, Tr)
    return f(x)

# Density model [cm-3]
def n(x):
    with open("n.dat", "r") as f:
        n_dat = f.readlines()

    z = []
    nr = []
    for data in n_dat:
        if data[0] != '#':
            a, b = data.split()
            z.append(float(a))
            nr.append(float(b))

    f = interp1d(z, nr)
    return f(x)

# Source function [erg/cm2 sec cm ster]
def S(x,wl):
    return blackbody_lambda(wl, T(x))* 1e8

#opacity [cm-1]
def k(x,wl):
    nu = c/wl
    # Ref Dulk (1985) eq. 21
    return 1e5*0.2*pow(n(x),2)*pow(T(x),-3/2)*pow(nu,-2)

#optical depth (adimensional)
def tau(dx,x,wl):
    return (dx/2.0)*(k(x-dx,wl) + k(x,wl))

def rayleigh(I,wl):
    return I*pow(wl,4)/(2.0*c*kB)

N = 6.96e4 #quantity of points
I0 = 0.0 #[erg/cm2 sec cm ster]
nu = 1e8 #Hz
dx = 1e1   #[km]
wl = c/nu #Amstrongs

layers = range(1,int(N+1))

I = I0


for i in tqdm(layers):
    x = float(i)*dx
    I = I*math.exp(-tau(dx,x,wl)) + S(x,wl)*(1-math.exp(-tau(dx,x,wl)))
    pass
print("%e"%rayleigh(I.value,wl))