
# This class does all the parsing and calling of libraries, while the solver takes care of the commandline input parameters.
# The InputOutput can:
# - parse instance into graph for htd
# - call htd, get TD with post-order for traversal, and all necessary information
# - change TD to match initial instance (e.g. have arguments a,b,c instead of 1,2,3)
import subprocess
import os
import ast

class InputOutput:
    instance_lp = []
    
    @classmethod
    def setInstance(cls, instance):
        f = open(instance,"r")
        for line in f:
            cls.instance_lp.append(line)

    @classmethod
    def getProbabilities(cls):
        probArgs = {}
        probAttacks = {}
        for line in cls.instance_lp:
            # Check if the line contains a 'p()' predicate
            if "p(" in line and not "%" in line:
                parts = line.strip("p().\n").split(',')
                # Normalize probability
                normalized_prob = parts[-1]
                if len(parts) == 2:  # Argument probabilities
                    probArgs[parts[0]] = normalized_prob
                elif len(parts) == 4:  # Attack probabilities
                    probAttacks[parts[1]+"-"+parts[2]] = normalized_prob
        return probArgs, probAttacks
    
    @classmethod
    def extract_extension(cls):
        ext = {}
        for line in cls.instance_lp:
            if "extension(" in line and not "%" in line:
                ext[line.strip("extension().\n")] = 'in'
        return ext