 start: exp_iff
 ?exp_iff: exp_imp (EQUIVALENCE exp_imp)*
 ?exp_imp: exp_or (IMPLICATION exp_or)*
 ?exp_or: exp_and (DISJUNCTION exp_and)*
 ?exp_and: exp_not (CONJUNCTION exp_not)*
 ?exp_not: NEGATION exp_not                     -> exp_not
        | atom
 atom: VAR                                      -> var
        | LPAREN start RPAREN
        | TRUE                                  -> true
        | FALSE                                 -> false

 VAR: /[A-Z]+/
 LPAREN: "("
 RPAREN: ")"
 TRUE: "true" | "top" | "t" | "\u22a4"
 FALSE: "false" | "bot" | "f" | "\u22A5"
 CONJUNCTION: "and" | "\u2227" | "\u00B7" | "\u0026"
 DISJUNCTION: "or" | "\u2228" | "\u002B" | "\u2225"
 NEGATION: "not" | "\u00AC" | "\u0021" | "\u02DC"
 IMPLICATION: "implies" | "\u21D2" | "\u2192"
 EQUIVALENCE: "iff" | "\u21D4" | "\u2194"

 %import common.WS
 %ignore WS
