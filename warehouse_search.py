######################################################################
# This file copyright the Georgia Institute of Technology
#
# Permission is given to students to use or modify this file (only)
# to work on their assignments.
#
# You may NOT publish this file or make it available to others not in
# the course.
#
######################################################################

'''
=== Introduction ===

Your file must be called `warehouse.py` and must have two classes
  called `DeliveryPlanner_PartA` and `DeliveryPlanner_PartB`.

- You may add additional classes and functions as needed provided they are all in this file `warehouse.py`.
- You may share code between partA and partB but it MUST BE IN THIS FILE
- Upload warehouse.py to Canvas in the Assignments section. Do NOT put it into an 
  archive with other files.
- Your warehouse.py file must not execute any code when imported.
- Ask any questions about the directions or specifications on Piazza.

=== Grading ===

- Your planner will be graded against a set of test cases, each equally weighted.
- If your planner returns a list of moves of total cost that is K times the minimum cost of 
  successfully completing the task, you will receive 1/K of the credit for that test case.
- Otherwise, you will receive no credit for that test case. This could happen for one of several 
  reasons including (but not necessarily limited to):
  - plan_delivery's moves do not deliver the boxes in the correct order.
  - plan_delivery's output is not a list of strings in the prescribed format.
  - plan_delivery does not return an output within the prescribed time limit.
  - Your code raises an exception.

=== Part A ===

In this Part A, you will build a planner that helps a robot
  find the best path through a warehouse filled with boxes
  that it has to pick up and deliver to a dropzone.

`DeliveryPlanner_PartA` must have an `__init__` function that takes three 
  arguments: `self`, `warehouse`, and `todo`.
`DeliveryPlanner_PartA` must also have a function called `plan_delivery` that 
  takes a single argument, `self`.

=== Part A Input Specifications ===

`warehouse` will be a list of m strings, each with n characters,
  corresponding to the layout of the warehouse. The warehouse is an
  m x n grid. warehouse[i][j] corresponds to the spot in the ith row
  and jth column of the warehouse, where the 0th row is the northern
  end of the warehouse and the 0th column is the western end.

The characters in each string will be one of the following:

'.' (period) : traversable space. The robot may enter from any adjacent space.
'#' (hash) : a wall. The robot cannot enter this space.
'@' (dropzone): the starting point for the robot and the space where all boxes must be delivered.
  The dropzone may be traversed like a '.' space.
[0-9a-zA-Z] (any alphanumeric character) : a box. At most one of each alphanumeric character 
  will be present in the warehouse (meaning there will be at most 62 boxes). A box may not
  be traversed, but if the robot is adjacent to the box, the robot can pick up the box.
  Once the box has been removed, the space functions as a '.' space.

For example, 
  warehouse = ['1#2',
               '.#.',
               '..@']
  is a 3x3 warehouse.
  - The dropzone is at the warehouse cell in row 2, column 2.
  - Box '1' is located in the warehouse cell in row 0, column 0.
  - Box '2' is located in the warehouse cell in row 0, column 2.
  - There are walls in the warehouse cells in row 0, column 1 and row 1, column 1.
  - The remaining five warehouse cells contain empty space. (The dropzone is empty space)
#
The argument `todo` is a list of alphanumeric characters giving the order in which the 
  boxes must be delivered to the dropzone. For example, if 
  todo = ['1','2']
  is given with the above example `warehouse`, then the robot must first deliver box '1'
  to the dropzone, and then the robot must deliver box '2' to the dropzone.

=== Part A Rules for Movement ===

- Two spaces are considered adjacent if they share an edge or a corner.
- The robot may move horizontally or vertically at a cost of 2 per move.
- The robot may move diagonally at a cost of 3 per move.
- The robot may not move outside the warehouse.
- The warehouse does not "wrap" around.
- As described earlier, the robot may pick up a box that is in an adjacent square.
- The cost to pick up a box is 4, regardless of the direction the box is relative to the robot.
- While holding a box, the robot may not pick up another box.
- The robot may put a box down on an adjacent empty space ('.') or the dropzone ('@') at a cost
  of 2 (regardless of the direction in which the robot puts down the box).
- If a box is placed on the '@' space, it is considered delivered and is removed from the ware-
  house.
- The warehouse will be arranged so that it is always possible for the robot to move to the 
  next box on the todo list without having to rearrange any other boxes.

An illegal move will incur a cost of 100, and the robot will not move (the standard costs for a 
  move will not be additionally incurred). Illegal moves include:
- attempting to move to a nonadjacent, nonexistent, or occupied space
- attempting to pick up a nonadjacent or nonexistent box
- attempting to pick up a box while holding one already
- attempting to put down a box on a nonadjacent, nonexistent, or occupied space
- attempting to put down a box while not holding one

=== Part A Output Specifications ===

`plan_delivery` should return a LIST of moves that minimizes the total cost of completing
  the task successfully.
Each move should be a string formatted as follows:

'move {d}', where '{d}' is replaced by the direction the robot will move:
   "n","e","s","w","ne","se","nw","sw"

'lift {x}', where '{x}' is replaced by the alphanumeric character of the box being picked up

'down {d}', where '{d}' is replaced by the direction the robot will move:
   "n","e","s","w","ne","se","nw","sw"

For example, for the values of `warehouse` and `todo` given previously (reproduced below):
  warehouse = ['1#2',
               '.#.',
               '..@']
  todo = ['1','2']
  
`plan_delivery` might return the following:
  ['move w',
   'move nw',
   'lift 1',
   'move se',
   'down e',
   'move ne',
   'lift 2',
   'down s']



=== Part B ===

In this Part B, you will build a planner that helps a robot
  find the best path through a warehouse to a single box
  that it has to pick up and deliver to a dropzone.  This part differs from 
  part A, in that there is a single box, but now the warehouse has
  an "uneven" floor that imposes an additional, positive, cost on each robot 
  command.  In addition, the robot may "wake up" at any point in the 
  warehouse and be tasked with retrieving the box and delivering it
  to the dropzone.  Because of this, this project is most easily solved
  using the dynamic programming approach covered in Lesson 12: 14-19 and 
  problem set 4, question 5.
  

`DeliveryPlanner_PartB` must have an `__init__` function that takes three 
  arguments: `self`, `warehouse`, 'warehouse_cost', and `todo`.
`DeliveryPlanner_PartB` must also have a function called `plan_delivery` that 
  takes the argument, `self` and a flag 'debug' set to default to False.

=== Part B Input Specifications ===

`warehouse` will be a list of m strings, each with n characters,
  corresponding to the layout of the warehouse. The warehouse is an
  m x n grid. warehouse[i][j] corresponds to the spot in the ith row
  and jth column of the warehouse, where the 0th row is the northern
  end of the warehouse and the 0th column is the western end.

The characters in each string will be one of the following:

'.' (period) : traversable space. The robot may enter from any adjacent space.
'#' (hash) : a wall. The robot cannot enter this space.
'@' (dropzone): the starting point for the robot and the space where all boxes must be delivered.
  The dropzone may be traversed like a '.' space.
'1' : the single box to be retrieved. A box may not
  be traversed, but if the robot is adjacent to the box, the robot can pick up the box.
  Once the box has been removed, the space functions as a '.' space.

For example:
  warehouse = ['1..',
			   '.#.',
			   '..@']
  is a 3x3 warehouse.
  - The dropzone is at the warehouse cell in row 2, column 2.
  - Box '1' is located in the warehouse cell in row 0, column 0.
  - There are walls in the warehouse cells in row 0, column 1 and row 1, column 1.
  - The remaining five warehouse cells contain empty space. (The dropzone is empty space)

The argument warehouse_cost is a list of lists such that indices i,j refer to 
  the positive cost at the row i and column j in the warehouse.  For the case above
  the corresponding warehouse_cost could be:

  warehouse_cost = [[0, 5, 2],
					[10, math.inf, 2],
					[2, 10, 2]]

  where the interior "wall" has cost=infinity.


The argument `todo` is a list of alphanumeric characters giving the order in which the 
  boxes must be delivered to the dropzone.  For part B this is limited to a single box
  as follows:
    todo = ['1']
  which indicates that box '1' must be retrieved and delivered to the dropzone

  Note: todo is kept consistent with part A for convenience and possible future expansion of
  the project requirements. 

There is no input for initial robot location because the robot may "wake up" at any point in 
  the warehouse and must be handed a "policy" so that no matter where it is it can retrieve
  the box.  Further, because it may lift the box from different squares depending on 
  its starting location, it requires another "policy" to deliver the box to the dropzone.
  

=== Part B Rules for Movement ===

Rules for Movement are the same as those for part A.  Please refer to part A documentation.

=== Part B Output Specifications ===

`plan_delivery` should return two policies, each as a LIST of LISTs of commands at each
square on the grid.  The format of the commands is the same as in part A.

For example, for the values of `warehouse` and `todo` given previously (reproduced below):
  warehouse = ['1..',
			   '.#.',
			   '..@']
  todo = ['1']
  
`plan_delivery` might return the following two policies:

	To Box Policy:
	[['B', 'lift 1', 'move w']
	['lift 1', -1, 'move nw']
	['move n', 'move nw', 'move n']]

	Deliver Box Policy:
	[['move e', 'move se', 'move s']
	['move ne', -1, 'down s']
	['move e', 'down e', 'move n']]

	where: 'B' indicates the box location.
    For the case of the "Deliver Box Policy", the dropzone includes the
    optimal move out of it in the event the robot starts on, lifts an 
    adjacent box, and then must move off the dropzone to deliver it.

The testing suite will pick a starting location for the robot and then execute the 
appropriate moves in the "To Box Policy" until it finds and lifts the box with a 'lift 1' 
command.  At this point execution transitions to the "Deliver Box Policy" and, given
the location of the robot when it lifted the box, the appropriate commands are 
executed until the the box is delivered to the dropzone.

Hint: before changing this file test your environment in two steps:
    
    1) From the command line type:  
      python warehouse.py
      *  A list of moves for Part A test case 1 should be printed
      *  A "to_box_policy" and "deliver_policy" will be printed
         for part B, test case 1
      
    2) From the command line type: 
      python testing_suite_PartA.py
      A list of test cases and their score should show that test case 1 passed
      and the remaining failed.
      There are more notes in testing_suite_partA.py to discuss how to run and
      debug it

    3) From the command line type:
      python testing_suite_PartB.py
      A list of test cases and their score should show that test case 1 passed
      and the remaining failed.
      There are more notes in testing_suite_partB.py to discuss how to run and
      debug it
'''

import math

class DeliveryPlanner_PartA:

    """
    Required methods in this class are:
    
      plan_delivery(self, debug = False) which is stubbed out below.  
        You may not change the method signature as it will be called directly 
        by the autograder but you may modify the internals as needed.
    
      __init__: which is required to initialize the class.  Starter code is 
        provided that intializes class variables based on the definitions in 
        testing_suite_partA.py.  You may choose to use this starter code
        or modify and replace it based on your own solution
    
    The following methods are starter code you may use for part A.  
    However, they are not required and can be replaced with your
    own methods.
    
      _set_initial_state_from(self, warehouse): creates structures based on
          the warehouse and todo definitions and intializes the robot
          location in the warehouse
    
      _search(self, debug=False): Where the bulk of the A* search algorithm
          could reside.  It should find an optimal path from the robot
          location to a goal.  Hint:  you may want to structure this based
          on whether looking for a box or delivering a box.
  
    """

    ## Definitions taken from testing_suite_partA.py
    ORTHOGONAL_MOVE_COST = 2
    DIAGONAL_MOVE_COST = 3
    BOX_LIFT_COST = 4
    BOX_DOWN_COST = 2
    ILLEGAL_MOVE_PENALTY = 100

    def __init__(self, warehouse, todo):
        
        self.todo = todo
        self.boxes_delivered = []
        self.total_cost = 0
        self._set_initial_state_from(warehouse)

        self.delta = [[-1, 0 ], # north
                      [ 0,-1 ], # west
                      [ 1, 0 ], # south
                      [ 0, 1 ], # east
                      [-1,-1 ], # northwest (diag)
                      [-1, 1 ], # northeast (diag)
                      [ 1, 1 ], # southeast (diag)
                      [ 1,-1 ]] # southwest (diag)

        self.delta_directions = ["n","w","s","e","nw","ne","se","sw"]

        # Can use this for a visual debug
        self.delta_name = [ '^', '<', 'v', '>','\\','/','[',']' ]

        # Costs for each move
        self.delta_cost = [  self.ORTHOGONAL_MOVE_COST, 
                             self.ORTHOGONAL_MOVE_COST, 
                             self.ORTHOGONAL_MOVE_COST, 
                             self.ORTHOGONAL_MOVE_COST,
                             self.DIAGONAL_MOVE_COST,
                             self.DIAGONAL_MOVE_COST,
                             self.DIAGONAL_MOVE_COST,
                             self.DIAGONAL_MOVE_COST ]

    ## state parsing and initialization function from testing_suite_partA.py
    def _set_initial_state_from(self, warehouse):
        """Set initial state.

        Args:
            warehouse(list(list)): the warehouse map.
        """
        rows = len(warehouse)
        cols = len(warehouse[0])

        self.warehouse_state = [[None for j in range(cols)] for i in range(rows)]
        self.dropzone = None
        self.boxes = dict()

        for i in range(rows):
            for j in range(cols):
                this_square = warehouse[i][j]

                if this_square == '.':
                    self.warehouse_state[i][j] = '.'

                elif this_square == '#':
                    self.warehouse_state[i][j] = '#'

                elif this_square == '@':
                    self.warehouse_state[i][j] = '*'
                    self.dropzone = (i, j)

                else:  # a box
                    box_id = this_square
                    self.warehouse_state[i][j] = box_id
                    self.boxes[box_id] = (i, j)

        self.robot_position = self.dropzone
        self.box_held = None

    def heuristic(self, location, goal):
        num_rows = abs(goal[0] - location[0])
        num_cols = abs(goal[1] - location[1])
        heuristic = num_rows + num_cols
        return heuristic
    
    def _search(self, init, goal, debug=False):
        """
        This method should be based on Udacity Quizes for A*, see Lesson 12, Section 10-12.
        The bulk of the search logic should reside here, should you choose to use this starter code.
        Please condition any printout on the debug flag provided in the argument.  
        You may change this function signature (i.e. add arguments) as 
        necessary, except for the debug argument which must remain with a default of False
        """
      
        # below code are mostly referenced to lesson 12 quiz 12

        grid = self.warehouse_state
        wall = ['#']
        closed = [[0 for col in range(len(grid[0]))] for row in range(len(grid))]
        action = [[-1 for col in range(len(grid[0]))] for row in range(len(grid))]
        closed[init[0]][init[1]] = 1

        x = init[0]
        y = init[1]
        g = 0
        f = g + self.heuristic((x, y), goal)

        open = [[f, g, x, y]]
        found = False  # flag that is set when search is complete
        resign = False  # flag set if we can't find expand

        while not found and not resign:
            if len(open) == 0:
                resign = True
                return 'fail'
            else:
                open.sort()
                open.reverse()
                next = open.pop()
                x = next[2]
                y = next[3]
                g = next[1]

                if x == goal[0] and y == goal[1]:
                    found = True
                else:
                    for i in range(len(self.delta)):
                        cost = self.delta_cost[i]
                        x2 = x + self.delta[i][0]
                        y2 = y + self.delta[i][1]

                        if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]):
                            if closed[x2][y2] == 0 and grid[x2][y2] not in wall:
                                g2 = g + cost
                                f2 = g2 + self.heuristic((x2, y2), goal)
                                open.append([f2, g2, x2, y2])
                                closed[x2][y2] = 1
                                action[x2][y2] = i

        if init == goal:
            for i in range(len(self.delta)):
                x2 = init[0] + self.delta[i][0]
                y2 = init[1] + self.delta[i][1]
                if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2] not in wall:
                    return (x2, y2), ['move {}'.format(self.delta_directions[i])], self.delta_directions[i+2]

        x = goal[0] - self.delta[action[goal[0]][goal[1]]][0]
        y = goal[1] - self.delta[action[goal[0]][goal[1]]][1]
        prior_to_goal_location = (x, y)
        direction_on_goal_location = self.delta_directions[action[goal[0]][goal[1]]]

        optimal_path = []
        while (x, y) != (init[0], init[1]):
            optimal_path = ['move {}'.format(self.delta_directions[action[x][y]])] + optimal_path
            x2 = x - self.delta[action[x][y]][0]
            y2 = y - self.delta[action[x][y]][1]
            x = x2
            y = y2

        return prior_to_goal_location, optimal_path, direction_on_goal_location
  
    def plan_delivery(self, debug = False):
        """
        plan_delivery() is required and will be called by the autograder directly.  
        You may not change the function signature for it.
        Add logic here to find the moves.  You may use the starter code provided above
        in any way you choose, but please condition any printouts on the debug flag
        """
        moves = []
        robot_location = self.dropzone

        while self.todo:
            box_id = self.todo[0]
            box_location = self.boxes[box_id]

            # search the path to the box
            robot_location, next_move, direction_on_goal_location = self._search(robot_location, box_location)
            moves += next_move

            # pick up the box
            moves += ['lift {}'.format(box_id)]

            # search path to the dropzone
            robot_location, next_move, direction_on_goal_location = self._search(robot_location, self.dropzone)
            moves += next_move

            # drop box to the dropzone
            moves += ['down {}'.format(direction_on_goal_location)]
            self.todo.remove(box_id)

        if debug:
            for i in range(len(moves)):
                print(moves[i])

        return moves


class DeliveryPlanner_PartB:

    """
    Required methods in this class are:

        plan_delivery(self, debug = False) which is stubbed out below.
        You may not change the method signature as it will be called directly
        by the autograder but you may modify the internals as needed.

        __init__: required to initialize the class.  Starter code is
        provided that intializes class variables based on the definitions in
        testing_suite_partB.py.  You may choose to use this starter code
        or modify and replace it based on your own solution

    The following methods are starter code you may use for part B.
    However, they are not required and can be replaced with your
    own methods.

        _set_initial_state_from(self, warehouse): creates structures based on
            the warehouse and todo definitions and intializes the robot
            location in the warehouse

        _find_policy(self, debug=False): Where the bulk of the A* search algorithm
            could reside.  It should find an optimal path from the robot
            location to a goal.  Hint:  you may want to structure this based
            on whether looking for a box or delivering a box.

    """

    # Definitions taken from testing_suite_partA.py
    ORTHOGONAL_MOVE_COST = 2
    DIAGONAL_MOVE_COST = 3
    BOX_LIFT_COST = 4
    BOX_DOWN_COST = 2
    ILLEGAL_MOVE_PENALTY = 100

    def __init__(self, warehouse, warehouse_cost, todo):

        self.todo = todo
        self.boxes_delivered = []
        self.total_cost = 0
        self._set_initial_state_from(warehouse)
        self.warehouse_cost = warehouse_cost

        self.delta = [[-1, 0],  # go up
                        [0, -1],  # go left
                        [1, 0],  # go down
                        [0, 1],  # go right
                        [-1, -1],  # up left (diag)
                        [-1, 1],  # up right (diag)
                        [1, 1],  # dn right (diag)
                        [1, -1]]  # dn left (diag)

        self.delta_directions = ["n", "w", "s", "e", "nw", "ne", "se", "sw"]

        # Use this for a visual debug
        self.delta_name = ['^', '<', 'v', '>', '\\', '/', '[', ']']

        # Costs for each move
        self.delta_cost = [self.ORTHOGONAL_MOVE_COST,
                        self.ORTHOGONAL_MOVE_COST,
                        self.ORTHOGONAL_MOVE_COST,
                        self.ORTHOGONAL_MOVE_COST,
                        self.DIAGONAL_MOVE_COST,
                        self.DIAGONAL_MOVE_COST,
                        self.DIAGONAL_MOVE_COST,
                        self.DIAGONAL_MOVE_COST]

    # state parsing and initialization function from testing_suite_partA.py
    def _set_initial_state_from(self, warehouse):
        """Set initial state.

        Args:
            warehouse(list(list)): the warehouse map.
        """
        rows = len(warehouse)
        cols = len(warehouse[0])

        self.warehouse_state = [[None for j in range(cols)] for i in range(rows)]
        self.dropzone = None
        self.boxes = dict()

        for i in range(rows):
            for j in range(cols):
                this_square = warehouse[i][j]

                if this_square == '.':
                    self.warehouse_state[i][j] = '.'

                elif this_square == '#':
                    self.warehouse_state[i][j] = '#'

                elif this_square == '@':
                    self.warehouse_state[i][j] = '*'
                    self.dropzone = (i, j)

                else:  # a box
                    box_id = this_square
                    self.warehouse_state[i][j] = box_id
                    self.boxes[box_id] = (i, j)

    def _find_policy(self, goal, pickup_box=True, debug=False):
        """
        This method should be based on Udacity Quizes for Dynamic Progamming,
        see Lesson 12, Section 14-20 and Problem Set 4, Question 5.  The bulk of
        the logic for finding the policy should reside here should you choose to
        use this starter code.  Please condition any printout on the debug flag
        provided in the argument. You may change this function signature
        (i.e. add arguments) as necessary, except for the debug argument which
        must remain with a default of False
        """

        ##############################################################################
        # insert code in this method if using the starter code we've provided
        ##############################################################################


        # get a shortcut variable for the warehouse (note this is just a view no copying)
        grid = self.warehouse_state
        grid_costs = self.warehouse_cost

        # These following code are referenced to lesson 12 quiz 18
        value = [[999 for row in range(len(grid[0]))] for col in range(len(grid))]
        action = [[-1 for row in range(len(grid[0]))] for col in range(len(grid))]
        policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
        wall = ['#']
        box_id = self.todo[0]

        if pickup_box:
            change = True
            while change:
                change = False

                for x in range(len(grid)):
                    for y in range(len(grid[0])):
                        if grid[x][y] in wall:
                            policy[x][y] = -1
                        if goal[0] == x and goal[1] == y:
                            if value[x][y] > 0:
                                value[x][y] = 0
                                change = True
                                policy[x][y] = 'B'

                        elif grid[x][y] not in wall:
                            for i in range(len(self.delta)):
                                x2 = x + self.delta[i][0]
                                y2 = y + self.delta[i][1]

                                if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2] not in wall:
                                    v2 = value[x2][y2] + self.delta_cost[i] + grid_costs[x2][y2]
                                    action[x2][y2] = i

                                    if v2 < value[x][y]:
                                        change = True
                                        value[x][y] = v2
                                        policy[x][y] = 'move' + ' ' + self.delta_directions[i]

            for j in range(len(self.delta)):
                adjacent_x = goal[0] + self.delta[j][0]
                adjacent_y = goal[1] + self.delta[j][1]
                if adjacent_x >= 0 and adjacent_x < len(grid) and adjacent_y >= 0 and adjacent_y < len(grid[0]) and grid[adjacent_x][adjacent_y] not in wall:
                    policy[adjacent_x][adjacent_y] = 'lift' + ' ' + box_id

        else:
            change = True
            while change:
                change = False
                for x in range(len(grid)):
                    for y in range(len(grid[0])):
                        if grid[x][y] in wall:
                            policy[x][y] = -1

                        if goal[0] == x and goal[1] == y:
                            if value[x][y] > 0:
                                value[x][y] = 0
                                change = True
                                policy[x][y] = 'move' + ' ' + self.delta_directions[0]

                        elif grid[x][y] not in wall:
                            for i in range(len(self.delta)):
                                x2 = x + self.delta[i][0]
                                y2 = y + self.delta[i][1]

                                if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2] not in wall:
                                    v2 = value[x2][y2] + self.delta_cost[i] + grid_costs[x2][y2]
                                    action[x2][y2] = i

                                    if v2 < value[x][y]:
                                        change = True
                                        value[x][y] = v2
                                        policy[x][y] = 'move' + ' ' + self.delta_directions[i]

            for i in range(len(self.delta)):
                adjacent_x = goal[0] + self.delta[i][0]
                adjacent_y = goal[1] + self.delta[i][1]
                if adjacent_x >= 0 and adjacent_x < len(grid) and adjacent_y >= 0 and adjacent_y < len(grid[0]) and grid[adjacent_x][adjacent_y] not in wall:
                    j = self.delta.index([-1 * self.delta[i][0], -1 * self.delta[i][1]])
                    policy[adjacent_x][adjacent_y] = 'down' + ' ' + self.delta_directions[j]

        return policy

    def plan_delivery(self, debug=False):
        """
        plan_delivery() is required and will be called by the autograder directly.  
        You may not change the function signature for it.
        Add logic here to find the policies:  First to the box from any grid position
        then to the dropzone, again from any grid position.  You may use the starter
        code provided above in any way you choose, but please condition any printouts
        on the debug flag
        """
        ###########################################################################
        # Following is an example of how one could structure the solution using
        # the starter code we've provided.
        ###########################################################################
        goal = self.boxes['1']

        # search the path to the box
        to_box_policy = self._find_policy(goal, True)

        # search the path to the dropzone
        deliver_policy = self._find_policy(self.dropzone, False)

        if debug:
            print("\nTo Box Policy:")
            for i in range(len(to_box_policy)):
                print(to_box_policy[i])

            print("\nDeliver Policy:")
            for i in range(len(deliver_policy)):
                print(deliver_policy[i])

            print("\n\n")

        return to_box_policy, deliver_policy


if __name__ == "__main__":
    """ 
    You may execute this file to develop and test the search algorithm prior to running 
    the delivery planner in the testing suite.  Copy any test cases from the
    testing suite or make up your own.
    Run command:  python warehouse.py
    """

    # Test code in here will not be called by the autograder

    # Testing for Part A
    # testcase 1
    # warehouse = ['1#2',
    #             '.#.',
    #             '..@']
    #
    # todo =  ['1','2']
    warehouse = ['..1.',
                 '..@.',
                 '....',
                 '2...']
    todo = ['1', '2']
    partA = DeliveryPlanner_PartA(warehouse, todo)
    partA.plan_delivery(debug=True)

    # Testing for Part B
    # testcase 1
    warehouse = ['1..',
                 '.#.',
                 '..@']

    warehouse_cost = [[0, 5, 2],
                      [10, math.inf, 2],
                      [2, 10, 2]]

    todo = ['1']

    partB = DeliveryPlanner_PartB(warehouse, warehouse_cost, todo)
    partB.plan_delivery(debug=True)







