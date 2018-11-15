from sudoku import Sudoku


def AC3(board):
    # queue of arcs (initially all constraints)
    arc_queue = list(board.constraints)
    while arc_queue:
        currentArc = arc_queue.pop(0)
        if revise(board, currentArc[0], currentArc[1]):
            # check if D1 is = 0, which means no solution
            if not board.domain[currentArc[0]]:
                return False
            # else for each neighbour of
            for neighbours in board.neighbours[currentArc[0]]:
                # will skip if x2 is found as we do not need this value appended
                if neighbours ==  currentArc[1]:
                    continue
                temp_list = [neighbours, currentArc[0]]
                arc_queue.append(temp_list)
    return True

# takes board, current_arc[0](a) and current_arc[1](b) as parameters
# returns true iff domain b is revised
def revise(board, a, b):
    revised = False
    # check each value in the domain of x1
    for x in board.domain[a]:
        if any([x != y for y in board.domain[b]]):
            revised = False
        else:
            board.domain[a].remove(x)   # delete from domain if true
            revised = True
    return revised

def isTheSame(a,b):
    if len(a) == len(b):
        return True
    
    return False
    

def backtrack(assignments, board):
    if isTheSame(assignments, board.variables):
        return assignments
    
    currentVar = minimum_remaining_values(assignments, board)
    
    #First look at the first heuristic Least Constraining Value
    for v in least_constraining_value(currentVar, board):
        if isConsistent(assignments,currentVar, v, board):
            assign(assignments, currentVar, v, board)
            solution = backtrack(assignments, board)
                        
            if solution:
                return solution
            unassign(assignments, currentVar, board)   

    return False

def define_assigned_vars(board):
    assigned = dict()
    for x in board.variables:
        if len(board.domain[x]) == 1:
            assigned[x] = board.domain[x][0]
    return assigned

#the minimum remaining values heuristic
#Gets the unassigned value with the fewest legal values
def minimum_remaining_values(assignments, board):
    unassigned = list()
    for x in board.variables:
        if x not in assignments:
            unassigned.append(x)
    min_var = min(unassigned, key=lambda tile: len(board.domain[tile]))
    return min_var

#the least constraining value heuristic
#chooses the VALUE that rules out the fewest choices for neighbouring tiles
def least_constraining_value(tile, board):
    if len(board.domain[tile]) == 1:
        return board.domain[tile]
    sorted_domain = sorted(board.domain[tile], key=lambda v: constraints(tile, v, board))
    return sorted_domain

#Function to count the amount of constraints that a given value would induce with the neighbours of a variable that we're assigning a value on
def constraints(tile, value, board):
    constraints = 0
    for x in board.neighbours[tile]:
        if len(board.domain[x]) > 1:
            if x in board.domain[x]:
                constraints += 1
    return constraints

#Checks whether the assignment of a variable results in a consistent board
def isConsistent(assignments, tile, value, board):
    consistent = True
    for key in assignments:
        if assignments[key] == value:
            if key in board.neighbours[tile]:
                consistent = False
    return consistent

def assign(assignments, tile, value, board):
    assignments[tile] = value
    #Each time we assign a value, we must perform a forward check to update domains of the neighbours
    forward_check(board, tile, value, assignments)

def unassign(assignments, tile, board):
    if tile in assignments:
        for tuple in board.updated[tile]:
            board.domain[tuple[0]].append(tuple[1])
        board.updated[tile] = list()
        del assignments[tile]

#Perform forward checking, check neighbours of a variable and update their domains with respect to the assignment of a variable
def forward_check(board, tile, value, assignment):
    for neighbour in board.neighbours[tile]:
        if neighbour not in assignment:
            if value in board.domain[neighbour]:
                board.domain[neighbour].remove(value)
                board.updated[tile].append((neighbour, value))

def solved(board):
    for x in board.domain:        
        if board.domain[x] == "":
            return False

    return True
                

def main():
    InputFile = open('sudoku.txt')
    game_board = list()
    for line in InputFile:
        game_board += [int(i) for i in line.split(' ')]
    # Close the text file
    InputFile.close
    # Create the sudoku object
    board = Sudoku(game_board)

    if AC3(board):
        isSolved = True
        for tile in board.variables:
            if len(board.domain[tile]) > 1:
                isSolved = False

        if(isSolved):
            print("Solution Found")
            # print(board.domain)
            print("|", end = "" )
            count = 0
            row = 0
            for x in board.domain:
                if count == 9:
                    count = 0
                    print()  # starts new line
                    row += 1
                    if row == 3 or row == 6:
                        print()
                    print('|', end='')
                if count == 3 or count == 6:
                    print("  |", end="")
                print("{}|".format(board.domain[x][0]), end="")
                count += 1
        else:
            assigned = define_assigned_vars(board)
            
            assignments = backtrack(assigned, board)
            
            for domain in board.domain:
                board.domain[domain] = assignments[domain] if len(domain) > 1 else board.domain[domain]

        
            print("Solution Found")
            # print(board.domain)
            print("|", end = "" )
            count = 0
            row = 0
            for x in board.domain:
                if count == 9:
                    count = 0
                    print()  # starts new line
                    row += 1
                    if row == 3 or row == 6:
                        print()
                    print('|', end='')
                if count == 3 or count == 6:
                    print("  |", end="")
                print("{}|".format(board.domain[x]), end="")
                count += 1
                    
if __name__ == '__main__':
    main()



