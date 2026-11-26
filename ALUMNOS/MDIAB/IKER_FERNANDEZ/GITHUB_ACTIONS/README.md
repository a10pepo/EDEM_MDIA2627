# Ejercicio Final GitHub Actions – Pipeline de Datos Seguro y Automatizado

**Alumno:** Iker Fernández (MDIA B)

## Contenido

| Fichero | Descripción |
|---|---|
| `ejercicio_entregable.yaml` | Workflow de GitHub Actions |
| `ventas.json` | Datos de ventas de ejemplo |
| `scripts/security_scan.py` | Escaneo de seguridad simulado: busca claves API expuestas (AWS, GitHub, `sk-…`, Google, Slack, `api_key = "…"`) y falla si encuentra alguna |
| `scripts/generar_reporte.py` | Procesa `ventas.json` y genera `reporte_<entorno>.txt` |
| `Capturas/` | Capturas de pantalla de las ejecuciones del workflow |

El workflow se ha ejecutado en mi repositorio
[`ikerfernandez16-col/ejercicio-github-actions`](https://github.com/ikerfernandez16-col/ejercicio-github-actions/actions)
(en `.github/workflows/`, con `ventas.json` y `scripts/` en la raíz del repo).
Ejecución #1 con tests de seguridad = **sí** y ejecución #2 con **no**; ambas en verde.

## Cómo cumple los requisitos

1. **Activación:** `workflow_dispatch` con un input `tests_seguridad` de tipo `choice` (`sí` / `no`).
2. **Job 1 – CI & Seguridad** (`ubuntu-latest`):
   - Valida `ventas.json` con `python -m json.tool`; si no es válido, el job falla.
   - El paso de escaneo tiene `if: inputs.tests_seguridad == 'sí'`, así que solo se ejecuta si el usuario elige "sí".
3. **Job 2 – Procesamiento:**
   - `needs: ci-seguridad`.
   - `strategy.matrix.entorno: [staging, production]`.
   - Cada entorno genera su propio `reporte_staging.txt` / `reporte_production.txt`.
   - Los reportes se suben con `actions/upload-artifact@v4` (`reporte-staging`, `reporte-production`).
4. **Job 3 – Notificación de Éxito:**
   - `needs: [ci-seguridad, procesamiento]` + `if: success()`.
   - Usa el secreto `DISCORD_WEBHOOK`; al hacer `echo`, GitHub lo enmascara como `***`.
