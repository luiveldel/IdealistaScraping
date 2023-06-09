## ![MarineGEO circle logo](https://img.europapress.es/fotoweb/fotonoticia_20220118143634_1200.jpg)

La finalidad de esta aplicación es extraer información de la API de Idealista volcando los resultados en varios formatos. 



## Entrada

Para conseguir acceso a la API hay que solicitarla en el siguiente enlace: [https://developers.idealista.com/access-request](https://developers.idealista.com/access-request)

## Ejecución

Para instalar los requerimientos:
```
python -m pip install -r requirements.txt
```

Ejecutar:
```
$ python main.py
```

## Salida

La aplicación volcará en la carpeta `output` los ficheros de salida:
*   xlsx
*   csv
*   base de datos en sqlite

### Notas: 

*   Los formatos de salida no son excluyentes pudiéndose generar a la vez.
*   La `API_KEY` y la `API_SECRET` no se encuentran en el código si no que se proporcinan en la ejecución.

La API devuelve información de las siguientes propiedades 

| Nombre | Unidad | Tipo |
| --- | --- | --- |
| price | precio en Euros | int |
| size | tamaño en m2 | int |
| rooms | # habitaciones | int |
| bathrooms | # baños | int |
| district | distrito | str |
| neighborhood | vecindario | str |