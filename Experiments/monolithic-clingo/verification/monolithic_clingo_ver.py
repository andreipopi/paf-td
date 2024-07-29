#ß ßThis py script calls "monolithic" econdings and computes solutions to various problems,
# on top of the enumartion of solutions given by the encoding.

import sys
import subprocess
from subprocess import*
import re


instance = sys.argv[1]


process = subprocess.Popen(["clingo", "encoding_COM_ver.lp", instance, "0"], stdout = subprocess.PIPE)
output = str(process.communicate()[0], "utf-8") #the output is in process.communicate()[0] and we need it in utf-8 for parsing
output = str(output.partition("Solving...")[2]) #get what comes after "Solving..."
print("output->",output)
output = re.sub('\n', '', output) #substitute \n with commas
output = str(output.replace("'",''))
output= str(output.replace("[", ''))
output = output.split(sep='Answer: ')
#output = re.sub('\n', '', output) #substitute \n with commas



arg_pattern = r'a\((.*?)\)'
atck_pattern = r'atck\((.*?)\)'
res_pattern = r'res\((.*?)\)'
in_pattern = r'in\((.*?)\)'
def_pattern = r'def\((.*?)\)'

#print(output.split(sep=','))
#list_output = output.split(sep=',')


# P-EXTsem(S)
solutions = []
Sum =0
for row in output:
    print(row)
    if row != '':
        args_in_subgraph = re.findall(arg_pattern,row)
        attacks_in_subgraph = re.findall(atck_pattern,row)
        res_in_subgraph = [f"res({elem})" for elem in re.findall(res_pattern, row)]
        inargs = [f"in({elem})" for elem in re.findall(in_pattern,row)]
        defargs =[f"def({elem})" for elem in  re.findall(def_pattern, row)]
        sol = args_in_subgraph+attacks_in_subgraph+inargs+defargs+res_in_subgraph
        if sol!= []:
            solutions.append(sol)
            res_number = int(row.split('res(')[1].split(')')[0])
            # Add the extracted number to the sum
            Sum += res_number
        print(sol)
# END P-EXTsem(S)


print("Solutions: "+ str(len(solutions)))
print("RESULT: "+ str(Sum))


#print(output.splitlines())
#print(output)
#output = re.sub(' ', '', output) #remove blanks
#output = re.sub('\n', ',', output) #substitute \n with commas
#output_as_array = output.split(sep=',') #['', 'UNSATISFIABLE', '', 'Models:0', 'Calls:1', 'Time:0.001s(Solving:0.00s1stModel:0.00sUnsat:0.00s)', 'CPUTime:0.001s', '']

#newoutput=output.split(sep=',')
#print(newoutput)

#models = next(x for x in output_as_array if 'Models:' in x) #Models:0

#output = list(filter(None, output)) #removed empty strings from the output


#print(output)