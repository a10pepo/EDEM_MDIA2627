# Configuración inicial — macOS

Esta guía reúne las herramientas que se utilizarán durante el máster en equipos macOS. Ejecuta los comandos de comprobación en Terminal una vez termine cada instalación.

## Homebrew

Homebrew permite instalar software desde Terminal. Instálalo con:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Al finalizar, ejecuta el comando que muestre el instalador para añadir Homebrew al `PATH`. Cierra y abre Terminal antes de continuar.

### CHECK

```bash
brew --version
```

## Visual Studio Code

Instala Visual Studio Code desde Terminal:

```bash
brew install --cask visual-studio-code
```

Para disponer del comando `code`, abre Visual Studio Code, pulsa `Cmd+Shift+P` y ejecuta **Shell Command: Install 'code' command in PATH**.

### CHECK

```bash
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

```bash
code --list-extensions
```

Comprueba que aparecen las extensiones instaladas en la lista.

## Git

Instala Git con Homebrew:

```bash
brew install git
```

### CHECK

```bash
git --version
```

## GitHub Desktop

Descarga e instala GitHub Desktop desde [desktop.github.com](https://desktop.github.com/). Inicia sesión con tu cuenta de GitHub al abrir la aplicación.

### CHECK

```bash
open -Ra "GitHub Desktop"
```

El comando no muestra salida si la aplicación está instalada y devuelve un error si no se encuentra.

## Node.js y npm

Instala la versión LTS de Node.js con Homebrew. npm se instala junto con Node.js:

```bash
brew install node
```

### CHECK

```bash
node --version
npm --version
```

## Python

Actualiza Homebrew e instala Python 3:

```bash
brew update
brew install python
```

### CHECK

```bash
python3 --version
```

## Claves SSH

Genera una clave SSH. Sustituye el correo por el de tu cuenta de GitHub:

```bash
ssh-keygen -t ed25519 -C "tu-correo@example.com"
```

Pulsa Intro para aceptar la ubicación predeterminada. No compartas nunca el fichero privado `id_ed25519`; solo se comparte la clave pública `id_ed25519.pub`.

### CHECK

```bash
test -f ~/.ssh/id_ed25519.pub && echo "Clave pública creada"
```

Para visualizar y copiar la clave pública:

```bash
cat ~/.ssh/id_ed25519.pub
```

## Docker Desktop

Descarga Docker Desktop desde [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/), eligiendo la versión adecuada para Apple Silicon o Intel. Abre la aplicación y completa el registro si se solicita.

Si el comando `docker` no está disponible, puedes instalar Docker Desktop con:

```bash
brew install --cask docker
```

### CHECK

```bash
docker ps
```

Si el comando informa de que el daemon no está disponible, abre Docker Desktop y espera a que termine de iniciarse.

## Anaconda

Instala Anaconda con Homebrew:

```bash
brew install --cask anaconda
```

Abre una nueva terminal al terminar la instalación.

### CHECK

```bash
conda --version
```
