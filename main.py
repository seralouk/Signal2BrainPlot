# Import libraries
import numpy as np, os, sys
from nilearn import plotting, datasets; from nilearn.surface import load_surf_data
sys.path.append('/Users/loukas/Desktop/Signal2Glasser/Utilities/')
from SeraPlot import plot_signal2glasser_2D, plot_signal2glasser_3D


# Path to the folder that contains the fslaverage & glasser subfolders
# Note: do not change anything to ensure full functionality
path_to_surfaces = '/Users/loukas/Desktop/Signal2Glasser/'

# Where to save the plots.
save_png_to = '/Users/loukas/Desktop/Signal2Glasser/example_outputs/'
if not os.path.exists(save_png_to):
	os.mkdir(save_png_to)


##############################################################################
##############################################################################
##############################################################################

# The signal for 2D visualization (should be a vector with 180 elements encoding the regional values of the desired hemisphere)
#signal_2D = np.random.randn(180,1) # plot random signal
signal_2D = np.arange(1,181).reshape(-1,1) # plot the glasser atlas

# For matlab users: load signal from .mat file -> uncomment the following 2 lines
# import scipy.io
# signal = scipy.io.loadmat('/Users/loukas/Downloads/Sera.mat')['D'][:180]

# Call the function
# 2D plot, does not pop-up, figure is saved
plot_signal2glasser_2D(signal_2D, path_to_surfaces, save_png_to, view='lateral', hemisphere='left', cmap='jet', colorbar = False, black_bg=True)

##############################################################################
##############################################################################
##############################################################################

# The signal for 3D visualization (should be a vector with 360 elements)
# The first 180 values should belong to LEFT hemishere and the remaining to the RIGHT
# 3D plot, html will automatically be saved and opened on your browser
# Note: IT'S INTERACTIVE :)

signal_3D = np.concatenate([np.arange(1,181),np.arange(1,181)]).reshape(-1,1) # plot the glasser atlas
# signal_3D = np.random.randn(360,1)

plot_signal2glasser_3D(signal_3D, path_to_surfaces, save_png_to, hemisphere='left', cmap='jet', colorbar = True, black_bg=True, symmetric_cmap=False)

