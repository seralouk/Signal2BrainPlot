import numpy as np, os, warnings
from nilearn import plotting, datasets; from nilearn.surface import load_surf_data
warnings.filterwarnings("ignore", category=RuntimeWarning)



def plot_signal2glasser(signal, path, save_plot, mode='2D', view='lateral', hemisphere='left',cmap='jet', colorbar = True):
	"""Function that plots a signal on the glasser atlas. The surface mesh is the fslaverage in high resolution.

	Author: Serafeim Loukas, EPFL, Nov 2019

    Parameters
    ----------
    signal : numpy array
        A numpy array containing the signal.

    path : string
        Specifies the path to the glasser annotation surface.

    save_plot : string
        Where to save the generated plot.

    mode : string
    	'2D' or '3D': the type of plot

    view : string, optional (default='lateral')
        Specifies the view of the plot. Available options:
        ['lateral', 'medial', 'dorsal', 'ventral', 'anterior', 'posterior'] 

    hemisphere : string, optional (default='left')
        The hemisphere. Options: 'left' or 'right'

    cmap : string, optional (default='jet')
        The colorbar's cmap

    colorbar : Boolean, optional (default='True')
        Display the colorbar

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
	if mode=='2D':
		plotting.plot_surf_roi(surface["pial_{}".format(hemisphere)], roi_map = parcellation, hemi = hemisphere, view = view, bg_map = surface["sulc_{}".format(hemisphere)], bg_on_data=True,
darkness = .5, output_file = save_plot +'2D_mapped_signal.png', cmap = cmap, colorbar = False)
	else:
		print("For the 3D case, the input arguments 'view' is omitted")
		view = plotting.view_surf(surface["pial_{}".format(hemisphere)], parcellation, cmap = cmap, bg_map = surface["sulc_{}".format(hemisphere)], symmetric_cmap = False)
		view.save_as_html(save_plot +'3D_mapped_signal.html')
		view.open_in_browser()

	return print("All done. The 2D plot was saved in: {}".format(save_plot))


