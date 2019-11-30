"""
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

# Source function [erg/cm2 sec cm ster]
def S(x,wl):
    return blackbody_lambda(wl, 273.15)* 1e8 # To change from cm to Angstroms at denominator

#Optical depth
# We used the Beer Lamber Law to obtain the optical depth from the absorption coefficient
# Beer Lamber Law: https://en.wikipedia.org/wiki/Beer%E2%80%93Lambert_law
# Optical Depth = (Columnar ozone, atm. cm) * absorption coefficient
# 1 atm-cm = 1000 Dobson
# If we want to calculate the optical depth, we'll have to divide the absorption coefficient by log10(e) to
# change the base, and then multiply by the atm-cm in the ozone column we're interested.


def tau(absortion_coeff, atm_cm, base='10'):
    if base=='10':
        return absortion_coeff/math.log10(math.e) * atm_cm
    
    elif base=='e':
        return absortion_coeff * atm_cm

def wien(I,wl):
    return (h*c)/((math.log((2.0*h*c**2.0)/(I*wl**5.0)))*kB*wl)


c=2.9979e10 # [cm/s]
kB= 1.38064e-16 # [ergK-1]
h = 6.626068e-27 # Planck's constant

# According to Osapublishing's article, for a 210nm wavelenght, Ozone has
# an absorption coefficient of 6.25/cm (base 10)
absortion_coeff = 6.25 # [1/cm = Hz] base 10 for a wavelenght of 210nm

# https://ozonewatch.gsfc.nasa.gov/facts/dobson_SH.html
# Global average of Ozone concentration according to Nasa
dobson_average = 300 # [Dobson]
atm_cm_average =  dobson_average/1000.0

# Ozone Layer's Hole average of Ozone according to Nasa
dobson_hole = 100 # [Dobson]
atm_cm_hole = dobson_hole/1000.0

# UV light has an average wavelenght of 210nm, which is 2100 Angstroms
wl_ang = float(2100) # wl_uv->[Angstroms] 
N = float(6.96e2) # quantity of points
I0 = 0.0 # [erg/cm2 sec cm ster]


def RTE(N, absortion_coeff, tot_distance, atm_cm, wl_ang, label, I0 = 0.0):
    dx = tot_distance/N # [km]
    layers = range(1,int(N+1))

    I = I0

    X = []
    Y = []

    for i in tqdm(layers):
        x = float(i)*dx
        X.append(x)
        I = I*math.exp(-tau(absortion_coeff, atm_cm)) + S(x,wl_ang)*(1-math.exp(-tau(absortion_coeff, atm_cm)))
        Y.append(wien(I.value, wl_ang/1e8))
        print(wien(I.value, wl_ang/1e8))

        pass

    ax.plot(X, Y, label=label)

fig, ax = plt.subplots()
RTE(N, absortion_coeff, 50.0, atm_cm_average, wl_ang, 'Global average', I0)
RTE(N, absortion_coeff, 50.0, atm_cm_hole, wl_ang, 'Hole', I0)
ax.legend()
ax.set_xlabel('Distance [km]')
ax.set_ylabel('Temperature [K]')
ax.set_xscale("log")
ax.set_yscale("log")
plt.show()
