"""Python (v2.7) code to accompany book:  Information Theory by JV Stone, 2015.
File: infortheory4_1.py.
Author: John De Pledge.
Copyright: 2015, JV Stone, Psychology Department, Sheffield University,
                    Sheffield, England.
This code can be downloaded from
    http://jim-stone.staff.shef.ac.uk/BookInfoTheory/InfoTheoryPython.html
Creative Commons License (http://creativecommons.org/licenses/by-nc/4.0/).
You are free to share and adapt for non-commercial purposes only.

Summary: Calculates entropy of channel inputs and outputs in Table 4.1.
Reproduces Equations 4.42, 4.45, 4.46, 4.48, 4.51, 4.63

Output:
    
    Table 4.1 frequencies

12   15   2    0    |29
4    21   10   0    |35
0    10   21   4    |35
0    2    15   12   |29
------------------------
16   48   48   16   |128

Eq. 4.42	HX     = 1.811 bits
Eq. 4.45	HY     = 1.994 bits
Eq. 4.46	HXY    = 3.296 bits
Eq. 4.48	HX+HY  = 3.805 bits
Eq. 4.51	I(X,Y) = 0.509 bits
Eq. 4.63	H(Y|X) = 1.484 bits"""

from matplotlib import pyplot
import information_theory as it

def main():
    """Main function for Table 4.1 example"""

    # Our 4x4 frequency data
    distribution = [[12, 15, 2, 0],
                    [4, 21, 10, 0],
                    [0, 10, 21, 4],
                    [0, 2, 15, 12]]

    col_total_frequencies = it.col_totals(distribution)  # Get col total freqs
    row_total_frequencies = it.row_totals(distribution)  # Get row total freqs

    allfrequencies = it.flatten(distribution)   # Make flat list of all freqs

    # HX is the entropy of the input values (col totals)
    HX = it.entropy_from_frequencies(col_total_frequencies)

    # HY is the entropy of the output values (row totals)
    HY = it.entropy_from_frequencies(row_total_frequencies)

    # HXY is the entropy of the whole distribution
    HXY = it.entropy_from_frequencies(allfrequencies)

    # IXY Mutual information
    IXY = HX + HY - HXY

    # Prepare the graphic
    pyplot.figure("Example 4.1", figsize=(10, 4))

    # Prepare the probability table for display
    tdat = [["y1"] + distribution[0] + [row_total_frequencies[0]],
            ["y2"] + distribution[1] + [row_total_frequencies[1]],
            ["y3"] + distribution[2] + [row_total_frequencies[2]],
            ["y4"] + distribution[3] + [row_total_frequencies[3]],
            ["Sum"] + col_total_frequencies + [sum(row_total_frequencies)]]

    pyplot.subplot(2, 1, 1)
    pyplot.title('Counts of Input Value X & Output Value Y')
    pyplot.axis('off')
    pyplot.table(cellText=tdat,
                 colLabels=["Y\X->", "x1", "x2", "x3", "x4", "Sum"],
                 colLoc='center',
                 loc='best')

    # Prepare the calculated entropy/MI/noise table for display
    ents = [["H(X)", it.strrounddp(HX, 3), "Eq. 4.42"],
            ["H(Y)", it.strrounddp(HY, 3), "Eq. 4.45"],
            ["H(X,Y)", it.strrounddp(HXY, 3), "Eq. 4.46"],
            ["H(X) + H(Y)", it.strrounddp(HX+HY, 3), "Eq. 4.48"],
            ["I(X,Y)", it.strrounddp(IXY, 3), "Eq. 4.51"],
            ["H(noise)", it.strrounddp(HY - IXY, 3), "Eq. 4.63"]]

    pyplot.subplot(2, 1, 2)
    pyplot.title('Calculated Values')
    pyplot.axis('off')
    pyplot.table(cellText=ents,
                 colLabels=["Entity", "Bits", "Reference"],
                 colLoc='center',
                 loc='best')

    pyplot.show()

if __name__ == "__main__":
    main()
