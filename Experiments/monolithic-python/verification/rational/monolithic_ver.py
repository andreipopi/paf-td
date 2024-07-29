import copy
from operator import pos
from itertools import combinations, chain, product
import re
from fractions import Fraction

# 1) create all possible subgraphs
# 2) for each subgraph create all possible complete extensions


class Monolithic:

    @classmethod
    def conflict_free(cls, graph, extension):
        for att in graph[1]:
            if att[0] in extension and att[1] in extension:
                return False
        return True

    @classmethod
    def verify(cls, prob_args, prob_attacks, extension):
        P = 0

        # [[G],[R],[I],[D],[U],P]
        possible_graphs = [[[],[],[],[],[],1]]

        for arg, prob in prob_args.items():
            new_rows = []
            if prob == '1':
                for graph in possible_graphs:
                    graph[0].append(arg)
            else:
                for graph in possible_graphs:
                    plus_arg = copy.deepcopy(graph)
                    plus_arg[0].append(arg)
                    new_rows.append(plus_arg)
            if new_rows != []:
                possible_graphs.extend(new_rows)

        for atck, pr in prob_attacks.items():
            new_rows = []
            a = atck.split("-")
            if pr == '1':
                for graph in possible_graphs:
                    if a[0] in graph[0] and a[1] in graph[0]:
                        graph[1].append([a[0],a[1]])
            else:
                for graph in possible_graphs:
                    plus_atck = copy.deepcopy(graph)
                    if a[0] in graph[0] and a[1] in graph[0]:
                        plus_atck[1].append([a[0],a[1]])
                        new_rows.append(plus_atck)
                if new_rows != []:
                    possible_graphs.extend(new_rows)

        #print(len(possible_graphs), " subgraphs")
        for graph in possible_graphs:
            prob = Fraction(graph[5])
            for arg, p in prob_args.items():
                if arg in graph[0]:
                    prob = prob * Fraction(p)
                else:
                    prob = prob *( 1 - Fraction(p))
            for atck, patt in prob_attacks.items():
                a = atck.split("-")
                attack = [a[0],a[1]]
                if attack[0] in graph[0] and attack[1] in graph[0]:
                    if attack in graph[1]:
                        prob = prob *Fraction(patt)
                    else:
                        prob = prob *(1- Fraction(patt))
            graph[5] = prob

        #-------------------------------

       #guesses of labellings 
        new_rows =[]
        P = 0
        for row in possible_graphs:
            arguments_present = [arg for arg in prob_args.keys() if arg in row[0]]
            rowstoadd = [[[],[],[]]]
            for arg in arguments_present:
                withnewarg=[]
                for r in rowstoadd:
                    newrI=copy.deepcopy(r)
                    newrD=copy.deepcopy(r)
                    newrU=copy.deepcopy(r)
                    if arg not in newrI[0]:
                        newrI[0].append(arg)
                        withnewarg.append(newrI)
                    if arg not in newrD[0]:
                        newrD[1].append(arg)
                        withnewarg.append(newrD)
                    if arg not in newrU[0]:
                        newrU[2].append(arg)
                        withnewarg.append(newrU)
                rowstoadd =[]
                rowstoadd.extend(withnewarg)
            #print("-------",row)

            for e in rowstoadd: #find a complete extension if yes count graph in
                matching_extension = True
                for x in extension.keys():
                    if x in row[0]:
                        if x not in e[0]:
                            matching_extension = False
                    else:
                        matching_extension = False

                for x in row[0]:
                    if x not in extension.keys():
                        if x in e[0]:
                            matching_extension = False
                
                if matching_extension:
                    if cls.conflict_free(row, e[0]):
                        all_true_defeated = cls.check_defeated(row[1], e)

                        all_true_undec = True
                            
                        all_true_undec = cls.check_undec(row[1], e)
                        
                        #cant be in but attacked by an undec.
                        in_but_attacked_by_undec = False
                        if e[2] != []:
                            for attack in row[1]:
                                if attack[1] in e[0] and attack[0] not in e[2]:
                                    in_but_attacked_by_undec = True
                        
                        if all_true_defeated and all_true_undec:
                            #print(e)

                            not_adm = False
                            for attack in row[1]:
                                if attack[1] in e[0] and attack[0] not in e[1]:
                                    not_adm = True
                            #print("notadm", not_adm)
                            #print("notdinbutdunde", in_but_attacked_by_undec)
                            if not not_adm and not in_but_attacked_by_undec:
                                #print("count this subgrah: ", row )
                                #print(e)
                                P = P + Fraction(row[5])
                                break #this is extremely ugly

        #print("RESULT: ", P)

        return possible_graphs, P
    
    @classmethod
    def check_defeated(cls, attacks, e):
        for arg in e[1]: #must be attacked by some in
            attacked_by_in = False
            for att in attacks:
                if att[1] == arg and att[0] in e[0]:
                    attacked_by_in = True
            if not attacked_by_in:
                return False
        return True

    @classmethod
    def check_undec(cls, attacks, e):

        attbundec = True
        notattbin = True
        for arg in e[2]: #must be attacked by some undec
            attacked_by_undec = False
            for att in attacks:
                if att[1] == arg and att[0] in e[2]:
                    attacked_by_undec = True
            if not attacked_by_undec:
                attbundec = False

        for arg in e[2]: #not attacked by in
            for att in attacks:
                if att[1] == arg and att[0] in e[0]:
                    notattbin = False
        if attbundec and notattbin:
            return True
        
                