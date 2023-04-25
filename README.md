## ![MarineGEO circle logo](https://img.europapress.es/fotoweb/fotonoticia_20220118143634_1200.jpg) API 🏘️

La finalidad de este script en Python es hacer consultas a la API de Idealista para extraer un archivo JSON y un archivo XLSX. 

Para conseguir acceso a la API hay que solicitarla en el siguiente enlace: [https://developers.idealista.com/access-request](https://developers.idealista.com/access-request)

*   Nota: La API\_KEY y la API\_SECRET están guardados en un archivo .py y ocultos en .gitignore.

En este código se hace uso de la clase Session de la libería `request`

```css
s = requests.Session()
s.headers.update({
        'Authorization' : 'Bearer ' + token,
        'Content-Type' : 'application/x-www-form-urlencoded;charset=UTF-8'
})
```

## Resultados

La API devuelve información de las siguientes propiedades 

| Columna | Unidad |
| --- | --- |
| price | precio en Euros (int) |
| size | tamaño en m2 (int) |
| rooms | habitaciones (int) |
| bathrooms | baños (int) |
| district | distrito (str) |
| neighborhood | vecindario (str) |