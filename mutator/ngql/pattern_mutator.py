from mutator.ngql.pattern_transformer import *
from mutator.ngql.helpers import *

class PatternMutator:
    def gen_pattern(self, pattern : str):
        pt = PatternTransformer()
        asg = pt.pattern_to_asg(pattern)
        return pt.asg_to_pattern(asg)

    def rev_pattern(self, pattern : str):
        return reverse_path(pattern)

if __name__ == "__main__":
    mutator = PatternMutator()
    print("OK")