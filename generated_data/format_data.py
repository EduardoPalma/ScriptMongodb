from typing import List
from numpy import ndarray
import pandas as pd
from variables.models import Data, AnalogicDTO
import os

def read_data_sitr_north() -> Data:
    df = pd.read_csv("generated_data/north_west/pmg_north_west.xlsx - Hoja 1.csv", delimiter=",",dtype=None)
    df_analogic = df[df["Tipo"] == "Análogo"]
    df_state = df[df["Tipo"] != "Análogo"]["Descripcion"].tolist()
    analogic_dot: List[AnalogicDTO] = df_to_analogic(df_analogic)
    subestacion = Data(name_coordinado="North West", subestation="North West Subestacion",
                      variables_analogic=analogic_dot, variables_state=df_state)
    return subestacion

def df_to_objetc(df_analogic: ndarray):
    analogic_dot: List[AnalogicDTO] = []
    for i in range(len(df_analogic)):
        obje = AnalogicDTO(name=df_analogic[i], unit="unit")
        analogic_dot.append(obje)

    return analogic_dot


def df_to_analogic(df_analogic: pd.DataFrame):
    analogic_dot: List[AnalogicDTO] = []
    for i in range(len(df_analogic)):
        obje = AnalogicDTO(name=df_analogic.iloc[i]["Descripcion"], unit=df_analogic.iloc[i]["Unidad de medida"])
        analogic_dot.append(obje)

    return analogic_dot


def read_data_sitr(delimeter_: str, coordinado_name: str) -> List[Data]:
    dir_ = "generated_data/data_las_vegas"
    file_path = os.listdir(dir_)
    files_csv = [file for file in file_path if file.endswith('.csv')]
    subestation_: List[Data] = []
    for name_file in files_csv:
        subestation_name = name_file.split("-")[3].replace(" ","").replace(".csv", "")
        df = pd.read_csv(dir_+"/"+name_file,delimiter=delimeter_,dtype=None)
        df = df.drop(columns=['ÍTEM', 'PRUEBA RTU ORION LX+', 'DIRECCIÓN DNP3'])

        df_analogic = df[df["Tipo"] == "Analoga"]
        df_name_analogic = df_analogic["VARIABLE"].unique()
        var_analogic = df_to_objetc(df_name_analogic)
        df_state = df[df["Tipo"] == "Digital"]
        df_name_state = df_state["VARIABLE"].unique()
        subestation = Data(name_coordinado=coordinado_name, subestation=subestation_name, 
                            variables_analogic=var_analogic, variables_state=df_name_state)
        subestation_.append(subestation)
    
    subestation_.append(read_data_sitr_north())
    return subestation_
