
import random
from dotenv import dotenv_values
from pymongo import MongoClient
from generated_data.variables_generated import generated_variables
from variables.models import Coordinado, Coordinated, Variable, Data
from datetime import datetime, timezone
from typing import List 
from generated_data.format_data import read_data_sitr
import time
import argparse
from bson import ObjectId

config = dotenv_values(".env")
uri = config['URL_MONGO']
#client = MongoClient(config["ADDRESS"], int(config["PORT"]))
client = MongoClient(uri)

def add_coordinated():
    """
    Solo para iniciar coordinados con substationes
    """
    subestations_data: List[Data] = read_data_sitr(delimeter_=",", coordinado_name="Las vegas")
    db = client[config["DB_NAME"]]
    collection_coordinado = db["coordinated"]
    collecion_substation = db["substations"]

    subestations = []
    
    name_coordinated = subestations_data[0].name_coordinado
    for subestation in subestations_data:
        if subestation.name_coordinado == "Las vegas":
            variables_collection = []
            for variables in subestation.variables_analogic:
                variables_collection.append({
                    "nameVariable": variables.name,
                    "unit": variables.unit,
                    "category": "analogic",
                    "variable_id": ObjectId()
                })
                
            for variables in subestation.variables_state:
                variables_collection.append({
                    "nameVariable": variables,
                    "category": "digital",
                    "variable_id": ObjectId()
                })
            
            collecion_substation.insert_one({
                "nameSubstation": subestation.subestation,
                "variables": variables_collection
            })

            id_substation: str = collecion_substation.find_one({"nameSubstation": subestation.subestation})["_id"]
            subestations.append({"idSubstation": id_substation} )
        else:
            variables_collection = []
            for variables in subestation.variables_analogic:
                variables_collection.append({
                    "nameVariable": variables.name,
                    "unit": variables.unit,
                    "category": "analogic",
                    "variable_id": ObjectId()
                })
                
            for variables in subestation.variables_state:
                variables_collection.append({
                    "nameVariable": variables,
                    "category": "digital",
                    "variable_id": ObjectId()
                })

            collecion_substation.insert_one({
                "nameSubstation": subestation.subestation,
                "variables": variables_collection
            })
            
            id_substation: str = collecion_substation.find_one({"nameSubstation": subestation.subestation})["_id"]
            substation_sobrante = [{"idSubstation": id_substation}]
            coordinated = Coordinated(nameCoordinated=subestation.name_coordinado, substations=substation_sobrante, email="test2@test.com", pw="admintest2")
            collection_coordinado.insert_one(coordinated.model_dump())
            
    coordinated = Coordinated(nameCoordinated=name_coordinated, substations=subestations, email="test@test.com",pw="admin")
    collection_coordinado.insert_one(coordinated.model_dump())


def generate_document(index: int):
    subestation: List[Data] = read_data_sitr(delimeter_=",", coordinado_name="Las vegas")
    subestation_select: Data = subestation[index] 
    name_subestation = subestation_select.subestation
    
    _variables: List[Variable] = generated_variables(variables_analogic=subestation_select.variables_analogic,
                                                     variables_state=subestation_select.variables_state)
    date = datetime.now(timezone.utc)
    documento = Coordinado(name = subestation_select.name_coordinado,subestacion=name_subestation,time=str(datetime.now()),
                                variables=_variables)
    dic = documento.model_dump()
    dic["time"] = date
    return dic

def create_time_series_variable_coll():
    db = client[config["DB_NAME"]]
    
    db.create_collection("variables", timeseries={
        "timeField": "timestamp",
        "metaField": "metadata",
        "granularity": "seconds"
    })

def generate_time_series_variable(index: int):
    db = client[config["DB_NAME"]]
    coll_substations = db["substations"]
    subestation: List[Data] = read_data_sitr(delimeter_=",", coordinado_name="Las vegas")
    name_substation: Data = subestation[index].subestation
    variables = coll_substations.find_one({"nameSubstation": name_substation})["variables"]
    
    return variables

def generated_variable(variables, coll_variable, delete_oldest_document):
    date = datetime.now(timezone.utc)
    for variable in variables:
        id_variable = variable["variable_id"]
        #elimino la mas antigua si se quiere eliminar
        if delete_oldest_document:
            oldest_document = coll_variable.find_one(
                sort=[("timestamp", 1)])  # 1 es ascendente, para obtener el más antiguo
            if oldest_document:
                coll_variable.delete_one({"_id": oldest_document["_id"]})

        if variable["category"] == "analogic":
            variable = {
                    "metadata": { "idVariable": id_variable,
                                 "unit": variable["unit"]},
                    "timestamp": date,
                    "value": random.randint(0, 2**12 - 1),
                    "unit": variable["category"]
            }
            coll_variable.insert_one(variable)
        else:
            variable = {
                    "metadata": { "idVariable": id_variable},
                    "timestamp": date,
                    "value": random.randint(0,1),
                    "unit": variable["category"]
            }
            coll_variable.insert_one(variable)
        
        
def connection_mongodb():
    db = client[config["DB_NAME"]]
    collections = db[config["COLLECTIONS"]]
    return collections

def batch_document(numero_de_horas, collection, type: str, index: int, delete_oldest_document):
    tiempo_total_segundos = numero_de_horas * 3600
    if type == "sec":
        for _ in range(numero_de_horas):
            variables = generate_time_series_variable(index)
            generated_variable(variables, collection, delete_oldest_document)
            time.sleep(1)
    else:
        for _ in range(tiempo_total_segundos):
            variables = generate_time_series_variable(index)
            generated_variable(variables, collection, delete_oldest_document)
            time.sleep(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Scrpit de simulacion de variables electricas en dos clientes, uno con 12 subestaciones y el otro solamente con 1, entregando por argumenntando la subestacion que se va a simular")
    parser.add_argument("-create", "--state")
    parser.add_argument("-index", "--indice", type=int, help="indice de la subestacion")
    parser.add_argument("-time", "--tiempo", type=str, help="variable Tiempo hrs o sec")
    parser.add_argument("-count", "--cantidad", type=int, help="cantidad de tiempo segundos o horas")
    parser.add_argument("-delete", "--delete", type=int, help="eliminar el documento mas antiguo")
    args = parser.parse_args()
    print(args)
    if args.state != None:
        add_coordinated()
        create_time_series_variable_coll()
    else:
        db = client[config["DB_NAME"]]
        collect = db.get_collection("variables")
        batch_document(args.cantidad, collect, args.tiempo, args.indice, args.delete)
        client.close()
    
    