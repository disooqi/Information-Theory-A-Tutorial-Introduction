"""Python (v2.7) code to accompany book:  Information Theory by JV Stone, 2015.
File: infotheory7_1.py.
Author: John De Pledge.
Copyright: 2015, JV Stone, Psychology Department, Sheffield University,
                    Sheffield, England.
This code can be downloaded from
    http://jim-stone.staff.shef.ac.uk/BookInfoTheory/InfoTheoryPython.html
Creative Commons License (http://creativecommons.org/licenses/by-nc/4.0/).
You are free to share and adapt for non-commercial purposes only.
Summary: The code recreates the Figure 7.1 P155, using Eq. 7.18, which shows how the 
capacity of a Gaussian channel increases with signal to noise ratio.

"""
from matplotlib import pyplot
import information_theory as it

POINTS_TO_PLOT = 100 + 1

def main():
    """Main function for Figure 7.1 example"""

    # Initialise our x & y lists
    x = [0] * POINTS_TO_PLOT
    y = [0] * POINTS_TO_PLOT

    # Work out the stepo size along the x axis
    xstep = 4.0 / float(POINTS_TO_PLOT)

    # Loop for each point up to POINTS_TO_PLOT
    for cnt in range(POINTS_TO_PLOT):
        # Calc signal to noise ratio
        signal_to_noise_ratio = cnt * xstep
        x[cnt] = signal_to_noise_ratio

        # Calculate the channel capacity using 1000 * Eq. 7.18
        y[cnt] = 500.0 * it.log2(1 + signal_to_noise_ratio)

    # Plot the curve
    pyplot.figure("Example 7.1")
    pyplot.plot(x, y)

    # Set title & label the axes
    pyplot.title("Gaussian Channel Capacity & SNR (P/N)",fontsize=20)
    pyplot.xlabel("Signal To Noise Ratio, (P/N)",fontsize=20)
    pyplot.ylabel("Channel Capacity (bits/s)",fontsize=20)

    # Display the graphic
    pyplot.show()

if __name__ == "__main__":
    main()
