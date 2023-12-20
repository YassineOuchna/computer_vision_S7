import matplotlib.pyplot as plt
import numpy as np



# Set up the polar plot
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.set_rlabel_position(90)
ax.set_theta_direction(-1)
ax.set_theta_offset(np.pi / 2.0)

# Create an empty line to update during real-time plotting
line, = ax.plot([], [], marker='o', linestyle='-', color='b')

# Initialize empty lists to store data
angles = []
distances = []

# Function to update the plot in real-time
def update_plot(frame):
    with open('data1.txt','r') as f:
        distances.append(f.readlines()[-2][1:].strip('} ]\n').split(','))
    angles.append(np.array([i for i in range(360)]))
    
    line.set_data(angles, distances)
    
    return line,

# Set up the animation
from matplotlib.animation import FuncAnimation

animation = FuncAnimation(fig, update_plot, frames=np.arange(0, 360, 1), interval=50, blit=True)

plt.show()