# usam-2025
Repositorio de proyecto usam 2025 

## Estandarizacion de los commit
- Feat: se utilizara al hacer cambios, crear o agregar neuvas funciones, archivos, archivos multimeda, cambios de arquitectura.
- Fix: se utilizara cuando solucionemos bugs
- Doc: se utilizara cuando hagamos cambios o agreguemos documentacion

## Requerimientos
- Python 3.12 o superior
- pip
- virtualenv

## Como correr la aplicacion
1. Clonar el repositorio
     ```bash
     https://github.com/iot-cloud-solution/IoT-automation.git
     ```
>[!NOTE]
>Debes estas en la carpeta raiz del proyecto

2. Crear entorno virtual
    ```bash
    virtualenv env
    ```

3. Activar entorno virtual, desde git bash usando tabby o propiamente git bash
    ```bash
    source env/Scripts/activate
    ```

4. Instalar las dependencias
    ```bash
    pip install -r requirements.txt
    ```
5. Instalar nodeJS desde el siguiente enlace, preferiblemente la version latest.
     ![image](https://github.com/user-attachments/assets/35023761-ed34-4ebe-a552-ce9d43bb55dc)

6. Validar con exito a instalacion de NodeJs y NPM, npm ya viene integrado con nodejs ya que es el gestor de paquetes por defecto, en caso de ejecutar los siguientes comandos y no ver nada o genere error cerrar git bash o tabby y abriro de nuevo para que puede resetear y leer los nuevos cambios en las variables de entorno del PATH. Deberiamos ver con exito las versiones de cada herramienta
    ```bash
    node -v
    ```
    ```bash
    npm -v
    ```

7. Ahora instalaremos las dependencias necesarias para trabajar con serverless framework. Cabe recalcar que serverless framework trabaja con nodejs por lo cual, es necesario trabajar con node y npm para correr en local o ejecutar serverless para a creacion de recursos.
    ```bash
    npm install
    ```

8. Ahora que tengamos instalado debemos configurar las variables de entorno. Para esto encontramos un archivo .env.template y este contiene las variables de entorno que debemos configurar. Crearemos un archivo .env en la raiz del proyecto y pegaremos el contenido del template, colocamos las credenciales propias nuestras para poder trabajar bien y listo. Deberia quedar de esta manera nuestra raiz del proyecto.

     ![image](https://github.com/user-attachments/assets/a5a5b968-4c5e-4f5d-af8b-a0e5fccd5778)

9. Ahora para testear en local lo que hay actualmente ejecutaremos el siguiente comando. (En funcion colocar el nombre de la funcion que se desea testear)
    ```bash
    npx serverless invoke local --function funcion
    ```