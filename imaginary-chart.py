import math
import numpy as np
import matplotlib.pyplot as plt


z = np.exp(np.pi * 1j)
z1 = np.exp(np.pi * 1j) + 0.5
z2 = -1 * np.exp(np.pi * 1j)
z3 = (1j) * np.exp(np.pi * 1j)
z4 = (-1j) * np.exp(np.pi * 1j)
z5 = np.exp(np.pi * 1j)

fig, ax = plt.subplots(figsize=(5,5))
ax.scatter(z.real, z.imag, color='red')
ax.scatter(z1.real, z1.imag, color='green')
ax.scatter(z2.real, z2.imag, color='blue')
ax.scatter(z3.real, z3.imag, color='purple')
ax.scatter(z4.real, z4.imag, color='pink')
ax.scatter(z5.real, z5.imag, color='black')

theta = np.linspace(0, 2*np.pi, 300)
gamma = np.linspace(1,2*np.pi, 100)
yota = np.linspace(0,(0.5*(2*np.pi)), 200)

ax.plot(np.cos(theta), np.sin(theta),linestyle="dashed", color="gray",alpha=0.6)
ax.plot(np.cos(gamma), np.sin(gamma), linestyle="solid", color="cyan", alpha=0.3)
ax.plot(np.cos(yota), np.sin(yota), linestyle="solid", color="green", alpha=0.8)   
ax.axhline(0, color='black', linewidth=0.5)
ax.axvline(0, color='black', linewidth=0.5)
ax.set_xlabel('Real')
ax.set_ylabel('Im')
ax.set_title("Plot of ${e^pii}$")
#ax.legend()

ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)

plt.grid()
plt.show()


