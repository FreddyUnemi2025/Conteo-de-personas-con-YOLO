Conteo-de-personas-con-YOLO
Sistema de detección y conteo de personas en tiempo real utilizando el modelo YOLO (You Only Look Once).

Instalación del Proyecto
Sigue los siguientes pasos para configurar y ejecutar el proyecto en tu máquina local.

1. Requisitos Previos
Asegúrate de tener instalado lo siguiente:

Python 3.8+: Es el lenguaje principal del proyecto.

Git: Necesario para clonar el repositorio.

2. Clonar el Repositorio
Abre tu terminal o línea de comandos y clona el proyecto:

Bash

git clone https://github.com/TU_USUARIO/Conteo-de-personas-con-YOLO.git
cd Conteo-de-personas-con-YOLO
Nota: Reemplaza https://github.com/TU_USUARIO/Conteo-de-personas-con-YOLO.git con la URL real de tu repositorio si es diferente.

3. Configuración del Entorno Virtual
Es fundamental trabajar dentro de un entorno virtual para aislar las dependencias del proyecto.

a. Crear el Entorno Virtual
Bash

# Para Windows:
python -m venv venv

# Para macOS/Linux:
python3 -m venv venv
b. Activar el Entorno Virtual
Bash

# Para Windows (Command Prompt):
.\venv\Scripts\activate

# Para Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Para macOS/Linux:
source venv/bin/activate
Verás que el nombre de tu entorno ((venv)) aparece al inicio de la línea de comandos, indicando que está activo.

4. Instalar Dependencias
Con el entorno virtual activado, instala todas las librerías necesarias utilizando el archivo requirements.txt:

Bash

pip install -r requirements.txt
Dependencias Clave:

opencv-python (o opencv-contrib-python): Para el manejo de vídeo y la interfaz con el modelo.

ultralytics (o el paquete específico de tu versión de YOLO, ej., torch, torchvision): Para cargar y ejecutar el modelo YOLO.

numpy: Para operaciones numéricas eficientes.
