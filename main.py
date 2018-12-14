import sys
import os

args = sys.argv[1:]

def IsUnitClause(x):
    '''
    check whether the predicate is unit clause
    :param x:
    :return: True if x is unit clause
    '''
    if len(x) == 1 and x[0][0] != '~':
        return True

def IsNegate(x):
    '''
    check whether the predicate is negate unit clause
    :param x:
    :return: True if x is negate unit clause
    '''
    if len(x) == 1 and x[0][0] == '~':
        return True

def resolve(x,y):
    '''
    check whether the 2 predicates can be resolved
    :param x:
    :param y:
    :return:
    '''
    if x == '~' + y or y == '~' + x:
        return True
    return False


def NegateConclusion(x):
    '''
    Negate the prove sentence to add to the KB
    :param x:
    :return:
    '''
    for i in range(0, len(x)):
        if x[i][0] == '~':
            x[i] = x[i][1]
        else:
            x[i] = '~' + x[i][0]

def ResolveMultiple(KB):
    '''
    Check whether there exists a pair of resolution creating empty clause
    :param KB:
    :return:
    '''
    for i in range (0,len(KB)):
        for j in range (0,len(KB)):
            count = 0
            if j!=i:
                if len(KB[i]) == len(KB[j]):

                    for m in range(0,len(KB[i])):
                        for n in range(0,len(KB[j])):
                            if resolve(KB[i][m],KB[j][n]):
                                count += 1
                    if count == len(KB[i]):
                        # KB[j] = []
                        # KB.remove(KB[i])
                        # print("Step " +str(step), KB)
                        # f.close()
                        return True
    return False
def HasResolvePair(KB):
    for i in range (0,len(KB)):
        for j in range (0,len(KB)):
            if j!=i:
                for m in range(0,len(KB[i])):
                    for n in range(0,len(KB[j])):
                        if resolve(KB[i][m],KB[j][n]):
                            return True
    return False

def process_data(path):
    '''
    process the data from input file to create KB
    :param path: the path of input file
    :return: the final Knowledge Base
    '''
    data = []
    KB = []
    with open(path,'r') as f:
        lines = f.readlines()
        for line in lines:
            data.append(line.strip())
    # print(data)
    for i in range(0,len(data)):
        if i != 0 and i != len(data) - 2:
            KB.append(data[i])
    # print("KB: ", KB)

    final_KB = []

    for i in range(0,len(KB)):
        final_KB.append(KB[i].split('|'))
    sentence_to_prove = final_KB[len(final_KB)-1].copy()
    NegateConclusion(final_KB[len(final_KB)-1])
    # print("F_KB", final_KB)
    if len(sentence_to_prove) == 1:
        print("".join(sentence_to_prove))
    else:
        print("|".join(sentence_to_prove))
    print_KB(final_KB)
    return final_KB

def print_KB(KB):
    '''
    Print the KB in the right format
    :param KB:
    :return:
    '''
    copy = KB.copy()
    temp = []
    for i in range(0, len(copy)):
        copy[i] = '|'.join(copy[i])
        temp.append(copy[i])
    temp = ','.join(temp)
    print(temp)


def resolution(final_KB):
    '''
    The main resolution algorithm, first resolve the negate unit clause then resolve the unit clause
    :param final_KB:
    :return:
    '''
    #firstly, if there exists a pair of resolution sentences with 2 or more predicates
    # if ResolveMultiple(final_KB) == True:
    #     return True

    #if there exists negate unit clause in KB, the check = true if there exists, false if not
    check = False
    for i in range(0,len(final_KB)):
        if len(final_KB)>2:
            if IsNegate(final_KB[i]):

                for j in range(0,len(final_KB)):
                    for k in range(0,len(final_KB[j])):
                        if resolve(final_KB[i][0],final_KB[j][k]):
                            check = True
                            final_KB[j].remove(final_KB[j][k])
                            # if final_KB[j] == None:
                            #     final_KB[j][0]== '...'
                            break
                # if(final_KB != original_KB):
                #     original_KB = final_KB
                #     break
                if check == True:
                    final_KB.remove(final_KB[i])
                    print_KB(final_KB)
                # print("Step " + str(step), final_KB)

                    break
    # if there isn't any negate clause in KB, check whether there exist unit clause in KB
    # check = False means there isn't any negate unit clause, then check the unit clause
    # if check = True, then it means there is negate unit clause and we exit the function to loop again
    if check == False:
        for i in range(0,len(final_KB)):
            if len(final_KB) > 2:
                if IsUnitClause(final_KB[i]):
                    check = False
                    for j in range(0,len(final_KB)):
                        for k in range(0,len(final_KB[j])):
                            if resolve(final_KB[i][0],final_KB[j][k]):
                                check = True
                                final_KB[j].remove(final_KB[j][k])
                                # if final_KB[j] == None:
                                #     final_KB[j][0]== '...'
                                break
                    # if(final_KB != original_KB):
                    #     original_KB = final_KB
                    #     break
                    if check == True:
                        final_KB.remove(final_KB[i])
                        print_KB(final_KB)
                    # print("Step " + str(step), final_KB)

                        break

if __name__ == "__main__":

    # path = input("Enter the name of your input file: ")
    # the 3 below lines aim to use the print to write to the output file
    orig_stdout = sys.stdout
    f = open(args[1], 'w')
    sys.stdout = f
    final_KB = process_data(args[0])
    # final_KB = process_data("input6.txt")

    # Loop the resolution until find a pair of resolve predicates
    while(not ResolveMultiple(final_KB) and len(final_KB)>2 and HasResolvePair(final_KB)):
        resolution(final_KB)
    if ResolveMultiple(final_KB) == True:
        print("True")
    else:
        print("False")

    sys.stdout = orig_stdout
    f.close()
