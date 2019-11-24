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

c=2.9979e10 #cm/s
kB= 1.38064e-16 #[ergK-1]
h = 6.626068e-27

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
# 1 atm-cm = 1000 Dobson
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
    return blackbody_lambda(wl, 273.15)* 1e8 # Para pasar de cm a angstroms en el denominador

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
        #return 1
        return absortion_coeff/math.log10(math.e) * atm_cm
        #return absortion_coeff * atm_cm * math.log(10) # Otra forma de calcular tau que parece ser equivalente tras haber comparado experimentalmente
    
    elif base=='e':
        return absortion_coeff * atm_cm

def rayleigh(I,wl):
    return I*pow(wl,4)/(2.0*c*kB)

def wien(I,wl):
    #freq = c/wl
    return (h*c)/((math.log((2.0*h*c**2.0)/(I*wl**5.0)))*kB*wl)


# https://ozonewatch.gsfc.nasa.gov/facts/dobson_SH.html
# Segun este recurso, tenemos las siguientes medidas interantes a comparar
# El promedio global de concentración de ozono es de 300 Dobson
dobson_average = 300# [Dobson]
atm_cm_average =  dobson_average/1000.0

# El promedio en el hoyo de ozono es de 100 Dobson
dobson_hole = 100 # [Dobson]
atm_cm_hole = dobson_hole/1000.0

# Se verifico que, efectivamente, el agujero de ozono aborbe menos intensidad, no logrando reducir tan efectivamente toda la intensidad. Sin embargo, no son pruebas realistas

# Pero por alguna razon la intensidad vuelve a aumentar conforme aproximacion a la superficie

absortion_coeff = 6.25 # [1/cm=Hz] base 10 para longitud de onda de 210nm

wl_ang = float(2100) #wl_uv->[Angstroms] 
N = float(6.96e2) #quantity of points
I0 = 0.0 #[erg/cm2 sec cm ster]
#nu = 1e8 # freq [Hz]
#dx = 0.05   #[km]
#wl = c/nu #[Angstroms]
tot_distance_average = atm_cm_average/100000.0 #[km]
tot_distance_hole = atm_cm_hole/100000.0

def RTE(N, absortion_coeff, tot_distance, atm_cm, wl_ang, label, I0 = 0.0):
    #tot_distance = atm_cm/100000.0
    #tot_distance = 50
    dx = tot_distance/N #[km]
    layers = range(1,int(N+1))

    I = I0

    X = []
    Y = []

    for i in tqdm(layers):
        x = float(i)*dx
        X.append(x)
        #print(S(x, wl_ang))
        I = I*math.exp(-tau(absortion_coeff, atm_cm)) + S(x,wl_ang)*(1-math.exp(-tau(absortion_coeff, atm_cm)))
        #Y.append(rayleigh(I.value, wl_ang/1e8)) #Transformar de angstroms a cm
        Y.append(wien(I.value, wl_ang/1e8))
        print(wien(I.value, wl_ang/1e8))

        pass

    ax.plot(X, Y, label=label)



#print("%e"%rayleigh(I.value,wl_ang))

fig, ax = plt.subplots()
RTE(N, absortion_coeff, 50.0, atm_cm_average, wl_ang, 'average', I0)
RTE(N, absortion_coeff, 50.0, atm_cm_hole, wl_ang, 'hole', I0)
#ax.plot(X, Y_average, label='average')
#ax.plot(X, Y_hole, label='hole')
ax.legend()
ax.set_xscale("log")
ax.set_yscale("log")
plt.show()
