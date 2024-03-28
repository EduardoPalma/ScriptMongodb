
from dotenv import dotenv_values
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from generated_data.variables_generated import generated_variables
from variables.models import Coordinado, Variable, Data
from datetime import datetime
from typing import List 
from generated_data.format_data import read_data_sitr
from urllib.parse import quote_plus
import time
import argparse

config = dotenv_values(".env")
uri = "mongodb+srv://adminconecta:"+quote_plus('9AAd96631')+"@conectatest.funtyje.mongodb.net/?retryWrites=true&w=majority&appName=ConectaTest"
client = MongoClient(config["ADDRESS"], int(config["PORT"]))


def generate_document(index: int):
    subestation: List[Data] = read_data_sitr(delimeter_=",", coordinado_name="Las vegas")
    subestation_select: Data = subestation[index] 
    name_subestation = subestation_select.subestation
    _variables: List[Variable] = generated_variables(variables_analogic=subestation_select.variables_analogic,
                                                     variables_state=subestation_select.variables_state)
    date = datetime.now()
    documento = Coordinado(name = subestation_select.name_coordinado,subestacion=name_subestation,time=str(datetime.now()),
                                variables=_variables)
    dic = documento.model_dump()
    dic["time"] = date
    return dic


def connection_mongodb():
    db = client[config["DB_NAME"]]
    collections = db[config["COLLECTIONS"]]
    return collections

def batch_document(numero_de_horas, collections, type: str, index: int):

    tiempo_total_segundos = numero_de_horas * 3600
    if type == "sec":
        for _ in range(numero_de_horas):
            doc = generate_document(index)
            collections.insert_one(doc)
            time.sleep(1)
    else:
        for _ in range(tiempo_total_segundos):
            doc = generate_document(index)
            collections.insert_one(doc)
            time.sleep(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Scrpit de simulacion de variables electricas en un cliente, con 12 subestaciones, entregando por argumnete la subestacion que se va a simular")
    parser.add_argument("-index", "--indice", type=int, help="indice de la subestacion")
    parser.add_argument("-time", "--tiempo", type=str, help="variable Tiempo hrs o sec")
    parser.add_argument("-count", "--cantidad", type=int, help="cantidad de tiempo segundos o horas")
    args = parser.parse_args()
    print(args)
    collect = connection_mongodb()
    batch_document(args.cantidad, collect, args.tiempo, args.indice)
    client.close()

    