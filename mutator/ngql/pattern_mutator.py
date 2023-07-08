from mutator.ngql.pattern_transformer import *
from mutator.ngql.mutator_helper_ngql import NGQLMutatorHelper


class PatternMutator:
    @staticmethod
    def gen_pattern(pattern: str):
        pt = PatternTransformer()
        asg = pt.pattern_to_asg(pattern)
        return pt.asg_to_pattern(asg)

    @staticmethod
    def rev_pattern(pattern: str):
        nmh = NGQLMutatorHelper()
        return nmh.reverse_path(pattern)
