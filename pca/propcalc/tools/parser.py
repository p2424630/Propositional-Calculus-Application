# @Author: GKarseras
# @Date:   17 Nov 2020 10:30

from lark import Lark, Transformer

from pca.propcalc.tools.proposition import ConjunctionOp, DisjunctionOp, EquivalenceOp, FalseProp
from pca.propcalc.tools.proposition import ImplicationOp, NegationOp, TrueProp, Variable


GRAMMAR = '''
             ?exp_iff: exp_imp (OP_EQUIVALENCE exp_imp)*
             ?exp_imp: exp_or (OP_IMPLICATION exp_or)*
             ?exp_or: exp_and (OP_DISJUNCTION exp_and)*
             ?exp_and: atom (OP_CONJUNCTION atom)*
             atom: OP_NEGATION atom                      -> exp_not
                  | VAR                                  -> atom_var
                  | TRUE                                 -> atom_true
                  | FALSE                                -> atom_false
                  | "(" exp_iff ")"                      -> atom_paren
            
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


# TODO: Fix value unpacking.
class AtomTransformer(Transformer):

    def exp_iff(self, value):
        return EquivalenceOp(value[0], value[2])

    def exp_imp(self, value):
        return ImplicationOp(value[0], value[2])

    def exp_or(self, value):
        return DisjunctionOp(value[0], value[2])

    def exp_and(self, value):
        return ConjunctionOp(value[0], value[2])

    def exp_not(self, value):
        return NegationOp(value[1])

    def atom_true(self, value):
        return TrueProp()

    def atom_false(self, value):
        return FalseProp()

    def atom_paren(self, value):
        return value[0]

    def atom_var(self, value):
        return Variable(value[0])


PARSER = Lark(GRAMMAR, parser='lalr', start='exp_iff', transformer=AtomTransformer())
