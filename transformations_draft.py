'''
Use the code format below to experiment with the data and 
to refine the data as per your requirements

below calculations wouldnt make sense since it was done for that specific instance,
so just take it as a refernece for your work.

the below code take the trackerdata from xlfile1 and works with it.
later at the end the new calculated data is saved in a new xlfile2

'''


import numpy as np
import pandas as pd

# Load Excel file and extract coordinates and sensor values as NumPy arrays
df = pd.read_excel('trackerdata.xlsx')
coordinates = df.values[:, :2]  # Assuming the coordinates are in the first two columns
sensor_values = df.values[:, 2]  # Assuming the sensor values are in the third column

# Convert angle to radians
theta = np.deg2rad(14)

# Create 2D rotation matrix
R = np.array([[np.cos(theta), -np.sin(theta)],
              [np.sin(theta), np.cos(theta)]])

# Rotate coordinates
rotated_coordinates = R @ coordinates.T  # Transpose coordinates to match matrix dimensions

# Create a new DataFrame with the rotated coordinates
df_rotated = pd.DataFrame(rotated_coordinates.T, columns=['x_rotated', 'y_rotated'])

# Convert sensor values from -180 to 180 range to 0 to 360 range
sensor_values_0_to_360 = (sensor_values + 360) % 360

# Add sensor values to DataFrame
df_rotated['sensor_values'] = sensor_values_0_to_360

# Apply 2D rotation of 180 degrees about the x-axis
R_x = np.array([[1, 0],
                [0, -1]])

final_coordinates = R_x @ df_rotated.values[:, :2].T  # Transpose coordinates to match matrix dimensions

# Update the DataFrame with the final coordinates
df_rotated['x_rotated'] = final_coordinates[0]
df_rotated['y_rotated'] = final_coordinates[1]

# Increase x_rotated by adding 0.5
df_rotated['x_rotated'] += 0.5
# Increase y_rotated by subtracting 1.0
df_rotated['y_rotated'] -= 1.0

# Save the DataFrame to a new Excel file with only the rotated coordinates and sensor values
df_rotated[['x_rotated', 'y_rotated', 'sensor_values']].to_excel('transformeddata_draft.xlsx', index=False)
