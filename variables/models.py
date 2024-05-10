from pydantic import BaseModel, SerializeAsAny, model_serializer
from typing import List
from bson.objectid import ObjectId as BsonObjectId

class Variable(BaseModel):
    name: str

class VariableAnalogic(Variable):
    value: int
    unit: str

class VariableState(Variable):
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
    
class PydanticObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, BsonObjectId):
            raise TypeError('ObjectId required')
        return str(v)

class Substation(BaseModel):
    idSubstation: PydanticObjectId

class Coordinated(BaseModel):
    nameCoordinated: str
    substations: List[dict]
    email: str
    pw: str    
