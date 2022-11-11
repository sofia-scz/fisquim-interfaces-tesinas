# Setear la masa del termostato NOSE HOOVER

Ref: Hünenberger, P. H. (2005). Thermostat Algorithms for Molecular Dynamics Simulations. Advances in Polymer Science, 105–149. doi:10.1007/b99427 

De acuerdo a la referencia el valor ideal de la masa de Nose-Hoover Q (SMASS en VASP) se estima segun

$$ Q \approx \frac{7}{5} N_{f} k_B T_0 \omega^2 $$

$N_f$: grados de libertad

$T_0$: temperatura del baño térmico

$\omega$: frecuencia de vibración de los fonones (orden de magnitud)

Detalles

$$ N_f = 3N - N_C - N_r $$

$3N$ corresponde a los grados de libertad totales del sistema. Si tenemos $N$ átomos libres y $3$ dimensiones tenemos $3N$. $N_G$ corresponde a los
grados de libertad que perdemos por las constraints, en principio sólo nos interesa el hecho de que algunos átomos quedan fijos en nuestras
simulaciones y por lo tanto se restarían sus grados de libertad. (no se entiende de donde sale esto) $N_r$ se toma como $3$ si el sistema tiene
condiciones de frontera periódicas como en nuestro caso. 

Ajustado a las constantes de VASP y demás queda aprox

$$ Q \approx 3.82 \times 10^{-8} T_0 \omega^2 $$

con $T_0$ en kelvin y $\omega$ en fs.
