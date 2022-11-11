# Setear la masa del termostato NOSE HOOVER

Ref: Hünenberger, P. H. (2005). Thermostat Algorithms for Molecular Dynamics Simulations. Advances in Polymer Science, 105–149. doi:10.1007/b99427 

De acuerdo a la referencia el valor ideal de la masa de Nose-Hoover Q (SMASS en VASP) se estima segun

$$ Q \approx \frac{7}{5} N_{f} k_B T_0 \tau_T^2 $$

$N_f$: grados de libertad

$T_0$: temperatura del baño térmico

$\tau_T$: tiempo de relajación de la temperatura


Detalles

$$ N_f = 3N - N_C - N_r $$

$3N$ corresponde a los grados de libertad totales del sistema. Si tenemos $N$ átomos libres y $3$ dimensiones tenemos $3N$. $N_G$ corresponde a los
grados de libertad que perdemos por las constraints, en principio sólo nos interesa el hecho de que algunos átomos quedan fijos en nuestras
simulaciones y por lo tanto se restarían sus grados de libertad. (no se entiende de donde sale esto) $N_r$ se toma como $3$ si el sistema tiene
condiciones de frontera periódicas como en nuestro caso. 

Por otro lado, $\tau_T$ sale de

$$ \frac{d}{dt}\mathcal{T}(t) = \frac{1}{\tau_T}\left[T_0 - \mathcal{T}(t)\right] $$

en la práctica se asume que $\tau_T \approx 100 fs$.
