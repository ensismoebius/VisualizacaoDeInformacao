rom dash import Dash, html, dash_table, dcc, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from scipy.io import loadmat
import numpy as np

from ipywidgets import interact, Dropdown, IntSlider
from PIL import Image

def joinIntoArray(start_col, end_col, newColumn, dataframe):
    cols_to_join = dataframe.iloc[:, start_col:end_col].columns
    dataframe[newColumn] = dataframe[cols_to_join].apply(lambda x: np.array(pd.to_numeric(x, errors='coerce')), axis=1)
    dataframe.drop(cols_to_join, axis=1, inplace=True)

def joinIntoValue(start_col, end_col, newColumn, dataframe):
    cols_to_join = dataframe.iloc[:, start_col:end_col].columns
    dataframe[newColumn] = dataframe[cols_to_join].apply(lambda x: pd.to_numeric(x, errors='coerce'), axis=1)
    dataframe.drop(cols_to_join, axis=1, inplace=True)

def loadData():
    mat = loadmat(
    '/home/ensismoebius/Documentos/UNESP/doutorado/databases/Base de Datos Habla Imaginada/S01/S01_EEG.mat',
    struct_as_record=True, squeeze_me=True, mat_dtype=False
    )

    df = pd.DataFrame(mat['EEG'])

    joinIntoArray(0, 4096, 'F3', df)
    joinIntoArray(0, 4096, 'F4', df)
    joinIntoArray(0, 4096, 'C3', df)
    joinIntoArray(0, 4096, 'C4', df)
    joinIntoArray(0, 4096, 'P3', df)
    joinIntoArray(0, 4096, 'P4', df)
    
    joinIntoValue(0, 1, 'Modalidade', df)
    joinIntoValue(0, 1, 'Estímulo', df)
    joinIntoValue(0, 1, 'Artefatos', df)
    
    return mat

def getEstimulos():
        estimulos = {
            1  : "A",
            2  : "E",
            3  : "I",
            4  : "O",
            5  : "U",
            6  : "Arriba",
            7  : "Abajo",
            8  : "Adelante",
            9  : "Atrás",
            10 : "Derecha",
            11 : "Izquierda",
        }
        
        return estimulos
    
def getTitulos():
        titulos = ["F3","F4","C3","C4","P3","P4"]
        return titulos