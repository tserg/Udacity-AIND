assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    for each_unit in unitlist:
        twin_list = {} # dictionary to store instances of boxes with 2 digits. Key = possibilities; Value = Box number
        
        for i in each_unit: 
            
            if len(values[i]) == 2: # checks if the box has 2 digits
                if (values[i]) in twin_list: # if value is not in dictionary, create new key
                    twin_list[values[i]] += [i]
                    
                else: # add boxes to existing key
                    twin_list[values[i]] = [i]
                    
     # Eliminate the naked twins as possibilities for their peers   
            
        for j in twin_list: # checks if the 2 digits has 2 boxes
            if len(twin_list[j]) == 2:
                for k in each_unit:
                    if len(values[k]) > 1 and k not in twin_list[j]: # checks whether the box has more than 1 digit and is not in the twin_list

                        new_value = values[k]
                        first_digit = j[0]
                        second_digit = j[1]
                        
                        new_value = new_value.replace(first_digit, '') # removes first digit
                        new_value = new_value.replace(second_digit, '') # removes second digit

                        values[k] = new_value

    
    
    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [i+j for i in A for j in B]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

diagonal1 = [a[0]+a[1] for a in zip(rows, cols)]
diagonal2 = [a[0]+a[1] for a in zip(rows, cols[::-1])]
diagonal_units = [diagonal1,diagonal2]

unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert(len(grid)==81)
    
    final_grid = dict(zip(boxes, grid))
    
    for key, value in final_grid.items():
        
        if value == '.':
            final_grid[key] = '123456789'
            
        assign_value(final_grid, key, value)
            
    
     
    
    return final_grid


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    
    if values == False:
        return None
    
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """Eliminate values that have been solved from peers.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the solved values eliminated from peers.
    """
    for key, value in values.items(): 
        if len(value) == 1: # checks if the box has been solved
            for j in peers[key]: # iterates through the peers of a solved box
                new_value = values[j].replace(value, '') # eliminates the value of the solved box
                values[j] = new_value
                
                    
    return values

def only_choice(values):
    """Solves the value of a box if it is the only choice for that number in an unit
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with only choice boxes solved.
    """
    for unit in unitlist:
        for digit in '123456789': 
            dplaces = [box for box in unit if digit in values[box]] # makes a list of possible boxes for each digit
            if len(dplaces) == 1: # checks if there is only one box for the digit
                values[dplaces[0]] = digit
                assign_value(values, dplaces[0], digit)

    return values

def reduce_puzzle(values):
    
    """Reduces the possibilities of the sudoku puzzle.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with solved values eliminated from peers and only choice boxes solved
    """
    
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        
        eliminate(values)

        # Your code here: Use the Only Choice Strategy
        
        only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    
    if values is False:
        return False ## Failed earlier
        
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
        
    # Choose one of the unfilled squares with the fewest possibilities
    
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    sudoku = grid_values(grid)
    
    return search(sudoku)
    

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    
    solution = solve(diag_sudoku_grid)
    
    display(solution)
    
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
