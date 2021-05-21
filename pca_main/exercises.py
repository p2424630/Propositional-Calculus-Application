# @Author: GKarseras
# @Date:   22 Feb 17:10

from pca_main import pcabuilder


SATISFIABLE = [
    {
        'question': "Are the propositions satisfiable? Answer in either true or false",
        'eval_methods': [pcabuilder.InitProp.satisfiable.__name__],
        'props': ['false', 'true or false', 'true and (false and true)']
    },
    {
        'question': "Are the following propositions satisfiable? "
                    "There exists an interpretation which results in true",
        'eval_methods': [pcabuilder.InitProp.satisfiable.__name__],
        'props': ['Q and false', 'Q or (P or R)', 'Q or P', 'Q ∧ (P ⇔ Q)']
    }
]

INVOLUTION = [
    {
        'question': "Using the Involution law, which removes double negations, "
                    "simplify the propositions below",
        'eval_methods': [pcabuilder.InitProp.involution.__name__],
        'props': ['not not A', 'not (not not (Q or not not P))']
    }
]

MAX_MIN = [
    {
        'question': "Using the Minimum Law, simplify the following propositions",
        'eval_methods': [pcabuilder.InitProp.minimum.__name__],
        'props': ['A or false', 'A and (B or false)']
    },
    {
        'question': "Using the Maximum law, simplify the propositions below",
        'eval_methods': [pcabuilder.InitProp.maximum.__name__],
        'props': ['A or true', 'A and (B or true)']
    },
    {
        'question': "Using Both Maximum and Minimum law, simplify the propositions below",
        'eval_methods': [pcabuilder.InitProp.minimum.__name__, pcabuilder.InitProp.maximum.__name__],
        'props': ['(A or true) and false', '(B and false) or (B and true)']
    }
]

DE_MORGAN = [
    {
        'question': "Apply De Morgan's law to the following propositions",
        'eval_methods': [pcabuilder.InitProp.de_morgan.__name__],
        'props': ['Q or P', 'Q and not P', 'Q or (P and R)']
    }
]

IDEMPOTENCE = [
    {
        'question': "Using Idempotence law, create the equivalence of the following Propositions",
        'eval_methods': [pcabuilder.InitProp.idempotence.__name__],
        'props': ['P and P', 'Q or P']
    }
]

COMMUTATIVITY = [
    {
        'question': "Apply Commutativity law on the following Propositions",
        'eval_methods': [pcabuilder.InitProp.commutativity.__name__],
        'props': ['P and Q', 'P iff Q', '(P and Q) and (Q or P)']
    }
]

TAUTOLOGY = [
    {
        'question': "Determine if the following Propositions are a Tautology. The result is true all interpretations",
        'eval_methods': [pcabuilder.InitProp.tautology.__name__],
        'props': ['P and Q', 'P or not P']
    }
]

CONTRADICTION = [
    {
        'question': "Determine if the following Propositions are a Contradiction. The result is never true for any interpretation",
        'eval_methods': [pcabuilder.InitProp.contradiction.__name__],
        'props': ['P or Q', 'P and not P']
    }
]

IMPLICATION = [
    {
        'question': "Apply the Implication law and transform the following Propositions",
        'eval_methods': [pcabuilder.InitProp.implication.__name__],
        'props': ['P implies Q', 'P implies (Q implies R)']
    }
]

COMBINATIONS = [
    {
        'question': "Apply De Morgan's and then Involution law to simplify the following propositions",
        'eval_methods': [pcabuilder.InitProp.de_morgan.__name__, pcabuilder.InitProp.involution.__name__],
        'props': ['not (Q or P)', 'Q or not P']
    },
    {
        'question': "Apply Involution law and then commutativity to the following propositions",
        'eval_methods': [pcabuilder.InitProp.involution.__name__, pcabuilder.InitProp.commutativity.__name__],
        'props': ['not not Q or P', 'Q or not not (P and R)']
    }
]

EXERCISES = {
    'SATISFIABLE': SATISFIABLE,
    'TAUTOLOGY': TAUTOLOGY,
    'CONTRADICTION': CONTRADICTION,
    'COMMUTATIVITY': COMMUTATIVITY,
    'IDEMPOTENCE': IDEMPOTENCE,
    'INVOLUTION': INVOLUTION,
    'MAX_MIN': MAX_MIN,
    'DE_MORGAN': DE_MORGAN,
    'IMPLICATION': IMPLICATION,
    'COMBINATIONS': COMBINATIONS
}
