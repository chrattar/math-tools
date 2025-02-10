# Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt

# Define complex numbers based on Euler's formula
z = np.exp(np.pi * 1j)  # e^(πi) = -1
z1 = np.exp(np.pi * 1j) + 0.5  # Shifted version
z2 = -1 * np.exp(np.pi * 1j)  # Still -1
z3 = (1j) * np.exp(np.pi * 1j)  # Rotated by 90 degrees
z4 = (-1j) * np.exp(np.pi * 1j)  # Rotated by -90 degrees

# Create a figure and axis for plotting
fig, ax = plt.subplots(figsize=(6,6))

# Scatter plot for the complex numbers
ax.scatter(z.real, z.imag, color='red', label=r'$e^{\pi i}$')
ax.scatter(z1.real, z1.imag, color='green', label=r'$e^{\pi i} + 0.5$')
ax.scatter(z2.real, z2.imag, color='blue', label=r'$-e^{\pi i}$')
ax.scatter(z3.real, z3.imag, color='purple', label=r'$i e^{\pi i}$')
ax.scatter(z4.real, z4.imag, color='pink', label=r'$-i e^{\pi i}$')

# Draw the unit circle
theta = np.linspace(0, 2 * np.pi, 300)
ax.plot(np.cos(theta), np.sin(theta), linestyle="dashed", color="gray", alpha=0.6, label="Unit Circle")

# Plot a sine wave along the real axis
x_sin = np.linspace(-1.5, 1.5, 300)
y_sin = 0.5 * np.sin(2 * np.pi * x_sin)  # Scaled sine wave
ax.plot(x_sin, y_sin, linestyle="solid", color="black", alpha=0.8, label="Sine Wave")

# Axes and Labels
ax.axhline(0, color='black', linewidth=0.5)
ax.axvline(0, color='black', linewidth=0.5)
ax.set_xlabel('Real')
ax.set_ylabel('Imaginary')
ax.set_title("Plot of $e^{\pi i}$ and Sine Wave")

# Adjust Limits
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)

# Grid and Legend
plt.grid()
plt.legend()
plt.show()
