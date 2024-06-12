import geopandas as gpd

# Especifica la ruta del archivo .shp
ruta_archivo_shp = 'C:/Users/mario/Downloads/mfe_madrid/MFE_30.shp'

# Lee el archivo .shp
datos_gis = gpd.read_file(ruta_archivo_shp)

# Visualiza los datos
print(datos_gis.head())
