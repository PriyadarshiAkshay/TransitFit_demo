# Importing necessary modules
import transitfit
import platform # To check python version
import dynesty # To check dynesty version
from pathlib import Path # To create output folders
import time # To calculate time taken

# Counter for start time
start_time = time.perf_counter()

# These are must-needed inputs for the retrieval
# Add input_data, priors and filterpath
inputdata = "./WASP-91b/data_paths.csv" # The list of lightcurve paths
priors = "./WASP-91b/WASP-91 b Priors_test.csv" # The list of priors
filterpath = "./WASP-91b/TESS_filter_path.csv" # The list of filter paths

# Stellar properties: radius, mass, temperature, metallicity
# These values can be found in the literature or exoplanet.eu or exoplanetarchive.ipac.caltech.edu
# The first input is the value and the second input is the uncertainty
# For WASP-91b, the values are:
host_r = (0.86, 0.03)
host_m = (0.84, 0.07)
host_T = (4920, 80)
host_z = (0.19, 0.13)


# Path for output folders
outpath = "./WASP-91b_TransitFit_output"

host_logg = transitfit.calculate_logg(host_m, host_r)

# Number of parallel processes
n_procs = 7

# Version check
print(f"Running on python version {platform.python_version()}")
print(f"Using TransitFit version {transitfit.__version__}")
print(f"Dynesty version {dynesty.__version__}")

# Check if output folder exists
print(f"Output will be saved in the folder {outpath}")
Path(outpath).mkdir(parents=True, exist_ok=True)


# Run the retrieval, the description of each parameter can be found in the documentation
results = transitfit.run_retrieval(
    inputdata,
    priors,
    filterpath,
    host_T=host_T,
    host_logg=host_logg,
    host_z=host_z,
    host_r=host_r,
    # cadence=120 /60,
    # walks=100,
    # slices=10,
    nlive=2000,
    allow_ttv=False,
    detrending_list=[["nth order", 2]],
    dynesty_sample="rslice",
    fitting_mode="folded",
    limb_darkening_model="quadratic",
    ld_fit_method="independent",  #'coupled',#'independent'
    ldtk_cache="ldtk_cache",
    max_batch_parameters=30,
    batch_overlap=2,
    #dlogz=1000,
    maxiter=None,
    maxcall=None,
    dynesty_bounding="multi",
    normalise=True,
    detrend=True,
    detrending_limits=[[-0.0015, 0.0015]],
    results_output_folder=outpath + "/output_parameters",
    final_lightcurve_folder=outpath + "/fitted_lightcurves",
    plot_folder=outpath + "/plots",
    plot=None,
    marker_color="dimgray",
    line_color="black",
    bin_data=True,
    binned_color="red",
    n_procs=n_procs,
    #normalise_limits=[0.9, 1.1],
    check_batchsizes=False,
    median_normalisation=True,
    #fit_ttv_taylor=True,
    error_scaling=False,
    # error_scaling_limits=[1e-7,2],
    # ldtk_uncertainty_multiplier=1.,
)

print(f"Time taken is {time.perf_counter()-start_time:f} seconds")
