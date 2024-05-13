from datetime import datetime
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

    
    collection_coordinado= collections("Coordinado", "SLRP")
    collection_eventos = collections("eventos", "SLRP")
    collection_ajustes = collections("ajustes", "SLRP")
    collection_oscilografia = collections("oscilografia", "SLRP")
  
    #aqui continuas con el codigo para insertar los documentos

    # Creación de la estructura de datos para inserción
    data_to_insert = []
    data_event = []
    data_oscilografia = []
    data_ajustes = []

    # Inserción de datos de coordinado y subestaciones
    for coordinado_objeto in objetos_coordinado:
        coordinado_data = {
            "_id": coordinado_objeto.codigo,
            "nombreCoordinador": coordinado_objeto.nombre,
            "subestaciones": []
        }
        
        for subestacion_objeto in objetos_subestacion:
            if subestacion_objeto.codigo_coord == coordinado_objeto.codigo:
                subestacion_data = {
                    "nombre": subestacion_objeto.proteccion_name,
                    "pañoBarra": []
                }
                
                for pano_barra_objeto in objetos_pano_barra:
                    if pano_barra_objeto.cod_subestacion == subestacion_objeto.codigo:
                        pano_barra_data = {
                            "name": pano_barra_objeto.nombrepb,
                            "categoria": categoria_pano_barra[pano_barra_objeto.cod_categoria_paño_barra],
                            "protecciones": []
                        }
                        
                        for proteccion_objeto in objetos_protecciones:
                            if proteccion_objeto.cod_identificacion_paño_barra == pano_barra_objeto.cod_identificacion_pano_barra:
                                proteccion_data = {
                                    "name": proteccion_objeto.nombre_proteccion
                                }
                                pano_barra_data["protecciones"].append(proteccion_data)
                                for evento_objeto in objetos_eventos:
                                    if evento_objeto.cod_proteccion == proteccion_objeto.cod_proteccion:
                                        fecha_datetime = datetime.strptime(evento_objeto.fecha_evento + ' ' + evento_objeto.hora, '%Y-%m-%d %H:%M:%S')
                                        evento_data = {
                                            "_idCoordinado": coordinado_objeto.codigo,
                                            "subestacion": subestacion_objeto.proteccion_name,
                                            "nombreProteccion": proteccion_objeto.nombre_proteccion,
                                            "datetime": fecha_datetime,
                                            "categoria": 'data'
                                        }
                                        data_event.append(evento_data)
                                for oscilografia_objeto in objetos_oscilografia:
                                    if oscilografia_objeto.cod_proteccion == proteccion_objeto.cod_proteccion:
                                        fecha_datetime = datetime.strptime(oscilografia_objeto.fecha_oscilografia + ' ' + oscilografia_objeto.hora, '%Y-%m-%d %H:%M:%S')
                                        oscilografia_data = {
                                            "_idCoordinado": coordinado_objeto.codigo,
                                            "subestacion": subestacion_objeto.proteccion_name,
                                            "nombreProteccion": proteccion_objeto.nombre_proteccion,
                                            "datetime": fecha_datetime,
                                            "otrodato": 'data'
                                        }
                                        data_oscilografia.append(oscilografia_data)
                                for ajuste_objeto in objetos_ajustes:
                                    if ajuste_objeto.cod_proteccion == proteccion_objeto.cod_proteccion:
                                        fecha_datetime = datetime.strptime(ajuste_objeto.fecha_ajuste + ' ' + ajuste_objeto.hora, '%Y-%m-%d %H:%M:%S')
                                        ajuste_data = {
                                            "_idCoordinado": coordinado_objeto.codigo,
                                            "subestacion": subestacion_objeto.proteccion_name,
                                            "nombreProteccion": proteccion_objeto.nombre_proteccion,
                                            "datetime": fecha_datetime,
                                            "otrodato": 'data'
                                         }
                                        data_ajustes.append(ajuste_data)
                                            
                        
                        subestacion_data["pañoBarra"].append(pano_barra_data)
                
                coordinado_data["subestaciones"].append(subestacion_data)
        
        data_to_insert.append(coordinado_data)

    collection_coordinado.insert_many(data_to_insert)
    collection_ajustes.insert_many(data_ajustes)
    collection_oscilografia.insert_many(data_oscilografia)
    collection_eventos.insert_many(data_event)
    
    client.close()

read_csv_slrp()
