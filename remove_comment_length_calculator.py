def solution(source):
    #set flag as false to keep track of block comments
    flag = False
    result = 0  # count variable
    if len(source)<=10:
        for line in source: #start iterating through lines
            if len(line)<=150:
                idx = 0# variable to deal with length/coounting characters of one linw
                while idx < len(line):
                    #if line has '/' symbol and the character is less then length of line and next character is '/'
                    # the // comment is complete and flag is not true
                    if line[idx] == '/' and idx < len(line) - 1 and line[idx + 1] == '/' and not flag:
                        break
                    #if line has '/' charcter and character is less then length of line and next character is '*'
                    #/* indicates opening of block comment and flag is not true
                    elif line[idx] == '/' and idx < len(line) - 1 and line[idx + 1] == '*' and not flag:
                        #make flag as true and increment idx
                        flag = True
                        idx += 1
                    #if line has '*' charcter and character is less then length of line and next character is '/'
                    #*/ indicates closing of existing block comment and flag is true
                    elif line[idx] == '*' and idx < len(line) - 1 and line[idx + 1] == '/' and flag:
                        #make flag as false and increase idx
                        flag = False
                        idx += 1
                    # if character is non space character and flag is false increment result count
                    elif line[idx] != ' ' and not flag:
                        #print(line[idx], idx)
                        result += 1
                     #go to next charcter
                    idx += 1
    return result
