
## Script de datos

Este repositorio corresponde para la inicializacion de datos para los sistemas implementados
SITR y SLRP con el modelo actual para ambos sistemas

## Creacion DB

Primero clonar el presente repositorio, dirigirse al path principal de el script, despues de eso necesitan 
crear su entorno virtual con el siguiente comando

```
python -m venv [nombre de entorno]
```

Luego dirigirse a la carpeta y ejecutar el entorno corresponde 

```
.\[nombre de entorno]\Scripts\activate 

```

Luego de esto porfavor instarlar los requerimientos necesarios para poder ejecutar el script con el siguiente comando

```
pip install -r requirements.txt

Para actualzar los requirements utilizen este comando

pip freeze | Out-File -Encoding UTF8 requirements.txt
```

### Database SITR

Para crear la base de datos del Sistema de Información en Tiempo Real, utilicen el siguiente comando

```
python -m script_sitr -create true
```
Con lo anterior, su base de datos MongoDB estará inicializada con los modelos definidos.

Para agregar datos a este modelo en tiempo real, necesitan ejecutar el siguiente comando
```
python -m main 
```
Se les solicitará la cantidad de veces que corresponde ejecutar el script, que puede variar entre 1 y 13 subestaciones. Además, se deberá especificar la categoría de tiempo en la que se ejecutará el script, ya sea en segundos (sec) o en horas (hrs). Finalmente, se pedirá ingresar la cantidad de horas o segundos según la selección anterior.

Ejemplo 
```
numero de veces a ejecutar : 13
Categoria de tiempo hrs o sec : hrs
Cantidad de horas o sec : 24
```
Lo anterior se ejecutara durante 24 horas, en 13 subestaciones.


### DataBase SLRP¨

Para crear la base de datos del Sistema de lectura de protecciones, utilicen el siguiente comando

```
python -m script_slrp
```
Con lo anterior, su base de datos MongoDB estará inicializada con los modelos definidos, ademas de los datos de los csv dentro de las carpetas.

Importante

**NECESITAN TENER INSTALADO MONGODB** 

En la version mas actualizada o por defecto en la version 5 posterior para el soporte de collecciones de series de tiempo