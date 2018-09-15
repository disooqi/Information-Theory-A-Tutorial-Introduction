"""Python (v2.7) code to accompany book:  Information Theory by JV Stone, 2015.

File: infotheory5_2.py.
Author: John De Pledge.
Copyright: 2015, JV Stone, Psychology Department, Sheffield University,
                    Sheffield, England.
This code can be downloaded from
    http://jim-stone.staff.shef.ac.uk/BookInfoTheory/InfoTheoryPython.html
Creative Commons License (http://creativecommons.org/licenses/by-nc/4.0/).
You are free to share and adapt for non-commercial purposes only.

Summary: Produces histograms of Gaussian data in Figs 5.2a-d.  
Also calculates the entropies of histograms with different bin widths.

Bin width = 1.0 --> H(X) = 2.104
Bin width = 0.5 --> H(X) = 2.062
Bin width = 0.1 --> H(X) = 2.047

As the data is generated randomly, there may be some variation in the calculated values."""

import math
import numpy as np
from matplotlib import pyplot
import matplotlib.mlab as mlab
import information_theory as it

PI = 3.14159265359
SIGFIGS = 3

def main():
    """Main function for Figs 5.2 example"""

    size = 1000 * 1000

    # Set standard deviation & mean of Gaussian distribution
    sd = 1.0
    mean = 0.0

    # Analytic differential entropy of Gaussian distribution. Eq 5.47.
    analytic_hx = 0.5 * it.log2(2.0 * PI * math.exp(1) * sd * sd)
    analytic_hx = it.strrounddp(analytic_hx, SIGFIGS)

    pyplot.figure("Example 5.2", figsize=(10, 8))

    xvals = np.random.normal(mean, sd, size)

    # Loop for each histogram for which we set a bin size and the number
    # of bins
    for bins in [(1.0, 11, 1, 7), (0.5, 23, 2, 15), (0.1, 111, 3, 71)]:
        binwidth, numbins, figure, bins_display = bins
        # Set the +/ standard deviation range
        sdrange = binwidth * numbins / 2.0
        # Ignore any values more than sdrange standard deviations out
        xtrunc = [x for x in xvals if abs(x) < sdrange]
        # Set the bin edges
        binedges = [x * binwidth - sdrange for x in range(numbins + 1)]
        # bin the data
        xhist, _ = np.histogram(xtrunc, binedges)
        # Eq. 5.18 P 116
        HX = it.entropy_from_frequencies(xhist)
        HX = it.strrounddp(HX, SIGFIGS)
        # Find differential entropy 
        HXdiff = it.entropy_from_frequencies(xhist) - it.log2(1.0 / binwidth)
        HXdiff = it.strrounddp(HXdiff, SIGFIGS)

        # Create the histogram graphic

        pyplot.subplot(2, 2, figure)

        # Further truncate the data for display to show bins_display bins
        # Set the +/ standard deviation range
        # Ignore any values more than sdrange standard deviations out
        sdrange = binwidth * bins_display / 2.0
        xtrunc = [x for x in xtrunc if abs(x) < sdrange]

        # Set the bin edges
        binedges = [x * binwidth - sdrange for x in range(bins_display + 1)]
        pyplot.hist(xtrunc, binedges, normed=1, histtype='bar')

        pyplot.title("Bin width = %s\n\nH(X) = %s bits, Hdiff(X) = %s bits" % (binwidth, HX,HXdiff))
        pyplot.axis('off')

    # Create PDF graphic
    pyplot.subplot(2, 2, figure + 1)
    pyplot.title("PDF Hdiff(X) = %s bits," % (analytic_hx,))
    x = np.linspace(-3.5, 3.5, 100)
    pyplot.plot(x, mlab.normpdf(x, mean, sd))
    pyplot.axis('off')
    pyplot.show()

if __name__ == "__main__":

    main()