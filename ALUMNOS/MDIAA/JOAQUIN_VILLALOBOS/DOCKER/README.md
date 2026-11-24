## Captura de Pantalla
Se deja la evidencia en "image.png" dónde se puede ver la invocación al contenedor docker y el resultado de su ejecución.

## Buildeo imagen
A modo de contexto, decidí realizar el buildeo de la imagen con docker compose, por eso es que en la captura de pantalla se puede ver que hay 2 comandos:
    - docker compose run <service_name> 3 4
    - docker run -it --rm <image_name> 4 3

## Imagen en Docker Hub
La imagen pública generada para este ejercicio está disponible en:
[Docker Hub - entregable_docker](https://hub.docker.com/r/joaquinvillalobos1993/entregable_docker)