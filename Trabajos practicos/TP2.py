# -*- coding: utf-8 -*-
"""Ejercitación 2, Marcos Tracchia.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TaxaGmQUtlUSrX86XCPn3zlCiUqwlo1g
"""

#Importo los datos desde mi cuenta de drive
import pandas as pd
from google.colab import drive
drive.mount('/content/drive')
filename = '/content/drive/My Drive/anticoncepcion_indonesia.csv' 
df = pd.read_csv(filename)
print(df)

#Binarizé el campo "metodo_anticonceptivo" 1 == 0 y, 2 y 3 == 1 
df.loc[df['metodo_anticonceptivo'] == 1, 'metodo_anticonceptivo'] = 0
df.loc[(df['metodo_anticonceptivo'] == 2) | (df['metodo_anticonceptivo'] == 3), 'metodo_anticonceptivo'] = 1
df_bin = df

#Imprimo las primeras 25 filas
print(df_bin[:25])

#Importo módulos de scikit learn para el entrenamiento y ajuste de parámetros
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

campos=["educacion_mujer","educacion_hombre","mujer_trabaja"]
X = df_bin[campos].values
y = df_bin['metodo_anticonceptivo']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)


scaler = MinMaxScaler() # primero creo un objeto MinMaxScaler. Por defecto, esto normaliza los datos al intervalo [0,1]
scaler.fit(X_train) # encuentro los parametros para el escaleo
X_train = scaler.transform(X_train) # aplico la transformacion

scaler = MinMaxScaler() # primero creo un objeto MinMaxScaler. Por defecto, esto normaliza los datos al intervalo [0,1]
scaler.fit(X_test) # encuentro los parametros para el escaleo
X_test = scaler.transform(X_test) # aplico la transformacion


regLog = LogisticRegression(penalty = 'l2', class_weight='balanced', max_iter=10000) # Inicializamos nuevamente el modelo
regLog.fit(X, y) # Ajustamos el modelo con los parámetros

score_train = regLog.score(X_train,y_train)
ypred_train = regLog.predict(X_train)
ypred_test= regLog.predict(X_test)
proba = regLog.predict_proba(X_test)
print(ypred_test)
print(proba[:,1])

'''
-Terminar de ver bien lo de regLog
-Ver qué atributos elegir para el mejor ajuste, cuidado con lo de los datos categoricos
-Si queda tiempo, ver cómo optimizar los hiperparametros
'''

#'/content/drive/My Drive/LaboDatos2021/coronadelicos_safe.csv' 
path = '/content/drive/My Drive/LaboDatos2021/anticoncepcion_indonesia_test.csv'
df_test = pd.read_csv(path)
df_test.columns

campos=["educacion_mujer","educacion_hombre","mujer_trabaja"]
X = df_test[campos].values

proba = regLog.predict_proba(X)

print(proba)

import numpy as np
save_path= '/content/drive/My Drive/Marcos_Tracchia.csv'
np.savetxt(save_path, proba, delimiter=",")