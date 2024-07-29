# operating on the TD of the PRIMAL graph of problem instance.
from copy import copy
from heapq import merge
from itertools import chain, combinations
from tokenize import group
from input_output import *
import copy
from fractions import Fraction

import pandas as pd


class Algorithm:
    prob_args = []
    prob_attacks = []
    childrenList = []
    tables = {}
    
    float_rational = "float"

    # ideally, query for in, and optionally for def
    # if not in the labelling, the code explicitly requires an arg to be def or undecided
    # querying for "undec" has no effect
    #labelling = {'a':'in', 'b':'in'}
    labelling = {}
    #labelling = {'a':'in', 'b':'in', 'c':'def'}
    #labelling = {'a':'in', 'b':'in', 'c':'undec'}
    #labelling = {'a':'in', 'b':'in', 'c':'undec'}

    #    labelling = {'a':'in', 'b':'in', 'c':'undec'} has the same result of
    #    labelling = {'a':'in', 'b':'in', 'c':'def'} on the fazzinga instance
    # because the code does not enforce 'c':undec, if it would, there would be no result
    # instead, it basically just counts the extension where a in and b in, which is the one where c def,
    # and that is why the result for both of the above is 0.792

    @classmethod
    def leaf_node(cls):
        return [[[],[],[],[],[],[],[],1]] #[G, R, I, D, Cd, U, Cu, P]

    @classmethod
    def introduce_node(cls, bag_elems, intro_elem, edges, child_tab):
        """
        Description: creates a table for introduction nodes
        Parameters:
            edges (list): list of edges "in the bag" (already returned by htd)
            bag_elems (list): vertices in the bag
            intro_elem (list): introduced vertex; nice TD, so just one. e.g. ['a']
            child_tab (list): a list of lists containing the child rows
        Returns: returns table (list).
        """
        table = []
        prob_introduced = float(cls.prob_args[intro_elem[0]])
        
        for c_row in child_tab: #[[],[],[],[],[],[],[],1]
            graph_prime = copy.deepcopy(c_row[0]) #G'
            row = copy.deepcopy(c_row)# G',L',C',P'

            #print("intro elem 0", intro_elem[0])
            #G+A
            graph_prime.append(str(intro_elem[0]))

            #print("graph prime", graph_prime)

            if(cls.float_rational == "rational"):
                P = Fraction(c_row[-1]) * Fraction(cls.prob_args[intro_elem[0]]) # only arg contributed at this point
            else:
                P = float(c_row[-1]) * float(cls.prob_args[intro_elem[0]]) # only arg contributed at this point


            #[[G'+ a],[],[],[],[],[],[],1]
            potential_edges = cls.valid_for_contribution(graph_prime, edges, intro_elem)# CHECK 2 i.e. edges incident to introduced, and both ends in subgraph
            edge_guesses = list(cls.powerset(potential_edges))
            #print("potential edges:", potential_edges)
            edge_guesses = cls.check_edge_guesses(potential_edges, edge_guesses) # CHECK 3 remove guesses that didnt guess in attacks with P=1
            if edge_guesses != []:
                for e_guess in edge_guesses:
                    P_with_args = P
                    for pe in potential_edges:
                        if pe in e_guess:
                            if(cls.float_rational == "rational"):
                                P_with_args = P_with_args * Fraction(cls.prob_attacks[str(pe[0])+"-"+str(pe[1])])
                            else:
                                P_with_args = P_with_args * float(cls.prob_attacks[str(pe[0])+"-"+str(pe[1])])
                        else:
                            if(cls.float_rational == "rational"):
                                P_with_args = P_with_args * (1-Fraction(cls.prob_attacks[str(pe[0])+"-"+str(pe[1])]))
                            else:
                                P_with_args = P_with_args * (1-float(cls.prob_attacks[str(pe[0])+"-"+str(pe[1])]))

                    row_copy = copy.deepcopy(row) 
                    row_copy[0] = graph_prime #has been extended with introduced argument
                    row_copy[1].extend(list(e_guess))
                    row_copy[-1] = P_with_args

                    #row_copy[-1] = cls.format_float(P_with_args)
                    #print(row_copy)

                    #                       R           I
                    if cls.conflict_free(row_copy[1], row_copy[2], intro_elem[0]):

                        row_I_plus = copy.deepcopy(row_copy) 
                        row_I_plus[2].append(intro_elem[0])
                        defcheck_prime = row_I_plus[5]
                        row_I_plus[5] = cls.check_defeated(bag_elems, row_I_plus[1], row_I_plus[2], defcheck_prime )
                        #print(row_I_plus)
                        table.append(row_I_plus)


                    if intro_elem[0] not in cls.labelling.keys():
                        row_D_plus = copy.deepcopy(row_copy) 
                        row_D_plus[3].append(intro_elem[0])
                        defcheck_prime = row_D_plus[5]
                        row_D_plus[5] = cls.check_defeated(bag_elems, row_D_plus[1], row_D_plus[2], defcheck_prime )
                        #print(row_D_plus)
                        table.append(row_D_plus)

                    if intro_elem[0] not in cls.labelling.keys():

                        #if cls.labelling[intro_elem[0]] == 'undec':
                        #U+a
                        row_U_plus = copy.deepcopy(row_copy) 
                        row_U_plus[4].append(intro_elem[0])
                        undeccheck_prime = row_U_plus[6]
                        row_U_plus[6] = cls.check_undecided(bag_elems, row_U_plus[1], row_U_plus[4], undeccheck_prime )
                        #print(row_U_plus)
                        table.append(row_U_plus)

                    #table.append(row_copy) #[['a', 'c'], [['c', 'a']], [], [], [], [], [], '0.540']
            
            else: #there are no "good" edges to contribute, and P stays as computed for intro_elem
                        row_copy = copy.deepcopy(row) 
                        row_copy[0] = graph_prime #has been extended with introduced argument
                        row_copy[-1] = P
                        #row_copy[-1] = cls.format_float(P)
                        #print(row_copy)
                        #I+a
                        if cls.conflict_free(row_copy[1], row_copy[2], intro_elem[0]):
                            row_I_plus = copy.deepcopy(row_copy) 
                            row_I_plus[2].append(intro_elem[0])
                            defcheck_prime = row_I_plus[5]
                            row_I_plus[5] = cls.check_undecided(bag_elems, row_I_plus[1], row_I_plus[2], defcheck_prime )
                            #print(row_I_plus)
                            table.append(row_I_plus)
                        
                        if intro_elem[0] not in cls.labelling.keys():
                            #D+a
                            row_D_plus = copy.deepcopy(row_copy) 
                            row_D_plus[3].append(intro_elem[0])
                            defcheck_prime = row_D_plus[5]
                            row_D_plus[5] = cls.check_defeated(bag_elems, row_D_plus[1], row_D_plus[2], defcheck_prime )
                            #print(row_D_plus)
                            table.append(row_D_plus)

                        if intro_elem[0] not in cls.labelling.keys():
                            #U+a
                            row_U_plus = copy.deepcopy(row_copy) 
                            row_U_plus[4].append(intro_elem[0])
                            undeccheck_prime = row_U_plus[6]
                            row_U_plus[6] = cls.check_undecided(bag_elems, row_U_plus[1], row_U_plus[4], undeccheck_prime )
                            #print(row_U_plus)
                            table.append(row_U_plus)
                            #dont append with not in I not in D not in U #[['a'], [], [], [], [], [], [], '0.100']
            #G_a
            if prob_introduced != 1:
                row_copy = copy.deepcopy(row) 
                #print("then we can create rows without a")
                #G-a,   everything stays the same. Update P w.r.t to arg only
                if(cls.float_rational == "rational"):
                    P = Fraction(c_row[-1]) * (1- Fraction(cls.prob_args[intro_elem[0]])) # P = 1-p(a)
                    row_copy[-1] = P
                else:
                    P = float(c_row[-1]) * (1- float(cls.prob_args[intro_elem[0]])) # P = 1-p(a)
                    row_copy[-1] = cls.format_float(P)
                if intro_elem[0] not in cls.labelling.keys():   
                    #print("then we can create rows without ", intro_elem[0])
                #   print(row_copy)
                    table.append(row_copy) #[[G'], [R'], [I'], [D'], [U'], [Cd], [Cu], [CWs] P]  
             
        return table

    @classmethod
    def remove_node(cls, bag_elems, removed_elem, child_tab):

        #table = []
        pandas_table = []

        #1) Filter #Todo
        #2) G,R,I,D,U, Cd, Cu \{a}
        table_minus_rem = []
        filtered_table = cls.sigma_forget(bag_elems, child_tab, removed_elem[0])
        #print("filtered child")
        #for r in filtered_table:
        #    print(r)
        for row in filtered_table:
            table_minus_rem.append(cls.minus_removed(removed_elem[0], row))
        #print("len graphs", len(considered_graphs))
        #print("tableminusrem")
        #for r in table_minus_rem:
        #   print(r)
        
        if table_minus_rem != []:

            #pandas approach of merging
            #print("df")
            df = pd.DataFrame(table_minus_rem)
            #print(df)
            # Create 'key' as a tuple for each row, then use it as an index
            df['key'] = df.apply(lambda x: tuple(x[:7]), axis=1)
            df.set_index('key', inplace=True)
            df.index = df.index.map(str)
            #print("df wrong")
            #print(df)
            df = df.drop(columns=list(range(7)))  # Drop original columns after using them to create the key
            df[7] = pd.to_numeric(df[7], errors='coerce')
            grouped = df.groupby('key', sort = False).agg({7:'sum'}).reset_index()

            # print(grouped)

            grouped['as_list'] = [ast.literal_eval(idx) for idx in grouped['key']]
            grouped.drop(columns=['key'], inplace=True)
            cols = ['as_list'] + [col for col in grouped.columns if col != 'as_list']
            grouped = grouped[cols]
            #print("as list")
            #print(grouped)
            grouped = grouped.to_numpy().tolist()
            #print(grouped)
            #print(merged[0])
            for r in grouped:
                new_row = []
                for x in r[0]:
                    new_row.append(x)
                new_row.append(r[1])
                pandas_table.append(new_row)

            #print("pandas table")
            #for r in pandas_table:
            #    print(r)
            #print("end table")

        '''
        #old merging
        #3) #core in remove node = [[G],[R],[I],[D],[U],[Cd],[Cu]]
        cores = []
        for row in table_minus_rem:
            core = copy.deepcopy(row[0:-1])
            if core not in cores:
                cores.append(core)
        print("cores", cores)
        #print("cores", cores)
        for core in cores:
            P = 0
            for row in table_minus_rem:
                if cls.equivalent_rows(core,row[0:-1],"remove"):
                        P = P + float(row[-1])
            core.append(str(cls.format_float(P)))
            #core.append((cls.format_float(P)))
            table.append(core)
        '''
        return pandas_table

    @classmethod
    def join_node(cls, bag_elems, tab_left, tab_right, edges):

        #pd.set_option('display.max_columns', None)  # No limit on the number of displayed columns
        #pd.set_option('display.max_rows', None)  # No limit on the number of displayed rows
        #pd.set_option('display.max_colwidth', None)  # No limit on the width of each column value
        #pd.set_option('display.width', 1000)  # Expand the total width of the output display
        #print("tab left")
        #print(tab_left)
        def create_dataframe(tab):
        # Sort each row and immediately create the key
            sorted_tab = [cls.sort_list_of_lists(row) for row in tab]
            df = pd.DataFrame(sorted_tab)
            # Create 'key' as a tuple for each row, then use it as an index
            df['key'] = df.apply(lambda x: tuple(x[:5]), axis=1)
            df.set_index('key', inplace=True)
            df.index = df.index.map(str)
            return df.drop(columns=list(range(5)))  # Drop original columns after using them to create the key

        left = create_dataframe(tab_left)
        right = create_dataframe(tab_right)        

        #print(right)


        #print("merged")
        merged = pd.merge(left, right, on='key', how='inner')
        #print(merged)

        def process_row(row):
            row['5'] = list(set(row['5_x'] + row['5_y']))
            row['6'] = list(set(row['6_x'] + row['6_y']))
            row['7'] = cls.format_float(float(row['7_x']) * float(row['7_y']))
            return row
        merged = merged.apply(process_row, axis=1)
        merged.drop(columns=['5_x', '5_y', '6_x', '6_y', '7_x', '7_y'], inplace=True)
        merged.reset_index(drop=False, inplace=True)  # This adds a new integer index and drops the existing one

        #print(merged)

        merged['as_list'] = [ast.literal_eval(idx) for idx in merged['key']]
        merged.drop(columns=['key'], inplace=True)
        cols = ['as_list'] + [col for col in merged.columns if col != 'as_list']
        merged = merged[cols]

        print("as list") 
       
        merged = merged.to_numpy().tolist()
        #print(merged)

        #print(merged[0])
        pandas_table = []
        for r in merged:
            new_row = []
            for x in r[0]:
                new_row.append(x)
            new_row.append(r[1])
            new_row.append(r[2])
       
            discount = 1
            potential_edges = cls.valid_for_contrib_join(r[0][0], edges)# CHECK 4 i.e. edges among bag edges that could have been picked in R
            for arg in bag_elems:
                parg = float(cls.prob_args[arg])
                if arg in r[0][0]:
                        discount = discount * parg
                else:
                        discount = discount * (1- parg)
            for e in potential_edges:
                pattck = float(cls.prob_attacks[str(e[0])+"-"+str(e[1])])
                if e in r[0][1]: #if edge is in R
                        discount = discount * pattck
                else:
                        discount = discount * (1-pattck)

           
            new_row.append(cls.format_float(float(r[3])/float(discount)))
            pandas_table.append(new_row)

        print()
        #for r in pandas_table:
        #    print(r)
        print("----------------")
        return pandas_table


#CHECKS & Utils

    #upon removal, filters rows that are not admissible, complete, and that don't match the query extension
    @classmethod
    def sigma_forget(cls, bag_elems, child_tab, removed_elem):
        copy_child_tab = copy.deepcopy(child_tab)
        filtered_child_tab = []

        for row in copy_child_tab:
            
            undecided_but_attacked_by_in = False
            for attack in row[1]:
                if attack[0] in row[2] and attack[1] in row[4]:
                    undecided_but_attacked_by_in = True

            not_true_defeated = removed_elem in row[3] and not removed_elem in row[5] or (removed_elem in row[5] and not removed_elem in row[3]) #G R I D U Cd Cu
            
            not_admissible = False
            for attack in row[1]:
                if attack[1] == removed_elem and removed_elem in row[2] and attack[0] not in row[3]:    #if removed was attacked by something not in def
                    not_admissible = True
            
            #not_true_undecided = removed_elem in row[4] and not removed_elem in row[6] or (removed_elem in row[6] and not removed_elem in row[4]) #G R I D U Cd Cu

            in_but_attacked_by_undec = False
            for attack in row[1]:
                if attack[0] == removed_elem and removed_elem in row[4] and attack[1] in row[2]:
                    in_but_attacked_by_undec = True

            match_query_labelling = True


            #if value == 'def' and not key in row[3]:
            #            match_query_labelling = False
            #if value == 'undec' and not key in row[4]:
            #            match_query_labelling = False

            #erase rows that didnt add a to the subgraph, but which are required by the labelling
            #required_but_not_in_subgraph = removed_elem in cls.labelling.keys() and removed_elem not in row[0]
            #if required_but_not_in_subgraph:
            #    match_query_labelling = False

            
            if "def" not in cls.labelling.values():
                for key,value in cls.labelling.items(): #
                    if key in row[0]:
                        if value == 'in' and not key in row[2]:
                            match_query_labelling = False
                for arg in row[0]:
                    if arg not in cls.labelling.keys() and arg in row[2]: # if not in extension, but IN
                        match_query_labelling = False
            else: # we have in and def in the labelling
                for key,value in cls.labelling.items(): #
                    if key in row[0]:
                        if value == 'in' and not key in row[2]:
                            match_query_labelling = False
                        if value == 'def' and not key in row[3]:
                            match_query_labelling = False
            

            if removed_elem in cls.labelling.keys():
                if cls.labelling[removed_elem] == 'in' and removed_elem not in row[2]:
                    match_query_labelling = False

            if not in_but_attacked_by_undec and not undecided_but_attacked_by_in and not not_true_defeated and not not_admissible and match_query_labelling:
                filtered_child_tab.append(row)
        
        return filtered_child_tab
    @classmethod
    def check_defeated(cls, bag_elems, attacks, in_set, def_check_prime):
        def_check = copy.deepcopy(def_check_prime)
        for att in attacks:
            for elem in bag_elems:
                if (att[0] in in_set and elem == att[1]):
                    def_check = list(set(def_check).union({elem}))
        return def_check

    @classmethod
    def check_undecided(cls, bag_elems, attacks, undec_set, undec_check_prime):
        undec_check = copy.deepcopy(undec_check_prime)
        for att in attacks:
            for elem in bag_elems:
                if (att[0] in undec_set and elem == att[1]) and elem in undec_set:
                    undec_check = list(set(undec_check).union({elem}))
        return undec_check

    @classmethod
    def conflict_free(cls, attacks, in_set, introduced_elem):
        #print("attacks", attacks, " in_set:", in_set, " intro:",introduced_elem)
        for att in attacks:
            if att[0] in in_set and introduced_elem==att[1]:
                return False
            if att[1] in in_set and introduced_elem == att[0]:
                return False
            
        return True

    @classmethod
    def equivalent_rows(cls, rowl, rowr, flag):
        equivalent = True
        if set(rowl[0]) != set(rowr[0]): #equivlanet G
            equivalent = False
        #print("sets",rowl[1], "   ", rowr[1] )
        if set(map(tuple,rowl[1])) != set(map(tuple,rowr[1])): #equivalent R map(tuple, rowl[1]) converts each inner list in rowl[1] to a tuple.
            equivalent = False
        if set(rowl[2]) != set(rowr[2]): #equivlanet I
            equivalent = False
        if set(rowl[3]) != set(rowr[3]): #equivlanet D
            equivalent = False
        if set(rowl[4]) != set(rowr[4]): #equivlanet U
            equivalent = False
        #for equivalence in remove nodes
        if flag == "remove":
            if set(rowl[5]) != set(rowr[5]): #equivlanet Cd
                equivalent = False
            if set(rowl[6]) != set(rowr[6]): #equivlanet Cu
                equivalent = False
        return equivalent

    # returns c_row with removed arguments from graph, attacks from R, and so on
    @classmethod
    def minus_removed(cls, removed_elem, c_row):
        rem_row = copy.deepcopy(c_row)
        edges = []
        for edge in rem_row[1]: 
            edges.append(edge)
        if removed_elem in rem_row[0]: #G
            rem_row[0].remove(removed_elem)
        for edge in edges:
            if edge[0] == removed_elem or edge[1] == removed_elem:
                rem_row[1].remove(edge) #R
        if removed_elem in rem_row[2]:  #I
            rem_row[2].remove(removed_elem)
        if removed_elem in rem_row[3]: #D
            rem_row[3].remove(removed_elem)
        if removed_elem in rem_row[4]: #U
            rem_row[4].remove(removed_elem)  
        if removed_elem in rem_row[5]: #Cd
            rem_row[5].remove(removed_elem) 
        if removed_elem in rem_row[6]: #Cu
            rem_row[6].remove(removed_elem)      
        return rem_row

    #CHECK 3
    #remove guesses that didnt guess in attacks with P=1
    @classmethod
    def check_edge_guesses(cls, potential_edges, guesses):
        good_guesses = [] #those that include attacks with P=1
        if potential_edges != []:
            for guess in guesses:
                bad_guess = False
                for edge in potential_edges:
                    prob_edge = cls.prob_attacks[str(edge[0])+"-"+str(edge[1])]
                    if prob_edge == "1" and edge not in list(guess):
                        bad_guess = True
                if not bad_guess:
                    good_guesses.append(guess)
        else:
            return []
        return good_guesses

    #CHECK 2
    # returns edges incident to introduced, and both ends in graph
    @classmethod
    def valid_for_contribution(cls, graph, edges, introducedElem): #e.g. ['a','b']
        potential_edges = []
        for edge in edges: #edges "in the bag"
            ok = (edge[0] in graph and edge[1] in graph) and (edge[0] == introducedElem[0] or edge[1] ==introducedElem[0])
            if ok:
                potential_edges.append(edge)
        return potential_edges

    #CHECK 4
    # specialised method for join - returns potential edges for this graph
    @classmethod
    def valid_for_contrib_join(cls, graph, edges): #e.g. ['a','b']
        potential_edges = []
        for edge in edges: #edges "in the bag"
            ok = (edge[0] in graph and edge[1] in graph)
            if ok:
                potential_edges.append(edge)
        return potential_edges

    @classmethod
    def format_float(cls,number, precision=15):
        return "{:.{}f}".format(number, precision)

    def powerset(iterable):
        s = list(iterable)
        return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

    @classmethod
    def setProbs(cls, p1, p2):
        cls.prob_args = p1
        cls.prob_attacks = p2

    @classmethod
    def store_table(cls, key, table):
        cls.tables[key] = table

    @classmethod
    def table_at_key(cls, key):
        return cls.tables[key]

    @classmethod
    def print_tables(cls):
        for key,value in cls.tables.items():
            print("Node ",key,":") 
            for row in value:
                print(row)

    @classmethod
    def set_extension(cls, e):
        cls.labelling = e
        return



    @classmethod
    def sort_list_of_lists(cls,row):
        new_row = []
        for index, item in enumerate(row):
            if isinstance(item, list):
                if index == 1:  # Special handling for the second item (arrays of arrays)
                    # Sort the sublists themselves based on their contents (not changing internal order of elements)
                    item.sort(key=lambda x: tuple(x))
                    new_row.append(item)
                elif all(isinstance(subitem, list) for subitem in item):  # General handling for other list of lists
                    # Sort each sublist and sort the lists of sublists
                    sorted_sublists = sorted([sorted(sublist) for sublist in item])
                    new_row.append(sorted_sublists)
                else:
                    # Simple list, sort normally
                    new_row.append(sorted(item))
            else:
                # If the item is not a list, just append it
                new_row.append(item)
        return new_row