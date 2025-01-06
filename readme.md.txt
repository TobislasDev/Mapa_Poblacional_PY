#Proyecto de Mapa Poblacional del Paraguay.

Este proyecto crea un mapa interactivo del Paraguay, con el que podremos visualizar los datos poblacionales de los distintos distritos.
Utilizamos archivos geoespaciales y datos poblacionales del país para mostrar el mapa detallado del Paraguay.

El proyecto utiliza archivos geoespaciales del Paraguay, también los datos poblacionales. 
Los archivos necesarios se pueden descargar en los siguientes enlaces:
- [Descargar datos SHP del Paraguay](https://www.ine.gov.py/microdatos/cartografia-digital-2012.php)
- [Descargar datos Poblacionales] (https://www.ine.gov.py/microdatos/indicador.php?ind=16)

Una vez descargados los archivos, colocalos dentro de la carpeta(puedes crear una estructura de carpetas si no existe), y copia las rutas de direccion.
Ejemplo=fg_paraguay_shp= gpd.read_file("Aqui debe ir la ruta de direccion/Ciudades_Paraguay.shp")

##Requisitos
-Python 3.x
-Pandas
-GeoPandas
-Folium

Ejemplo para poder instalar dependencias necesarias.
-pip install pandas geopandas folium


