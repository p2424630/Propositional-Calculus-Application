# @Author: GKarseras
# @Date:   17 Nov 2020 10:30

from lark import Lark


class LogicSymbols:
    NEGATION = ('\u00AC', '\u0021', '\u02DC', 'not')
    IMPLICATION = ('\u21D2', '\u2192', 'implies')
    EQUIVALENCE = ('\u21D4', '\u2194', 'iff')
    CONJUNCTION = ('\u2227', '\u00B7', '\u0026', 'and')
    DISJUNCTION = ('\u2228', '\u002B', '\u2225', 'or')
    # EXCLUSIVEOR = ('\u2295', '\u22BB', 'xor')


SYMBOLS = ['\u00AC', '\u21D2', '\u21D4', '\u2227', '\u2228']

# PRECEDENCE = {
#     LogicSymbols.NEGATION: 1,
#     LogicSymbols.CONJUNCTION: 2,
#     LogicSymbols.DISJUNCTION: 3,
#     LogicSymbols.IMPLICATION: 4,
#     LogicSymbols.EQUIVALENCE: 5
# }


PARSER = Lark('''
            ?exp_iff: exp_imp (EQUIVALENCE exp_imp)*
            ?exp_imp: exp_or (IMPLICATION exp_or)*
            ?exp_or: exp_and (DISJUNCTION exp_and)*
            ?exp_and: variable (CONJUNCTION variable)*
            ?variable: var | NEGATION variable | "(" exp_iff ")"
            var: /[a-z]+/
            
            CONJUNCTION: "AND" | "\u2227" | "\u00B7" | "\u0026"
            DISJUNCTION: "OR" | "\u2228" | "\u002B" | "\u2225"
            NEGATION: "NOT" | "\u00AC" | "\u0021" | "\u02DC"
            IMPLICATION: "IMPLICATION" | "IMPLIES" | "\u21D2" | "\u2192"
            EQUIVALENCE: "EQUIVALENCE" | "IFF" | "\u21D4" | "\u2194"
            
            %import common.WS
            %ignore WS
         ''', start='exp_iff', parser='lalr')
