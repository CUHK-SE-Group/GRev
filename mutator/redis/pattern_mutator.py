from mutator.redis.pattern_transformer import *
from mutator.redis.mutator_helper_redis import RedisMutatorHelper


class PatternMutator:
    @staticmethod
    def gen_pattern(pattern: str):
        pt = PatternTransformer()
        asg = pt.pattern_to_asg(pattern)
        return pt.asg_to_pattern(asg)

    @staticmethod
    def rev_pattern(pattern: str):
        rmh = RedisMutatorHelper()
        return rmh.reverse_path(pattern)
