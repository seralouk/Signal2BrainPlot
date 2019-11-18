import numpy as np, os, warnings, matplotlib.pyplot as plt
from nilearn import plotting, datasets; from nilearn.surface import load_surf_data
warnings.filterwarnings("ignore", category=RuntimeWarning)


def plot_signal2glasser_2D(signal, path, save_plot, view='lateral', hemisphere='left',cmap='jet', colorbar = True, black_bg=True):
	"""Function that plots a signal on the glasser atlas. The surface mesh is the fslaverage in high resolution.

	Author: Serafeim Loukas, EPFL, Nov 2019

    Parameters
    ----------
    signal : numpy array
        A numpy array containing the signal. 
        It should be a 180-D signal that corresponds to the selected hemisphere.

    path : string
        Specifies the path to the glasser annotation surface.

    save_plot : string
        Where to save the generated plot.

    view : string, optional (default='lateral')
        Specifies the view of the plot. Available options:
        ['lateral', 'medial', 'dorsal', 'ventral', 'anterior', 'posterior'] 

    hemisphere : string, optional (default='left')
        The hemisphere. Options: 'left' or 'right'

    cmap : string, optional (default='jet')
        The colorbar's cmap

    colorbar : Boolean, optional (default='True')
        Display the colorbar

    black_bg : Boolean, optional (default='True')
        Use black background       

    Attributes
    ----------
	None.  A plot is saved in "save_plot" location.

	"""

	# Load the fsaverage (high-resolution) surface file
	surface = {'pial_right': path + '/fsaverage/pial_right.gii',
 				'sulc_right':  path + '/fsaverage/sulc_right.gii',
 				'sulc_left':   path + '/fsaverage/sulc_left.gii',
 				'pial_left':   path + '/fsaverage/pial_left.gii',
 				'infl_left':   path + '/fsaverage/inflated_left.gii',
 				'infl_right':  path + '/fsaverage/inflated_right.gii'}

	#surface = datasets.fetch_surf_fsaverage('fsaverage')

	# Get the glasser annotation filenames
	parcellation_files = [f for f in sorted(os.listdir(path + 'glasser/')) if 'HCPMMP1' in f]
	if parcellation_files == []:
		raise ValueError("No glasser annotation files were found")
	
	# Get the glasser annotation file for the desired hemisphere
	if hemisphere == 'left':
		parcellation = load_surf_data(path + 'glasser/' + parcellation_files[0])
	else:
		parcellation = load_surf_data(path + 'glasser/' + parcellation_files[1])
	
	# Check view input argument
	available_views = ['lateral', 'medial', 'dorsal', 'ventral', 'anterior', 'posterior']
	if view not in available_views:
		raise ValueError("Invalid 'view' choice, options : {}".format(available_views))
	
	# Check signal dimensions
	if signal.shape[0] != 180:
		raise ValueError("The signal should be an [180,1] array")

	# Map the signal
	parcellation = parcellation.reshape(-1,1)
	for region in range(signal.shape[0]):
		parcellation = np.where(parcellation == (region+1), signal[region], parcellation)
	parcellation = parcellation.ravel()

	# Plotting
	plotting.plot_surf_roi(surface["pial_{}".format(hemisphere)], roi_map = parcellation, hemi = hemisphere, view = view, bg_map = surface["sulc_{}".format(hemisphere)], bg_on_data = True,
darkness = 0.6, output_file = save_plot +'2D_mapped_signal.png', cmap = cmap, colorbar = colorbar, black_bg=black_bg, figure=plt.figure(dpi=400))

	print("All done. The 2D plot was saved in: {}".format(save_plot))
	return





def plot_signal2glasser_3D(signal, path, save_plot, cmap='jet', colorbar = True, black_bg=True, symmetric_cmap=False):
	"""Function that plots a signal on the glasser atlas. The surface mesh is the fslaverage in high resolution.

	Author: Serafeim Loukas, EPFL, Nov 2019

    Parameters
    ----------
    signal : numpy array
        A numpy array containing the signal (signal.size = [360,1])
        The first 180 elements of the vector should encode the regional values of the **left** hemisphere,
        and the remaining 180 elements the values of the **right** hemisphere. 
        The mapping is done based on this rule.

    path : string
        Specifies the path to the glasser annotation surface.

    save_plot : string
        Where to save the generated plot.

    cmap : string, optional (default='jet')
        The colorbar's cmap

    colorbar : Boolean, optional (default='True')
        Whether to display the colorbar.

    black_bg : Boolean, optional (default='True')
        Use black background

    symmetric_cmap : Boolean, optional (default='False')
        Whether to make the cmap symmetric.           

    Attributes
    ----------
	None.  A plot is saved in "save_plot" location.

	"""

	# Load the fsaverage (high-resolution) surface file
	surface = {'pial_right': path + '/fsaverage/pial_right.gii',
 				'sulc_right':  path + '/fsaverage/sulc_right.gii',
 				'sulc_left':   path + '/fsaverage/sulc_left.gii',
 				'pial_left':   path + '/fsaverage/pial_left.gii',
 				'infl_left':   path + '/fsaverage/inflated_left.gii',
 				'infl_right':  path + '/fsaverage/inflated_right.gii'}

	# Load fsaverage surface of each hemishere
	left = load_surf_data(surface['pial_left'])
	right = load_surf_data(surface['pial_right'])

	# Combine fsaverage surfaces together (update vertices indices)
	combined_vertices = np.concatenate([left[0], right[0]])
	combined_faces = np.concatenate([left[1], right[1] + left[0].shape[0]])
	combined_surface= [combined_vertices, combined_faces]

	# Get the glasser annotation filenames
	parcellation_files = [f for f in sorted(os.listdir(path + 'glasser/')) if 'HCPMMP1' in f]
	if parcellation_files == []:
		raise ValueError("No glasser annotation files were found")
	
	# Get the glasser annotation file for both hemispheres and combine
	parcellation_left = load_surf_data(path + 'glasser/' + parcellation_files[0])
	parcellation_right = load_surf_data(path + 'glasser/' + parcellation_files[1])
	
	# Check signal dimensions
	if signal.shape[0] != 360:
		raise ValueError("The signal should be an [360,1] array")

	# Split the signal in case the signal is not symmetric across the hemispheres
	signal_left = signal[0:int(signal.shape[0]/2)]
	signal_right = signal[int(signal.shape[0]/2):]
	
	# Map the signal to both hemispheres
	parcellation_left = parcellation_left.reshape(-1,1)
	for region in range(signal_left.shape[0]):
		parcellation_left = np.where(parcellation_left == (region+1), signal_left[region], parcellation_left)
	
	parcellation_right = parcellation_right.reshape(-1,1)
	for region in range(signal_right.shape[0]):
		parcellation_right = np.where(parcellation_right == (region+1), signal_right[region], parcellation_right)

	# Put them together
	parcellation_both = np.concatenate([parcellation_left, parcellation_right])
	parcellation_both = parcellation_both.ravel()
	assert(combined_vertices.shape[0] == parcellation_both.shape[0])

	# Load fsaverage sulc surface of each hemishere
	left_sulc = load_surf_data(surface['sulc_left'])
	right_sulc = load_surf_data(surface['sulc_right'])
	combined_sulc = np.concatenate([left_sulc, right_sulc])

	print("For the 3D case, the input arguments 'view' is omitted")
	view = plotting.view_surf(combined_surface, parcellation_both, cmap = cmap, bg_map = combined_sulc, symmetric_cmap = symmetric_cmap, black_bg = black_bg, colorbar = colorbar)
	view.save_as_html(save_plot +'3D_mapped_signal.html')
	view.open_in_browser()

	print("All done. The 2D plot was saved in: {}".format(save_plot))
	return

















