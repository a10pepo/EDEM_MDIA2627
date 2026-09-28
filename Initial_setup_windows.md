# Configuración inicial — Windows

Esta guía reúne las herramientas que se utilizarán durante el máster en equipos con Windows. Ejecuta los comandos de comprobación en PowerShell una vez termine cada instalación.

## Antes de empezar

Comprueba que tienes permisos de administrador y espacio suficiente en disco. Para Docker, Windows 10/11 debe tener la virtualización habilitada.

## Visual Studio Code

Descarga e instala Visual Studio Code desde [su web oficial](https://code.visualstudio.com/download). Durante la instalación, marca la opción para añadir `code` al `PATH`.

### CHECK

```powershell
code --version
```

## Extensiones de Visual Studio Code

En la vista **Extensions** de Visual Studio Code, instala estas extensiones:

- Python
- Docker
- Markdown
- Git

Reinicia Visual Studio Code cuando termine la instalación.

### CHECK

```powershell
code --list-extensions
```

Comprueba que aparecen las extensiones instaladas en la lista.

## Git

Descarga e instala Git desde [git-scm.com/download/win](https://git-scm.com/download/win). Mantén las opciones predeterminadas salvo que el profesorado indique otra cosa.

### CHECK

```powershell
git --version
```

## GitHub Desktop

Descarga e instala GitHub Desktop desde [desktop.github.com](https://desktop.github.com/). Inicia sesión con tu cuenta de GitHub al abrir la aplicación.

### CHECK

```powershell
Get-Process GitHubDesktop
```

El comando debe mostrar el proceso de GitHub Desktop mientras la aplicación está abierta.

## Node.js y npm

Descarga e instala la versión **LTS** de Node.js desde [nodejs.org](https://nodejs.org/). npm se instala junto con Node.js.

### CHECK

```powershell
node --version
npm --version
```

## Python

Descarga Python 3.10 o superior desde [python.org/downloads/windows](https://www.python.org/downloads/windows/). Durante la instalación, activa la opción **Add Python to PATH**.

### CHECK

```powershell
python --version
```

## Claves SSH

Abre PowerShell y genera una clave. Sustituye el correo por el de tu cuenta de GitHub:

```powershell
ssh-keygen -t ed25519 -C "tu-correo@example.com"
```

Pulsa Intro para aceptar la ubicación predeterminada. No compartas nunca el fichero privado `id_ed25519`; solo se comparte la clave pública `id_ed25519.pub`.

### CHECK

```powershell
Test-Path "$HOME\.ssh\id_ed25519.pub"
```

El resultado debe ser `True`. Puedes copiar la clave pública con:

```powershell
Get-Content "$HOME\.ssh\id_ed25519.pub"
```

## Docker Desktop

Descarga e instala Docker Desktop desde [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/). Inicia Docker Desktop y acepta la configuración de WSL si se solicita.

Si aparece un error de WSL, abre PowerShell como administrador y ejecuta:

```powershell
wsl --update
```

Reinicia el equipo antes de abrir Docker Desktop de nuevo. Si aparece un error de virtualización, actívala en la BIOS o consulta al profesorado.

### CHECK

```powershell
docker ps
```

## Anaconda

Descarga e instala Anaconda desde [anaconda.com/download](https://www.anaconda.com/download). Sigue el asistente de instalación y abre una nueva terminal al terminar.

### CHECK

```powershell
conda --version
```
