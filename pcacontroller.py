# @Author: GKarseras
# @Date:   22 Jan 2021 14:04

from fastapi import FastAPI
from lark.exceptions import UnexpectedCharacters

from pca_main import pcabuilder

app = FastAPI()


# @app.get("/api/calc/{prop}")
# async def calc_prop(prop):
#     try:
#         r = pcabuilder.InitProp(prop)
#     except UnexpectedCharacters as UC:
#         return {'Error': repr(UC)}
#
#     return {
#         "prop": r.prop,
#         'parsed': repr(r.parsed),
#         'sat': repr(r.satisfiable()),
#         'taut': repr(r.tautology()),
#         'contr': repr(r.contradiction()),
#         'truth': repr(r.build_interp()),
#     }


@app.get("/api/sat/{prop}")
async def calc_prop(prop):
    try:
        r = pcabuilder.InitProp(prop)
    except UnexpectedCharacters as UC:
        return {'Error': UC.get_context(prop)}
    return {'sat': repr(r.satisfiable())}


# @app.get("/api/taut/{prop}")
# async def calc_prop(prop):
#     try:
#         r = pcabuilder.InitProp(prop)
#     except UnexpectedCharacters as UC:
#         return {'Error': repr(UC)}
#     return {'taut': repr(r.tautology())}
#
#
# @app.get("/api/contr/{prop}")
# async def calc_prop(prop):
#     try:
#         r = pcabuilder.InitProp(prop)
#     except UnexpectedCharacters as UC:
#         return {'Error': repr(UC)}
#     return {'contr': repr(r.contradiction())}
#
#
# @app.get("/api/truth/{prop}")
# async def calc_prop(prop):
#     try:
#         r = pcabuilder.InitProp(prop)
#     except UnexpectedCharacters as UC:
#         return {'Error': repr(UC)}
#     return {'truth': repr(r.build_interp())}

