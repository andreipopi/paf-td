# python probableSolver.py instance.lp
from ast import arguments
from monolithic_ver import Monolithic
from input_output import *
from itertools import chain, combinations

import sys

def process_input_output(instance):
    InputOutput.setInstance(instance)
    prob_args, prob_attacks = InputOutput.getProbabilities()
    
    #print("probArgs", prob_args, "probattack", prob_attacks)

    #print("-------------------------------------------------------")

    return prob_args, prob_attacks

if len(sys.argv) == 1:
    print("-----------------------MonolithicSolver-----------------------")
    print("Try passing an .lp instance!")
else:
    #INPUT OUTPUT-------------------------
    #GET INSTANCE TO htd FORMAT
    instance = sys.argv[1]
    prob_args, prob_attacks = process_input_output(instance)

    extension = InputOutput.extract_extension()
    rows, P = Monolithic.verify(prob_args, prob_attacks, extension)
    for row in rows:
        print(row)
    
    print("RESULT: ", P)

    
    


