# @Author: GKarseras
# @Date:   22 Feb 17:10

from pca_main import pcabuilder

satisfiable = [
    {
        'question': "Are the following propositions satisfiable? Answer in either true or false",
        'eval_methods': [pcabuilder.InitProp.satisfiable.__name__],
        'props': ['Q and false', 'Q or (P or R)', 'Q or P', 'Q ∧ (P ⇔ Q)']
    }
]

involution = [
    {
        'question': "Using the Involution law, which removes double negations, "
                    "simplify the propositions below",
        'eval_methods': [pcabuilder.InitProp.involution.__name__],
        'props': ['not not A', 'not (not not (Q or not not P))']
    }
]

max_min = [
    {
        'question': "Using the Minimum Law, simplify the following propositions",
        'eval_methods': [pcabuilder.InitProp.minimum.__name__],
        'props': ['A or false', 'A and (B or false)']
    },
    {
        'question': "Using the Maximum law, simplify the propositions below",
        'eval_methods': [pcabuilder.InitProp.maximum.__name__],
        'props': ['A or true', 'A and (B or true)']
    }
]
de_morgan = [
    {
        'question': "Apply De Morgan's law to the following propositions",
        'eval_methods': [pcabuilder.InitProp.de_morgan.__name__],
        'props': ['Q or P', 'Q or (P or R)']
    },
    {
        'question': "Apply De Morgan's and then Involution law to simplify the following propositions",
        'eval_methods': [pcabuilder.InitProp.de_morgan.__name__, pcabuilder.InitProp.involution.__name__],
        'props': ['not (Q or P)', 'Q or not(P)']
    }
]

exercises = {
    'satisfiable': satisfiable,
    'involution': involution,
    'max_min': max_min,
    'de_morgan': de_morgan,
}
