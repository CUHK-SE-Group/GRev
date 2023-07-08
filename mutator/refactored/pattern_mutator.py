from mutator.refactored.pattern_transformer import *
from mutator.refactored.mutator_helper_refactored import RefactoredMutatorHelper


class PatternMutator:
    def gen_pattern(self, pattern : str):
        pt = PatternTransformer()
        asg = pt.pattern_to_asg(pattern)
        return pt.asg_to_pattern(asg)

    def rev_pattern(self, pattern : str):
        rmh = RefactoredMutatorHelper()
        return rmh.reverse_path(pattern)
