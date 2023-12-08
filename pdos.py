import math;
import numpy;
import h5py;
import matplotlib.pyplot as plt

##############################################################
# Open the banddos.hdf file and name some data groups in it. #
##############################################################
banddosFile = h5py.File('banddos.hdf', 'r')

cellData = banddosFile['cell']
kptsData = banddosFile['kpts']
generalData = banddosFile['general']
localData = banddosFile['Local']

# Read in number of spins in the calculation. The plot should
# feature two panels for two spins and a single panel for
# a nonmagnetic calculation.
nSpins = generalData.attrs["spins"][0]

###################
# Initialize plot #
###################
minY = -9.0 ; maxY = 5.0
#minY = -5.0 ; maxY = 9.0 # choice for 2nd example

if nSpins == 2:
   figure, axes = plt.subplots(1, 2, sharey=True, figsize=(6, 6))
   figure.subplots_adjust(wspace=0.0)
else:
   axes = [1]
   figure, axes[0] = plt.subplots(1, 1, figsize=(4, 6))
   figure.subplots_adjust(left=0.2)

# Note: For nSpins==1 nSpins-1 is 0 and we do some things twice.
#       For 2 spins addressing indices 0 and nSpins-1 affects the
#       different subplots.
axes[0].set_ylim(ymin=minY,ymax=maxY)
axes[nSpins-1].set_ylim(ymin=minY,ymax=maxY)
axes[0].set_ylabel("$E - E_\mathrm{F}$ (eV)").set_size(16)
axes[0].set_xlabel("states / eV").set_size(16)
axes[nSpins-1].set_xlabel("states / eV")

############
# Plot DOS #
############
colors = ['black','red','blue','green','purple'] # different colors for different weights

# Select the weights of the DOS contributions to be plotted.
# We are interested in the total DOS and the d-like DOS in the MT sphere of
# the 1st atom type.
weightNames = ["Total","MT:1d"]
#weightNames = ["Total","MT:2p","MT:2d","MT:1s","INT"] # choice of weights for 2nd example
# Some other weights:
# weightName = "INT"   # DOS in the interstitial region
# weightName = "MT:1s" # s-like DOS in the 1st atom type's MT sphere.
# weightName = "MT:1p" # p-like DOS in the 1st atom type's MT sphere.
# weightName = "MT:1f" # f-like DOS in the 1st atom type's MT sphere.
# weightName = "MT:2s" # s-like DOS in the 2nd atom type's MT sphere (if available).
#####################################################################################
# Plot the DOS for the selected weights                                             #
# Note: 1. In the banddos.hdf file the energy grid is stored in Hartree relative to #
#          the Fermi energy. We transform that to eV.                               #
#       2. The DOS is stored in states/Hartree. We transform that to states/eV.     #
#####################################################################################
energies = localData["DOS"]["energyGrid"][:] * 27.211
for iSpin in range(nSpins):
   for iWeight in range(len(weightNames)):
      values = []
      values[:] = localData["DOS"][weightNames[iWeight]][iSpin][:] / 27.211
      minIndex = 0
      maxIndex = len(values)-1
      for i in range(len(values)):
         if energies[i] < minY: minIndex = i
         if energies[i] > maxY:
            maxIndex = i
            break
      axes[iSpin].plot(values[minIndex:maxIndex+1],energies[minIndex:maxIndex+1],
                       color=colors[iWeight],label=weightNames[iWeight],zorder=2)

##########################################################################################
# Do some postprocessing in the plot                                                     #
# 1. Norm the x axis of the two subplots for spin-polarized calculation.                 #
# 2. Plot a line to indicate the Fermi level.                                            #
# 3. Plot spin-indicating arrow symbols in the subplots for spin-polarized calculations. #
# 4. Put a legend in one of the subplots.                                                #
# 5. Invert the x axis in the left subplot for spin-polarized calculations.              #
##########################################################################################
xlims = [axes[0].get_xlim(),axes[nSpins-1].get_xlim()]
maxX = max(xlims[0][1],xlims[nSpins-1][1])
axes[0].set_xlim(xmin=0.0,xmax=maxX)
axes[nSpins-1].set_xlim(xmin=0.0,xmax=maxX)

axes[0].plot([0.0, maxX], [0.0, 0.0], color='cyan', linestyle='-',linewidth=1.0, zorder=1)
axes[nSpins-1].plot([0.0, maxX], [0.0, 0.0], color='cyan', linestyle='-',linewidth=1.0, zorder=1)

if nSpins == 2:
   spinArrows = [r"$\uparrow$",r"$\downarrow$"]
   for iSpin in range(nSpins):
      xlims = axes[iSpin].get_xlim()
      axes[iSpin].annotate(spinArrows[iSpin], [0.75*xlims[1],3.5],ha="center",va="center",size=24)

axes[nSpins-1].legend(loc='lower right')

if nSpins == 2:
   axes[0].invert_xaxis()
   axes[1].get_yaxis().set_visible(False)
##################################################
# Store the plot as an image to the file DOS.png #
# and as a vector graphic to the file DOS.svg    #
##################################################
plt.savefig('DOS.png',dpi=300)
plt.savefig('DOS.svg')

###########################################
# Alternatively, show the plot in a window #
###########################################
plt.show()
