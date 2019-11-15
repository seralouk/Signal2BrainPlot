# Import libraries
import numpy as np, os, sys
from nilearn import plotting, datasets; from nilearn.surface import load_surf_data
sys.path.append('/Users/loukas/Desktop/Signal2Glasser/Utilities/')
from SeraPlot import plot_signal2glasser


# Path to the folder that contains the fslaverage & glasser subfolders
# Note: do not change anything to ensure full functionality
path_to_surfaces = '/Users/loukas/Desktop/Signal2Glasser/'

# Where to save the plot. The plot will be saved only in the 2D plotting case.
save_png_to = '/Users/loukas/Desktop/'

# The signal (should be a vector with 180 elements)
# signal = np.random.randn(180,1)
signal = np.arange(1,181).reshape(-1,1)

# For matlab users: load signal from .mat file -> uncomment the following 2 lines
# import scipy.io
# signal = scipy.io.loadmat('/Users/loukas/Downloads/Sera.mat')['D'][:180]

# Call the function
# 2D plot, does not pop-up, figure is saved
plot_signal2glasser(signal, path_to_surfaces, save_png_to, mode='2D', view='lateral', hemisphere='left', cmap='jet', colorbar = False)

# 3D plot, html will automatically be saved and opened on your browser
# Note: IT'S INTERACTIVE :)
plot_signal2glasser(signal, path_to_surfaces, save_png_to, mode='3D', hemisphere='left', cmap='jet',  colorbar = True)

