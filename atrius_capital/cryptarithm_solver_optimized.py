# run !pip install ortools
#or tools is mathematicaal optimizarion model for solving complex problems
from __future__ import print_function
from ortools.sat.python import cp_model


class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):

    def __init__(self, variables):
        #initialization of solver
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables #initialization of variables
        self.__solution_count = 0 #initialization of number of solutions

    def on_solution_callback(self):
        self.__solution_count += 1 #increment for every possible solution

    def solution_count(self):
        return self.__solution_count #return count

def split_string(str):
    # function to convert word into string of letters
    # eg "send" becomes ["s","e","n","d"]
    return [char for char in str]


def solution(crypt):
    # Constraint programming engine
    model = cp_model.CpModel() #initialize model
    split_word_array=[] # list of words (letters of each word)
    letters_dict = {}
    for i in range(0,len(crypt)):
      split_word = split_string(crypt[i]) #split word into letters
      split_word_array.append(split_word)
    base = 10

    # Generate int variable for each unique letter
    for word in split_word_array:
        for char in word:
            if char not in letters_dict:
      
                #if the word is at index 0 and only if length of that word is > 1 intialize it from 1 to 9
                if word.index(char) == 0 and len(word)>1:
                    letters_dict[char] = model.NewIntVar(1, base-1, char)
                #if the word is at index 0 and if length of that word is = 1 intialize it from 0 to 9
                elif word.index(char) == 0 and len(word)==1:
                    letters_dict[char] = model.NewIntVar(0, base-1, char)
                else:
                  #initliaze rest from 0 to 9
                    letters_dict[char] = model.NewIntVar(0, base-1, char)
    #check the number of digits
    intvar_array = letters_dict.values()

    # Make sure there are enough digits
    assert base >= len(intvar_array)

    # Generate string version of equation "send + more = money"
    lhs = " + ".join(crypt[:len(crypt)-1]) 
    rhs = " = " + crypt[len(crypt)-1]
    equation = lhs + rhs + "\n"
    

    # Compute the equation
    constraint_array = []
    for word in split_word_array:
        exp = len(word)-1
        value = 0
        for char in word:
            # to get permutations eg like s * 10000 as its first char
            value += letters_dict[char] * pow(base, exp)
            exp -= 1
        constraint_array.append(value)
    
    constraint_lhs = sum(constraint_array[:len(constraint_array)-1])
    constraint_rhs = constraint_array[len(constraint_array)-1]

    # Define constraints
    model.AddAllDifferent(intvar_array)
    model.Add(constraint_lhs == constraint_rhs)

    # Solve model
    solver = cp_model.CpSolver()
    solution_printer = VarArraySolutionPrinter(intvar_array)
    status = solver.SearchForAllSolutions(model, solution_printer)
    print(solution_printer.solution_count())


solution(['SEND','MORE','MONEY'])
solution(["GREEN", "BLUE", "BLACK"])
solution(["A", "B", "B"])
