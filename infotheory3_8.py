"""Python (v2.7) code to accompany book:  Information Theory by JV Stone, 2015.
File: infotheory3_8.py.
Author: John De Pledge.
Copyright: 2015, JV Stone, Psychology Department, Sheffield University,
                    Sheffield, England.
This code can be downloaded from
    http://jim-stone.staff.shef.ac.uk/BookInfoTheory/InfoTheoryPython.html
Creative Commons License (http://creativecommons.org/licenses/by-nc/4.0/).
You are free to share and adapt for non-commercial purposes only.

Summary: This code is an annotated version of Clement Pit_claudel's code
at "http://pit-claudel.fr/clement/blog/
   an-experimental-estimation-of-the-entropy-of-english-in-
   50-lines-of-python-code/#more-691
   This method is slightly different from the method in the book, but the entropy estimates are similar for large samples.

Produces  entropy for model order = 1 for romeo.txt of 3.463bits"""

# Copyright (C) 2013, Clement Pit--Claudel (http://pit-claudel.fr/clement/blog)
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import codecs
import random
import re
import textwrap
from collections import defaultdict, deque, Counter
import information_theory as it

def main():
    """Main function for 3.8 example"""

    model_order = 3
    sample_size = 300
    
    filename = "romeo.txt"

    # The entropy of characters
    model = markov_model(chars(filename), model_order)

    print "Letter Entropy:", entropy_rate(model), ' bits/letter.'
    print 'Model order = ', model_order

    #
    # Output the a random sample text generated from the input sample
    # Format it as a block of chars width 70 (default for
    # textwrap.fill()
    print 'Model letter output:'
    print textwrap.fill("".join(generate(model, sample_size)))

    #
    # The entropy of words
    #
    model = markov_model(words(filename), model_order)

    print "\n\n"
    print "Word Entropy = :", entropy_rate(model), ' bits/word.'
    print "Model order", model_order

    #
    # Output the a random sample text generated from the input sample
    # Format it as a block of chars width 70 (default for
    # textwrap.fill()
    print 'Model word output:'
    print textwrap.fill(" ".join(generate(model, 100)))

def markov_model(stream, model_order):
    """Function counts the frequency of all distinct strings in the stream
    beginning with a prefix of length model_order.  It returns a list of
    counters."""

    #
    # Initialise our Counters.
    # model is a dictionary mapping (n?1)-character prefixes to a Counter;
    # that Counter maps each possible nth character to the number of times
    # this character followed the (n?1)-character prefix.
    # For example, model could be
    # model = {
    #          ('w', 'h'): {'y':25, 'o':12, 'a':16, ...},
    #          ('t', 'h'): {'i':15, 'a':18, 'e':34, ...},
    #          ...
    #         }

    # Making model a defaultdict (as opposed a simple dict, like model = {} )
    # means that we can just increment its count without first checking
    # if a key value exists.

    model = defaultdict(Counter)

    #
    # Create a queue for appending each token we read.  We are using the deque
    # as a pipe of length model_order.
    # We add to the pipe by appending to it.
    #
    # Pipe State     Append
    # <empty>        D
    # D              O
    # DO             G
    # DOG            G
    # OGG            E
    # GGE            D
    # GED            etc.

    pipe = deque(maxlen=model_order)

    for token in stream:
        #
        # If the pipe holds model_order characters, then store it contents.
        #
        if len(pipe) == model_order:

            # Convert the pipe contents to something hashable, which can then
            # used as a dict key.  Do this with the tuple() function
            model[tuple(pipe)][token] += 1

        pipe.append(token)

    return model


def tokenize(file_path, tokenizer):
    """A generator function reads in the file at file_path and uses the passed
    tokenizer function to yield tokens.  Generator functions are 'lazy'.  They
    only do what work they have to do to yield the next value.  This means
    large files are handled with little memory use.

       Arguments:
            file_path:  string.  The path to the file to read in.
            tokenizer: function.  A function to split up the data into
                tokens
       returns:
            token:  the next token in the input"""

    # Open the file for reading.
    # break down each line in the file into tokens and yield them one at a
    # time.
    with codecs.open(file_path, mode="r", encoding="utf-8") as infile:
        for line in infile:
            for token in tokenizer(line.lower().strip()):
                yield token


def append_space(text):
    """Appends a space to a string"""

    return text + " "


def chars(file_path):
    """A function to read in data from a file and convert it to
    single characters
       Arguments:
            file_path:  string.  The path to the file to read in.
       returns:
            token:  the next character in the input"""

    #
    # tokenize will open and read file_path.  For each line it will
    # append a space and return its contents one character at a time.
    #
    return tokenize(file_path, append_space)


def break_into_words(text):
    """Function will break the text into words"""

    return re.findall(r"[a-zA-Z']+", text)


def words(file_path):
    """A function to read in data from a file and convert it to
    words
       Arguments:
            file_path:  string.  The path to the file to read in.
       returns:
            token:  the next word in the input"""

    #
    # tokenize will open and read file_path.  For each line it will
    # break the line into words and return them one at a time.
    #
    return tokenize(file_path, break_into_words)


def entropy_rate(model):
    """Calculates the average entropy of the model data.  Does this by
    calculating the entropy for each prefix and weighting it by the
    frequency with which the prefix appears."""

    # Initialise counts
    total_freq = 0
    weighted_entropy = 0

    # Loop for all prefixes
    for prefix in model:
        # The square brackets denote a list comprehension, which is read from
        # left to right.
        # In words : "Make a list of the frequencies for
        # each item beginning with prefix.
        freqs = [freq for freq in model[prefix].values()]

        # Calculate the total frequency of all tokens beginning with
        # this prefix
        prefix_freq = sum(freqs)

        # Increment the total frequency for the whole model
        total_freq += prefix_freq

        # Calculate the weighted entropy from this prefix.
        weighted_entropy += prefix_freq * it.entropy_from_frequencies(freqs)

    # Calculate the average entropy across all the prefix distributions
    return weighted_entropy / total_freq


def generate(model, length):
    """A function to create a random sample of length tokens (a token could be
    a word or character).
    After each iteration we modify the seed/state
    by removing the first element of the token and appending a random prefix
    from our model based on the new value of state."""

    text = []

    # Pick a random seed as a start point
    # e.g. For words with a prefix length of 3, this could be
    # "of each organic"
    prefix = seed(model)

    # Loop building up text
    for _ in range(length):

        # Store the first word/char of the current state
        # In our example, would be 'of' for first pass in our example
        text.append(prefix[0])

        # Pick a new word to append to the current prefix.  The pick function
        # looks at the distribution of words/chars starting with prefix
        # and picks one at random from the distribution
        # For example, or new prefix now drops the 'of' and may become
        # "each organic compound".
        # Then loop with this new prefix.
        prefix = prefix[1:] + (pick(model[prefix]), )

    return text


def pick(counter):
    """Randomly pick from our counter, weighted by frequency"""

    # Calc size of counter - the total of the frequencies
    size = sum(counter.values())
    if size <= 0:
        print counter
        raise ValueError("No frequency values in passed counter")

    # Pick a random element as a target
    target = random.randint(1, size)

    # Step through the model unitil we reach/pass our target
    cumulative_frequency = 0
    for suffix, frequency in counter.items():
        cumulative_frequency += frequency

        # If we have reached our target, we are done
        if cumulative_frequency >= target:
            return suffix

    # If we get here we have not picked a suffix
    raise ValueError("Unable to obtain sample")


def seed(model):
    """Randomly pick a prefix from our model, weighted by frequency"""

    # Calc size of model
    size = sum([sum(p.values()) for p in model.values()])
    if size <= 0:
        raise ValueError("No frequency values in passed model")

    # Pick a random element
    target = random.randint(1, size)

    # Step through the model unitil we reach/pass our target
    cumulative_frequency = 0
    for prefix, possibles in model.items():
        cumulative_frequency += sum(possibles.values())

        # If we have reached our target, we are done
        if cumulative_frequency >= target:
            return prefix

    # If we get here, we have not found a seed.
    raise ValueError("Unable to obtain seed")


if __name__ == "__main__":
    main()
