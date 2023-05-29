<p align = center  
<br>
<img src="https://res-5.cloudinary.com/crunchbase-production/image/upload/c_lpad,h_256,w_256,f_auto,q_auto:eco/v1455514364/pim02bzqvgz0hibsra41.png" align="center"><br><FONT FACE="times new roman" SIZE=6>
<b>Parcial #3: Big Data</b>
<br>
<i><b>Autores:</b></i> Juan Pablo Barrios Suarez y Paula Sofía Godoy Salamanca
<br>
<i><b>Semestre:</b></i> 9º
<br>
<i><b>Asignatura:</b></i> Big Data
<br>
<i><b>Docente:</b></i> Camilo Rodríguez
<br>
<i><b>Fecha: </b>29/05/2022
<br>
<b>Ciencias de la computación e inteligencia artificial</b></i>
<br>
</FONT>
</p>

# Objetivo
Diseñar e implementar un sistema de procesamiento y monitoreo para datos financieros haciendo uso de servicios como PySpark, AWS Glue, AWS Kinesis y QuickSight.

# Desarrollo

1) Dibujar franjas de Bollinger con una ventana de 20 horas en Quick Sight para el proyecto del precio del dólar (posiblemente se necesite una consulta en athena).

https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/bollinger-bands#:~:text=Bollinger%20Bands%20are%20envelopes%20plotted,Period%20and%20Standard%20Deviations%2C%20StdDev.

2) Crear un pipeline de procesamiento para los datos de noticias del parcial 2 usandoPyspark ML. Se debe vectorizar usando TFxIDF. Implementar el pipeline en AWS GLUE o ejecutarlo en EMR con spark submit.
Usar de guía:

https://spark.apache.org/docs/latest/ml-pipeline.html

3) Implementar 2 productores que envíen datos de las acciones(como el ejemplo de clase) a un stream en AWS Kinesis. Implementar un consumidor que se encargue de tomar de la cola y muestre una alerta cada vez que el precio de alguna acción supera la franja superior de Bollingener. Implementar un segundo consumidor que se encargue de tomar de la cola y muestre una alerta cada vez que el  precio de alguna acción esté por debajo de la franja inferior de Bollingener. Cada uno de los productores y consumidores deben estar en una máquina EC2.

# Resultados

## 1. Franjas de Bollinger

Para este ejercicio, se decidio hacer uso del proyecto del dólar realizado en el primer corte. Sin embargo, tambien se aplico el procedimiento a un conjunto de datos de Yahoo Finanzas, con el fin de corroborar el método. Para ello se ejecutaron los siguientes pasos:
1. Se creó una vista para agregar una columna adicional que almacenaria los datos de la desviación estándar móvil.
2. Luego, a partir de esa vista, se calculó la media móvil y los limites de la franja de Bollinger (superior e inferior).

A continuación se ve el resultado de las dos implementaciones:

- **Franja de Bollinger para el conjunto de datos del Banco de la Republica**

![image](https://github.com/JuanPabloBarrios30/Parcial_3_Big_Data/assets/89982238/b539bc49-47fb-4452-a6f8-8cdc5e826b12)
- **Franja de Bollinger para el conjunto de datos de Yahoo Finanzas**

![image](https://github.com/JuanPabloBarrios30/Parcial_3_Big_Data/assets/89982238/5a597938-a817-45d1-a3ac-18a9c695a815)

## 2. Pipeline con PySpark ML
Para este ejercicio, se crea un Pipeline de procesamiento para los datos que se generaron en el parcial #2 (Noticias de El tiempo y El espectador) haciendo uso de PySpark ML. Para ello, a continuación se ven cada una de las etapas del Pipeline:

- StringIndexer: Esta etapa convierte una columna de etiquetas de texto (_c0) en una columna numérica de etiquetas (label) utilizando la técnica de codificación de etiquetas.

- Tokenizer: Esta etapa divide el texto de la columna _c1 en palabras individuales. Crea una nueva columna llamada "words" que contiene una lista de palabras.

- HashingTF: Esta etapa convierte la lista de palabras en una característica numérica utilizando la técnica de "Term Frequency" (TF) con hash. Crea una nueva columna llamada "rawFeatures" que contiene vectores dispersos que representan la frecuencia de cada palabra.

- IDF: Esta etapa aplica el esquema "Inverse Document Frequency" (IDF) a los vectores dispersos de "rawFeatures". Calcula un factor de ponderación que disminuye la importancia de las palabras comunes y resalta las palabras más distintivas. Crea una nueva columna llamada "features" que contiene los vectores ponderados.

Después de definir el pipeline, se ajusta a los datos de entrada (df) utilizando el método fit(), lo que devuelve un modelo de pipeline. Luego, se aplica el modelo al conjunto de datos de entrada mediante el método transform(), lo que genera un nuevo DataFrame llamado "processed_data" que contiene todas las columnas originales junto con las columnas resultantes de cada etapa del pipeline.

El resultado obtenido despues de la ejecución del Pipeline se puede ver a continuación, en un archivo en formato Parquet almacenado en s3:

![image](https://github.com/JuanPabloBarrios30/Parcial_3_Big_Data/assets/89982238/483b6348-b1e1-4040-9c31-157183e444ff)

## 3. Productores y consumidores de datos del dólar

Para el ejercicio final, se crean cuatro programas en Python, donde dos de ellos van a ser productores, y los otros dos, consumidores. Los programas productores van a generar datos del dólar en un intervalo de horas específico, y los van a transmitir a través de una secuencia de datos en Kinesis. Finalmente, los programas consumidores van a recibir esos datos y los procesan de tal forma que puedan hallar la franja de Bollinger para los datos transmitidos y, en caso de que suceda, arrojen una alerta en caso de que se sobrepase la franja superior o se esté por debajo de la franja inferior.

A continuación se ve el código de los productores en ejecución:

![image](https://github.com/JuanPabloBarrios30/Parcial_3_Big_Data/assets/89982238/1bfcb577-c681-454e-904b-18dc82c13a59)

De igual forma, está el código del consumidor que procesa los datos recibidos por parte de los productores:

![image](https://github.com/JuanPabloBarrios30/Parcial_3_Big_Data/assets/89982238/0f1d3580-7352-4514-b030-0d3fd1493586)

En caso de que alguno de los valores entregados por el productor, esté por debajo de la franja, se arroja la siguiente alerta:

![image](https://github.com/JuanPabloBarrios30/Parcial_3_Big_Data/assets/89982238/60207297-55f7-43fa-9ae7-b7a7d64082f3)

Por otro lado, en caso de que los valores entregados por el productor, esten por encima de la franja, salta la siguiente alerta:

![image](https://github.com/JuanPabloBarrios30/Parcial_3_Big_Data/assets/89982238/c1826056-31d9-4b36-9a81-4aa39fd62a88)

