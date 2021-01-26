# @Author: GKarseras
# @Date:   22 Jan 2021 14:04
from typing import List, Tuple, Dict, Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pca_main import pcabuilder
from pca_main.pcaprop import Variable, TrueProp, FalseProp

app = FastAPI()

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CalcModel(BaseModel):
    Proposition: str
    Satisfiable: bool
    Tautology: bool
    Contradiction: bool
    Variables: List[str]
    Interpretations: List[List[bool]]


@app.get("/api/calc/{prop}", response_model=CalcModel)
async def calc_prop(prop):
    print(prop)
    try:
        r = pcabuilder.InitProp(prop)
        return {
            "Proposition": r.prop,
            'Satisfiable': bool(r.satisfiable()),
            'Tautology': bool(r.tautology()),
            'Contradiction': bool(r.contradiction()),
            'Variables': [variable.name for variable in r.unique_vars()],
            'Interpretations': [[bool(bool_val) for bool_val in interp] for interp in r.interpretations()],
        }
    except Exception as e:
        return {'Error': repr(e)}


@app.get("/api/sat/{prop}")
async def calc_prop(prop):
    try:
        r = pcabuilder.InitProp(prop)
    except Exception as e:
        return {'Error': repr(e)}
    return {'sat': repr(r.satisfiable())}


@app.get("/api/taut/{prop}")
async def calc_prop(prop):
    try:
        r = pcabuilder.InitProp(prop)
    except Exception as e:
        return {'Error': repr(e)}
    return {'taut': repr(r.tautology())}


@app.get("/api/contr/{prop}")
async def calc_prop(prop):
    try:
        r = pcabuilder.InitProp(prop)
    except Exception as e:
        return {'Error': repr(e)}
    return {'contr': repr(r.contradiction())}


@app.get("/api/truth/{prop}")
async def calc_prop(prop):
    try:
        r = pcabuilder.InitProp(prop)
    except Exception as e:
        return {'Error': repr(e)}
    return {'truth': repr(r.interpretations())}


# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app, port=8085, host='0.0.0.0')
