from math import pi, sqrt

f = 2450_000_000                # Frequency
mi = 1.256*(10**-6)  # Permeability of water
# Conductivity of water (saltwater=5,freshwater=0.05)
sigma = 5

print(1/sqrt(2*pi*f*mi*sigma))
print(1/(2*pi*sigma*25))
