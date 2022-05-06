# TDA-TP3

## Formato Archivos

Las primeras dos líneas corresponden al nodo fuente y sumidero respectivamente.

Continúa con una línea por cada eje del grafo con el formato:

    ORIGEN,DESTINO,COSTO UNITARIO,CAPACIDAD.

Ejemplo

```
BS AS
QATAR
BS AS,RIO,2,8
BS AS,MADRID,3,4
MADRID,NEW YORK,2,5
MADRID,QATAR,1,2
```

## Ejemplos

La salida muestra la cantidad máxima de personas y el costo mínimo.

    nombre -> costo, #personas

- directo1 -> 12, 4
- directo2 -> 18, 3
- bifurcaciones1 -> 18, 3
- bifurcaciones2 -> 24, 3
- multiple1 -> 24, 4
- multiple2 -> 
- cycle1 -> 
- cycle2 -> 