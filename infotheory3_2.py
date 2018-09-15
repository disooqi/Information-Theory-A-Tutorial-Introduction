"""Python (v2.7) code to accompany book:  Information Theory by JV Stone, 2015.
File: infotheory3_2.py.
Author: John De Pledge.
Copyright: 2015, JV Stone, Psychology Department, Sheffield University,
                    Sheffield, England.
This code can be downloaded from
    http://jim-stone.staff.shef.ac.uk/BookInfoTheory/InfoTheoryPython.html
Creative Commons License (http://creativecommons.org/licenses/by-nc/4.0/).
You are free to share and adapt for non-commercial purposes only.

Summary: Calculates entropy of two dice.
Reproduces histogram in Figure 3.2b, p54 """

from collections import Counter
import itertools
import numpy as np
from matplotlib import pyplot
from information_theory import entropy_from_probabilities, strrounddp

def main():
    """Main function for Figure 3.2b example"""

    # Create a list holding the possible outcomes for a single dice
    dice = [1, 2, 3, 4, 5, 6]

    # Get the combinations of two dice
    # Use itertools.product which gives the Cartesian product of two lists.
    combinations = itertools.product(dice, dice)

    # Work out the sum of each combination.
    # The square brackets denote a list comprehension, which is read from
    # left to right.
    # In words : "Make a list of the sum of each combination for every
    # combination in combinations.
    dice_totals = [sum(combination) for combination in combinations]

    # Generate a dict of items and their frequencies
    counterdict = Counter(dice_totals)

    # Extract the frequencies & sums
    frequencies = counterdict.values()
    two_dice_totals = counterdict.keys()

    # Transform the frequencies to probabilities
    #
    # The square brackets denote a list comprehension.
    # The probability of an event is its frequency divided by the total of all
    # frequencies.  Working this out is the first part of the list
    # comprehension, which is read from left to right.
    # In words : "calculate the probabilty for each frequency in the
    # list of frequencies"

    sum_of_frequencies = sum(frequencies)

    probabilities = [freq / float(sum_of_frequencies) for freq in frequencies]

    HX = entropy_from_probabilities(probabilities)

    # Use pyplot class from matplotlib to draw a bar chart
    # First create a pair of default axes
    pyplot.figure("Example 3.2b")
    axes = pyplot.subplot(111)

    width = 0.2                 # Set the bar width

    # Add a blank label to shift the bars right
    two_dice_totals = [" "] + two_dice_totals

    # Create the bars.  Prepend a zero value to the probability list
    # to go with the blank label.
    axes.bar(range(len(two_dice_totals)), [0] + probabilities, width=width)

    # Space the ticks and set the labels to be the dice throw totals.
    axes.set_xticks(np.arange(len(two_dice_totals)) + width / 2)
    axes.set_xticklabels(two_dice_totals)

    # Set the title using our entropy result, rounded to 3 sig figs
    # Label the axes
    pyplot.title("Entropy = %s bits/pair" % strrounddp(HX, 3),fontsize=20)
    pyplot.xlabel("Outcome value", fontsize=20)
    pyplot.ylabel("Outcome probability",fontsize=20)

    # Display the result
    pyplot.show()


if __name__ == "__main__":
    main()
