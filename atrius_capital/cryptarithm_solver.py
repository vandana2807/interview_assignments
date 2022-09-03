import re
def solve(cryptarithm):
    words = re.findall('[A-Za-z]+', cryptarithm)
    all_letters = set(''.join(words))
    if len(all_letters) > 10:
        print('There are more than 10 letters, this is not a valid cryptarithm.')
        return
    letters_starting_a_word = set(w[0] for w in words)
    all_letters_with_those_starting_a_word_first = ''.join(letters_starting_a_word) + ''.join(all_letters - letters_starting_a_word)
    number_of_letters_starting_a_word = len(letters_starting_a_word)
    counter=[]
    for possible_solution in permutations('0123456789', len(all_letters)):
        if '0' not in possible_solution[:number_of_letters_starting_a_word]:
            equation = cryptarithm.translate(str.maketrans(all_letters_with_those_starting_a_word_first, ''.join(possible_solution)))
            try:
                if eval(equation):
                    counter.append(equation)
            except ArithmeticError:
                pass
            except:
                print('Incorrect expression, this is not a valid cryptarithm.')
                return
            
    return counter

def solution(z):
    s=""
    for i in range(0,len(z)):
        if i!=len(z)-1:
            #print(z[i])
            if len(s)==0:
                s=z[i]
            else:
                s=s+"+"+z[i]
    s=s+"=="+z[-1]
    print(s)
    r=solve(s)
    return len(r)
z=["GREEN", "BLUE", "BLACK"]
solution(z)
