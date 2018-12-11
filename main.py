import sys
#
# orig_stdout = sys.stdout
# f = open('out.txt', 'w')
# sys.stdout = f
#
# for i in range(2):
#     print 'i = ', i
#
# sys.stdout = orig_stdout
# f.close()
def IsUnitClause(x):
    if len(x) == 1:
        return True

def IsNegate(x):
    if len(x) == 1 and x[0][0] == '~':
        return True

def resolve(x,y):
    if x == '~' + y or y == '~' + x:
        return True

def hasEmptyClause(final_KB):
    for i in range(0, len(final_KB)):
        if len(final_KB[i]) == 0:
            # f.close()
            return True
    return False

def NegateConclusion(x):
    for i in range(0, len(x)):
        if x[i][0] == '~':
            x[i] = x[i][1]
        else:
            x[i] = '~' + x[i][0]
step = 1


def ResolveMultiple(KB):
    global step
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

data = []
KB = []
with open("input4.txt",'r') as f:
    lines = f.readlines()
    for line in lines:
        data.append(line.strip())


print(data)

for i in range(0,len(data)):
    if i != 0 and i != len(data) - 2:
        KB.append(data[i])
# if len(KB[len(KB)-1]) <= 2:
#     if KB[len(KB)-1][0] != '~':
#         KB[len(KB)-1] = '~' + KB[len(KB)-1]
#     else:
#         KB[len(KB)-1] = KB[len(KB)-1][1]

print("KB: ", KB)

final_KB = []

for i in range(0,len(KB)):
    final_KB.append(KB[i].split('|'))

NegateConclusion(final_KB[len(final_KB)-1])
def print_KB(KB):
    copy = KB.copy()
    temp = []
    for i in range(0, len(copy)):
        copy[i] = '|'.join(copy[i])
        temp.append(copy[i])
    temp = ','.join(temp)
    print(temp)

print("F_KB", final_KB)
print_KB(final_KB)
# final_KB[5].remove(final_KB[5][0])
# print(final_KB)
original_KB = final_KB
# print(len(final_KB[6]), final_KB[6][0][0], final_KB[6][0][1])
# print(IsNegate(final_KB[6]))
# print(final_KB[4], len(final_KB[4]))


def resolution(final_KB):
    global original_KB
    global step
    if ResolveMultiple(final_KB) == True:
        return
    #if there exist negate unit clause in KB

    for i in range(0,len(final_KB)):
        if IsNegate(final_KB[i]):
            for j in range(0,len(final_KB)):
                for k in range(0,len(final_KB[j])):
                    if resolve(final_KB[i][0],final_KB[j][k]):
                        final_KB[j].remove(final_KB[j][k])
                        # if final_KB[j] == None:
                        #     final_KB[j][0]== '...'
                        break
            if(final_KB != original_KB):
                original_KB = final_KB
                break
            final_KB.remove(final_KB[i])
            print_KB(final_KB)
            # print("Step " + str(step), final_KB)
            step +=1
            break
    # if there isn't any negate clause in KB, check whether there exist unit clause in KB
    for i in range(0,len(final_KB)):
        if IsUnitClause(final_KB[i]):
            for j in range(0,len(final_KB)):
                for k in range(0,len(final_KB[j])):
                    if resolve(final_KB[i][0],final_KB[j][k]):
                        final_KB[j].remove(final_KB[j][k])
                        # if final_KB[j] == None:
                        #     final_KB[j][0]== '...'
                        break
            if(final_KB != original_KB):
                original_KB = final_KB
                break
            final_KB.remove(final_KB[i])
            print_KB(final_KB)
            # print("Step " + str(step), final_KB)
            step +=1
            break

while(not hasEmptyClause(final_KB)):
    resolution(final_KB)

sys.exit()
# print(final_KB[4], len(final_KB[4]), IsNegate(final_KB[4]))
# print(final_KB)

# x = '~m'
# y = 'm'
# if resolve(x,y):
#     print("True")
