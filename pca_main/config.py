# @Author: GKarseras
# @Date:   10 Feb 10:16

MAPPING = {
    " \u21D4 ": ("iff", "\u21D4", "\u2194"),
    " \u21D2 ": ("implies", "\u21D2", "\u2192"),
    " \u2228 ": ("or", "\u002B", "\u2228", "\u2225"),
    " \u2227 ": ("and", "\u00B7", "\u2227", "\u0026"),
    " \u00AC ": ("not", "\u0021", "\u00AC", "\u02DC"),
    " \u22a4 ": ("true", "top", "\u22a4"),
    " \u22A5 ": ("false", "bot", "\u22A5")
}


def prop_pretty(s: str) -> str:
    for key, values in MAPPING.items():
        for value in values:
            s = s.replace(value, key)
    return " ".join(s.split())


def prop_to_string(prop) -> str:
    return ''
