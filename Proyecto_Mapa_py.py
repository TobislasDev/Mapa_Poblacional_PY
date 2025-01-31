#Importamos las librerias a utilizar.
import folium
from folium.plugins import MarkerCluster, HeatMap, MiniMap
from branca.colormap import linear
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import unicodedata
#Proyecto MAPS PY, en este proyecto realizaremos un mapa interactivo con datos relacionados a Paraguay, en el cual podremos ver la cantidad de poblacion en los distintos departamentos del Pais.


#Definimos una funcion para normalizar los datos.
#NFD: El modo NFD Normal Form Decoposition, descompone los caracteres compuestos, (como á,é) en sus componentes básicos.
def normalizar_texto(texto):
    if isinstance(texto, str):
        texto=unicodedata.normalize('NFD', texto)
        texto=''.join(char for char in texto if unicodedata.category(char)!='Mn')
        texto=texto.upper()
    return texto


#Leemos el archivo shaperfile con la ruta correspondiente
fg_paraguay_shp= gpd.read_file("C:/Users/tobislasdev/Desktop/Proyecto MAPS/SHP PY/PAIS/PAIS/Ciudades_Paraguay.shp")
#Generamos un diccionario para poder modificar las tildes y letras como ñ, de tal modo a poder mostrar los datos limpios en pantalla
reemplazos = {'CONCEPCI�N': 'CONCEPCION',
             'BEL�N': 'BELEN',
             'SAN L�ZARO': 'SAN LORENZO',
             'YBY YA�': 'YBY YAU',
             'SARGENTO JOS� F�LIX L�PEZ':'SARGENTO JOSE FELIX LOPEZ',
             'SAN PEDRO DEL YCUAMANDYY�': 'SAN PEDRO DEL YCUAMANDYYU',
             'CHOR�': 'CHORE', 
             'ITACURUB� DEL ROSARIO': 'ITACURUBI DEL ROSARIO', 
             'TACUAT�': 'TACUATI', 
             'UNI�N': 'UNION',
             'LIBERACI�N':'LIBERACION',
             'CAACUP�':'CAACUPE', 
             'ATYR�':'ATYRA', 
             'ISLA PUC�':'ISLA PUCU',
             'ITACURUB� DE LA CORDILLERA':'ITACURUBI DE LA CORDILLERA', 
             'TOBAT�':'TOBATI',
             'CAPIT�N MAURICIO JOS� TROCHE':'CAPITAN MAURICIO JOSE TROCHE',
             'CORONEL MART�NEZ':'CORONEL MARTINEZ',
             'F�LIX P�REZ CARDOZO':'FELIX PEREZ CARDOZO', 
             'ITAP�':'ITAPI', 
             'JOS� FASSARDI':'JOSE FASSARDI', 
             '�UM�':'NUMI',
             'CAAGUAZ�':'CAAGUAZU', 
             'CARAYA�':'CARAYAO', 
             'DR. CECILIO B�EZ':'DR. CECILIO BAEZ',
             'REPATRIACI�N':'REPATRIACION', 
             'SAN JOAQU�N':'SAN JOAQUIN', 
             'SAN JOS� DE LOS ARROYOS':'SAN JOSE DE LOS ARROYOS', 
             'YH�':'YHU',
             'RA�L ARSENIO OVIEDO':'RAUL ARSENIO OVIEDO', 
             'JOS� DOMINGO OCAMPOS':'JOSE DOMINGO OCAMPOS',
             'MARISCAL FRANCISCO SOLANO L�PE':'MARISCAL FRANCISCO SOLANO LOPE', 
             'SIM�N BOLIVAR':'SIMON BOLIVAR', 
             'VAQUER�A':'VAQUERIA', 
             'TEMBIAPOR�':'TEMBIAPORA',
             'CAAZAP�':'CAAZAPA',
             'ABA�':'ABAI', 
             'DR. MOIS�S S. BERTONI':'DR. MOISES S. BERTONI',
             'TAVA�':'TAVAI',
             'ENCARNACI�N':'ENCARNACION', 
             'CAMBYRET�':'CAMBYRETA', 
             'CAPIT�N MEZA':'CAPITAN MEZA', 
             'CAPIT�N MIRANDA':'CAPITAN MIRANDA', 
             'CARMEN DEL PARAN�':'CARMEN DEL PARANA', 
             'CARLOS ANTONIO L�PEZ':'CARLOS ANTONIO LOPEZ',
             'JES�S':'JESUS', 
             'JOS� LEANDRO OVIEDO':'JOSE LEANDRO OVIEDO', 
             'MAYOR JULIO DIONISIO OTA�O':'MAYOR JULIO DIONISIO OTANO', 
             'SAN PEDRO DEL PARAN�':'SAN PEDRO DEL PARANA', 
             'SAN RAFAEL DEL PARAN�':'SAN RAFAEL DEL PARANA', 
             'TOM�S ROMERO PEREIRA':'TOMAS ROMERO PEREIRA', 
             'ALTO VER�':'ALTO VERA', 
             'SAN JUAN DEL PARAN�':'SAN JUAN DEL PARANA', 
             'PIRAP�':'PIRAPO', 
             'ITAP�A POTY':'ITAPUA POTY',
             'SANTA MAR�A':'SANTA MARIA', 
             'PARAGUAR�':'PARAGUARI', 
             'CAAPUC�':'CAAPUCU', 
             'CARAPEGU�':'CARAPEGUA', 
             'PIRAY�':'PIRAYU', 
             'QUYQUYH�':'QUYQUYHO',
             'SAPUC�I':'SAPUCAI', 
             'TEBICUARY-M�':'TEBICUARY-MI',
             'YAGUAR�N':'YAGUARON', 
             'YBYCU�':'YBYCUI', 
             'YBYTYM�':'YBYTYMI', 
             'DOMINGO MART�NEZ DE IRALA':'DOMINGO MARTINEZ DE IRALA',
             'DR. JUAN LE�N MALLORQU�N':'DR. JUAN LEON MALLORQUIN', 
             '�ACUNDAY':'NACUNDAY', 
             'YGUAZ�':'YGUAZU', 
             'MINGA GUAZ�':'MINGA GUAZU', 
             'MINGA POR�':'MINGA PORA', 
             'MBARACAY�':'MBARACAYU', 
             'IRU�A':'IRUNA', 
             'SANTA FE DEL PARAN�':'SANTA FE DEL PARANA', 
             'DR. RA�L PE�A':'DR. RAUL PENA',
             'AREGU�':'AREGUA', 
             'CAPIAT�':'CAPIATA', 
             'GUARAMBAR�':'GUARAMBARE', 
             'IT�':'ITA',
             'ITAUGU�':'ITAUGUA', 
             'LAMBAR�':'LAMBARE', 
             '�EMBY':'NEMBY', 
             'YPACARA�':'YPACARAI',
             'YPAN�':'YPANE',
             'GRAL. JOS� EDUVIGIS D�AZ':'GRAL. JOSE EDUVIGIS DIAZ',
             'GUAZ�-CU�':'GUAZU-CUA',
             'HUMAIT�':'HUMAITA',
             'ISLA UMB�':'ISLA UMBU', 
             'MAYOR JOS� DEJES�S MART�NEZ': 'MAYOR JOSE DEJESUS MARTINEZ',
             'SAN JUAN BAUTISTA DE �EEMBUC�':'SAN JUAN BAUTISTA DE NEEMBUCU', 
             'VILLALB�N':'VILLALBIN',
             'CAPIT�N BADO':'CAPITAN BADO', 
             'ZANJA PYT�':'ZANJA PYTY', 
             'SALTO DEL GUAIR�':'SALTO DEL GUAIRA', 
             'VILLA YGATIM�':'VILLA YGATIMI', 
             'ITANAR�':'ITANARA',
             'YPEJH�':'YPEJHU',
             'KATUET�':'KATUETR',
             'LA PALOMA DEL ESP�RITU SANTO':'LA PALOMA DEL ESPIRITU SANTO',
             'YASY CA�Y':'YASY CANY',
             'YBYRAROBAN�':'YBYRAROBANA', 
             'BENJAM�N ACEVAL':'BENJAMIN ACEVAL', 
             'JOS� FALC�N':'JOSE FALCON', 
             'TTE. 1� MANUEL IRALA FERN�NDEZ':'TTE. 1RO MANUEL IRALA FERNANDEZ',
             'TENIENTE ESTEBAN MART�NEZ':'TENIENTE ESTEBAN MARTINEZ', 
             'GENERAL JOS� MAR�A BRUGUEZ':'GENERAL JOSE MARIA BRUGUEZ',
             'MARISCAL JOS� F�LIX ESTIGARRIB':'MARISCAL JOSE FELIX ESTIGARRIB',
             'BAH�A NEGRA':'BAHIA NEGRA',
             'ASUNCI�N':'ASUNCION'}



#Lectura de archivos adicionales, datos de Asuncion y la poblacion en general.
fg_asuncion_shp= gpd.read_file("C:/Users/tobislasdev/Desktop/Proyecto MAPS/00 ASUNCION/00 ASUNCIÓN/Departamento_Asuncion.shp")
fg_poblacion_csv = pd.read_csv("C:/Users/tobislasdev/Desktop/Proyecto MAPS/Poblacion_PY.csv")
reemplazos['ASUNCI�N']='ASUNCION'
#Archivo para los datos del departamentos.
fg_departamentos_shp=gpd.read_file("C:\\Users\\tobislasdev\\Desktop\\Proyecto MAPS\\SHP PY\\PAIS\\PAIS\\Departamentos_Paraguay.shp")


fg_asuncion_shp['DPTO_DESC'] = fg_asuncion_shp['DPTO_DESC'].apply(normalizar_texto)

for original, reemplazo in reemplazos.items():
        fg_asuncion_shp['DPTO_DESC'] = fg_asuncion_shp['DPTO_DESC'].replace(original, reemplazo)
      
#Realizamos los cambios del archivo con nuestro diccionario generado
for original, reemplazo in reemplazos.items():
    fg_paraguay_shp['DIST_DESC'] = fg_paraguay_shp['DIST_DESC'].replace(original, reemplazo)

paraguay_ciudades = list(fg_paraguay_shp['DIST_DESC'])
punto = Point(-57.601,-25.286)
lat_lon = [punto.y, punto.x]
poblacion_distrito= list(fg_poblacion_csv['#'])
poblacion_distrito= list(fg_poblacion_csv['2025'])

#Definimos una funcion para poder pasar los datos en Mayusculas.
def pasar_nombres_mayus(dataframe, columna):
    dataframe[columna]=dataframe[columna].str.upper()
    return dataframe

poblacion_distrito=pasar_nombres_mayus(fg_poblacion_csv,'#')

#Procedemos a normalizar los datos con la funcion que habiamos generado con anterioridad.
fg_paraguay_shp['DIST_DESC']=fg_paraguay_shp['DIST_DESC'].astype(str).apply(normalizar_texto)

#Generamos una funcion para asignar colores en base a la cantidad poblacional

fg_poblacion_csv['2025'] = pd.to_numeric(fg_poblacion_csv['2025'], errors='coerce')
fg_poblacion_csv['2025'] = fg_poblacion_csv['2025'].fillna(0)

def obtener_color(poblacion):
    if poblacion < 20000:
        return 'green'
    elif poblacion < 120000:
        return 'blue'  
    elif poblacion < 150000:
        return 'orange'  
    elif poblacion < 200000:
        return 'red' 
    else:
        return 'darkred'  

#Generamos HTML para implementar en el mapa
html="""<h3>Distrito:</h3>"""
map = folium.Map(location=lat_lon, zoom_start=12, tiles="CartoDB Positron")

fg = MarkerCluster(name="PY MAP")
#Generamos un titulo para el MAPA
title_html = title_html = '''
<div style="
    position: absolute;
    top: 10px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 1000;
    background-color: rgba(255, 255, 255, 0.95);
    padding: 12px 24px;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(0, 0, 0, 0.1);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 18px;
    font-weight: 600;
    color: #333;
    text-align: center;
    transition: all 0.3s ease;
    cursor: pointer;
    animation: fadeIn 1s ease-in-out;
">
    Mapa Interactivo de Paraguay - Población 2025
</div>

<style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateX(-50%) translateY(-20px); }
        to { opacity: 1; transform: translateX(-50%) translateY(0); }
    }
</style>
'''

# Añadir el título al mapa
map.get_root().html.add_child(folium.Element(title_html))

legend_html = '''
<div style="
    position: fixed;
    bottom: 50px;
    left: 50px;
    width: 250px;
    background-color: rgba(255, 255, 255, 0.9);
    border: 1px solid rgba(0, 0, 0, 0.2);
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    z-index: 9999;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 14px;
    padding: 15px;
    color: #333;
    transition: all 0.3s ease;  /* Transición suave */
">
    <b style="font-size: 16px; margin-bottom: 10px; display: block;">Mapa de Población</b>
    <div style="display: flex; align-items: center; margin-bottom: 8px;">
        <span style="background-color: green; width: 20px; height: 20px; display: inline-block; margin-right: 10px; border-radius: 4px;"></span>
        Menos de 20,000
    </div>
    <div style="display: flex; align-items: center; margin-bottom: 8px;">
        <span style="background-color: blue; width: 20px; height: 20px; display: inline-block; margin-right: 10px; border-radius: 4px;"></span>
        20,000 - 89,999
    </div>
    <div style="display: flex; align-items: center; margin-bottom: 8px;">
        <span style="background-color: orange; width: 20px; height: 20px; display: inline-block; margin-right: 10px; border-radius: 4px;"></span>
        90,000 - 120,000
    </div>
    <div style="display: flex; align-items: center; margin-bottom: 8px;">
        <span style="background-color: red; width: 20px; height: 20px; display: inline-block; margin-right: 10px; border-radius: 4px;"></span>
        120,000 - 199,999
    </div>
    <div style="display: flex; align-items: center;">
        <span style="background-color: darkred; width: 20px; height: 20px; display: inline-block; margin-right: 10px; border-radius: 4px;"></span>
        Más de 200,000
    </div>
</div>

<script>
    // Efecto al pasar el ratón
    const legend = document.querySelector('div');
    legend.addEventListener('mouseover', () => {
        legend.style.backgroundColor = 'rgba(245, 245, 245, 0.98)';
        legend.style.boxShadow = '0 6px 16px rgba(0, 0, 0, 0.3)';
    });
    legend.addEventListener('mouseout', () => {
        legend.style.backgroundColor = 'rgba(255, 255, 255, 0.9)';
        legend.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.2)';
    });
</script>
'''
map.get_root().html.add_child(folium.Element(legend_html))

#Vamos a proceder a agregar los polígonos de los departamentos, lo que realiza es lo siguiente, enmarca con una linea negra los limites de los distintos departamentos, esto gracias a nuestro archivo fg_departamento_shp.

folium.GeoJson(
    fg_departamentos_shp,
    name='Limites de Departamentos',
    style_function=lambda x: {
        'fillColor': 'transparent',
        'color': 'black',
        'weight': 1
    }
).add_to(map)

#Personalizamos con HTML/CSS el ICON.

icon_html = '''
<div style="
    background-color: white;
    border: 2px solid black;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
    display: flex;
    align-items: center;
    justify-content: center;
">
    <span style="color: red; font-size: 14px;">📍</span>
</div>
'''

#Agregamos un MiniMap, ayuda al usuario a desplazarse por el mapa.

minimap =  MiniMap(toggle_display=True, position="bottomright")
map.add_child(minimap)
#Creamos una lista para el mapa de calor
mapa_calor=[]
#Añadimos los marcadores para cada ciudad, con este bucle recorremos cada fila de nuestro archivo fg_paraguau_shp, luego buscamos la poblacion correspondiente a cada distrito. 
for _, row in fg_paraguay_shp.iterrows():
    if row.geometry:  # Validar que la geometría no sea nula
        punto = row.geometry
        if punto.geom_type == 'Point':  # Asegurarse de que sea un punto
            lat_lon = [punto.y, punto.x]
            name = row['DIST_DESC']
            name_normalized=name.upper()

            # Buscar la población correspondiente al distrito
            poblacion = fg_poblacion_csv.loc[fg_poblacion_csv['#'] == name, '2025'].values
            if len(poblacion) > 0:
                mapa_calor.append([punto.y, punto.x, int(poblacion[0])])
                poblacion_texto =int(poblacion[0])
                color = obtener_color(poblacion_texto)
                poblacion_texto = f"Población: {poblacion_texto:,}"
            else:
                color='gray' #Agregamos un color por defecto en caso de que no podamos obtener la poblacion
                poblacion_texto = "Población: No disponible"

            iframe = folium.IFrame(f"<h4>{name}</h4><p>{poblacion_texto}</p>", width=200, height=100)
            fg.add_child(
                folium.Marker(
                    location=lat_lon,
                    radius=6,
                    popup=folium.Popup(iframe),
                    tooltip=name,
                    icon=folium.DivIcon(html=icon_html)
                )
            )
if mapa_calor: #validamos y agregamos HeatMap a nuestro mapa
    heatmap_layer=HeatMap(
        mapa_calor, 
        min_opacity=0.4, 
        radius=15,
        blur=10,
        max_zoom=10)
    
map.add_child(heatmap_layer)
map.add_child(fg)


#Guardamos el mapa.
map.save("Mapa_Paraguay.html")