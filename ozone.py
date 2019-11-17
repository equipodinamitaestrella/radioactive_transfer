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


# La luz ultravioleta tiene en promedio una longitud de onda de 200nm, lo cual se traduce a 2000 angstroms
# Pero mas generalmente, hablamos de un rango de 100 a 4000 angstroms
# Afortunadamente, el rango de 2000 a 3000 angstroms esta presente en el grafico encontrado del coeficiente de absorcion para el ozono
# Para este analisis, se considerara una longitud de onda de 210nm o 2100 angstroms, lo cual esta dentro del rango de los rayos ultravioleta peligrosos por su baja longitud de onda

# Investigar utilidad:
# https://gist.github.com/jgomezdans/5443793
# https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-129.pdf
# Aunque las longitudes de onda presentes aqui son mayores a las de la luz ultravioleta

# Investigar como obtener numero de particulas para estimacion de la opacidad
# Si se trabajara una sola "columna" de aire que definira nuestro numero de particulas (investigar medida atm-cm y unidad Dobson)
# O si se trabajaran varias capas o segmentos divididos de cierto volumen para de ellos definir el numero de particulas en cada uno (tendria que trabajarse lo de interpolacion n(x)?)

# Se tiene que sustituir la funcion de profundidad optica por una constante de opacidad determinada por atm-cm * coeficiente_de_absorcion (en 1/cm)
# 1 Dobson = 1000 atm-cm
# atm-cm se refiere al grosor en cm que tendria toda una columna de ozono si se trajera a la superficie

# Tras indagacion, se descubrio que los datos experimentales para el coeficiente de absorcion del ozono en https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-129.pdf y en https://www.osapublishing.org/josa/abstract.cfm?uri=josa-43-10-870 son bastante parecidos. Ambos usaron la ley de Beer Lambert para el calculo del coeficiente de aborcion, solo que en el primero se uso una base e natural en la ecuacion por usar la profundidad optica y en el segundo se uso una base 10 por usar la aborbancia.

# Beer Lamber Law: https://en.wikipedia.org/wiki/Beer%E2%80%93Lambert_law

# Con este conocimiento, sabemos entonces como llegar directamente a la profundidad optica con estos coeficientes, dado que la opacidad (en cm^2/gr) no se puede inferir facilmente del coeficiente de absorcion en (1/cm), teniendo que considerar cierta medida de densidad o numero de particulas

# Las medidas de atm-cm y Dobson fueron ideadas por la comunidad de la ciencia atmosferica para no tener que involucrar directamente la presion atmosferica, volumen y densidad del gas: https://www.harrisgeospatial.com/Support/Self-Help-Tools/Help-Articles/Help-Articles-Detail/ArtMID/10220/ArticleID/19211/3502

# Temperature model [K]
def T(x):
    with open("T_stratosphere.dat", "r") as f:
        T_dat = f.readlines()

    z = []
    Tr = []
    for data in T_dat:
        if data[0] != '#':
            a, b = data.split()
            z.append(float(a))
            Tr.append(float(b))
    #print(z, Tr)
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
    return blackbody_lambda(wl, T(x))* 1e8 # Para pasar de cm a angstroms en el denominador

#opacity [cm-1]
def k(x,wl):
    nu = c/wl
    # Ref Dulk (1985) eq. 21
    # http://planeterrella.osug.fr/IMG/pdf/stellar_emissions.pdf
    return 1e5*0.2*pow(n(x),2)*pow(T(x),-3/2)*pow(nu,-2)

#optical depth (adimensional)
# Segun el articulo de osapublishing, para una longitud de onda de 210 nanometros, el ozono tiene un coeficiente de absorcion de 6.25/cm (en base 10) aproximadamente
# Si queremos calcular la profundidad optica, tendremos que dividir por log10(e) para el cambio de base y despues multiplicar por la cantidad de atm-cm presentes en una columna de atmosfera de interes
def tau(absortion_coeff, atm_cm, base='10'):
    if base=='10':
        return absortion_coeff/math.log10(math.e) * atm_cm
    
    elif base=='e':
        return absortion_coeff * atm_cm

def rayleigh(I,wl):
    return I*pow(wl,4)/(2.0*c*kB)


# https://ozonewatch.gsfc.nasa.gov/facts/dobson_SH.html
# Segun este recurso, tenemos las siguientes medidas interantes a comparar
dobson_average = 300 # El promedio global de ozono
atm_cm_average =  dobson_average/1000.0

dobson_hole = 100 # El promedio en el hoyo de ozono
atm_cm_hole = dobson_hole/1000.0

absortion_coeff = 6.25 # /cm base 10 para longitud de onda de 210nm

wl_ang = 2100
N = 6.96e2 #quantity of points
I0 = 0 #[erg/cm2 sec cm ster]
#nu = 1e8 # Hz
dx = 0.05   #[km]
#wl = c/nu #Amstrongs

layers = range(1,int(N+1))

I_average = I0
I_hole = I0

X = []
Y_average = []

Y_hole = []

for i in tqdm(layers):
    x = float(i)*dx
    X.append(x)
    
    I_average = I_average*math.exp(-tau(absortion_coeff, atm_cm_average)) + S(x,wl_ang)*(1-math.exp(-tau(absortion_coeff, atm_cm_average)))
    Y_average.append(rayleigh(I_average.value, wl_ang/1e8)) #Transformar de angstroms a cm
    
    I_hole = I_hole*math.exp(-tau(absortion_coeff, atm_cm_hole)) + S(x,wl_ang)*(1-math.exp(-tau(absortion_coeff, atm_cm_hole)))
    Y_hole.append(rayleigh(I_hole.value, wl_ang/1e8))
    
    pass

#print("%e"%rayleigh(I.value,wl_ang))

fig, ax = plt.subplots()
ax.plot(X, Y_average, label='average')
ax.plot(X, Y_hole, label='hole')
ax.legend()
ax.set_xscale("log")
ax.set_yscale("log")
plt.show()
