from pydantic import BaseModel, SerializeAsAny, model_serializer
from typing import List


class Variable(BaseModel):
    valid_data: str
    valid_time: bool

class VariableAnalogic(Variable):
    name: str
    value: int
    unit: str

class VariableState(Variable):
    name: str
    state: int


class Coordinado(BaseModel):
    name: str
    subestacion: str
    time: str
    variables: List[SerializeAsAny[Variable]]
    

class AnalogicDTO(BaseModel):
    name: str
    unit: str

class Data(BaseModel):
    name_coordinado: str
    subestation: str
    variables_state: List[str]
    variables_analogic: List[AnalogicDTO]