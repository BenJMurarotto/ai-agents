from une_ai.models import Agent
import numbers

class SnakeAgent(Agent):

    DIRECTIONS = ["up", "down", "left", "right"]
    # DO NOT CHANGE THE PARAMETERS OF THIS METHOD
    def __init__(self, agent_program):
        # DO NOT CHANGE THE FOLLOWING LINES OF CODE
        super().__init__("Snake Agent", agent_program)

        """
        If you need to add more instructions
        in the constructor, you can add them here
        """

    """
    TODO:
    In order for the agent to gain access to all 
    the sensors specified in the assignment's 
    requirements, it is essential to implement 
    this method.
    You can add a single sensor with the method:
    self.add_sensor(sensor_name, initial_value, validation_function)
    """
    def body_sensor_validation(self, v):
        if isinstance(v, list):
            for body_tuple in v:
                if isinstance(body_tuple, tuple) and len(body_tuple) == 2:
                    if all(isinstance(coord, numbers.Number) for coord in body_tuple):
                        continue
                    else:
                        return False
                else:
                    return False
            return True
        return False
    
    def food_sensor_validation(self, v):
        if isinstance(v, list):
            for food_tuple in v:
                if isinstance(food_tuple, tuple) and len(food_tuple) == 3:
                    if all(isinstance(coord, numbers.Number) for coord in food_tuple):
                        continue
                    else:
                        return False
                else:
                    return False
            return True
        return False       

    def obstacle_sensor_validation(self, v): ## may need to change this to implement check for body sensor
        if not isinstance(v, list):
            return False
        for coord in v:
            if not (isinstance(coord, tuple) and len(coord) == 2):
                return False
            x, y = coord
            if not (isinstance(x, int) and isinstance(y, int)):
                return False
        return True

        
    def add_all_sensors(self):
        self.add_sensor(sensor_name="body-sensor",
                        initial_value=[(0, 0), (0, 1), (0, 2)],
                        validation_function=self.body_sensor_validation)
        self.add_sensor(sensor_name="food-sensor",
                        initial_value=[(0, 0, 0)],
                        validation_function=self.food_sensor_validation)
        self.add_sensor(sensor_name="obstacles-sensor",
                        initial_value=[(0, 0)],
                        validation_function=self.obstacle_sensor_validation)
        self.add_sensor(sensor_name="clock",
                        initial_value=0,
                        validation_function=lambda v: isinstance(v, int))
        
       
        pass

    """
    TODO:
    In order for the agent to gain access to all 
    the actuators specified in the assignment's 
    requirements, it is essential to implement 
    this method.
    You can add a single actuator with the method:
    self.add_actuator(actuator_name, initial_value, validation_function)
    """

    def get_head(self):
        return self.read_actuator_value("head")
    def add_all_actuators(self):
        self.add_actuator(actuator_name="head",
                            initial_value="up",
                            validation_function=lambda v: v in SnakeAgent.DIRECTIONS)
        self.add_actuator(actuator_name="mouth",
                          initial_value="close",
                          validation_function=lambda v: v == "open" or v == "close")
        pass

    """
    TODO:
    In order for the agent to gain access to all 
    the actions specified in the assignment's 
    requirements, it is essential to implement 
    this method.
    You can add a single action with the method:
    self.add_action(action_name, action_function)
    """
    def add_all_actions(self):

        self.add_action(action_name="move-up",
                        action_function=lambda: {"head": "up"} if self.get_head() != "down" else {})
        self.add_action(action_name="move-down",
                        action_function=lambda: {"head": "down"} if self.get_head() != "up" else {})
        self.add_action(action_name="move-left",
                        action_function=lambda: {"head": "left"} if self.get_head() != "right" else {})
        self.add_action(action_name="move-right",
                        action_function=lambda: {"head": "right"} if self.get_head() != "left" else {})
        self.add_action(action_name="open-mouth",
                        action_function=lambda: {"mouth": "open"})
        self.add_action(action_name="close-mouth",
                        action_function=lambda: {"mouth": "close"})





