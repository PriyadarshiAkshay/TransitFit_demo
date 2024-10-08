# TransitFit_demo

A demonstration to help get started with using TransitFit. In this demo, we are using TESS lightcurves for WASP-91b as an example.

## Prerequisites

Before using TransitFit, you must have the following:

1. **List of lightcurves** for the exoplanet. inputdata.csv
2. **List of corresponding filters** for the lightcurves. filterpath.csv
3. **Priors** for the fitting. priors.csv
4. **Stellar properties**

### 1. List of Lightcurves

One lightcurve corresponds to a single epoch/transit-event. If you have a lightcurve with multiple transits, please split them. A lightcurve should have 3 columns: Time,Flux,Flux_err. Check the plot of an example lightcurve in demo.ipynb

Lightcurves can be retrieved from:
- ExoMast
- Vizier
- Literature

If you have images from any telescope, usually there's a well-defined method to extract lightcurves from them. Eg:
- To extract lightcurves for TESS targets, you can use [firefly](https://github.com/sourestdeeds/firefly)
- To extract lightcurves from JWST-NIRISS images, see [TransitFit JWST instructions](https://github.com/SPEARNET/TransitFit/tree/master/jwst)
- To extract HST lightcurves, use Iraclis.


The list must be provided in a .csv file in this format:

```csv
Path,Telescope,Filter,Epochs,Detrending  
./WASP-91b_input_files/mastDownload/tess2018206045859-s0001-0000000238176110-0120-s/split_curve_0.csv,0,0,0,0  
./WASP-91b_input_files/mastDownload/tess2018206045859-s0001-0000000238176110-0120-s/split_curve_1.csv,0,0,1,0  
```

In this example we have 2 lightcurves, both from the same telescope (0), both in the same filter (0), both have same detrending requirements (0), but they have different transit-mid times (0 and 1).

If they were from two different telescopes, then we would provide 0 for the telescope column corresponding to first lightcurve and 1 for the second one. Eg.  
```csv
Path,Telescope,Filter,Epochs,Detrending  
./WASP-91b_input_files/mastDownload/tess2018206045859-s0001-0000000238176110-0120-s/split_curve_0.csv,0,0,0,0  
./WASP-91b_input_files/mastDownload/tess2018206045859-s0001-0000000238176110-0120-s/split_curve_1.csv,1,0,1,0  
```

### 2. List of Corresponding Filters

Usually this information is provided along with the lightcurves. Some filter profiles can be accessed here: [SVO Filter Profile Service](http://svo2.cab.inta-csic.es/theory/fps/). A filter profile should have two columns: # Wavelength (nm), lambda Transmission. Check the plot of an example lightcurve in demo.ipynb

This is essentially explaining what the filter indexes mean in the list of lightcurves. Eg. if we have all the lightcurves in the same TESS filter, we would write 0 as the filter index in the list of lightcurves, and then we would prepare the list of filters in a .csv file as:

```csv
filter_idx,low_wl,high_wl  
0,./WASP-91b_input_files/TESS_filter.csv,
```
For 2 different filters, we could write

```csv
filter_idx,low_wl,high_wl  
0,./WASP-91b_input_files/TESS_filter.csv,  
1,./WASP-91b_input_files/TESS_filter2.csv,  
```

### 3. The priors for the fitting. 
Sort of, the best guess that you have about the parameters that you want to fit. Better priors generally result in faster results. In some cases, we have seen that fititng is extremely sensitive to the range of priors. So, it might help to provide a narrower range for priors. These values can be found in the literature or exoplanet.eu or exoplanetarchive.ipac.caltech.edu.

This must be provided in a .csv file in this format:

```csv
Parameter,Distribution,Input_A,Input_B,Filter
P,gaussian,2.798579071616348,1.0987784248566104e-07
t0,gaussian,2456297.719503299,9.830024959407715e-05
a,gaussian,0.03741664754813431,0.0013772917483009732
inc,gaussian,88.49414514807431,0.5718276161969188  
w,fixed,90.0,,  
ecc,fixed,0.0,,  
rp,uniform,0.10522606200514388,0.12522606200514388,0
```

The first column lists the parameters, the second column informs whether the parameter has to be kept fixed or to be fitted. The distribution 'gaussian' generates a gaussian distribution with mean as Input_A and std as Input_B for the prior. The distribution 'uniform' generates a uniform distribution between Input_A and Input_B for the prior. See examples of gaussian and uniform samples in demo.ipynb

In case of filter-dependendent parameters like radius, we also need to provide the index of the filter, this index should be consistent with the list of lightcurves and list of filters. If there are 2 different filters used in lightcurve list, we must provide two separate priors for rp. Eg.

```csv
Parameter,Distribution,Input_A,Input_B,Filter
P,gaussian,2.798579071616348,1.0987784248566104e-07
t0,gaussian,2456297.719503299,9.830024959407715e-05
a,gaussian,0.03741664754813431,0.0013772917483009732
inc,gaussian,88.49414514807431,0.5718276161969188  
w,fixed,90.0,,  
ecc,fixed,0.0,,  
rp,uniform,0.10522606200514388,0.12522606200514388,0
rp,uniform,0.10522606200514388,0.12522606200514388,0
```

### 4. Stellar properties. 
These values can also be found in the literature or exoplanet.eu or exoplanetarchive.ipac.caltech.edu. You'll need to provide them in form of tuples. (Value, Uncertainty).

radius, mass, temperature, metallicity

Eg: 
```python
host_r = (0.86, 0.03)  
host_m = (0.84, 0.07)  
host_T = (4920, 80)  
host_z = (0.19, 0.13)
```

Once we have all these, we can prepare a .py file with all the necessary information. Eg. [WASP-91b.py](https://github.com/PriyadarshiAkshay/TransitFit_demo/blob/main/WASP-91b.py). Then we call 

```bash
python3 WASP-91b.py
```

This step for WASP-91b.py should roughly take <10 minutes. But for different use cases, it could take a while (upto days) depending on CPU, quality and number of lightcurves, quality of priors, parameters to be fitted etc. Over here we have specified output to be saved in WASP-91b_TransitFit_output file, and hence all the output can be found in that folder. 

## Output

If we look at the WASP-91b_TransitFit_output folder, we will find 3 subfolders:

1. **fitted_lightcurves**: All the lightcurves (now detrended and normalised, if specified so) along with the best fit curve generated from the best fit parameters.
2. **output_parameters**: All the best-fit values for the parameters which were fitted by TransitFit. results_with_asymmetric_errors.csv is the set of results we recommend to use. This handles the asymmetric nature of sample distribution around the best fit value and provides the errors accordingly. Other files show the standard deviation of samples as the error. 
3. **plots**: The plots comparing the raw lightcurve with the best fit lightcurve. Also, the plots corresponding to posterior distribution of the parameters.
You should definitely check the plot provided in folded_curves/with_errorbars to check the quality of the fitting.

## Transmission Spectroscopy

To do transmission spectrocopy, you will need lightcurves taken in different filters/wavelength bands. Say you have 100 lightcurves, taken across different wavelength ranges. You will need to fit all those 100 lightcurves in the way described above. Ensure that the lightcurves have appropriate filter indices, and those filter indices are explained in the list of filters. Also, the priors for radius (or other wavelength-dependent parameter) is provided separately for all of them.

The results will provide the effective radius of the planet corresponding to different filters. This can be plotted to generate the spectrum. An example spectrum from TransitFit analysis of WASP-96~b using JWST-NIRISS data is shown in demo.ipynb

## TTV analysis

For TTV analysis, there are two modes:
1. Fit for all the parameters, then use the value of P from the first fit as the prior and fit again. This time, provide the parameter allow_ttv=False when calling run_retrieval. This will result in separate t0 values for each epoch. These all t0 values will be fitted on the provided prior. To find the corresponding transit-mid time for a lightcurve 5 epochs away from the prior, add 5*P to the value of t0 for this epoch.

2. P-dot and P-double dot fitting. This fits for the first and second derivative of period. Use fit_ttv_taylor=True, when calling run_retrieval.