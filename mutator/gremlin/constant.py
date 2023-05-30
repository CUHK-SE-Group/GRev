import random
import string
from configs.conf import new_logger, config


class Constant_Generator:
    def __init__(self, max_count = 10000000): 
        self.max_count = max_count
        self.logger = new_logger("logs/gremlin.log")

    def Generate(self, my_type):
        '''
        Given the type that the constant belongs, return (x, y),
        where x denotes the constant value store in python,
        ans y denotes the constant value in the string format.
        '''
        
        if my_type == "count":
            value = random.randint(0, self.max_count)
            return (value, str(value))
        if my_type == "integer":
            value = random.randint(-(2 ** 31), (2 ** 31) - 1)
            return (value, str(value))
        if my_type == "long":
            value = random.randint(-(2 ** 63), (2 ** 63) - 1)
            return (value, str(value))
        if my_type == "float" or my_type == "double":
            if random.randint(1, 2) > 1:
                value = random.random() * random.randint(-(2 ** 63), (2 ** 63) - 1)
                return (value, str(value))
            else:
                index = random.randint(0, 2)
                Types = [(float("inf"), "Double.POSITIVE_INFINITY"), \
                         (float("-inf"), "Double.NEGATIVE_INFINITY"), \
                         (float("NaN"), "Double.NaN")
                        ]
                return Types[index]
            
        if my_type == "boolean":
            if random.randint(0, 1) == 1: return (True, "true")
            else: return (False, "false")
        if my_type == "string":
            length = random.randint(1, 20)
            ran = ''.join(random.choices( \
                string.ascii_uppercase + string.ascii_lowercase + string.digits, k = length))
            return (ran, '"' + ran + '"')
        
        self.logger.error("Unknown type in Generating Constant:" + my_type)
        raise ValueError

if __name__ == "__main__":
    CG = Constant_Generator()
