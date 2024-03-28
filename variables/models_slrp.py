from pydantic import BaseModel
 
    
class CoordinadoCSV(BaseModel):
    codigo: str
    nombre: str
    
    
class SubestacionCSV(BaseModel):
    codigo: int
    proteccion_name: str
    codigo_coord: str
    
    
class ProteccionCSV(BaseModel):
    cod_proteccion: str
    nombre_proteccion: str
    cod_identificacion_paño_barra: str
    
    
class EventosCSV(BaseModel):
    cod_eventos: str
    fecha_evento: str
    hora: str
    cod_proteccion: str
    
class OscilografiaCSV(BaseModel):
    cod_oscilografia: str
    fecha_oscilografia: str
    hora: str
    cod_proteccion: str
    
class AjustesCSV(BaseModel):
    cod_ajustes: str
    fecha_ajuste: str
    hora: str
    cod_proteccion: str
    
class PanoBarraCSV(BaseModel):
    cod_identificacion_pano_barra: str
    nombrepb: str
    cod_subestacion: int
    cod_categoria_paño_barra: str