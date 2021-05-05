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
        'props': ['Q or P', 'Q and not P', 'Q or (P and R)']
    }
]

idempotence = [
    {
        'question': "Using Idempotence law create the equavelence of the following Propositions",
        'eval_methods': [pcabuilder.InitProp.idempotence.__name__],
        'props': ['P and P', '(Q and P) or (Q and P)']
    }
]

commutativity = [
    {
        'question': "Apply Commutativity law on the following Propositions",
        'eval_methods': [pcabuilder.InitProp.commutativity.__name__],
        'props': ['P and Q', '(P and Q) and (Q or P)', 'P iff Q']
    }
]

tautology = [
    {
        'question': "Determine if the following Propositions are a Tautology - for all interpretations the final "
                    "result is True",
        'eval_methods': [pcabuilder.InitProp.tautology.__name__],
        'props': ['P and Q', 'P or not P']
    }
]

contradiction = [
    {
        'question': "Determine if the following Propositions are a Contradiction - for all interpretations the final "
                    "result is False",
        'eval_methods': [pcabuilder.InitProp.contradiction.__name__],
        'props': ['P or Q', 'P and not P']
    }
]

implication = [
    {
        'question': "Apply the Implication law and transform the following Propositions",
        'eval_methods': [pcabuilder.InitProp.implication.__name__],
        'props': ['P implies Q', 'P implies (Q implies R)']
    }
]

combinations = [
    {
        'question': "Apply De Morgan's and then Involution law to simplify the following propositions",
        'eval_methods': [pcabuilder.InitProp.de_morgan.__name__, pcabuilder.InitProp.involution.__name__],
        'props': ['not (Q or P)', f'Q or not P']
    },
    {
        'question': "Apply Involution law and then commutativity to the following propositions",
        'eval_methods': [pcabuilder.InitProp.involution.__name__, pcabuilder.InitProp.commutativity.__name__],
        'props': ['not not Q or P', f'Q or not not (P and R)']
    }
]

exercises = {
    'idempotence': idempotence,
    'satisfiable': satisfiable,
    'tautology': tautology,
    'contradiction': contradiction,
    'involution': involution,
    'max_min': max_min,
    'de_morgan': de_morgan,
    'commutativity': commutativity,
    'implication': implication,
    'combinations': combinations
}
