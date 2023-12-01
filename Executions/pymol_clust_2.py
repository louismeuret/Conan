import pandas as pd
import pymol
import matplotlib.pyplot as plt
import matplotlib
# Read the pickled DataFrame
unpickled_df = pd.read_pickle("../parametres/temp_files/list_results.pkl")

# Create a new DataFrame with selected columns
new_df = pd.DataFrame(unpickled_df, columns=['lig', 'Energy', 'logp', 'molwt', 'complexity', 'coord'])

# Launch PyMOL
pymol.finish_launching()

# Get the energy values
energies = new_df['Energy'].tolist()

# Normalize the energy values for color mapping
norm = matplotlib.colors.Normalize(vmin=min(energies), vmax=max(energies))

# Create a reversed colormap based on the normalized energy values
colors = plt.cm.seismic(norm(energies))[::-1]

# Loop through the DataFrame and visualize atoms in PyMOL
for index, row in new_df.iterrows():
    name = row['lig'].replace(":", "")
    x, y, z = row['coord']
    energy = row['Energy']
    
    # Get the color based on the reversed colormap
    color = colors[index]

    # Check the condition and modify the color accordingly
    if int(row['lig'].split('_')[1].replace("ligand", "")) > 500:
        color = [0.0, 0.0, 1.0]  # Blue
    else:
        color = [1.0, 0.0, 0.0]  # Red

    r, g, b = color
    print(r, g, b)
    
    # Create a pseudoatom with a specific name and position
    pymol.cmd.pseudoatom(name, pos=[x, y, z])

    # Set the color for the pseudoatom
    pymol.cmd.set_color('point_color', [r, g, b])

    # Color the pseudoatom
    pymol.cmd.color('point_color', name)

    # Show the spheres for the pseudoatom
    pymol.cmd.show('spheres', name)

