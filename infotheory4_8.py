"""Python (v2.7) code to accompany book:  Information Theory by JV Stone, 2015.
File: infotheory4_8.py.
Author: John De Pledge.
Copyright: 2015, JV Stone, Psychology Department, Sheffield University,
                    Sheffield, England.
This code can be downloaded from
    http://jim-stone.staff.shef.ac.uk/BookInfoTheory/InfoTheoryPython.html
Creative Commons License (http://creativecommons.org/licenses/by-nc/4.0/).
You are free to share and adapt for non-commercial purposes only.

Summary: We show the binary images of Figures 4.8a & 4.8b, generate the joint probability
table and calculate the entropy values.  The actual values will
vary from run to run as we are generating the probability data using
random numbers.

Eq. 4.68	HX     = 0.850 bits
Eq. 4.71	HY     = 0.906 bits
Eq. 4.75	HXY    = 1.319 bits
Eq. 4.78	IXY    = 0.437 bits
Eq. 4.81	H(X|Y) = 0.415 bits
Eq. 4.84	H(Y|X) = 0.470 bits
Eq. 4.88	H(noise) = 0.469 bits
"""

import random
from matplotlib import pyplot
from PIL import Image
import information_theory as it

PNOISE = 0.1 # noise level added to binary image
SIGFIGS = 3

def main():
    """Main function for Python example for Fig. 4.8"""

    # Open the image
    image = Image.open("image1_6.jpg")

    # Get image size
    xsize, ysize = image.size

    # Load pixels
    pixels = image.load()

    # Make a black and white image from the original
    # Loop over all pixels if greyscale value > 150 make black, else white
    for row in range(ysize):
        for col in range(xsize):
            if pixels[col, row] > 150:
                pixels[col, row] = 255
            else:
                pixels[col, row] = 0

    pyplot.figure("Example 4.8", figsize=(10, 8))

    # Show the black and white image
    pyplot.subplot(2, 2, 1)
    pyplot.title("Original (input, X)")
    pyplot.imshow(image, cmap='gray')
    pyplot.axis('off')

    # Initialise the joint probability of input-->output (ref Table 4.3 P99)
    jointprob = [[0.0, 0.0], [0.0, 0.0]]

    # each occurrence of a particular outcome is equivalent to a small
    # probability increment.
    probability_increment = 1.0 / (xsize * ysize)

    # Loop over all pixels and changes its state with probability PNOISE
    for row in range(0, ysize):
        for col in range(0, xsize):
            if random.random() >= (1.0 - PNOISE):
                if pixels[col, row]:
                    pixels[col, row] = 0
                    jointprob[1][0] += probability_increment
                else:
                    pixels[col, row] = 255
                    jointprob[0][1] += probability_increment
            elif pixels[col, row]:
                jointprob[1][1] += probability_increment
            else:
                jointprob[0][0] += probability_increment

    # Show the noisy black and white image
    pyplot.subplot(2, 2, 2)
    pyplot.title("Noisy (output, Y)")
    pyplot.imshow(image, cmap='gray')
    pyplot.axis('off')

    col_total_probabilities = it.col_totals(jointprob)
    row_total_probabilities = it.row_totals(jointprob)

    allprobabilities = it.flatten(jointprob)

    # HX is the entropy of the input (original binary image)
    HX = it.entropy_from_probabilities(row_total_probabilities)

    # HY is the entropy of the output (noisy binary image)
    HY = it.entropy_from_probabilities(col_total_probabilities)

    # HXY is the entropy of the joint distribution
    HXY = it.entropy_from_probabilities(allprobabilities)
    
    # IXY = mutual information between input and output
    IXY = HX + HY - HXY    # Eq 4.76

    # Analytic value for noise Eq. 4.88
    noise = sum([p * it.log2(1.0 / p) for p in [PNOISE, 1.0 - PNOISE]])

    # Prepare the probability table for display
    tdat = [["Input=0",
             it.strrounddp(jointprob[0][0], SIGFIGS),
             it.strrounddp(jointprob[0][1], SIGFIGS),
             it.strrounddp(jointprob[0][0] + jointprob[0][1], SIGFIGS)],
            ["Input=1",
             it.strrounddp(jointprob[1][0], SIGFIGS),
             it.strrounddp(jointprob[1][1], SIGFIGS),
             it.strrounddp(jointprob[1][0] + jointprob[1][1], SIGFIGS)],
            ["Totals",
             it.strrounddp(jointprob[0][0] + jointprob[1][0], SIGFIGS),
             it.strrounddp(jointprob[0][1] + jointprob[1][1], SIGFIGS),
             it.strrounddp(sum(jointprob[0]) + sum(jointprob[1]), SIGFIGS)]]

    pyplot.subplot(2, 2, 3)
    pyplot.title('Joint Probabilities')
    pyplot.axis('off')
    pyplot.table(cellText=tdat,
                 colLabels=["State", "Output=0", "Output=1", "Totals"],
                 colLoc='center',
                 loc='best')

    # Prepare the calculated entropy/MI/noise table for display
    ents = [["H(X)", it.strrounddp(HX, SIGFIGS), "Eq. 4.68"],
            ["H(Y)", it.strrounddp(HY, SIGFIGS), "Eq. 4.71"],
            ["H(X,Y)", it.strrounddp(HXY, SIGFIGS), "Eq. 4.75"],
            ["I(X,Y)", it.strrounddp(IXY, SIGFIGS), "Eq. 4.78"],
            ["H(X|Y)", it.strrounddp(HX - IXY, SIGFIGS), "Eq. 4.81"],
            ["H(Y|X)", it.strrounddp(HY - IXY, SIGFIGS), "Eq. 4.84"],
            ["H(noise)", it.strrounddp(noise, SIGFIGS), "Eq. 4.88"]]

    pyplot.subplot(2, 2, 4)
    pyplot.title('Calculated Values')
    pyplot.axis('off')
    pyplot.table(cellText=ents,
                 colLabels=["Entity", "Bits", "Reference"],
                 colLoc='center',
                 loc='best')

    pyplot.show()

if __name__ == "__main__":
    main()
