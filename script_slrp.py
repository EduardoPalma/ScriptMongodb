
from dotenv import dotenv_values
from pydantic import BaseModel
from pymongo import MongoClient
from variables.models_slrp import *
from typing import List, TypeVar
import pandas as pd
# Define un tipo genérico para los objetos
T = TypeVar('T', bound=BaseModel)
categoria_pano_barra = {
    '69749F': 'Paño',
    '88844B': 'Barra'
}

config = dotenv_values(".env")
client = MongoClient(config["ADDRESS"], int(config["PORT"]))

def transforms_object(df: pd.DataFrame, obje_type: T) -> List[T]:
    object_type = []
    for _, fila in df.iterrows():
        objeto = obje_type(**fila.to_dict())
        object_type.append(objeto)
    
    return object_type

def collections(name_collections: str, db_name: str):
    db = client[db_name]
    collections = db[name_collections]
    return collections

def read_csv_slrp():
    df_coordinado = pd.read_csv("generated_data/slrp_data/coordinado.csv", delimiter=",",dtype=None)
    df_subestacion = pd.read_csv("generated_data/slrp_data/subestacion.csv", delimiter=",",dtype=None)
    df_panobarra = pd.read_csv("generated_data/slrp_data/pañobarra.csv", delimiter=",",dtype=None)
    df_proteccion = pd.read_csv("generated_data/slrp_data/protecciones.csv", delimiter=",",dtype=None)
    
    #estos datos se ingresan casi inmediatamente al documento respectivo
    df_eventos = pd.read_csv("generated_data/slrp_data/eventos.csv", delimiter=",",dtype=None)
    df_oscilografia = pd.read_csv("generated_data/slrp_data/oscilografia.csv", delimiter=",",dtype=None)
    df_ajustes =pd.read_csv("generated_data/slrp_data/ajustes.csv", delimiter=",",dtype=None)

    
    #Listas con cada objeto creado el archivo models_slrp.py contiene los modelos utilizados
    objetos_coordinado: List[CoordinadoCSV] = transforms_object(df_coordinado, CoordinadoCSV)
    objetos_subestacion: List[SubestacionCSV]  = transforms_object(df_subestacion, SubestacionCSV)
    objetos_protecciones: List[ProteccionCSV] = transforms_object(df_proteccion, ProteccionCSV)
    objetos_pano_barra : List[PanoBarraCSV] = transforms_object(df_panobarra, PanoBarraCSV)
    objetos_eventos: List[EventosCSV] = transforms_object(df_eventos, EventosCSV)
    objetos_oscilografia: List[OscilografiaCSV] = transforms_object(df_oscilografia, OscilografiaCSV)
    objetos_ajustes: List[AjustesCSV] = transforms_object(df_ajustes, AjustesCSV)
    
    collection = collections("Coordinado", "SLRP")
    #aqui continuas con el codigo para insertar los documentos
    
    
    client.close()
    
if __name__ == '__main__':
    read_csv_slrp()
