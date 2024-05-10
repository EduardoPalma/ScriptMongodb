from typing import List
from variables.models import VariableAnalogic, VariableState, Variable, AnalogicDTO
import random

def generated_num():
    #mejorar la generarcion de numeros, esto popdria retornar tambien la unidad
    return random.randint(0, 2**16 - 1)


def generated_variables(variables_analogic: List[AnalogicDTO], variables_state: List[str]) -> List[Variable]:
    variables: List[Variable] = []

    variables_analogic_generated: List[VariableAnalogic] = generated_v_analogic(variables_analogic)
    variables_state_generated: List[VariableState] = generated_v_state(variables_state)
    variables.extend(variables_analogic_generated)
    variables.extend(variables_state_generated)

    return variables


def generated_v_analogic(variables_analogic_names: List[AnalogicDTO]) -> List[VariableAnalogic]:
    variables: list[VariableAnalogic] = []

    for analogic_var in variables_analogic_names:
        var_analogic = VariableAnalogic(name=analogic_var.name, value=generated_num(), unit=analogic_var.unit)
        variables.append(var_analogic)

    return variables


def generated_v_state(variables_state_names: List[str]) -> List[VariableState]:
    variables: list[VariableState] = []

    for variable_name in variables_state_names:
        var_analogic = VariableState(name=variable_name, state=random.randint(0,1))
        variables.append(var_analogic)

    return variables