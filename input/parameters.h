************************************************************************
* This file contains definitions and DEFAULT values of all BSE parameters.
************************************************************************
* See Tout et al., 1997, MNRAS, 291, 732 for a description of many of the
* processes in the code as well as the relevant references mentioned
* within the code. 
*
* Reference for the stellar evolution formulae is 
* Hurley, Pols & Tout, 2000, MNRAS, 315, 543 (SSE paper).  
* Giacobbo, Mapelli, Spera, 2018, MNRAS 480, (first MOBSE paper)
* Giacobbo, Mapelli, 2020, MNRAS 480, (kicks paper)
*
* Reference for the binary evolution algorithm is 
* Hurley, Tout & Pols, 2002, MNRAS, 329, 897 (BSE paper). 
************************************************************************
* BSE parameters:
************************************************************************

* neta is the Reimers mass-loss coefficient (neta*4x10^-13)
* DEFAULT: 0.5
       neta = 0.5

* bwind is the binary enhanced mass loss parameter (inactive for single)
* DEFAULT: 0.0
       bwind = 0.0

* hewind if a factor to control the amount of He star mass-loss, i.e.
* 1.0e-13*hewind*L^(2/3) gives He star mass-loss
* DEFAULT: 1.0
       hewind = 1.0

* alpha1 is the common-envelope efficiency parameter
* DEFAULT: 5.0
      alpha1 = 5.0

* lambda is associated with the binding energy factor for common envelope 
* evolution, as follows:
*	> 0: binding energy parameter is computed as described in Claeys et al. (2014)
*	     and a fraction lambda of recombination energy is used to help in the
*	     envelope expulsion
*	= 0: binding energy parameter is computed as described in Claeys et al. (2014)
*	     and no recombination energy is used in the process
*	< 0: binding energy parameter is constant and given by ABS(lambda)
* DEFAULT: 0.1
      lambda = 0.1

* ceflag procedure for common-envelope evolution:
*	0 : use the procedure described in Hurley et al. (2002)
*	3 : use de Kool (or Podsiadlowski) prescription
* DEFAULT: 0
       ceflag = 0

* tflag > 0 activates tidal circularisation
* DEFAULT: 1
       tflag = 1

* ifflag > 0 uses WD IFMR of HPE, 1995, MNRAS, 272, 800
* DEFAULT: 0
       ifflag = 0 

* wdflag > 0 uses modified-Mestel cooling for WDs
* DEFAULT: 1
       wdflag = 1 

* bhflag > 0 allows velocity kick at BH formation
* DEFAULT: 3
      bhflag = 3.0

* nsflag > 0 SN explosion mechanim
* DEFAULT: 3
      nsflag = 3

* piflag > activates the PPISN and PISN
* DEFAULT: 1
       piflag = 1

* mxns is the maximum NS mass
* DEFAULT: 3.0
       mxns = 3.0

* idum is the random number seed used by the kick routine. 
       idum = 29769

* Next come the parameters that determine the timesteps chosen in each
* evolution phase:
*   pts1 - MS                  
*   pts2 - GB, CHeB, AGB, HeGB 
*   pts3 - HG, HeMS            
* as decimal fractions of the time taken in that phase.
* DEFAULT: pts1 = 0.05, pts2 = 0.01, pts3 = 0.02
       pts1 = 0.05
       pts2 = 0.01
       pts3 = 0.02

* sigmas are the dispersion in the Maxwellian for the SN kick speed (km/s)
* DEFAULT: sigma1 = sigma2 = 265.0 
       sigma1 = 265.0
       sigma2 = 265.0

* beta is wind velocity factor: proportional to vwind**2
* DEFAULT: 0.125 
       beta = 0.125

* xi is the wind accretion efficiency factor
* DEFAULT: 1.0 
       xi = 1.0 

* acc2 is the Bondi-Hoyle wind accretion factor
* DEFAULT: 1.5 
       acc2 = 1.5

* epsnov is the fraction of accreted matter retained in nova eruption
* DEFAULT: 0.001 
       epsnov = 0.001

* eddfac is Eddington limit factor for mass transfer
* DEFAULT: 1.0 
       eddfac = 1.0

* gamma is the angular momentum factor for mass lost during Roche
* DEFAULT: -1.0
       gamma = -1.0

* dtp is the timestep (in Myr) for allocating the track
* Note that this can be zero (full info). However, for numerical
* stability, it is recommended to have it >= 1.0 and <= dtsaveMZ
* DEFAULT: 0.0
       dtp = 0.0
***********************************************************************