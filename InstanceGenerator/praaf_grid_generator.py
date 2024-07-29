import sys
import random
import os

# What do we need to generate?
# We need instances in the "classical" asp predicate format
# as a primal graph. Something like:
#arg(a).
#arg(b).
#arg(c).
#p(a,1).
#p(b,1).
#p(c,0.9).
#%we need ids for the attacks in the iterative multiplication, in the D-FLAT/Clingo approach.
#p(1,a,c,0.4).
#p(2,c,a,1).
#p(3,b,c,0.8).
#p(4,c,b,0.4).
#att(a,c).
#att(c,a).
#att(b,c).
#att(c,b).
#query(a).
#extension(a).
#extension(b).
#this instance can be directly use by
# -ClingoSystem
# -DFLATSystem
# -and is the format parsed by the input_output.py in PythonSystem

arguments = []
attacks = []

prob_args = []
prob_attacks = []

grid = [] # grid used to select attacks and stuff.
framework = [] # the framework created in lp format.
 
#METHODS
def initialise(n_total_sentences):
    args = ["a" + str(i) for i in range(n_total_sentences)]
    #contraries = {asmpt: random.choice(atoms+assumptions) for asmpt in assumptions}
    print("Arguments: ",args)
    return args

def create_grid(k,n):
    grid_content = arguments.copy()
    random.shuffle(grid_content)
    index = 0
    for _ in range(0, n):
        row = []
        for _ in range(0, k):
            row.append(grid_content[index])
            index = index + 1
        grid.append(row)
    return grid

def print_grid(grid):
    print()
    print("Grid")
    for row in grid:
        print(row,"\n")
    print()
    return

#i,j is the position of current
#direction is "up" "down" "left" or "right"
def neighbourhood(i, j, direction, size):
    max_rows = len(grid)
    max_cols = len(grid[0]) if max_rows > 0 else 0
    neighbours = []

    if direction == 'up':
        for k in range(1, size + 1):
            if i - k >= 0:  #ensure not moving above the grid
                neighbours.append(grid[i - k][j])
            else:
                break  #went above the top edge of the grid, so stop adding neighbors

    elif direction == 'down':
        for k in range(1, size + 1):
            if i + k < max_rows:  #ensure not moving below the grid
                neighbours.append(grid[i + k][j])
            else:
                break  #went below the bottom edge of the grid, so stop adding neighbors

    elif direction == 'left':
        for k in range(1, size + 1):
            if j - k >= 0:  #ensure not moving to the left of the grid
                neighbours.append(grid[i][j - k])
            else:
                break  #went to the left of the left edge of the grid, so stop adding neighbors

    elif direction == 'right':
        for k in range(1, size + 1):
            if j + k < max_cols:  #ensure not moving to the right of the grid
                neighbours.append(grid[i][j + k])
            else:
                break  #went to the right of the right edge of the grid, so stop adding neighbors
    return neighbours


def create_framework(n, k):
    
    directions = {1: 'up', 2:'down', 3:'left', 4:'right'}
    prob_args = {}
    prob_attacks = {}


    prob_args_asp = {}
    prob_attacks_asp = {}

    p_being_attacked = 0.5
    probabilities = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    weights = [4]* 9 + [1]

    probabilities_asp = {'0.1': 1000, '0.2': 2000, '0.3':3000, '0.4': 4000, '0.5':5000, '0.6': 6000, '0.7': 7000,  '0.8':8000, '0.9':9000, '1':10000}

    p_being_picked_in_extension = 0.12
    query = ''
    extension = {}

    id_atck = 0
    for i in range(0, n):
        for j in range(0, k):
            #arg_probability = random.sample(probabilities,1)[0]
            arg_probability = random.choices(probabilities, weights, k=1)[0]

            prob_args[grid[i][j]] = arg_probability
            prob_args_asp[grid[i][j]] = probabilities_asp[str(arg_probability)]

            being_attacked = random.random() < p_being_attacked 
            select_in_extension = random.random() < p_being_picked_in_extension
            
            if select_in_extension:
                extension[grid[i][j]] = 'in'
            
            if being_attacked:
                #atck_probability = random.sample(probabilities,1)[0]
                atck_probability = random.choices(probabilities, weights, k=1)[0]

                atck_probability_asp = probabilities_asp[str(atck_probability)]


                pick = random.sample(range(1,5),1)[0]
                selection_set = neighbourhood(i,j,directions[pick],4)
                if selection_set != []:
                    attacker = random.sample(selection_set,1)[0]
                    prob_attack = [attacker, grid[i][j], atck_probability]
                    prob_attack_asp = [attacker, grid[i][j], atck_probability_asp]
                    attack = [attacker, grid[i][j]]
                    prob_attacks[id_atck] = prob_attack
                    prob_attacks_asp[id_atck] = prob_attack_asp
                
                    attacks.append(attack)
                    id_atck += 1
    flattened_grid = [item for sublist in grid for item in sublist]
    query = random.sample(flattened_grid,1)[0] 
                    
    return prob_args, prob_args_asp, prob_attacks, prob_attacks_asp, attacks, query, extension


def create_instance_file(arguments, pargs, pargs_asp, attacks, patts, patts_asp, query, extension, out_filename):
    """
    Print the given framework in ASP format.
    """
    print("out filnemae", out_filename)
    if not os.path.exists(os.path.dirname("generated_instances/")):
        os.makedirs(os.path.dirname("generated_instances/"))

    
    with open("generated_instances/"+out_filename, 'w') as out:
        for arg in arguments:
            out.write("arg(" + arg + ").\n")
        for arg, parg in pargs.items():
            out.write("p(" + str(arg) +","+ str(parg)+ ").\n")
        for att in attacks:
            out.write("att("+str(att[0])+","+att[1]+").\n")
        for at, patt in patts.items():
            out.write("p(" + str(at) + "," + patt[0] + ","+ patt[1]+","+ str(patt[2])+").\n")
        for elem in extension:
            out.write("extension("+elem+").\n")
        out.write("query(" + str(query) + ").")
    out.close()

    if not os.path.exists(os.path.dirname("generated_instances_asp/")):
        os.makedirs(os.path.dirname("generated_instances_asp/"))

    with open("generated_instances_asp/"+out_filename, 'w') as out:
        for arg in arguments:
            out.write("arg(" + arg + ").\n")
        for arg, parg in pargs_asp.items():
            out.write("p(" + str(arg) +","+ str(parg)+ ").\n")
        for att in attacks:
            out.write("att("+str(att[0])+","+att[1]+").\n")
        for at, patt in patts_asp.items():
            out.write("p(" + str(at) + "," + patt[0] + ","+ patt[1]+","+ str(patt[2])+").\n")
        for elem in extension:
            out.write("extension("+elem+").\n")
        out.write("query(" + str(query) + ").")
    out.close()
    
    

# main()
k = int(sys.argv[1])
n = int(sys.argv[2])
id_instance = int(sys.argv[3])

n_sentences = k * n #arguments in the grid

print()
print("total n arguments: ", n_sentences )

arguments = initialise(n_sentences)

create_grid(k,n)
print_grid(grid)
p1, p1_asp, p2, p2_asp, att, q, ext = create_framework(n,k)
print("prob args", p1)
print("prob attacks", p2)
print("attacs", att)
print("extension", ext)
print("query", q)

create_instance_file(sorted(arguments), p1, p1_asp, att, p2, p2_asp, q, sorted(ext), "k"+str(k)+"_"+"n"+str(n)+"_q"+str(q)+"_"+str(id_instance)+".lp")

