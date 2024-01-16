import re
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Function to parse lidar data from the text file
def parse_lidar_data(file_path):
    with open(file_path, 'r') as file:
        data = file.readlines()

    lidar_data = []
    for line in data:
        # Use regular expression to find all float numbers in the line
        values = [float(match.group()) for match in re.finditer(r'\d+\.\d+', line)]
        lidar_data.append(values)

    return lidar_data[-1]

# Function to update the polar plot in real time
def update(frame):
    ax.clear()
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    lidar_data = parse_lidar_data(file_path)
    distances_and_angles = []
    for x in lidar_data:
        if x==0.0:
            distances_and_angles.append(12000)
        else:
            distances_and_angles.append(x)
    # Extract distances and angles from lidar_data
    distances = distances_and_angles[:len(distances_and_angles) // 2]
    angles = np.linspace(0, 2 * np.pi, len(distances), endpoint=False)

    # Plot the polar plot with lines
    ax.plot(angles, distances, label='Lidar Data', linestyle='-', marker='', color='b')
    ax.set_rmax(11000)  # Adjust rmax based on the maximum distance in the current frame
    ax.legend()

# Path to the text file containing lidar data
file_path = "data1.txt"

# Parse lidar data


# Create a figure and axis for the polar plot
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

# Create an animation
ani = animation.FuncAnimation(fig, update, frames=1, interval=100, repeat=True)

# Show the polar plot
plt.show()