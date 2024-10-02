# TransitFit_demo
A demonstration to help get started with using TransitFit. In this demo we are using TESS lightcurves for WASP-91b as an example.

Must have before using TransiFit: 
1. List of lightcurves for the exoplanet. One lightcurve corresponds to a single epoch/transit-event. If you have a lightcurve which has multiple transits, please split them.
Lightcurves can be retrieved from ExoMast/Vizier/Literature. If you have images from any telescope, usually there's a well-defined method to extract lightcurves from them. For TESS targets, you can use https://github.com/sourestdeeds/firefly to run TransitFit.
Additionally, we also provide instruction to extract JWST-NIRISS lightcurves in TransitFit https://github.com/SPEARNET/TransitFit/tree/master/jwst.
HST lightcurves can be extracted using Iraclis.

The list must be provided in this format:

Path,Telescope,Filter,Epochs,Detrending  
./WASP-91b_input_files/mastDownload/tess2018206045859-s0001-0000000238176110-0120-s/split_curve_0.csv,0,0,0,0  
./WASP-91b_input_files/mastDownload/tess2018206045859-s0001-0000000238176110-0120-s/split_curve_1.csv,0,0,1,0  

In this example we have 2 lightcurves, both from the same telescope (0), both in the same filter (0), both have same detrending requirements (0), but they have different transit-mid times (0 and 1).

If they were from two different telescopes, then we would provide 0 for the telescope column corresponding to first lightcurve and 1 for the second one. Eg.  
Path,Telescope,Filter,Epochs,Detrending  
./WASP-91b_input_files/mastDownload/tess2018206045859-s0001-0000000238176110-0120-s/split_curve_0.csv,0,0,0,0  
./WASP-91b_input_files/mastDownload/tess2018206045859-s0001-0000000238176110-0120-s/split_curve_1.csv,1,0,1,0  

2. The list of corresponding filters for the lightcurves. Usually this information is provided along with the lightcurves. Some filter profiles can be accessed here: http://svo2.cab.inta-csic.es/theory/fps/

This is essentially explaining what the filter indexes mean in the list of lightcurves. Eg. if we have all the lightcurves in the same TESS filter, we would write 0 as the filter index in the list of lightcurves, and then we would prepare the list of filters as:

filter_idx,low_wl,high_wl  
0,./WASP-91b_input_files/TESS_filter.csv,

For 2 different filters, we could write

filter_idx,low_wl,high_wl  
0,./WASP-91b_input_files/TESS_filter.csv,  
1,./WASP-91b_input_files/TESS_filter2.csv,  


3. The priors for the fitting. Sort of, the best guess that you have about the parameters that you want to fit. Better priors generally result in faster results. In some cases, we have seen that fititng is extremely sensitive to the range of priors. So, it might help to provide a narrower range for priors. These values can be found in the literature or exoplanet.eu or exoplanetarchive.ipac.caltech.edu.

This must be provided in this format:

Parameter,Distribution,Input_A,Input_B,Filter
P,gaussian,2.798579071616348,1.0987784248566104e-07
t0,gaussian,2456297.719503299,9.830024959407715e-05
a,gaussian,0.03741664754813431,0.0013772917483009732
inc,gaussian,88.49414514807431,0.5718276161969188  
w,fixed,90.0,,  
ecc,fixed,0.0,,  
rp,gaussian,0.11522606200514388,0.0014251379213954217,0

The first column lists the parameters, the second column informs whether the parameter has to be kept fixed or to be fitted. The distribution 'gaussian' generates a gaussian distribution with mean as Input_A and std as Input_B for the prior. The distribution 'uniform' generates a uniform distribution between Input_A and Input_B for the prior. 

In case of filter-dependendent parameters like radius, we also need to provide the index of the filter, this index should be consistent with the list of lightcurves and list of filters. If there are 2 different filters used in lightcurve list, we must provide two separate priors for rp. Eg.

Parameter,Distribution,Input_A,Input_B,Filter
P,gaussian,2.798579071616348,1.0987784248566104e-07
t0,gaussian,2456297.719503299,9.830024959407715e-05
a,gaussian,0.03741664754813431,0.0013772917483009732
inc,gaussian,88.49414514807431,0.5718276161969188  
w,fixed,90.0,,  
ecc,fixed,0.0,,  
rp,gaussian,0.11522606200514388,0.0014251379213954217,0
rp,gaussian,0.11522606200514388,0.0014251379213954217,1


4. Stellar properties. These values can also be found in the literature or exoplanet.eu or exoplanetarchive.ipac.caltech.edu. You'll need to provide them in form of tuples. (Value, Uncertainty).

radius, mass, temperature, metallicity

Eg: 
host_r = (0.86, 0.03)  
host_m = (0.84, 0.07)  
host_T = (4920, 80)  
host_z = (0.19, 0.13)