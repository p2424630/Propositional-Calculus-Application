# @Author: GKarseras
# @Date:   22 Jan 2021 14:04

from typing import List, Dict

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pca_main import exercises, pcabuilder, pcalaws
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080"
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


class SectionsModel(BaseModel):
    Sections: List[str]


class AllLawsModel(BaseModel):
    Laws: List[str]


class ExercisesModel(BaseModel):
    Exercises: List[Dict]


class ExerciseEvalModel(BaseModel):
    Result_Prop: str
    Result: bool


class PartialEvalModel(BaseModel):
    Result: str


class PropException(Exception):
    def __init__(self, error: str):
        self.error = error


@app.exception_handler(PropException)
async def prop_exception_handler(request: Request, exc: PropException):
    return JSONResponse(
        status_code=406,
        content={"Error": exc.error},
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
        raise PropException(error=str(e))


@app.get("/api/exercises", response_model=SectionsModel)
async def ex_sections():
    try:
        return {
            'Sections': list(exercises.EXERCISES.keys())
        }
    except Exception as e:
        raise PropException(error=str(e))


@app.get("/api/exercises/{section}", response_model=ExercisesModel)
async def sections_ex(section):
    try:
        return {
            'Exercises': exercises.EXERCISES[section],
        }
    except Exception as e:
        raise PropException(error=str(e))


@app.get("/api/exercises/eval/{q_prop}", response_model=ExerciseEvalModel)
async def exercise_eval(q_prop, methods, t_prop):
    try:
        q_proposition = _apply_methods(q_prop, methods)
        t_proposition = pcabuilder.InitProp(t_prop)
        return {
            'Result_Prop': str(q_proposition),
            'Result': q_proposition == t_proposition,
        }
    except Exception as e:
        raise PropException(error=str(e))


@app.get("/api/partial/{prop}", response_model=PartialEvalModel)
async def partial_application(prop, methods):
    try:
        return {
            'Result': str(_apply_methods(prop, methods)),
        }
    except Exception as e:
        raise PropException(error=str(e))


@app.get("/api/laws", response_model=AllLawsModel)
async def all_laws():
    try:
        return {
            'Laws': [law for law in dir(pcalaws.Laws) if
                     not law.startswith(("__", "_", "proposition")) and callable(getattr(pcalaws.Laws, law))]
        }
    except Exception as e:
        raise PropException(error=str(e))


def _apply_methods(prop, methods):
    prop = pcabuilder.InitProp(prop)
    methods = [getattr(pcabuilder.InitProp, method) for method in methods.split(',')]
    for method in methods:
        prop = method(prop)
        prop = pcabuilder.InitProp(str(prop))
    return prop
