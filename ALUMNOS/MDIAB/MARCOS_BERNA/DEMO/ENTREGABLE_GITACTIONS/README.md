# ENTREGABLE_GITACTIONS

Ejercicio final de GitHub Actions: **Pipeline de Datos Seguro y Automatizado**.

## Estructura

| Archivo | Descripción |
|---|---|
| `.github/workflows/ejercicio_entregable.yaml` | Workflow principal |
| `ventas.json` | Datos de ventas de ejemplo |
| `scripts/security_scan.py` | Simula un escaneo de seguridad buscando claves API expuestas |
| `scripts/procesar_ventas.py` | Genera un reporte `.txt` por entorno |

## Funcionamiento

1. **Activación manual** (`workflow_dispatch`) con un input para elegir si se ejecutan los Tests de Seguridad (sí/no).
2. **Job 1 – CI & Seguridad**: valida que `ventas.json` es un JSON válido y, si se eligió "sí", ejecuta el escaneo de seguridad.
3. **Job 2 – Procesamiento**: depende del Job 1 y usa una matrix (`staging`, `production`) para generar un reporte distinto por entorno y subirlo como artefacto.
4. **Job 3 – Notificación**: solo si todo fue bien, usa el secreto `DISCORD_WEBHOOK` para simular el envío de una notificación (la URL aparece enmascarada como `***`).
