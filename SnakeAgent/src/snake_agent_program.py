"""
You can import modules if you need
NOTE:
your code must function properly without 
requiring the installation of any additional 
dependencies beyond those already included in 
the Python package une_ai
"""
# import ...
from queue import Queue
import random

from snake_agent import SnakeAgent
from une_ai.models import GridMap, GraphNode

w_env = 64
h_env = 48

environment_map = GridMap(w_env, h_env, None)

ACTIONS = {
    'move-up': (0, -1),
    'move-down': (0, 1),
    'move-left': (-1, 0),
    'move-right': (1, 0)
}
ILLEGAL_MOVES = {
    "move-up": "move-down",
    "move-down": "move-up",
    "move-left": "move-right",
    "move-right": "move-left"
}

path_to_food = []
body_location = []
goal_node = None
mouth_flag = False

DIRECTIONS = SnakeAgent.DIRECTIONS

def is_food(node_state):
    global environment_map
    state_value = environment_map.get_item_value(node_state[0], node_state[1])
    if state_value == "F":
        return True
    else:
        return False
    
def is_legal_square(node_state):
    global environment_map
    state_value = environment_map.get_item_value(node_state[0], node_state[1])
    if state_value == None:
        return True
    else:
        return False
    
def edge_case_beater(legal_square_function, next_action_direction, agent_location):
    filter_moves = list(ACTIONS.keys())
    filter_moves.remove(next_action_direction)
    legal_moves = []

    for move in filter_moves:
        dx, dy = ACTIONS[move]
        new_x = agent_location[0] + dx
        new_y = agent_location[1] + dy

        try:
            if legal_square_function((new_x, new_y)):
                legal_moves.append(move)
        except:
            continue

    if legal_moves:
        return random.choice(legal_moves)
    else:
        print("Edge case failed... we might be cooked")
        return None   



def expand(node):
    global environment_map
    successors = []
    cur_state = node.get_state()
    last_action = node.get_action()

    for action, offset in ACTIONS.items():
        if last_action and action == ILLEGAL_MOVES.get(last_action):
            continue

        new_x, new_y = cur_state[0] + offset[0], cur_state[1] + offset[1]

        try:
            item = environment_map.get_item_value(new_x, new_y)
        except:
            continue 

        if item in ['W', 'S']:
            continue

        cost = 1
        successor = GraphNode((new_x, new_y), node, action, cost)
        successors.append(successor)

    return successors

def bfs(start_coords, goal_function): ### code implemented from UNE AI workshop 3

    initial_state = GraphNode(start_coords, None, None, 0)
    if goal_function(initial_state.get_state()):
        return initial_state
    frontier = Queue()
    frontier.put(initial_state)
    reached = [initial_state.get_state()]
    while frontier.qsize() > 0:
        cur_node = frontier.get()
        successors = expand(cur_node)
        for successor in successors:
            if goal_function(successor.get_state()):
                return successor
            successor_state = successor.get_state()
            if successor_state not in reached:
                reached.append(successor_state)
                frontier.put(successor)
        
    return False

"""
TODO:
You must implement this function with the
agent program for your snake agent.
Please, make sure that the code and implementation 
of your agent program reflects the requirements in
the assignment. Deviating from the requirements
may result to score a 0 mark in the
agent program criterion.

Please, do not change the parameters of this function.
"""


def snake_agent_program(percepts, actuators):
    global path_to_food
    global goal_node
    global mouth_flag
    actions = []
    body_location = percepts["body-sensor"]
    food_location = percepts["food-sensor"]
    wall_location = percepts["obstacles-sensor"]
    
    ### setting map values
    for x in range(w_env):
        for y in range(h_env):
            environment_map.set_item_value(x, y, None)
            
    for wall in wall_location:
        environment_map.set_item_value(wall[0], wall[1], "W")


    for food in food_location:
        environment_map.set_item_value(food[0], food[1], "F")


    for body_part in body_location:
        environment_map.set_item_value(body_part[0], body_part[1], "S")


    #num_s_grid = 0
    #for tile in environment_map.find_value("S"):
       # num_s_grid += 1

    #print(f"Number of body parts = {len(body_location)} \n Number of stale S state = {num_s_grid}")

    head_location = body_location[0]
    #print(head_location)
    cur_direction = actuators["head"]
    next_action_direction = "move-{0}".format(cur_direction)

    if mouth_flag:
        if path_to_food:
            actions.append(path_to_food.pop(0)) 
        actions.append("close-mouth")
        mouth_flag = False
        print("Closed the mouth")
        return actions
    
    if food_location:
        if len(path_to_food) == 0:
                goal_node = bfs(head_location, is_food)
                if goal_node != None:
                    print("Search was successful!")
                    path_to_food, _ = goal_node.get_path()
                    print(f"Current direction: {cur_direction} \n Path: {path_to_food}")

            
        if path_to_food:
            next_action_direction = path_to_food.pop(0)
            if next_action_direction == ILLEGAL_MOVES.get("move-{0}".format(cur_direction)):
                print("Edge case start.. Removed illegal move")
                path_to_food = []
                goal_node = None
                last_resort = edge_case_beater(is_legal_square, next_action_direction, head_location)
                actions.append(last_resort)
                return actions
            else:
                if len(path_to_food) == 0 and mouth_flag == False:
                    actions.append("open-mouth")
                    print("Opened the mouth")
                    mouth_flag = True
                    return actions
                else:
                    actions.append(next_action_direction)

    return actions