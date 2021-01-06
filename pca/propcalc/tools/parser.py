# @Author: GKarseras
# @Date:   17 Nov 2020 10:30

from lark import Lark, Transformer


GRAMMAR = '''
             ?exp_iff: exp_imp (OP_EQUIVALENCE exp_imp)*
             ?exp_imp: exp_or (OP_IMPLICATION exp_or)*
             ?exp_or: exp_and (OP_DISJUNCTION exp_and)*
             ?exp_and: exp_not (OP_CONJUNCTION exp_not)*
             ?exp_not: OP_NEGATION exp_not                  -> exp_not
                     | atom
             atom: VAR                                      -> atom_var
                 | TRUE                                     -> atom_true
                 | FALSE                                    -> atom_false
                 | "(" exp_iff ")"                          -> atom_paren
            
             VAR: /[A-Z]+/
             TRUE: "true" | "top" | "t" | "\u22a4"
             FALSE: "false" | "bot" | "f" | "\u22A5"
             OP_CONJUNCTION: "and" | "\u2227" | "\u00B7" | "\u0026"
             OP_DISJUNCTION: "or" | "\u2228" | "\u002B" | "\u2225"
             OP_NEGATION: "not" | "\u00AC" | "\u0021" | "\u02DC"
             OP_IMPLICATION: "implies" | "\u21D2" | "\u2192"
             OP_EQUIVALENCE: "iff" | "\u21D4" | "\u2194"
            
             %import common.WS
             %ignore WS
         '''

PARSER = Lark(GRAMMAR, parser='lalr', start='exp_iff')


class SimpleTransformer(Transformer):

    def __init__(self):
        super().__init__()
        self._prop_vars = []

    def atom_var(self, value):
        val = value[0]
        if val not in self._prop_vars:
            self._prop_vars.append(val)
        return value

    @property
    def prop_vars(self):
        return self._prop_vars
