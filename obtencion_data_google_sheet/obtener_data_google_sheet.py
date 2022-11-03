import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import pandas as pd

"""agregué otra forma de conectar y funciona bien como la primera.
 Hice un segundo proyecto y otra cuenta de servicio que falló al abrir el archivo.
 Si bien, no es la 2° forma la solución, al usar explícitamente los scopes (el alcance de los permisos)
  me di cuenta que el archivo que estaba solicitando no estaba guardado en mi unidad (fuera del scope)"""

######## PRIMERA FORMA ####################

"""se leen las respuestas de Forms desde Google Drive"""
# seguir pasos previos:
# 1) crear proyecto en https://console.cloud.google.com
# 2) en API y servicios de la misma página habilitar Google Sheet API
# 3) luego crear credenciales como cuenta de servicio: se descarga el json con keys y se guarda en ~/.config/gspread

sa = gspread.service_account()  # el json con keys lo tengo en carpeta ~/.config/gspread/...
sh = sa.open('reporte_respuestas')  # abrir el archivo
wks = sh.worksheet('respuestas')  # abrir hoja de trabajo
df_resp = pd.DataFrame(wks.get_all_records())  # se usa pandas para trabajar como df
df_resp_test = df_resp.iloc[[0, 3, 4], :]  # df_resp.drop(index=0)
df_resp.drop(index=[0, 3, 4], inplace=True)  # se eliminan respuestas que prueban el flujo del instrumento
df_resp.reset_index(drop=True, inplace=True)

"""normalizar el nombre de variables"""
etiq_var = df_resp.columns.values.astype('str')
nom_var = 'ID_FECHA reg_fecha clave_cambio rc rc1 it it1 it1_01 it1_02 it1_03 it1_04 it1_05 it1_06 it1_07 it1_08 it1_09 it1_10 it1_11 it1_12 it1_13 it1_14 it1_15 rec rec1 rec2 rec3 rec4 clave_reth reth1 discurso'.split()

"""crear variables necesarias"""
df_resp.set_axis(nom_var, axis='columns', inplace=True)
df_resp['reg_fecha'] = pd.to_datetime(df_resp['reg_fecha'])
df_resp['month'] = df_resp.reg_fecha.dt.month_name()
df_resp['year'] = df_resp.reg_fecha.dt.year

"""guardar"""

df_resp.to_csv('data/respuestas.csv')

######## PRIMERA FORMA ####################

os.chdir('/')

with open('/keys.txt') as k:
    keys = k.readline()

archivo = 'nombrearchivo'
gc = gspread.service_account(filename=keys)
scopes = gc.auth.scopes
credentials = ServiceAccountCredentials.from_json_keyfile_name(keys, scopes)
servicio = gspread.authorize(credentials)
libro = servicio.open(archivo)

# %%
