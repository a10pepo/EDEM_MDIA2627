# Creating a GitHub Repository Using `gh` CLI on macOS

## Instalar Terraform en macOS y Windows

Consulta la [guía oficial de instalación de Terraform](https://developer.hashicorp.com/terraform/install) para ver las versiones compatibles y las descargas más recientes.

### macOS

Si tienes [Homebrew](https://brew.sh/) instalado, abre Terminal y ejecuta:

```sh
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
```

Comprueba la instalación con:

```sh
terraform -version
```

### Windows

1. Descarga el archivo ZIP de Terraform para Windows desde la [página oficial de instalación](https://developer.hashicorp.com/terraform/install). Elige la arquitectura de tu equipo (normalmente **AMD64**).
2. Crea una carpeta para el ejecutable, por ejemplo `C:\terraform`.
3. Extrae `terraform.exe` del ZIP y guárdalo directamente en `C:\terraform`.
4. Añade esa carpeta a la variable de entorno `Path`:
   - Abre el menú Inicio, busca **Editar las variables de entorno del sistema** y abre la ventana.
   - Selecciona **Variables de entorno…**.
   - En **Variables de usuario** (solo para tu cuenta) o **Variables del sistema** (para todos los usuarios), selecciona `Path` y pulsa **Editar**.
   - Pulsa **Nuevo**, escribe `C:\terraform` y confirma con **Aceptar** en todas las ventanas.
   - Si `Path` no existe, créala como variable nueva llamada `Path` y añade `C:\terraform` como valor.
5. Cierra y vuelve a abrir PowerShell o Símbolo del sistema para que cargue el `Path` actualizado.
6. Comprueba la instalación en una nueva terminal:

```powershell
terraform -version
```

Si Windows indica que no reconoce el comando, confirma que `terraform.exe` está dentro de `C:\terraform`, que esa carpeta aparece en `Path` y que abriste una terminal nueva.

This guide walks you through installing the GitHub CLI (`gh`), authenticating, creating a new repository, **and** generating a Personal Access Token (PAT) for use with Terraform or other CLI tools.

---

## 1. Install GitHub CLI

Open Terminal and run:

```sh
brew install gh
```

---

## 2. Authenticate with GitHub

Authenticate the CLI tool with your GitHub account:

```sh
gh auth login
```

- Select **GitHub.com**
- Choose **HTTPS** for authentication
- Follow the prompts to authenticate in your web browser

---

## 3. Create a New Repository

Navigate to or create a folder for your project:

```sh
mkdir my-new-repo
cd my-new-repo
```

(Optional): Initialize a new git repository and add a README:

```sh
git init
echo "# My Project" > README.md
git add README.md
git commit -m "Initial commit"
```

Create a repository on GitHub and push your code:

```sh
gh repo create my-new-repo --public --source=. --remote=origin --push
```

- Select public or private as needed.

---

## 4. View Your Repository in the Browser

```sh
gh repo view my-new-repo --web
```

---

## 5. (Optional) Create a GitHub Personal Access Token (PAT)

If you want to use Terraform (or other tools) to access GitHub via API, you need a Personal Access Token (PAT). Follow these steps:

### a. Generate a GitHub Token

1. Go to [https://github.com/settings/tokens](https://github.com/settings/tokens)
2. Click **"Generate new token"** (classic) or **"Fine-grained token"** if using the newer version.
3. Enter a **name**, and select **expiration** (choose "No expiration" for long-term use).
4. **Select scopes/permissions:**  
   - For Terraform, you typically need:
     - `repo` (Full control of private repositories)
     - `admin:repo_hook`
     - `delete_repo` (if needed)
     - `workflow` (if using actions)
     - (Adjust based on your needs)
5. Click **"Generate token"**.
6. **Copy the generated token once displayed**. You will not be able to retrieve it again.

### b. Set the Token as an Environment Variable

In your terminal, run:

```sh
export GITHUB_TOKEN=your_generated_token_here
```

You can add this line to your `~/.zshrc`, `~/.bash_profile`, or `~/.bashrc` to persist it:

```sh
echo 'export GITHUB_TOKEN=your_generated_token_here' >> ~/.zshrc
# Or use ~/.bash_profile or ~/.bashrc for other shells
```

Reload your shell config (if you added it):

```sh
source ~/.zshrc
```

---

## 6. (Optional) Use the Token with Terraform

Terraform and many other CLI tools will automatically use the `GITHUB_TOKEN` environment variable for authentication.  
You do **not** need to put the token in your Terraform code.

Example in a Terraform provider configuration:

```hcl
provider "github" {
  token = var.github_token  # Or rely on the GITHUB_TOKEN environment variable
  owner = "your_github_username"
}
```
If `token` is not specified, Terraform will use the `GITHUB_TOKEN` environment variable by default.

---

You’re done! You have installed `gh`, authenticated, created a repository, **and** set up a GitHub token for Terraform or API access.
