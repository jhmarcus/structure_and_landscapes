"""
Implementation of Stuart Kauffman's NK Model.

Genomes are bitstrings of length "n".
The number of epistatic neighbors of a loci is denoted "k".

When k = 0, the adaptive landscape is smooth.
When k = n - 1, the landscape is maximally rugged.

Every locus in the bitstring has a respective function requiring
the state of the locus and its "k" neighbors (those immediately
following with wrapping about ends).

The outcome of each function is drawn from a  uniformly
distribution. The mean contribution of each locus is the fitness.
"""
from random import Random
module_random_generator = Random()


class NKModel(object):
    """
    Class which is used to evaluate the fitness of a bitstring.
    """
    def __init__(self, n=2, k=0, random_generator=module_random_generator):
        """
        NKModel instances default to a simple smooth landscape (n=2, k=0),
        and using the module's random number generator (seeded by time).
        """
        self.n = n
        self.k = k
        self.random_generator = random_generator
        self._contribution_lookup = contribution_lookup_table(self.n, self.k, self.random_generator)

    def _initialize_contribution_lookup(self):
        """
        Fitness is the mean of the contribution of each loci.
        Each loci has its own lookup table composed of 2^(k+1) uniformly
        distributed entries corresponding to the numerical value of the
        subbitstring (locus + k neighbors).
        """
        self._contribution_lookup = [
            [random_generator.random() for _ in range(2 ^ (self.k + 1))]
            for _ in range(self.n)]


def contribution_lookup_table(n, k, random_generator=module_random_generator):
    return [[random_generator.random() for _ in range(2 ^ (k + 1))]
            for _ in range(n)]
