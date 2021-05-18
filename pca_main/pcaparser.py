# @Author: GKarseras
# @Date:   17 Nov 2020 10:30

from lark import Lark, Transformer
from pca_main import pcaprop


GRAMMAR = '''
             ?exp_iff: exp_implies (OP_EQUIVALENCE exp_implies)*
             ?exp_implies: exp_or (OP_IMPLICATION exp_or)*
             ?exp_or: exp_and (OP_DISJUNCTION exp_and)*
             ?exp_and: atom (OP_CONJUNCTION atom)*
             atom: OP_NEGATION atom                      -> exp_not
                  | VAR                                  -> atom_var
                  | TRUE                                 -> atom_true
                  | FALSE                                -> atom_false
                  | "(" exp_iff ")"                      -> atom_paren
            
             VAR: /[A-Z]+/
             TRUE: "true" | "top" | "\u22a4"
             FALSE: "false" | "bot" | "\u22A5"
             OP_CONJUNCTION: "and" | "\u2227" | "\u00B7"
             OP_DISJUNCTION: "or" | "\u2228" | "\u002B" | "\u2225"
             OP_NEGATION: "not" | "\u00AC" | "\u0021" | "\u02DC"
             OP_IMPLICATION: "implies" | "\u21D2" | "\u2192"
             OP_EQUIVALENCE: "iff" | "\u21D4" | "\u2194"
            
             %import common.WS
             %ignore WS
         '''


class PropTransformer(Transformer):

    def exp_iff(self, value):
        if len(value) == 3:
            return pcaprop.EquivalenceOp(value[0], value[2])
        return self._rec_object(value, 'exp_iff')

    def exp_implies(self, value):
        if len(value) == 3:
            return pcaprop.ImplicationOp(value[0], value[2])
        return self._rec_object(value, 'exp_implies')

    def exp_or(self, value):
        if len(value) == 3:
            return pcaprop.DisjunctionOp(value[0], value[2])
        return self._rec_object(value, 'exp_or')

    def exp_and(self, value):
        if len(value) == 3:
            return pcaprop.ConjunctionOp(value[0], value[2])
        return self._rec_object(value, 'exp_and')

    def exp_not(self, value):
        return pcaprop.NegationOp(value[1])

    def atom_true(self, value):
        return pcaprop.TrueProp()

    def atom_false(self, value):
        return pcaprop.FalseProp()

    def atom_paren(self, value):
        return value[0]

    def atom_var(self, value):
        return pcaprop.Variable(value[0])

    def _rec_object(self, value, function):
        f = getattr(self, function)
        if len(value) == 3:
            return f(value)
        # List Slicing to replace first 3 elements with corresponding proposition
        value[:3] = [f(value[:3])]
        return self._rec_object(value, function)


PARSER = Lark(GRAMMAR, parser='lalr', start='exp_iff', transformer=PropTransformer())
