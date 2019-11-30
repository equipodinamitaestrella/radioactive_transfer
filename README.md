# Ozone's Radiative Transfer

## Summary

Ozone (O<sub>3</sub>) is a highly reactive gas whose molecules are comprised of three oxygen atoms. Its concentration in the atmosphere naturally fluctuates depending on seasons and latitudes, but it generally was stable when global measurements began in 1957. Groundbreaking research in the 1970s and 1980s revealed signs of trouble.<br>

This project uses the radiative transfer equation to measure the thermal emission of a healthy section of the Ozone Layer and the Ozone Layer Hole so we can compare them and reach some conclusions. In the following sections you will find out a brief and concise explanation of what the Radiation Transfer is and some other concepts you need to know to understand the problem and the way to solve it.

## Introduction

Ozone absorbs ultraviolet (UV) radiation from the sun (particularly harmful UVB-type rays,) in a layer of the atmosphere called the stratosphere, the ozone layer is a sunscreen, shielding the planet from potentially harmful ultraviolet radiation. Exposure to UVB radiation is linked with increased risk of skin cancer and cataracts, as well as damage to plants and marine ecosystems. Atmospheric ozone is sometimes labeled as the "good" ozone, because of its protective role, and shouldn't be confused with tropospheric, or ground-level, "bad" ozone, a key component of air pollution that is linked with respiratory disease.<br>

### Ozone Layer's Depletion

In 1974, Mario Molina and Sherwood Rowland, two chemists at the University of California, Irvine, published an article in <a href="https://www.nature.com/articles/249810a0.pdf">Nature</a> detailing threats to the ozone layer from chlorofluorocarbon (CFC) gases. As they reach the stratosphere, the sun's UV rays break CFCs down into substances that include chlorine.

The groundbreaking research—for which they were awarded the 1995 Nobel Prize in chemistry—concluded that the atmosphere had a “finite capacity for absorbing chlorine” atoms in the stratosphere.

One atom of chlorine can destroy more than 100,000 ozone molecules, according to the U.S. Environmental Protection Agency, eradicating ozone much more quickly than it can be replaced.

Molina and Rowland’s work received striking validation in 1985, when a team of English scientists found a hole in the ozone layer over Antarctica that was later linked to CFCs. The "hole" is actually an area of the stratosphere with extremely low concentrations of ozone that reoccurs every year at the beginning of the Southern Hemisphere spring (August to October). Spring brings sunlight, which releases chlorine into the stratospheric clouds. <br>

### The Dobson Unit

The Dobson Unit is the most common unit for measuring ozone concentration. One Dobson Unit is the number of molecules of ozone that would be required to create a layer of pure ozone 0.01 millimeters thick at a temperature of 0 degrees Celsius and a pressure of 1 atmosphere (the air pressure at the surface of the Earth). Expressed another way, a column of air with an ozone concentration of 1 Dobson Unit would contain about 2.69x1016ozone molecules for every square centimeter of area at the base of the column. Over the Earth’s surface, the ozone layer’s average thickness is about 300 Dobson Units or a layer that is 3 millimeters thick.<br>

Ozone in the atmosphere isn’t all packed into a single layer at a certain altitude above the Earth’s surface; it’s dispersed. Even the stratospheric ozone known as “the ozone layer” is not a single layer of pure ozone. It is simply a region where ozone is more common than it is at other altitudes. Satellite sensors and other ozone-measuring devices measure the total ozone concentration for an entire column of the atmosphere. The Dobson Unit is a way to describe how much ozone there would be in the column if it were all squeezed into a single layer.<br>

The average amount of ozone in the atmosphere is roughly 300 Dobson Units, equivalent to a layer 3 millimeters (0.12 inches) thick What scientists call the Antarctic Ozone “Hole” is an area where the ozone concentration drops to an average of about 100 Dobson Units. One hundred Dobson Units of ozone would form a layer only 1 millimeter thick if it were compressed into a single layer.

### Radiative Transfer and the Radiative Transfer Equation (RTE)

Radiative transfer is the physical phenomenon of energy transfer in the form of electromagnetic radiation. The propagation of radiation through a medium is affected by absorption, emission, and scattering processes. The equation of radiative transfer describes these interactions mathematically. Equations of radiative transfer have application in a wide variety of subjects including optics, astrophysics, atmospheric science, and remote sensing. <br>

The equation of radiative transfer simply says that as a beam of radiation travels, it loses energy to absorption, gains energy by emission, and redistributes energy by scattering. The differential form of the equation for radiative transfer is:

<img src="https://latex.codecogs.com/gif.latex?\inline&space;\large&space;{\frac&space;{1}{c}}{\frac&space;{\partial&space;}{\partial&space;t}}I_{\nu&space;}&plus;{\hat&space;{\Omega&space;}}\cdot&space;\nabla&space;I_{\nu&space;}&plus;(k_{\nu&space;,s}&plus;k_{\nu&space;,a})I_{\nu&space;}=j_{\nu&space;}&plus;{\frac&space;{1}{4\pi&space;}}k_{\nu&space;,s}\int&space;_{\Omega&space;}I_{\nu&space;}d\Omega" title="\large {\frac {1}{c}}{\frac {\partial }{\partial t}}I_{\nu }+{\hat {\Omega }}\cdot \nabla I_{\nu }+(k_{\nu ,s}+k_{\nu ,a})I_{\nu }=j_{\nu }+{\frac {1}{4\pi }}k_{\nu ,s}\int _{\Omega }I_{\nu }d\Omega" /> <br>
where **_c_** is the speed of light, **_j<sub>v</sub>_** is the emission coefficient, **_k<sub>v,s</sub>_** is the scattering opacity, **_k<sub>v,a</sub>_** is the absorption opacity, and the <img src="https://latex.codecogs.com/png.latex?\inline&space;\small&space;{\displaystyle&space;{\frac&space;{1}{4\pi&space;}}k_{\nu&space;,s}\int&space;_{\Omega&space;}I_{\nu&space;}d\Omega&space;}" title="\small {\displaystyle {\frac {1}{4\pi }}k_{\nu ,s}\int _{\Omega }I_{\nu }d\Omega }" /> term represents radiation scattered from other directions onto a surface.

### Discrete Iterative Solution to RTE

<img src="https://latex.codecogs.com/png.latex?\inline&space;\small&space;I_{i}&space;=&space;I_{i-1}\exp^{-\tau_{i}}&space;&plus;&space;S_{i}(1-e^{-\tau_{i}})" title="\small I_{i} = I_{i-1}\exp^{-\tau_{i}} + S_{i}(1-e^{-\tau_{i}})" /> <br>

where <img src="https://latex.codecogs.com/gif.latex?\small&space;\tau_{i}&space;=&space;\frac{\Delta&space;x}{2}&space;(k_{i}&space;&plus;&space;k_{i-1})" title="\small \tau_{i} = \frac{\Delta x}{2} (k_{i} + k_{i-1})" />, **_k<sub>i</sub>_** is the opacity and **_S<sub>i</sub>_** is the Source function.<br>

### Black-Body Radiation and Planck's Law

A black-body is an idealised object which absorbs and emits all radiation frequencies. Near thermodynamic equilibrium, the emitted radiation is closely described by Planck's law and because of its dependence on temperature, Planck radiation is said to be thermal radiation, such that the higher the temperature of a body the more radiation it emits at every wavelength.<br>

Planck's law describes the spectral density of electromagnetic radiation emitted by a black body in thermal equilibrium at a given temperature T, when there is no net flow of matter or energy between the body and its environment. The spectral radiance per unit wavelength λ  is given by:<br>

<img src="https://latex.codecogs.com/gif.latex?{\displaystyle&space;I_{\lambda&space;}(\lambda&space;,T)={\frac&space;{2hc^{2}}{\lambda&space;^{5}}}{\frac&space;{1}{e^{\frac&space;{hc}{\lambda&space;k_{\mathrm&space;{B}&space;}T}}-1}},}" title="{\displaystyle B_{\lambda }(\lambda ,T)={\frac {2hc^{2}}{\lambda ^{5}}}{\frac {1}{e^{\frac {hc}{\lambda k_{\mathrm {B} }T}}-1}},}" /> <br>

where _k<sub>B</sub>_ is the Boltzmann constant, _h_ is the Planck constant, _T_ is the absolute temperature and _c_ is the speed of light in the medium, whether material or vacuum.<br>

In the limit of low frequencies (i.e. long wavelengths), Planck's law tends to the Rayleigh–Jeans law, while in the limit of high frequencies (i.e. small wavelengths such as UV radiation) it tends to the Wien approximation.

## Objectives

1) Understand the _Radiative Transfer Equation_.
2) Use the _RTE_ and the _Wien approximation_ to describe Ozone's spectrum of thermal radiation.
3) Compare the Ozone Layer Hole's emission vs emission of a healthy section of the Ozone Layer.

## Methodology

For the reproducibility of our results, please consider the following: <br>
* Our code is based on the code we developed in _Modeling and simulation_ class at ENES UNIDAD MORELIA, UNAM. Its main file is included in this repository as _main.py_. 
* The main file of _Ozone's Radiative Transfer_ is named _ozone.py_ .
* Since it was difficult to find measurements that would fit the _main.py_ code, we had to do several changes to it such as: 
&nbsp;&nbsp;&nbsp; * Units, we introduce the use of the _Dobson unit_ and _atm-cm_. <br>
&nbsp;&nbsp;&nbsp; * The way to calculate the optical depth. <br>
&nbsp;&nbsp;&nbsp; * We made the temperature constant in the source function. <br>
&nbsp;&nbsp;&nbsp; * Got rid of some functions implemente before. <br>

### Initial Conditions 

c = 2.9979e10 [cm/s] <br>
kB = 1.38064e-16 [ergK-1] <br>
h = 6.626068e-27 Planck's constant <br>

absortion_coeff = 6.25 [1/cm] <br>

dobson_average = 300 [Dobson] <br>
dobson_hole = 100 [Dobson] <br>

wl_ang = float(2100) [Angstroms] <br>
N = float(6.96e2) quantity of points <br>
I0 = 0.0 [erg/cm2 sec cm ster] <br>
tot_distance = 50 [km]<br>
T = 273.15 [K] <br>

### Execution

After you have downloaded or cloned this repository, run this project by executing the following on your command line:

bash testing.sh

## Results

With the aforementioned initial conditions, we got the following graph: <br>

![pictures/Results.png](pictures/Results.png)<br>

## Conclusions

1) We can observe that the Ozone Layer in the Hole area has a lower emission, with low temperatures even close to the Earth's surface, while the healthy area of the Ozone Layer seems to keep a stable rate of temperatures.
2) Even though they start at different rates, around 3x10⁻¹ km above the surface both curves converge in the absolute zero, 273.15 K. And then it continues to infinity. We think that we could have reached this phenomenon called **the ultraviolet catastrophe or Rayleigh–Jeans catastrophe**. This typically occurs by calculating the total amount of radiant energy (i.e., the sum of emissions in all frequency ranges), it can be shown that a blackbody in this case would release an infinite amount of energy, which is in contradiction with the law of conservation of energy.

## Bibliography
[1] Ozonewatch.gsfc.nasa.gov. (2019). NASA Ozone Watch: Latest status of ozone. [online] Available at: https://ozonewatch.gsfc.nasa.gov/ [Accessed 15 Nov. 2019]. <br>

[2] Batakliev, T., Georgiev, V., Anachkov, M., Rakovsky, S., & Zaikov, G. E. (2014). Ozone decomposition. Interdisciplinary toxicology, 7(2), 47–59. doi:10.2478/intox-2014-0008 <br>

[3] T. Yu. Chesnokova, Yu. V. Voronina, A. V. Chentsov, K. M. Firsov, and A. A. Razmolov "Simulation of atmospheric radiative transfer using different ozone absorption cross-sections in the UV spectral region", Proc. SPIE 10466, 23rd International Symposium on Atmospheric and Ocean Optics: Atmospheric Physics, 104660C (30 November 2017); https://doi.org/10.1117/12.2288091 <br>

[4] Brion, J., Chakir, A., Charbonnier, J. et al. Journal of Atmospheric Chemistry (1998) 30: 291. https://doi.org/10.1023/A:1006036924364<br>

[5] CHAPTER 10. STRATOSPHERIC OZONE. (n.d.). Retrieved November 15, 2019, from http://acmg.seas.harvard.edu/people/faculty/djj/book/bookchap10.html. <br>

[6] Absorption cross-sections of ozone in the ultraviolet and visible spectral regions: Status report 2015, Journal of Molecular  Spectroscopy, Volume 327, 2016, Pages 105-121, ISSN 0022-2852, https://doi.org/10.1016/j.jms.2016.07.007. <br>

[7] Blumberg, S. (2019, October 21). 2019 Ozone Hole is the Smallest on Record Since Its Discovery. Retrieved November 15, 2019, from https://www.nasa.gov/feature/goddard/2019/2019-ozone-hole-is-the-smallest-on-record-since-its-discovery. <br>

[8] Thiessen, M. (2019, April 18). The facts about ozone depletion. Retrieved November 15, 2019, from https://www.nationalgeographic.com/environment/global-warming/ozone-depletion/#close. <br>

[9] Planck's law. (2019, November 19). Retrieved November 22, 2019, from https://en.wikipedia.org/wiki/Planck's_law. <br>
https://en.wikipedia.org/wiki/Wien_approximation <br>

[10] Radiative transfer. (2019, November 19). Retrieved November 22, 2019, from https://en.wikipedia.org/wiki/Radiative_transfer. <br>

[11] Table of Wavelength Versus Ozone Absorption Coefficients . (n.d.). Retrieved November 15, 2019, from https://gist.github.com/jgomezdans/5443793. <br>

[12] Aerosol Optical Depth Value-Added Product. (2013). doi: DOE/SC-ARM/TR-129. URL: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-129.pdf <br>

[13] Inn, E. C. Y., & Tanaka, Y. (1953, October 1). Absorption Coefficient of Ozone in the Ultraviolet and Visible Regions. Retrieved November 28, 2019, from https://www.osapublishing.org/josa/abstract.cfm?uri=josa-43-10-870. <br>

[14] Ultraviolet Catastrophe - Rayleigh-Jeans Catastrophe. (n.d.). Retrieved November 28, 2019, from https://www.nuclear-power.net/nuclear-engineering/heat-transfer/radiation-heat-transfer/ultraviolet-catastrophe-rayleigh-jeans-catastrophe/. <br>

[15] Chapter 2: The blackbody spectrum and the “ultraviolet catastrophe”. Luis M. Molina .Departamento de Física Teórica, Atómica y Óptica. Quantum Physics. Retrieved November 28, 2019, from: http://metodos.fam.cie.uva.es/latex/fisica-cuantica/Clase-002.pdf
