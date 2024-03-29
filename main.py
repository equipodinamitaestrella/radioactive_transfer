"""
main.py solve the n-body problem using newton
Copyright (C) 2019 Jorge Antonio Camarena Pliego (camarenapliego@gmail.com)
Keshava Tonathiu Sanchez Barbosa (keshava.t.s.b@gmail.com)
Stephany Dzoara Vargas Mier (stephanydvm@comunidad.unam.mx)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>."""


import math
from astropy.modeling.blackbody import blackbody_lambda
from tqdm import tqdm
from scipy.interpolate import interp1d
import matplotlib
import matplotlib.pyplot as plt

c=3e10 #cm/s
kB= 1.38e-16 #[ergK-1]

# num_particulas * coeficiente de absorcion para obtener opacidad
# num_particulas = densidad / volumen
# densidad = num_particulas / volumen -> buscar densidad en estas unidades de n/cm^3, no g/cm^3
# En n.dat, por ejemplo, tenemos la densidad en particulas por cm^3 que hay en la corona de Sol

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
    return blackbody_lambda(wl * 1e8, T(x))* 1e8

#opacity [cm-1]
def k(x,wl):
    nu = c/wl
    # Ref Dulk (1985) eq. 21
    # http://planeterrella.osug.fr/IMG/pdf/stellar_emissions.pdf
    return 1e5*0.2*pow(n(x),2)*pow(T(x),-3/2)*pow(nu,-2)

#optical depth (adimensional)
def tau(dx,x,wl):
    return (dx/2.0)*(k(x-dx,wl) + k(x,wl))

def rayleigh(I,wl):
    return I*pow(wl,4)/(2.0*c*kB)

N = 6.96e2 #quantity of points
I0 = 0.0 #[erg/cm2 sec cm ster]
nu = 1e8 #Hz
dx = 1e3   #[km]
wl = c/nu #Amstrongs

layers = range(1,int(N+1))

I = I0

X = []
Y = []

for i in tqdm(layers):
    x = float(i)*dx
    I = I*math.exp(-tau(dx,x,wl)) + S(x,wl)*(1-math.exp(-tau(dx,x,wl)))
    X.append(x)
    Y.append(rayleigh(I.value, wl))
    pass

print("%e"%rayleigh(I.value,wl))

fig, ax = plt.subplots()
ax.plot(X, Y)
ax.set_xscale("log")
ax.set_yscale("log")
plt.show()
