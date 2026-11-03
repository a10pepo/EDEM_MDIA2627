# Entrega de GitHub Actions

Esta carpeta contiene los diez ejercicios de `EXERCISES.md` y el desafío final. Los ejercicios 1–10 son los workflows que preparé en [mi repositorio de prácticas](https://github.com/Lunkynono/github-actions-edem-2026).

## Desafío final

`20.desafio_final.yaml` define tres jobs:

1. Valida `ventas.json` y ejecuta `scan_seguridad.py` si se elige «si» en el input manual.
2. Genera un reporte para `staging` y otro para `production` con `generar_reporte.py`, y los sube como artefactos separados.
3. Simula la notificación de éxito usando el secreto `DISCORD_WEBHOOK` cuando está configurado.

Los datos de ejemplo están en `ventas.json`. El escáner informa de la ruta de cualquier campo que parezca contener una clave API sin mostrar su valor.

## Ejecución

GitHub ejecuta los workflows cuando están en `.github/workflows/` de un repositorio. Esta carpeta conserva los archivos para la entrega. Los workflows están publicados en [mi repositorio de prácticas](https://github.com/Lunkynono/github-actions-edem-2026); allí se pueden ejecutar desde la pestaña **Actions**.

Para probar el desafío final localmente desde esta carpeta:

```bash
python -m json.tool ventas.json
python scan_seguridad.py ventas.json
python generar_reporte.py ventas.json staging
python generar_reporte.py ventas.json production
```

El [workflow final](https://github.com/Lunkynono/github-actions-edem-2026/blob/main/.github/workflows/20.desafio_final.yaml) se ejecuta manualmente en GitHub con la opción de activar o desactivar el escáner. Los reportes quedan disponibles como artefactos de la ejecución. El secreto `DISCORD_WEBHOOK` es opcional para esta simulación.
