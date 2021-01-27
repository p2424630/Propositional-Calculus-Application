# @Author: GKarseras
# @Date:   22 Jan 2021 14:04

from typing import List
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pca_main import pcabuilder

app = FastAPI()

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CalcModel(BaseModel):
    Proposition: str
    Parsed: str
    Satisfiable: bool
    Tautology: bool
    Contradiction: bool
    Variables: List[str]
    Interpretations: List[List[bool]]


class CalcSatModel(BaseModel):
    Proposition: str
    Parsed: str
    Satisfiable: bool


class CalcTautModel(BaseModel):
    Proposition: str
    Parsed: str
    Tautology: bool


class CalcContrModel(BaseModel):
    Proposition: str
    Parsed: str
    Contradiction: bool


class CalcInterpModel(BaseModel):
    Proposition: str
    Parsed: str
    Variables: List[str]
    Interpretations: List[List[bool]]


class PropException(Exception):
    def __init__(self, err: str):
        self.err = err


@app.exception_handler(PropException)
async def prop_exception_handler(request: Request, exc: PropException):
    return JSONResponse(
        status_code=406,
        content={"Error": exc.err},
    )


@app.get("/api/calc/{prop}", response_model=CalcModel)
async def calc_prop(prop):
    print(prop)
    try:
        r = pcabuilder.InitProp(prop)
        return {
            'Proposition': r.prop,
            'Parsed': repr(r.parsed),
            'Satisfiable': bool(r.satisfiable()),
            'Tautology': bool(r.tautology()),
            'Contradiction': bool(r.contradiction()),
            'Variables': [variable.name for variable in r.unique_vars()],
            'Interpretations': [[bool(bool_val) for bool_val in interp] for interp in r.interpretations()],
        }
    except Exception as e:
        raise PropException(err=repr(e))


@app.get("/api/sat/{prop}", response_model=CalcSatModel)
async def calc_prop_sat(prop):
    try:
        r = pcabuilder.InitProp(prop)
        return {
            'Proposition': r.prop,
            'Parsed': repr(r.parsed),
            'Satisfiable': repr(r.satisfiable())
        }
    except Exception as e:
        raise PropException(err=repr(e))


@app.get("/api/taut/{prop}", response_model=CalcTautModel)
async def calc_prop_taut(prop):
    try:
        r = pcabuilder.InitProp(prop)
        return {
            'Proposition': r.prop,
            'Parsed': repr(r.parsed),
            'Tautology': bool(r.tautology())
        }
    except Exception as e:
        raise PropException(err=repr(e))


@app.get("/api/contr/{prop}", response_model=CalcContrModel)
async def calc_prop_contr(prop):
    try:
        r = pcabuilder.InitProp(prop)
        return {
            'Proposition': r.prop,
            'Parsed': repr(r.parsed),
            'Contradiction': bool(r.contradiction())
        }
    except Exception as e:
        raise PropException(err=repr(e))


@app.get("/api/interp/{prop}", response_model=CalcInterpModel)
async def calc_prop_interp(prop):
    try:
        r = pcabuilder.InitProp(prop)
        return {
            'Proposition': r.prop,
            'Parsed': repr(r.parsed),
            'Variables': [variable.name for variable in r.unique_vars()],
            'Interpretations': [[bool(bool_val) for bool_val in interp] for interp in r.interpretations()]
        }
    except Exception as e:
        raise PropException(err=repr(e))


# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app, port=8085, host='0.0.0.0')
