import string
import random

class ConstantGenerator:
    
    def gen(self, mytype):
        if mytype == "int":
            value = random.randint(-(2 ** 63), (2 ** 63) - 1)
            return str(value)
        if mytype == "float":
            value = random.random() * random.randint(-(2 ** 63), (2 ** 63) - 1)
            return format(value, '.20f')
            
        if mytype == "bool":
            if random.randint(0, 1) == 1: return "true"
            else: return "false"
        
        if mytype == "string":
            length = random.randint(1, 20)
            ran = ''.join(random.choices( \
                string.ascii_uppercase + string.ascii_lowercase + string.digits, k = length))
            return '"' + ran + '"'
