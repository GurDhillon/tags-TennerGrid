'''
Construct and return Tenner Grid CSP models.
'''

from cspbase import *
import itertools


def create_variables(initial_tenner_board):
    """Return representation of initial_tenner_board using Variable objects.
    """
    result = []
    for i in range(len(initial_tenner_board)):
        representation = []
        for j in range(10):
            num = initial_tenner_board[i][j]
            if num == -1:
                representation.append(Variable('({}, {})'.format(i, j), domain=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
            else:
                var = Variable('({}, {})'.format(i, j), domain=[num])
                var.assign(num)
                representation.append(var)

        result.append(representation)
    return result


def get_all_combinations(scope):
    """
    """
    domains = [var.cur_domain() for var in scope]
    all_combs = list(itertools.product(*domains))

    no_duplicates = []
    for comb in all_combs:
        if len(set(comb)) == len(comb):
            no_duplicates.append(comb)

    return no_duplicates


def create_row_binary_cons(variables):
    """Return a list of binary constraints for each row of the tenner board.
    """
    cons = []
    for k in range(len(variables)):
        row = variables[k]
        for i in range(9):
            for j in range(i + 1, 10):
                scope = [row[i], row[j]]
                con = Constraint('({}, {}), ({}, {})'.format(k, i, k, j), scope=scope)
                con.add_satisfying_tuples(get_all_combinations(scope))
                cons.append(con)
    return cons


def create_adjacent_cons(variables):
    """Return a list of binary constraints for each adjacent cells of the tenner board.
    """
    cons = []
    for k in range(len(variables) - 1):
        for i in range(10):
            scope = [variables[k][i], variables[k + 1][i]]
            con = Constraint('({}, {}), ({}, {})'.format(k, i, k + 1, i), scope=scope)
            con.add_satisfying_tuples(get_all_combinations(scope))
            cons.append(con)

            if i != 0:
                scope = [variables[k][i], variables[k + 1][i - 1]]
                con = Constraint('({}, {}), ({}, {})'.format(k, i, k + 1, i - 1), scope=scope)
                con.add_satisfying_tuples(get_all_combinations(scope))
                cons.append(con)

            if i != 9:
                scope = [variables[k][i], variables[k + 1][i + 1]]
                con = Constraint('({}, {}), ({}, {})'.format(k, i, k + 1, i + 1), scope=scope)
                con.add_satisfying_tuples(get_all_combinations(scope))
                cons.append(con)

    return cons


def create_sum_cons(variables, sums):
    """
    """
    cons = []
    n = len(variables)

    for i in range(len(sums)):
        satisfiers = [comb for comb in list(itertools.product(range(10), repeat=n)) if sum(comb) == sums[i]]
        scope = [variables[k][i] for k in range(n)]

        con = Constraint('Col {}'.format(i), scope=scope)
        con.add_satisfying_tuples(satisfiers)
        cons.append(con)

    return cons


def tenner_csp_model_1(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along 
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner grid using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from 
       (0,0) to (n,9)) where n can be 3 to 7.
       
       
       The input board is specified as a pair (n_grid, last_row). 
       The first element in the pair is a list of n length-10 lists.
       Each of the n lists represents a row of the grid. 
       If a -1 is in the list it represents an empty cell. 
       Otherwise if a number between 0--9 is in the list then this represents a 
       pre-set board position. E.g., the board
    
       ---------------------  
       |6| |1|5|7| | | |3| |
       | |9|7| | |2|1| | | |
       | | | | | |0| | | |1|
       | |9| |0|7| |3|5|4| |
       |6| | |5| |0| | | | |
       ---------------------
       would be represented by the list of lists
       
       [[6, -1, 1, 5, 7, -1, -1, -1, 3, -1],
        [-1, 9, 7, -1, -1, 2, 1, -1, -1, -1],
        [-1, -1, -1, -1, -1, 0, -1, -1, -1, 1],
        [-1, 9, -1, 0, 7, -1, 3, 5, 4, -1],
        [6, -1, -1, 5, -1, 0, -1, -1, -1,-1]]
       
       
       This routine returns model_1 which consists of a variable for
       each cell of the board, with domain equal to {0-9} if the board
       has a 0 at that position, and domain equal {i} if the board has
       a fixed number i at that cell.
       
       model_1 contains BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.).
       model_1 also constains n-nary constraints of sum constraints for each 
       column.
    '''
    n_grid, last_row = initial_tenner_board[0], initial_tenner_board[1]
    variables = create_variables(n_grid)

    row_cons = create_row_binary_cons(variables)
    adjacent_cons = create_adjacent_cons(variables)
    sum_cons = create_sum_cons(variables, last_row)

    csp = CSP('csp')

    for row in variables:
        for var in row:
            csp.add_var(var)

    for con in row_cons:
        csp.add_constraint(con)
    for con in adjacent_cons:
        csp.add_constraint(con)
    for con in sum_cons:
        csp.add_constraint(con)

    return csp, variables

##############################


def create_row_nary_cons(variables):
    """Return a list of n-ary constraints for each row of the tenner board.
    """
    cons = []
    for k in range(len(variables)):
        scope = [var for var in variables[k]]
        con = Constraint('Row {}'.format(k), scope=scope)
        con.add_satisfying_tuples(get_all_combinations(scope))
        cons.append(con)
    return cons


def tenner_csp_model_2(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along 
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from 
       (0,0) to (n,9)) where n can be 3 to 7.

       The input board takes the same input format (a list of n length-10 lists
       specifying the board as tenner_csp_model_1.
    
       The variables of model_2 are the same as for model_1: a variable
       for each cell of the board, with domain equal to {0-9} if the
       board has a -1 at that position, and domain equal {i} if the board
       has a fixed number i at that cell.

       However, model_2 has different constraints. In particular, instead
       of binary non-equals constaints model_2 has a combination of n-nary 
       all-different constraints: all-different constraints for the variables in
       each row, and sum constraints for each column. You may use binary 
       contstraints to encode contiguous cells (including diagonally contiguous 
       cells), however. Each -ary constraint is over more 
       than two variables (some of these variables will have
       a single value in their domain). model_2 should create these
       all-different constraints between the relevant variables.
    '''
    n_grid, last_row = initial_tenner_board[0], initial_tenner_board[1]
    variables = create_variables(n_grid)

    row_cons = create_row_nary_cons(variables)
    adjacent_cons = create_adjacent_cons(variables)
    sum_cons = create_sum_cons(variables, last_row)

    csp = CSP('csp')

    for row in variables:
        for var in row:
            csp.add_var(var)

    for con in row_cons:
        csp.add_constraint(con)
    for con in adjacent_cons:
        csp.add_constraint(con)
    for con in sum_cons:
        csp.add_constraint(con)

    return csp, variables
