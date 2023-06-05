import numpy as np
import matplotlib.pyplot as plt

# Generate angles for the points on the circle
angles = [0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi]

# Create the figure and axis
fig, ax = plt.subplots()

# Draw the circle
circle = plt.Circle((0, 0), radius=1, fill=False)

# Add the circle to the plot
ax.add_patch(circle)

# Plot the points on the circle
for angle in angles:
    x = np.cos(angle)
    y = np.sin(angle)
    plt.plot(x, y, 'ro')

# Set the aspect ratio to equal
ax.set_aspect('equal')

# Set the plot limits
plt.xlim(-1.5, 1.5)
plt.ylim(-1.5, 1.5)

# Add labels to the points
labels = ['0', 'π/4', 'π/2', '3π/4', 'π']
for i, txt in enumerate(labels):
    plt.annotate(txt, (np.cos(angles[i]), np.sin(angles[i])))

# Show the plot
plt.show()
