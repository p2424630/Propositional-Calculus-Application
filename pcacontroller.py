# @Author: GKarseras
# @Date:   22 Jan 2021 14:04

from typing import List, Dict
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pca_main import pcabuilder, exercises

app = FastAPI()

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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


class CalcSatModel(BaseModel):
    Proposition: str
    Satisfiable: bool


class CalcTautModel(BaseModel):
    Proposition: str
    Tautology: bool


class CalcContrModel(BaseModel):
    Proposition: str
    Contradiction: bool


class CalcInterpModel(BaseModel):
    Proposition: str
    Variables: List[str]
    Interpretations: List[List[bool]]


class SectionsModel(BaseModel):
    Sections: List[str]


# class ExerciseModel(BaseModel):
#     Question: str
#     Propositions: List[str]


class ExercisesModel(BaseModel):
    Exercises: List[Dict]


class ExerciseEvalModel(BaseModel):
    Proposition: str
    t_proposition: str
    Result: bool


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
    try:
        r = pcabuilder.InitProp(prop)
        return {
            'Proposition': str(r),
            'Satisfiable': bool(r.satisfiable()),
            'Tautology': bool(r.tautology()),
            'Contradiction': bool(r.contradiction()),
            'Variables': [variable.name for variable in r.unique_vars()],
            'Interpretations': [[bool(bool_val) for bool_val in interp] for interp in r.interpretations()]
        }
    except Exception as e:
        raise PropException(err=repr(e))


@app.get("/api/exercises", response_model=SectionsModel)
async def ex_sections():
    try:
        return {
            'Sections': list(exercises.exer.keys())
        }
    except Exception as e:
        raise PropException(err=repr(e))


@app.get("/api/exercises/{section}", response_model=ExercisesModel)
async def sections_ex(section):
    try:
        return {
            'Exercises': exercises.exer[section],
        }
    except Exception as e:
        raise PropException(err=repr(e))


@app.get("/api/exercises/eval/{q_prop}", response_model=ExerciseEvalModel)
async def exercise_eval(q_prop, method, t_prop):
    try:
        q_proposition = pcabuilder.InitProp(q_prop)
        t_proposition = pcabuilder.InitProp(t_prop)
        q_result = pcabuilder.InitProp(str(getattr(q_proposition, method)()))
        return {
            'Proposition': str(q_result),
            't_proposition': str(t_proposition),
            'Result': q_result == t_proposition,
        }
    except Exception as e:
        raise PropException(err=repr(e))


# @app.get("/api/sat/{prop}", response_model=CalcSatModel)
# async def calc_prop_sat(prop):
#     try:
#         r = pcabuilder.InitProp(prop)
#         return {
#             'Proposition': str(r),
#             'Satisfiable': bool(r.satisfiable())
#         }
#     except Exception as e:
#         raise PropException(err=repr(e))
#
#
# @app.get("/api/taut/{prop}", response_model=CalcTautModel)
# async def calc_prop_taut(prop):
#     try:
#         r = pcabuilder.InitProp(prop)
#         return {
#             'Proposition': str(r),
#             'Tautology': bool(r.tautology())
#         }
#     except Exception as e:
#         raise PropException(err=repr(e))
#
#
# @app.get("/api/contr/{prop}", response_model=CalcContrModel)
# async def calc_prop_contr(prop):
#     try:
#         r = pcabuilder.InitProp(prop)
#         return {
#             'Proposition': str(r),
#             'Contradiction': bool(r.contradiction())
#         }
#     except Exception as e:
#         raise PropException(err=repr(e))
#
#
# @app.get("/api/interp/{prop}", response_model=CalcInterpModel)
# async def calc_prop_interp(prop):
#     try:
#         r = pcabuilder.InitProp(prop)
#         return {
#             'Proposition': str(r),
#             'Variables': [variable.name for variable in r.unique_vars()],
#             'Interpretations': [[bool(bool_val) for bool_val in interp] for interp in r.interpretations()]
#         }
#     except Exception as e:
#         raise PropException(err=repr(e))


# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app, port=8085, host='0.0.0.0')
