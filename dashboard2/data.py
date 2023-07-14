import numpy as np
import pandas as pd
from scipy.io import loadmat

class Dashdata:
    def __init__(self):
        
        ####################
        ### Loading data ###
        ####################
        
        sensorsTags = [
               "FP1","FP2",
               "F3", "F4", "F7", "F8", "FZ",
               "A1","A2","T3","T4","C3","C4","CZ",
               "T5","T6","P3","P4","PZ",
               "O1","O2"
               ]

        sensorsColors = [
            "#FF3C00",  # Vivid Orange
            "#FF9700",  # Bright Orange
            "#FFD300",  # Sunflower Yellow
            "#FF4D6E",  # Coral Pink
            "#FF66B2",  # Bubblegum Pink
            "#FF8AC3",  # Light Pink
            "#FF00D8",  # Magenta
            "#6A00FF",  # Vivid Purple
            "#A050FF",  # Lavender Purple
            "#FFA6FF",  # Cotton Candy
            "#00C4FF",  # Sky Blue
            "#00E6FF",  # Aqua Blue
            "#00FFD4",  # Mint Green
            "#1AFFB5",  # Turquoise
            "#00FF89",  # Neon Green
            "#00FF00",  # Lime Green
            "#FFFF33",  # Bright Yellow
            "#F9FF66",  # Lemon Yellow
            "#FF9F00",  # Amber
            "#FF7733",  # Coral Orange
            "#FFAF40"   # Peach
        ]
        
        mat = loadmat(
        '/home/ensismoebius/Documentos/UNESP/doutorado/databases/Base de Datos Habla Imaginada/S01/S01_EEG.mat',
        struct_as_record=True, squeeze_me=True, mat_dtype=False
        )
        
        #################################
        ### Setting up the properties ###
        #################################

        self.dataframe = pd.DataFrame(mat['EEG'])

        self._joinIntoArray(0, 4096, 'F3', self.dataframe)
        self._joinIntoArray(0, 4096, 'F4', self.dataframe)
        self._joinIntoArray(0, 4096, 'C3', self.dataframe)
        self._joinIntoArray(0, 4096, 'C4', self.dataframe)
        self._joinIntoArray(0, 4096, 'P3', self.dataframe)
        self._joinIntoArray(0, 4096, 'P4', self.dataframe)
        
        self._joinIntoValue(0, 1, 'Modalidade', self.dataframe)
        self._joinIntoValue(0, 1, 'Estímulo', self.dataframe)
        self._joinIntoValue(0, 1, 'Artefatos', self.dataframe)
        
        
        # Seetting the sensors to colors relationship
        self.sensorToColorRelationship = dict(zip(sensorsTags, sensorsColors))
        
        # Setting subjects names and codes
        self.subjectsNamesAndCodes = {
            'Imaginado': {'Sujeito01':'1', 'Sujeito02' : '2'}, 
            'Falado': {'Sujeito03' : '3'}
        }

        # Getting the stimuli
        self.estimulos = {
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
            
        # Create the SVG pane
        self.brainSvgImage = open("brain.svg").read()

    def _joinIntoArray(self, start_col, end_col, newColumn, dataframe):
        cols_to_join = dataframe.iloc[:, start_col:end_col].columns
        dataframe[newColumn] = dataframe[cols_to_join].apply(lambda x: np.array(pd.to_numeric(x, errors='coerce')), axis=1)
        dataframe.drop(cols_to_join, axis=1, inplace=True)
    
    def _joinIntoValue(self, start_col, end_col, newColumn, dataframe):
        cols_to_join = dataframe.iloc[:, start_col:end_col].columns
        dataframe[newColumn] = dataframe[cols_to_join].apply(lambda x: pd.to_numeric(x, errors='coerce'), axis=1)
        dataframe.drop(cols_to_join, axis=1, inplace=True)
        
