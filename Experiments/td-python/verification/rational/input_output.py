
# This class does all the parsing and calling of libraries, while the solver takes care of the commandline input parameters.
# The InputOutput can:
# - parse instance into graph for htd
# - call htd, get TD with post-order for traversal, and all necessary information
# - change TD to match initial instance (e.g. have arguments a,b,c instead of 1,2,3)
import subprocess
import os
import ast
import re
class InputOutput:

    order_args = {}
    instance_lp = []
    arguments_digits = {}
    attacks_digits = []
    traversal_section = ""
    machine_td_section = ""

    traversal = [] #traversal in array format - includes parents, not children.
    children_relations = [] #infer these from parents that are returned from htd, and available in "traversal".
    traversal_dict = {} #transformed into a dictionary so faster access e.g. to children - includes children, not parents.

    @classmethod
    def args_char_to_digit(cls, instance):
        digit = 1  # Start mapping from digit 1
        f = open(instance,"r")
        count = 0
        for line in f:
            cls.instance_lp.append(line)

            if 'arg(' in line and not "%" in line: # Check if the line contains 'arg'
                #argument = line.split('arg(')[1].split(')')[0]   # Extract the argument between parentheses
            
                #argument = re.search(r'arg\(([^)]+)\)', line).group(1)
                match = re.search(r'arg\(([^)]+)\)', line)
                #print("match ", match.group(1))
                if match:
                    argument = str(match.group(1))
                    if argument not in cls.arguments_digits:   # If the argument is not already in the mapping, add it
                        cls.arguments_digits[argument] = digit
                        digit += 1
                count += 1
                if count == 5:
                    print(cls.arguments_digits)

        
        return cls.arguments_digits

    @classmethod
    def attacks_char_to_digit(cls, instance):
        with open(instance, "r") as f:
            for line in f:
                if 'att(' in line and  "%" not in line: # Check if the line contains 'att'
                    args = line.split('att(')[1].split(')')[0] # Extract the arguments between parentheses
                    attack = args.split(',') # Split the arguments by comma
                    #print("attack 0", attack[0])
                    #print("attack 0", attack[1])

                    cls.attacks_digits.append([cls.arguments_digits[attack[0]],cls.arguments_digits[attack[1]] ]) # Add the attack as a list [a, b] to the attacks array
        #print("cls.attackdigits", cls.attacks_digits)
        
        return cls.attacks_digits

    @classmethod
    def getarguments_digits(cls):
        return cls.arguments_digits

    @classmethod
    def getattacks_digits(cls):
        return cls.attacks_digits

    # gets input from an .lp file, in the format of a primal graph.
    @classmethod
    def to_htd_format(cls, nArgs, nAtts):
        instance = "p tw "+str(nArgs)+" "+ str(nAtts) +"\n"
        for attack in cls.attacks_digits:
            instance += str(attack[0]) +" " + str(attack[1]) + "\n"

        #print("htd instance", instance)
        return instance
    
    @classmethod
    def call_htd(cls, grInstanceString):
        filename = "temp"
        file = open(filename, "w")
        file.write(grInstanceString)
        file.close()    
        command = "/home/andreipopi/Documents/GitLab/praaf-tree-decomposition/Experiments/td-python/verification/rational_efficient_join/htd-binary/linux/htd_main-1.2.0 < temp"
        process = subprocess.Popen(command, shell = True, stdout= subprocess.PIPE)
        output = str(process.communicate()[0], "utf-8") #the output is in process.communicate()[0] and we need it in utf-8 for parsing       
        if os.path.exists(filename):
            os.remove(filename)
        return output
    
    #get the string output from htd
    @classmethod
    def extract_sections(cls, input_text):
        # Identifiers for each section
        traversalStart = "Traversal"
        humanTdStart = "Human Tree Decomposition"
        #machineTdStart = "Machine Tree Decomposition"
        # Find the start indices of each section
        traversalIndex = input_text.find(traversalStart)
        humanTdIndex = input_text.find(humanTdStart)
        # Extract each section
        cls.traversal_section = input_text[traversalIndex:-1]
        cls.humanTdSection = input_text[humanTdIndex:traversalIndex]
        #print(cls.humanTdSection)
        #cls.machine_td_section = input_text[machineTdIndex:traversalIndex]
        return cls.traversal_section

    def str_to_list(s):
    # Converts a string representation of a list into a Python list
        if s == '[]' or s == '' or s ==None:
            return []
        else:
            return ast.literal_eval(s)

    # get the traversal as string output from htd and put it in an array format "cls.traversal", and then in a dictionary format "cls.traversal_dict"
    @classmethod
    def stringTraversalToDict(cls):
        lines_traversal =[]
        for line in cls.traversal_section.split("\n"):
            lines_traversal.append(line)
        del lines_traversal[0] #remove first line which just says "Traversal"
    
        #print(cls.traversal_section)
        for line in lines_traversal:
            line_as_array = line.split(" ")
            cls.traversal.append(line_as_array)
        #print(cls.traversal)

        for item in cls.traversal:
            cls.children_relations.append([int(item[0]),int(item[-1])])

       # print("children_relations", cls.children_relations)
        for item in cls.traversal:
            
            key = int(item[0])
            value = []
            value.append(cls.str_to_list(item[1]))
            value.append(item[2])

            if item[2] == "intro" or item[2] == "rem": #if it is a remove or introduced node, then 
                value.append(cls.str_to_list(item[3])) #list of removed or introduced
                if "edges" in item:
                    value.append(item[4]) #edges
                    value.append(cls.str_to_list(item[5])) #appen the list of edges if there
                    #print(type(item[5]))
                    #print("item5", item[5])
                    if item[5] == str([]): #when using the htd without join, a weird node is created that is a leaf
                                           #also for some reason, in an introduce node an attack for a bag that already includes both edges is not visible until later in the path decomposition
                        edges = []
                        for edge in cls.attacks_digits:
                            #print("edge", edge, type(edge))
                            #print(type(item[1]))
                            if edge[0] in value[0] and edge[1] in value[0]:
                                edges.append(edge)
                        value[-1] = edges
            else:
                if item[2] == 'join': #then we need to check for edges, which are one position before because we have no removed/intro elements
                    if "edges" in item:
                        value.append(item[3]) #edges
                        value.append(cls.str_to_list(item[4])) #appen the list of edges if there
                        #somehow it can happen that htd postoponsed inferring the edges, so 
                        #we need to compute them ourselves
                        

                        if item[5] == []:
                            edges = []
                            for edge in cls.attacks_digits:
                                if edge[0] in item[1] and edge[1] in item[1]:
                                    edges.append[edge]
                            value[-1] = edges

                           
                #else: #nothing, this means its a leaf or root, and these are empty
            cls.traversal_dict[key] = value

            #add children to traversal
            children =[]
            for relation in cls.children_relations:
                if relation[1] == key: 
                    children.append(int(relation[0])) #then the first element is a child
            value.append("children")
            value.append(children)
        #NOTETOSELF: the last remove node in the traversal, is actually the root.


    # transform the traversal we previously saved in a dictionary, in such a way that has literals for arguments instead of digits.
    @classmethod
    def digitsToLiterals(cls, dict):

        #print("so far", cls.traversal_dict)
        for key,value in cls.traversal_dict.items():
            bagArguments = []
            for arg in value[0]:
                bagArguments.append(next(k for k,v in cls.arguments_digits.items() if v==arg))
            cls.traversal_dict[key][0] = bagArguments

            #print("bag arguments", bagArguments)
            if value[1] == "intro" or value[1] == "rem":
                intrRemArguments = []
                for arg in value[2]:
                    intrRemArguments.append(next(k for k,v in cls.arguments_digits.items() if v==arg))
                cls.traversal_dict[key][2] = intrRemArguments
                if "edges" in value: #then we know this was pos 3, and we need to change pos 4 with literals
                    edgeArgs = []
                    for edge in value[4]:
                        edgeArgs.append([next(k for k,v in cls.arguments_digits.items() if v==edge[0]), next(k for k,v in cls.arguments_digits.items() if v==edge[1]) ])
                    cls.traversal_dict[key][4] = edgeArgs

            else: #if join then there might be edges 
                    if "edges" in value: #then we know this was pos 3, and we need to change pos 4 with literals
                        edgeArgs = []
                        for edge in value[3]:
                            edgeArgs.append([next(k for k,v in cls.arguments_digits.items() if v==edge[0]), next(k for k,v in cls.arguments_digits.items() if v==edge[1]) ])
                        cls.traversal_dict[key][3] = edgeArgs
       
        return
               
    @classmethod
    def printDictionary(cls, dict):
        for key,value in dict.items():
            print(key, value)

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
    def getTraversalDict(cls):
        return cls.traversal_dict
    
    @classmethod
    def init_ordering(cls):
        significance = len(cls.prob_args)
        #print("significance", significance)
        for key,value in cls.prob_args.items():
            cls.order_args[key] = significance
            significance -= 1
        #print("ordering", cls.order_args)

    @classmethod
    def extract_extension(cls):
        ext = {}
        for line in cls.instance_lp:
            if "extension(" in line and not "%" in line:
                ext[line.strip("extension().\n")] ='in'
        return ext
        