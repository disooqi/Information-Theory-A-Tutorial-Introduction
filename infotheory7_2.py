"""Python (v2.7) code to accompany book:  Information Theory by JV Stone, 2015.
File: infotheory7_2.py.
Author: John De Pledge.
Copyright: 2015, JV Stone, Psychology Department, Sheffield University,
                    Sheffield, England.
This code can be downloaded from
    http://jim-stone.staff.shef.ac.uk/BookInfoTheory/InfoTheoryPython.html
Creative Commons License (http://creativecommons.org/licenses/by-nc/4.0/).
You are free to share and adapt for non-commercial purposes only.
Summary: The code recreates the Figure 7.2 P160, using Eq. 7.40,
which shows the probability of error as a function of message length.
"""
import math
from matplotlib import pyplot
import information_theory as it

POINTS_TO_PLOT = 100 + 1

def main():
    """Main function for Figure 7.1 example"""

    # Initialise our x & y result lists
    xvals = [0] * POINTS_TO_PLOT
    yvals = [0] * POINTS_TO_PLOT

    # Work out the step size along the x axis
    xstep = 4000.0 / float(POINTS_TO_PLOT)

    # Calculate the error using Eq. 7.40 P159
    # Uses P = 10, N = 1, R = 0.99, C = 1.0
    # The terms involving just P, N, R & C are static, so calculate
    # them out of the loop
    #  math.sqrt((2 * P * (P + N)) / (N * (P + 2 * N))) * (R - C)
    static = math.sqrt(220.0 / 12.0) * -0.01

    # Loop to work out the list of x & y values
    for cnt in range(POINTS_TO_PLOT):
        message_length = cnt * xstep

        xvals[cnt] = message_length
        yvals[cnt] = it.cumulative_gaussian(math.sqrt(message_length) * static)

    # Plot the curve, set title & label the axes
    pyplot.figure("Example 7.2")
    pyplot.plot(xvals, yvals)
    pyplot.title("Probability of Decoding Error",fontsize=20)
    pyplot.xlabel("Message length, n",fontsize=20)
    pyplot.ylabel("P(error)",fontsize=20)

    # Display the graphic
    pyplot.show()

if __name__ == "__main__":
    main()
