#!/usr/bin/env python
# coding: utf-8

# In[2]:


#GRUPO LMJ
# Alamo Malena
# Lucio Tag
# Jeremias Laria Guaza


# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as sp


# # CREAMOS LOS DATAFRAMES VACIOS

# In[3]:


# PK = {'establecimiento'}
df_estab_prod = pd.DataFrame(columns=['establecimiento', 'departamento', 'clae2', 'prop_muj','letra'])


# In[4]:


# PK = {'establecimiento', 'productos'}
df_prod_org = pd.DataFrame(columns=['productos', 'establecimiento'])


# In[5]:


# PK = {'clae2'}
df_dicc_clae = pd.DataFrame(columns = ['clae2, clae2_desc'])


# In[6]:


# PK = {'nom_depto'}
df_deptos = pd.DataFrame(columns = ['nom_depto', 'nom_prov'])


# In[7]:


# PK = {'departamento', 'razon_social'}
df_oper_org = pd.DataFrame(columns=['establecimiento', 'razon_social'])


# In[8]:


# PK = {'provincia_id'}
df_prov = pd.DataFrame(columns=['provincia_id', 'provincia'])


# ## IMPORTAMOS FUENTES PRIMARIAS Y SECUNDARIAS

# In[9]:


import csv

padron = "\malen\Deskpot\DATOS\CARRERA\labodatos\padron.csv"
establecimientos = "\malen\Deskpot\DATOS\CARRERA\labodatos\establecimientos.csv"
localidad_bahra = "\malen\Deskpot\DATOS\CARRERA\labodatos\localidad_bahra.csv"
clae_agg = "\malen\Deskpot\DATOS\CARRERA\labodatos\clae_agg.csv"

with open(padron, 'r', encoding='utf-8', errors='replace') as file:
    padron = file.read()
with open(establecimientos, 'r', encoding='utf-8', errors='replace') as file:
    establecimiento = file.read()
with open(localidad_bahra, 'r', encoding='utf-8', errors='replace') as file:
    localidades = file.read()
with open(clae_agg, 'r', encoding='utf-8', errors='replace') as file:
    clae_agg = file.read()

from io import StringIO
df_padron = pd.read_csv(StringIO(padron))
df_establecimiento = pd.read_csv(StringIO(establecimiento))
df_localidades = pd.read_csv(StringIO(localidades))
df_clae = pd.read_csv(StringIO(clae_agg))


# # Analizamos las fuentes para ver que informacion tenemos

# ## Informacion de cada tabla

# In[ ]:


print('Establecimiento')
print(" ")
print(df_establecimiento.info())


# In[ ]:


print('Padron')
print(" ")
print(df_padron.info())


# In[ ]:


print('Dicc Clae')
print(" ")
print(df_clae.info())


# In[ ]:


print('Localidades')
print(" ")
print(df_localidades.info())


# ## Miramos los primeros datos

# In[ ]:


df_establecimiento.head()


# In[ ]:


df_localidades.head()


# In[ ]:


df_clae.head()


# In[ ]:


df_padron.head()


# ## Algunas observaciones y arreglos

# In[ ]:


#Vemos que razon_social no implica departamento, ya que hay razones sociales con mas de un departamento (para elegir primary key).
razones_multiples_departamentos = df_padron.groupby('raz�n social')['departamento'].nunique()
razones_con_mas_de_un_departamento = razones_multiples_departamentos[razones_multiples_departamentos > 1]
print(razones_con_mas_de_un_departamento)


# In[ ]:


#Ejemplo de razon social con mas de un departamento
df_padron[df_padron['raz�n social']=='ALVIPA SRL']


# In[ ]:


df_deptos


# In[ ]:


#Vemos los repetidos
depto_prov = df_localidades[['nombre_departamento','nombre_provincia']]


depto_prov = depto_prov.drop_duplicates()

departamentos = depto_prov['nombre_departamento']

cantidad = departamentos.value_counts()

repetidos = cantidad[cantidad>1]

cantidad


# In[ ]:


def eliminarDuplicados():
    for lugar,cant in repetidos.items():
        df_padron.loc[df_padron['departamento'] == lugar, 'departamento'] += " " + df_padron['provincia']
        df_localidades.loc[df_localidades['nombre_departamento'] == lugar.capitalize(), 'nombre_departamento'] += " " + df_localidades['nombre_provincia']
        df_establecimiento.loc[df_establecimiento['departamento'] == lugar.capitalize(), 'departamento'] += " " + df_establecimiento['departamento']


# In[ ]:


eliminarDuplicados()


# In[ ]:


#Repetimos a ver si se eliminaron:

depto_prov = df_padron[['departamento','provincia']]

depto_prov = depto_prov.drop_duplicates()

departamentos = depto_prov['departamento']

print(departamentos.value_counts())


# # Creamos los Dataframes

# In[ ]:


df_dicc_clae = df_clae[['clae2', 'clae2_desc']]
df_dicc_clae = df_dicc_clae.drop_duplicates()


# In[ ]:


df_deptos = df_localidades[['nombre_departamento', 'nombre_provincia']]
df_deptos = df_deptos.drop_duplicates()


# In[ ]:


df_oper_org = df_padron[['establecimiento', 'raz�n social']]
df_oper_org = df_oper_org.drop_duplicates()


# In[ ]:


df_prod_org = df_padron[['establecimiento','productos']]
df_prod_org = df_prod_org[df_prod_org['establecimiento']!='NC']
df_prod_org = df_prod_org.drop_duplicates()


# In[ ]:


df_estab_prod = df_establecimiento[['ID','departamento','clae2','proporcion_mujeres','letra']]
df_estab_prod = df_estab_prod.drop_duplicates()


# In[ ]:


df_est_deptos_org = df_padron[['establecimiento','departamento']]


# # LIMPIEZA DE DATOS

# ### Deptos

# Convertimos el atributo nombre_departamento en atomico. Lo unico a modificar es el caso de las comunas de Buenos Aires, vamos a tener una fila por cada comuna.

# In[ ]:


df_deptos[df_deptos["nombre_departamento"]=='Comuna 1,Comuna 10,Comuna 11,Comuna 12,Comuna 13,Comuna 14,Comuna 15,Comuna 2,Comuna 3,Comuna 4,Comuna 5,Comuna 6,Comuna 7,Comuna 8,Comuna 9\n']


# In[ ]:


# Eliminamos la fila que cambiamos.
df_deptos.drop(3526, inplace=True)


# In[ ]:


df_deptos["nombre_departamento"].unique()


# In[ ]:


## Convertimos la fila de comunas a atributos atomicos

comunas = [
    'Comuna 1', 'Comuna 10', 'Comuna 11', 'Comuna 12', 'Comuna 13',
    'Comuna 14', 'Comuna 15', 'Comuna 2', 'Comuna 3', 'Comuna 4',
    'Comuna 5', 'Comuna 6', 'Comuna 7', 'Comuna 8', 'Comuna 9'
]

df_comunas = pd.DataFrame({'nombre_departamento': comunas,'nombre_provincia': ['Ciudad de Buenos Aires'] * len(comunas)})

df_deptos = pd.concat([df_deptos, df_comunas], ignore_index=True)


# In[ ]:


# Verificamos que el cambio este bien.
df_deptos["nombre_departamento"].unique()


# ### Prod Org

# In[ ]:


df_prod_org


# In[ ]:


df_prod_org['establecimiento'].unique()


# In[ ]:


# Reemplazamos manualmente los errores, ya que depende de la fila.
df_prod_org["establecimiento"] = df_prod_org["establecimiento"].str.replace("N�", "N")
df_prod_org["establecimiento"] = df_prod_org["establecimiento"].str.replace("MALARG�E", "MALARGUE")
df_prod_org["establecimiento"] = df_prod_org["establecimiento"].str.replace("DESAG�E", "DESAGUE")


# In[ ]:


# Las que quedan son ñ's
df_prod_org["establecimiento"] = df_prod_org["establecimiento"].str.replace("�", "N")


# In[ ]:


df_prod_org[df_prod_org["productos"].isna()]


# In[ ]:


# Eliminamos los datos nulos.
df_prod_org = df_prod_org.drop(628)
df_prod_org = df_prod_org.drop(784)


# In[ ]:


# Convertimos el atributo productos en atomico
def separar_productos(fila):
    productos = fila['productos'].split(',') # Primero corregimos los productos separados por coma.
    for producto in productos:
        subproductos = producto.split(" Y ") # Luego corregimos los productos que esten separados por Y.
        for subproducto in subproductos:
            nueva_fila = fila.copy()
            nueva_fila['productos'] = subproducto
            df_prod_org.loc[df_prod_org.index.max() + 1] = nueva_fila


# In[ ]:


# Con .apply aplicamos la funcion separar_productos en cada fila de df_prod_org
df_prod_org.apply(separar_productos, axis=1)


# In[ ]:


# Como en la funcion agregamos las filas corregidas al final del dataframe, borramos las primeras 919.
df_prod_org = df_prod_org.iloc[919:]


# In[ ]:


df_prod_org["productos"].unique()


# In[ ]:


# Buscamos los productos que tengan un +
for producto in df_prod_org["productos"]:
        if "+" in producto:
            print(producto)


# In[ ]:


df_prod_org[df_prod_org["productos"]=="MIEL + EXTRACCION DE MIEL"]


# In[ ]:


df_prod_org[df_prod_org["productos"]=="MIEL + EXTRACCION"]


# In[ ]:


# Reemplazamos manualmente los casos donde hay un +
df_prod_org.loc[1794, "productos"] = "MIEL"
df_prod_org.loc[3083, "productos"] = "MIEL"


# In[ ]:


# Funcion para separar los productos divididos por -
def separar_iones(fila):
    if ("-" in fila['productos']):
        productos = fila['productos'].split('-')
        for producto in productos:
            nueva_fila = fila.copy()
            nueva_fila['productos'] = producto
            df_prod_org.loc[df_prod_org.index.max() + 1] = nueva_fila


# In[ ]:


df_prod_org.apply(separar_iones, axis=1)


# In[ ]:


df_prod_org[df_prod_org["productos"]=="CEBADA-ALFALFA-VICIA-RABANITO-NABO-REMOLACHA-RUCULA-LECHUGA-PUERRO-CEBOLLA"]


# In[ ]:


df_prod_org = df_prod_org.drop(1523)


# In[ ]:


def separar_signos(fila):
    if ("\?" in fila['productos']):
        productos = fila['productos'].split('\?')
        for producto in productos:
            nueva_fila = fila.copy()
            nueva_fila['productos'] = producto
            df_prod_org.loc[df_prod_org.index.max() + 1] = nueva_fila


# In[ ]:


df_prod_org.apply(separar_signos,axis=1)


# In[ ]:


filtro = df_prod_org['productos'].str.contains('\?', na=False)
df_prod_org[filtro]


# In[ ]:


df_prod_org = df_prod_org.drop(1810)
df_prod_org = df_prod_org.drop(3181)
df_prod_org = df_prod_org.drop(3182)


# In[ ]:


# Analizamos lo que nos quedo
df_prod_org["productos"].unique()


# In[ ]:


# Reemplazamos manualmente los casos especificos.

df_prod_org.loc[df_prod_org['productos'].str.contains("HORTICULTURA"  ), 'productos'] = "HORTICULTURA"

df_prod_org.loc[df_prod_org['productos'].str.contains("CHIA"  ), 'productos'] = "CHIA"

df_prod_org.loc[df_prod_org['productos'].str.contains("OLIVO"  ), 'productos'] = "OLIVOS"

df_prod_org.loc[df_prod_org['productos'].str.contains("GANADERIA OVINA"  ), 'productos'] = "GANADERIA OVINA"

condicion_avellana = (df_prod_org['productos'].str.contains("LANA") & ~df_prod_org['productos'].str.contains("AVELLANAS"))
df_prod_org.loc[condicion_avellana, 'productos'] = "LANA"

condicion_uvas = (df_prod_org['productos'].str.contains("UVA") & ~df_prod_org['productos'].str.contains("PASA") & ~df_prod_org['productos'].str.contains("VINIFICAR"))
df_prod_org.loc[condicion_uvas, 'productos'] = "UVAS"

df_prod_org.loc[df_prod_org['productos'].str.contains("CA�A DE AZUCAR"  ), 'productos'] = "CANA DE AZUCAR"

df_prod_org.loc[df_prod_org['productos'].str.contains("CA�A DE CASTILLA"  ), 'productos'] = "CANA DE CASTILLA"

df_prod_org.loc[df_prod_org['productos'].str.contains("ALFALFA"  ), 'productos'] = "ALFALFA"

df_prod_org.loc[df_prod_org['productos'].str.contains("HORTALIZA"  ), 'productos'] = "HORTALIZAS"

df_prod_org.loc[df_prod_org['productos'].str.contains("CASTA�A"  ), 'productos'] = "CASTANA"

df_prod_org.loc[df_prod_org['productos'].str.contains("\:"  ), 'productos'] = "FRUTALES"

df_prod_org.loc[df_prod_org['productos'].str.contains("GIRASOL"  ), 'productos'] = "GIRASOL"

df_prod_org.loc[df_prod_org['productos'].str.contains("ARANDANO"  ), 'productos'] = "ARANDANO"

df_prod_org.loc[df_prod_org['productos'].str.contains("VERDEO"  ), 'productos'] = "CEBOLLA DE VERDEO"

df_prod_org.loc[df_prod_org['productos'].str.contains("ARVEJA"  ), 'productos'] = "ARVEJAS"

df_prod_org.loc[df_prod_org['productos'].str.contains("BERENJENA"  ), 'productos'] = "BERENJENAS"

df_prod_org.loc[df_prod_org['productos'].str.contains("CERELAES"  ), 'productos'] = "CEREALES"

df_prod_org.loc[df_prod_org['productos'].str.contains("CIRUELA"  ), 'productos'] = "CIRUELAS"

df_prod_org.loc[df_prod_org['productos'].str.contains("DAMASCO"  ), 'productos'] = "DAMASCOS"

df_prod_org.loc[df_prod_org['productos'].str.contains("ESPARRAGO"  ), 'productos'] = "ESPARRAGO"

condicion_uvas = (df_prod_org['productos'].str.contains("FRUT") & ~df_prod_org['productos'].str.contains("FRUTILLA"))
df_prod_org.loc[condicion_uvas, 'productos'] = "FRUTOS"

df_prod_org.loc[df_prod_org['productos'].str.contains("GUINDA"  ), 'productos'] = "GUINDAS"

df_prod_org.loc[df_prod_org['productos'].str.contains("HIGO"  ), 'productos'] = "HIGOS"

df_prod_org.loc[df_prod_org['productos'].str.contains("HOJA"  ), 'productos'] = "HOJAS"

df_prod_org.loc[df_prod_org['productos'].str.contains("KIWI"  ), 'productos'] = "KIWIS"

df_prod_org.loc[df_prod_org['productos'].str.contains("MANZANA"  ), 'productos'] = "MANZANAS"

df_prod_org.loc[df_prod_org['productos'].str.contains("MANZANZA"  ), 'productos'] = "MANZANAS"

df_prod_org.loc[df_prod_org['productos'].str.contains("MEDICINALES"  ), 'productos'] = "MEDICINALES"

df_prod_org.loc[df_prod_org['productos'].str.contains("MORA"  ), 'productos'] = "MORAS"

df_prod_org.loc[df_prod_org['productos'].str.contains("NUECES"  ), 'productos'] = "NUEZ"

df_prod_org.loc[df_prod_org['productos'].str.contains("OELAGINOSAS"  ), 'productos'] = "OLEAGINOSAS"

df_prod_org.loc[df_prod_org['productos'].str.contains("PALTA"  ), 'productos'] = "PALTAS"

df_prod_org.loc[df_prod_org['productos'].str.contains("PAK CHOY"  ), 'productos'] = "PACK CHOI"

df_prod_org.loc[df_prod_org['productos'].str.contains("PAST"  ), 'productos'] = "PASTURA"

df_prod_org.loc[df_prod_org['productos'].str.contains("PIMIENTO"  ), 'productos'] = "PIMIENTOS"

df_prod_org.loc[df_prod_org['productos'].str.contains("PONELO"  ), 'productos'] = "POMELO"

df_prod_org.loc[df_prod_org['productos'].str.contains("PUERRO"  ), 'productos'] = "PUERROS"

df_prod_org.loc[df_prod_org['productos'].str.contains("REMNOLACHA"  ), 'productos'] = "REMOLACHA"

df_prod_org.loc[df_prod_org['productos'].str.contains("ZUCCHINI"  ), 'productos'] = "ZUCCINI"


# In[ ]:


# Ordenamos alfabeticamente y verificamos si quedo algo por arreglar.
sorted(df_prod_org["productos"].unique())


# In[ ]:


# Eliminamos los espacios al principio y al final de los strings
df_prod_org['productos'] = df_prod_org['productos'].str.strip()


# In[ ]:


filas_duplicadas = df_prod_org.duplicated()
filas_duplicadas.sum()


# In[ ]:


# Eliminamos duplicados
df_prod_org.drop_duplicates(inplace=True)


# In[ ]:


# Eliminamos los puntos y los ) al final de los strings. 
df_prod_org['productos'] = df_prod_org['productos'].str.rstrip('.')
df_prod_org['productos'] = df_prod_org['productos'].str.rstrip(')')


# ### Estab Prod

# In[ ]:


df_estab_prod.info()


# In[ ]:


# Verificamos los departamentos
sorted(df_estab_prod["departamento"].unique())


# In[ ]:


# Verificamos si se repite algun ID.
df_estab_prod["ID"].value_counts()


# In[ ]:


# Verificamos que los valores esten entre 0 y 1
df_estab_prod["proporcion_mujeres"].describe()


# In[ ]:


# Analizamos los clae2 en estab_prod
sorted(df_estab_prod["clae2"].unique())


# In[ ]:


# Verificamos si estan todos en nuestro diccionario de clae
sorted(df_clae["clae2"].unique())


# In[ ]:


## Vemos que el clae2 97 y 99 no figuran en el diccionario de clae 2. Tomamos la decision de reemplazarlo por 999 que corresponde a la categoria otros
df_estab_prod.loc[df_estab_prod["clae2"]==99, "clae2"] = 999
df_estab_prod.loc[df_estab_prod["clae2"]==97, "clae2"] = 999


# ### DICC CLAE

# In[ ]:


df_dicc_clae


# In[ ]:


# Analizamos la descripcion y vemos que no hay nada para limpiar
df_dicc_clae["clae2_desc"].unique()


# ### Operadores Organicos

# In[ ]:


df_oper_org


# In[ ]:


# Cambiamos nombre de columna razon social
df_oper_org = df_oper_org.rename(columns={'raz�n social': 'razon_social'})


# In[ ]:


# Ordenamos las razones sociales para chequear que tenemos que limpiar
sorted(df_oper_org["razon_social"].unique())


# In[ ]:


# Sacamos los espacios de el principio y el final del string
df_oper_org["razon_social"].str.strip()


# In[ ]:


# Corregimos algunos detalles de siglas
df_oper_org['razon_social'] = df_oper_org['razon_social'].str.replace(' SA', ' S.A.')
df_oper_org['razon_social'] = df_oper_org['razon_social'].str.replace(' SRL', ' S.R.L')
df_oper_org['razon_social'] = df_oper_org['razon_social'].str.replace(' SH', ' S.H.')


# In[ ]:


# Reemplazamos las ñ's de razon social
df_oper_org["razon_social"] = df_oper_org["razon_social"].str.replace('�', 'n')


# In[ ]:


# Chequeamos si nos quedo algo
sorted(df_oper_org["razon_social"].unique())


# In[ ]:


# Cambiamos a mano ciertos valores de Establecimiento
df_oper_org["establecimiento"] = df_oper_org["establecimiento"].str.replace("N�", "N")
df_oper_org["establecimiento"] = df_oper_org["establecimiento"].str.replace("MALARG�E", "MALARGUE")
df_oper_org["establecimiento"] = df_oper_org["establecimiento"].str.replace("DESAG�E", "DESAGUE")


# In[ ]:


# Las que quedan son ñ's
df_oper_org["establecimiento"] = df_oper_org["establecimiento"].str.replace("�", "N")


# ## Establecimientos productivos organicos 

# In[ ]:


df_est_deptos_org


# In[ ]:


## Reemplazamos los � de departamento
df_est_deptos_org["departamento"] = df_est_deptos_org["departamento"].str.replace("1� DE MAYO", "1 DE MAYO")
df_est_deptos_org["departamento"] = df_est_deptos_org["departamento"].str.replace("G�EMES", "GUEMES")
df_est_deptos_org["departamento"] = df_est_deptos_org["departamento"].str.replace("MALARG�E", "MALARGUE")
df_est_deptos_org["departamento"] = df_est_deptos_org["departamento"].str.replace("G�ER", "GUER")


# In[ ]:


filtro = df_est_deptos_org['departamento'].str.contains('�')
df_est_deptos_org[filtro]


# In[ ]:


##Las que quedan son ñ's
df_est_deptos_org["departamento"] = df_est_deptos_org["departamento"].str.replace("�", "N")
df_est_deptos_org["departamento"] = df_est_deptos_org["departamento"].str.replace("n", "N")


# In[ ]:


# Reemplazamos los � de establecimiento
df_est_deptos_org["establecimiento"] = df_est_deptos_org["establecimiento"].str.replace("N�", "N")
df_est_deptos_org["establecimiento"] = df_est_deptos_org["establecimiento"].str.replace("MALARG�E", "MALARGUE")
df_est_deptos_org["establecimiento"] = df_est_deptos_org["establecimiento"].str.replace("DESAG�E", "DESAGUE")


# In[ ]:


# Las que quedan son ñ's
df_est_deptos_org["establecimiento"] = df_est_deptos_org["establecimiento"].str.replace("�", "N")


# In[ ]:


# Chequeamos que no haya quedado ninguna
filtro = df_est_deptos_org['departamento'].str.contains('�')
df_est_deptos_org[filtro]


# ## CONSULTAS SQL

# In[ ]:


import pandas as pd
from inline_sql import sql, sql_val


# i) Para cada producto (producido por un productor orgánico) detallar en qué provincias se produce. El orden del reporte debe respetar la cantidad de provincias en las cuales se produce dicho producto (de mayor a menor). En caso de empate, ordenar alfabéticamente por nombre de producto.

# In[ ]:


# Hacemos un join entre df_prod_org y df_est_deptos_org para tener la tabla PRODUCTO-ESTABLECIMIENTO-DEPARTAMENTO
prod_est_dep = sql^"""SELECT p.productos, p.establecimiento, e.departamento 
            FROM df_prod_org AS p
            INNER JOIN df_est_deptos_org AS e
            ON p.establecimiento=e.establecimiento
            """


# Hacemos un join de la tabla anterior con df_deptos para tener la tabla PRODUCTO-PROVINCIA
prod_prov = sql^"""SELECT DISTINCT p.productos, d.nombre_provincia
                FROM prod_est_dep AS p
                INNER JOIN df_deptos AS d
                ON p.departamento=UPPER(d.nombre_departamento)
                ORDER BY productos ASC
                """
#print(prod_prov)

# Agrupamos por producto y provincia para contar la cantidad
cant_prov_prod = sql^"""SELECT productos, COUNT(nombre_provincia) AS cantidad
                FROM prod_prov
                GROUP BY productos
                ORDER BY cantidad DESC, productos ASC
                """

# Hacemos un JOIN entre prod_prov y cant_prov_prod para poder ordenar prod_prov segun cant_prov_prod
prod_prov_ordenado = sql^""" SELECT p.productos, p.nombre_provincia
                FROM prod_prov as p
                INNER JOIN cant_prov_prod as c
                ON c.productos=p.productos
                ORDER BY c.cantidad DESC, p.productos ASC"""

print(prod_prov_ordenado)


# ii) ¿Cuál es el CLAE2 más frecuente en establecimientos productivos?
# Mencionar el Código y la Descripción de dicho CLAE2.

# In[ ]:


# Agrupamos df_estab_prod segun clae y contamos la cantidad de establecimientos. Como tenemos un establecimiento por fila podemos usar *
clae2_cantidad = sql^""" SELECT clae2, COUNT(*) AS cantidad_clae
                FROM df_estab_prod
                GROUP BY clae2
                ORDER BY COUNT(*) DESC
"""

# Hacemos JOIN con df_dicc_clae para agregar descripcion y ordenamos segun cantidad 
clae2_desc_cant = sql^""" SELECT c.clae2 as codigo_clae, d.clae2_desc as descripcion_clae
                FROM clae2_cantidad AS c
                INNER JOIN df_dicc_clae AS d
                ON c.clae2=d.clae2
                ORDER BY c.cantidad_clae DESC
"""

#Devolvemos la primera clae
print(clae2_desc_cant.head(1))


# iii) ¿Cuál es el producto más producido (que lo producen más establecimientos de operadores orgánicos)?¿Qué Provincia-Departamento los producen?
# 

# In[ ]:


#Agrupamos df_prod_org por producto y contamos cantidad de establecimientos

prod_cant_est = sql^""" SELECT productos, COUNT(*) as cantidad_establecimientos
                    FROM df_prod_org
                    GROUP BY productos
                    ORDER BY cantidad_establecimientos DESC
"""

print("Producto mas producido")
print(prod_cant_est.head(1))

print("")


# Hacemos un JOIN entre prod_est_dep (tabla creada en la primera consulta) con departamentos para agregar la provincia. Filtramos por 'MANZANAS'.
dep_prod_mas_producido = sql^""" SELECT DISTINCT p.productos, p.departamento, d.nombre_provincia
                        FROM prod_est_dep AS p 
                        INNER JOIN df_deptos AS d
                        ON p.departamento=UPPER(d.nombre_departamento)
                        WHERE p.productos='MANZANAS'
                        ORDER BY nombre_provincia
"""

print("Departamentos donde se produce manzana")
print(dep_prod_mas_producido)


# iv) ¿Existen departamentos que no presentan Operadores Orgánicos Certificados? ¿En caso de que sí, cuántos y cuáles son?
# 

# In[ ]:


# Aca tenemos los departamentos que tienen razones sociales, osea, Operadores Organicos Certificados
deptos_con_OOC = sql^"""SELECT o.razon_social, d.establecimiento, d.departamento
                    FROM df_oper_org AS o
                    JOIN df_est_deptos_org AS d
                    ON o.establecimiento=d.establecimiento
"""

# Luego, los departamentos que esten en la tabla departamentos y que no esten en la query anterior, no van a tener OOC's.
deptos_sin_OOC = sql^"""SELECT d.nombre_departamento
                    FROM df_deptos as d
                    LEFT OUTER JOIN deptos_con_OOC as o
                    ON UPPER(d.nombre_departamento)=o.departamento
                    WHERE o.departamento IS NULL
"""

# Departamentos sin Operadores Organicos Certificados
print(deptos_sin_OOC)


# v) ¿Cuál es la tasa promedio de participación de mujeres en cada
# provincia?¿Cuál es su desvío? En cada caso, mencionar si es mayor o
# menor al promedio de todo el país

# In[ ]:


#Agrupamos los Est Prod por departamento y calculamos la media de la proporcion de mujeres y el desvio.
dep_prop_desv = sql^"""SELECT departamento, AVG(proporcion_mujeres) as media_mujeres, STDDEV(proporcion_mujeres) as desvio
                    FROM df_estab_prod
                    GROUP BY departamento
"""

# Hacemos JOIN con df_deptos para poder agregar la provincia con su media y desvio
prov_prop_desv = sql^"""SELECT  d.nombre_provincia, AVG(c.media_mujeres) AS media_mujeres, AVG(c.desvio) as desvio
                      FROM dep_prop_desv AS c
                      INNER JOIN df_deptos AS d
                      ON c.departamento=d.nombre_departamento
                      GROUP BY d.nombre_provincia
                      ORDER BY d.nombre_provincia ASC

 """

#Calculamos la media
media_pais = sql^"""SELECT AVG(media_mujeres) as promedio_pais
                    FROM prov_prop_desv """

#Agregamos la columna 
final = sql^""" SELECT *, CASE WHEN desvio>=0.274775 THEN 'True' ELSE 'False' END AS desvio_mayor_a_media
                FROM prov_prop_desv"""

print(final)


# vi) Mostrar por cada provincia-departamento cuántos establecimientos productivos y cuántos emprendimientos orgánicos posee

# In[ ]:


# Hacemos JOIN entre df_estab_prod y df_deptos para agregar la provincia y agrupamos por departamento y provincia. Usamos deptos_con_OOC del punto iv)
cant_estab_prov = sql^""" SELECT e.departamento, d.nombre_provincia, COUNT(*) as cantidad_establecimientos
                    FROM df_estab_prod as e
                    INNER JOIN df_deptos as d
                    ON e.departamento=d.nombre_departamento
                    GROUP BY e.departamento, d.nombre_provincia

"""

# Hacemos JOIN entre df_estab_prod y df_deptos para agregar la provincia y agrupamos por departamento y provincia
cant_emp_org_prov = sql^ """SELECT p.departamento, d.nombre_provincia, COUNT(*) AS cantidad_operadores
                    FROM deptos_con_OOC as p
                    INNER JOIN df_deptos as d
                    ON p.departamento=UPPER(d.nombre_departamento)
                    GROUP BY p.departamento, d.nombre_provincia
"""

#Hacemos JOIN entre ambas
cantidad_prod_y_org = sql^"""SELECT e.departamento, e.nombre_provincia, e.cantidad_establecimientos, o.cantidad_operadores
                            FROM cant_estab_prov as e 
                            INNER JOIN cant_emp_org_prov as o
                            ON UPPER(e.departamento)=o.departamento and e.nombre_provincia=o.nombre_provincia
                            """


# # Visualizacion

# Cantidad de establecimientos productivos por provincia.

# In[ ]:


#Agregamos la cantidad de establecimientos de la provincia
cant_estab_prov['cant_total'] = cant_estab_prov.groupby('nombre_provincia')['cantidad_establecimientos'].transform('sum')


# In[ ]:


#Eliminamos las columnas de mas
cant_estab_prov.drop(columns=['departamento', 'cantidad_establecimientos'], inplace=True)


# In[ ]:


#Eliminamos duplicados
cant_estab_prov.drop_duplicates()


# In[ ]:


#Graficamos usando un histograma
plt.figure(figsize=(12,8))

plt.bar(cant_estab_prov['nombre_provincia'], cant_estab_prov['cant_total'],color='pink')

# Agregamos los titulos
plt.title('Cantidad total por provincia')
plt.xlabel('Nombre de Provincia')
plt.ylabel('Cantidad total')
plt.xticks(rotation=45, ha='right')  # Acomodamos para que se visualicen los nombres

plt.show()


# Boxplot, por cada provincia, donde se pueda observar la cantidad de productos por operador

# In[ ]:


#Queremos crear una nueva tabla donde por cada razon social, tengamos la cantidad de productos que produce. La vamos a generar con SQL a partir de las tablas df_prod_org, df_oper_org y df_est_deptos_org

#Agrego departamento a la razon social
establecimiento_razon = sql^"""
                            SELECT o.razon_social, e.departamento, e.establecimiento
                            FROM df_oper_org AS o
                            INNER JOIN df_est_deptos_org AS e
                            ON o.establecimiento = e.establecimiento
                            WHERE e.establecimiento != 'NC'
"""

#Agrego la provincia
provincia_razon = sql^"""
                        SELECT e.razon_social, e.establecimiento, d.nombre_provincia
                        FROM establecimiento_razon AS e
                        INNER JOIN df_deptos AS d
                        ON e.departamento=UPPER(d.nombre_departamento) 
                        
"""

#Agrego los productos de la razon social
productos_operador = sql^"""
                        SELECT e.nombre_provincia, e.razon_social, COUNT(DISTINCT d.productos) AS cant_productos
                        FROM provincia_razon AS e
                        INNER JOIN df_prod_org AS d
                        ON e.establecimiento=d.establecimiento
                        GROUP BY e.nombre_provincia, e.razon_social
"""


# In[ ]:


# Creamos el boxplot

plt.figure(figsize=(10,6))
sns.boxplot(data=productos_operador,y='nombre_provincia',x='cant_productos',color='pink')
plt.xticks(rotation=45, ha='right')  # Acomodamos para que se visualicen los nombres


# Relación entre cantidad de establecimientos de operadores orgánicos certificados de cada provincia y la proporción de mujeres empleadas en establecimientos productivos de dicha provincia. Para este punto deberán generar una tabla de equivalencia, de manera manual, entre la letra de CLAE y el rubro de del operador orgánico.

# In[ ]:


## Analizamos el rubro de los productores organicos

print('RUBROS OPERADORES ORGANICOS',df_padron[df_padron["establecimiento"]!='NC']["rubro"].unique())
info = df_clae[['clae2','clae2_desc','letra']]

print("")

#Analizamos las descripciones de las clases con letra A
letraA = info[info["letra"]=='A']
print('CLAE CON LETRA A',letraA["clae2_desc"].unique())


# In[ ]:


#Como vemos que los operadores organicos tienen CLAE con letra A, nos quedamos con esos establecimientos productivos
df_estab_prod_letraA = df_estab_prod[df_estab_prod["letra"]=='A']


# In[ ]:


# Agregamos la provincia a los establecimientos productivos
estab_prod_con_prov = sql^"""SELECT *
                             FROM df_estab_prod_letraA as e
                             INNER JOIN df_deptos as d
                             ON e.departamento = d.nombre_departamento"""

# Proporcion de mujeres por provincia
prop_muj_prov = sql^"""SELECT nombre_provincia, AVG(proporcion_mujeres) as prop_muj
                        FROM estab_prod_con_prov
                        GROUP BY nombre_provincia """

# Cantidad de establecimientos por provincia
estab_por_prov = sql^"""SELECT nombre_provincia, COUNT(ID) as cant_est
                        FROM estab_prod_con_prov
                         GROUP BY nombre_provincia """

# Hacemos Join de las dos ultimas tablas
prop_estab_por_prov = sql^"""SELECT p.nombre_provincia, p.prop_muj, e.cant_est
                FROM estab_por_prov as e
                INNER JOIN prop_muj_prov as p
                ON e.nombre_provincia=p.nombre_provincia"""


# In[ ]:


#Realizamos un scatterplot para poder analizar si existe relacion o no

plt.scatter(prop_estab_por_prov['cant_est'], prop_estab_por_prov['prop_muj'], color='pink')
plt.xlabel('Cantidad de Establecimientos por Provincia')
plt.ylabel('Proporción de Mujeres por Provincia')
plt.title('Comparación de Establecimientos vs. Proporción de Mujeres por Provincia')


# In[ ]:


#Analizamos ahora por departamento para ver si obtenemos mas informacion

# Cantidad establecimiento por departamento
cantidad_estab_por_dep = sql^""" SELECT e.departamento, COUNT(e.ID) as cantidad_est, d.nombre_provincia
                                FROM df_estab_prod_letraA as e
                                INNER JOIN df_deptos as d
                                ON e.departamento=d.nombre_departamento
                                 GROUP BY e.departamento,d.nombre_provincia """

# Proporcion mujeres por departamento
prop_por_dep = sql^""" SELECT e.departamento, AVG(e.proporcion_mujeres) as media_prop_muj, d.nombre_provincia
                                FROM df_estab_prod_letraA as e
                                INNER JOIN df_deptos as d
                                ON e.departamento=d.nombre_departamento
                                GROUP BY e.departamento, nombre_provincia """

cantidad_prop_dep = sql^""" SELECT p.departamento, p.nombre_provincia, e.cantidad_est as cantidad_establecimientos, p.media_prop_muj
                FROM cantidad_estab_por_dep as e
                INNER JOIN prop_por_dep as p
                ON p.departamento=e.departamento"""


# In[ ]:


cantidad_prop_dep


# In[ ]:


# Realizamos el scatterplot por departamento

plt.figure(figsize=(6,6))
sns.scatterplot(data=cantidad_prop_dep, x='cantidad_establecimientos', y='media_prop_muj',hue='nombre_provincia')
plt.xlabel('Cantidad de Establecimientos por departamento')
plt.ylabel('Proporción de Mujeres por departamento')
plt.title('Comparación de Establecimientos vs. Proporción de Mujeres por departamento')

plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5),fontsize=8.6)


# ¿Cuál es la distribución de los datos correspondientes a la proporción de mujeres empleadas en establecimientos productivos en Argentina? Realicen un violinplot por cada provincia. Mostrarlo en un solo gráfico.

# In[ ]:


# Creo una tabla donde tenga provincia, departamento y proporcion de mujeres en ese establecimiento
prov_prop_muj = sql^"""
                    SELECT d.nombre_provincia, e.proporcion_mujeres
                    FROM df_deptos AS d
                    INNER JOIN df_estab_prod AS e
                    ON d.nombre_departamento = e.departamento
                    WHERE e.letra='A'
"""

# Cada entrada es un establecimiento, por lo que pueden haber repetidos, igualmente los queremos conservar porque vamos a cuantificar cantidades


# In[ ]:


#Podemos ver que en Mendoza hay mucha mas densidad de valores cercanos al 0.

sns.violinplot(data=prov_prop_muj[prov_prop_muj['nombre_provincia']=='Mendoza'], x='nombre_provincia', y='proporcion_mujeres',color='pink')


# In[ ]:


#Creamos el violinplot por provincia
plt.figure(figsize=(24,6))

sns.violinplot(data=prov_prop_muj, x='nombre_provincia', y='proporcion_mujeres',color="pink")

plt.xlabel('Provincia')
plt.ylabel('Proporcion de Mujeres')
plt.xticks(rotation=45, ha='right')

plt.show()


# In[ ]:


#Podemos ver que generalmente la distribucion suele ser mayor en torno al 0, y que en valores intermedios entre 0 y 1 no suele haber mucha info. 
#Se puede ver que el promedio es 0.078 y que la desviacion estandar es 0.21 lo que nos dice que los resultados estan muy distribuidos respecto al 0. Tambien vemos que los cuantiles 0.25, 0.5 y 0.75, son todos 0.

prov_prop_muj.describe()


# In[ ]:


#Vemos que de 98.621 establecimientos, 79.451 no tienen ninguna mujer. Esto tambien podria deberse a una irresponsabilidad de parte de los establecimientos al cargar los datos.
prov_prop_muj['proporcion_mujeres'].value_counts()


# In[ ]:

# Analizamos segun los graficos que no existe relacion.
# Hablamos mas sobre esta situacion en la seccion conclusiones del informe.
