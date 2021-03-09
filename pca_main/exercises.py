# @Author: GKarseras
# @Date:   22 Feb 17:10

# class Exercise:
#
#     def __init__(self, prop, question):
#         self.prop = prop
#         self.question = question
#
#
# class DeMorgan(Exercise):
#     pass
from pca_main import pcabuilder


de_morgan = [
    {
        'question': "Apply De Morgan's law to the following propositions",
        'eval_method': pcabuilder.InitProp.de_morgan.__name__,
        'props': ['Q or (P or R)', 'Q or P']
    },
    {
        'question': "Ex2",
        'eval_method': pcabuilder.InitProp.de_morgan.__name__,
        'props': ['Q or (P or R)', 'Q or P']
    }
]

involution = [
    {
        'question': "Using the Involution law, which removes obsolete double negations, "
                    "simplify the propositions below",
        'eval_method': pcabuilder.InitProp.involution.__name__,
        'props': ['not not A', 'not (not not (Q or not not P))']
    }
]

max_min = [
    {
        'question': "Using the Minimum Law, simplify the following propositions",
        'eval_method': pcabuilder.InitProp.minimum.__name__,
        'props': ['A or false', 'A and (B or false)']
    },
    {
        'question': "Using the Maximum law, simplify the propositions below",
        'eval_method': pcabuilder.InitProp.maximum.__name__,
        'props': ['A or true', 'A and (B or true)']
    }
]

exer = {
    'de_morgan': de_morgan,
    'involution': involution,
    'max_min': max_min
}
