# Proyecto de Pruebas Automatizadas con Selenium  
![selenium-selenium](https://github.com/user-attachments/assets/1ddf7df4-5ba3-4f14-83e8-1d0c156943d0)

Este proyecto contiene pruebas automatizadas para [DemoQA](https://demoqa.com) usando Selenium WebDriver. Las pruebas cubren formularios de registro, carga/descarga de archivos, manejo de alertas y ejecución en modo headless.

## Tabla de Contenidos

- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Ejecución de Pruebas](#ejecución-de-pruebas)
- [Reportes](#reportes)
- [Manejo de Descargas](#manejo-de-descargas)
- [Modo Headless](#modo-headless)
- [Casos de Prueba](#casos-de-prueba)
- [Evidencias de Pruebas](#evidencias-de-pruebas)
- [Desarrolladora](#desarrolladora)
- [Conclusión](#conclusión)


## Requisitos

- Python 3.8+
- Navegador Chrome 
-- ChromeDriver (debe descargarse por separado)
- Git

## Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/su-usuario/selenium-test.git
   cd selenium-test
   ```

2. **Crear un entorno virtual (opcional pero recomendado):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate

   Nota: La carpeta del entorno virtual (venv) no está incluida en el repositorio y debe ser creada localmente.
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar WebDriver:**
   - Descargar [ChromeDriver](https://sites.google.com/chromium.org/driver/) compatible con tu versión de Chrome
   - Crear una carpeta `chromedriver-win64` en la raíz del proyecto
   - Extraer el ChromeDriver descargado en esta carpeta
   - Alternativamente, puedes usar webdriver-manager que instalará automáticamente el driver adecuado

## Estructura del Proyecto

```
selenium-test/
├── alertas/                   # Scripts y evidencias de pruebas de alertas
├── carga_archivos/            # Scripts y evidencias de pruebas de carga de archivos
├── chromedriver-win64/        # [Crear esta carpeta y añadir ChromeDriver]
├── downloads/                 # Carpeta para archivos descargados
├── headless/                  # Scripts y evidencias de pruebas en modo headless
├── registro_usuarios/         # Scripts y evidencias de pruebas de registro
├── [capturas de pantalla]     # Pantallazos de pruebas y evidencias
├── requirements.txt           # Dependencias del proyecto
├── HEADLESS_DOWNLOADS.md      # Explicación de descargas y modo headless
└── README.md                  # Documentación principal
```

## Ejecución de Pruebas

Para ejecutar las pruebas de los diferentes módulos:

### Registro de Usuarios:
```bash
python registro_usuarios/test_form.py
```

### Carga/Descarga de Archivos:
```bash
python carga_archivos/test_upload_download.py
```

### Alertas:
```bash
python alertas/test_alerts.py
```

### Modo Headless:
```bash
python headless/test_headless.py
```

## Reportes

El proyecto incluye capturas de pantalla como evidencia de la ejecución exitosa de las pruebas. Las capturas se encuentran en sus respectivas carpetas y también en la raíz del proyecto.

Para generar reportes HTML automáticos, se puede implementar `pytest-html`:

1. Instalar el plugin:
```bash
pip install pytest-html
```

2. Ejecutar pruebas con generación de reportes:
```bash
pytest --html=report.html
```

## Manejo de Descargas

Las descargas se configuran para guardarse automáticamente en la carpeta `downloads` del proyecto. El proceso se realiza mediante la configuración de opciones de Chrome:

```python
options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": download_path,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True
}
options.add_experimental_option("prefs", prefs)
```

La verificación de las descargas se realiza comprobando la existencia del archivo en la carpeta especificada después de la acción de descarga.

Para más detalles, consulte el archivo [HEADLESS_DOWNLOADS.md](HEADLESS_DOWNLOADS.md).

## Modo Headless

El modo headless permite ejecutar pruebas sin abrir una ventana visible del navegador. Se implementa añadiendo opciones específicas al navegador:

```python
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
```

Las pruebas headless se encuentran en la carpeta `headless` y siguen la misma lógica que las pruebas normales pero sin interfaz gráfica visible.

Para más detalles, consulte el archivo [HEADLESS_DOWNLOADS.md](HEADLESS_DOWNLOADS.md).

## Casos de Prueba

### Registro de Usuario
- **URL**: https://demoqa.com/automation-practice-form
- **Descripción**: Completa el formulario de registro con datos de prueba
- **Validación**: Verifica el mensaje "Thanks for submitting the form"
- **Ubicación**: carpeta `registro_usuarios`

### Carga de Archivos
- **URL**: https://demoqa.com/upload-download
- **Descripción**: Sube un archivo al sistema
- **Validación**: Verifica que el nombre del archivo aparezca en la página
- **Ubicación**: carpeta `carga_archivos`

### Descarga de Archivos
- **URL**: https://demoqa.com/upload-download
- **Descripción**: Descarga el archivo "sampleFile.jpeg"
- **Validación**: Verifica la existencia del archivo en la carpeta de descargas
- **Ubicación**: carpeta `carga_archivos`

### Alertas
- **URL**: https://demoqa.com/alerts
- **Descripción**: Interactúa con diferentes tipos de alertas
- **Validación**: Verifica las respuestas correctas a cada interacción
- **Ubicación**: carpeta `alertas`

## Evidencias de Pruebas

El repositorio incluye capturas de pantalla que demuestran la ejecución exitosa de todas las pruebas requeridas:
- Las capturas de pantalla muestran el estado antes y después de cada operación
- Las evidencias están organizadas en sus respectivas carpetas de componentes
- También se incluyen algunas capturas en la raíz del proyecto para fácil acceso

Estas evidencias demuestran el correcto funcionamiento de todas las pruebas automatizadas implementadas para el proyecto.

## Desarrolladora

Este proyecto fue desarrollado por Johana Saavedra estudiante de tercer semestre en Técnica profesional en programación de aplicaciones de software de la Universidad compensar

![Foto hoja de vida](https://github.com/user-attachments/assets/293dde5c-6ce0-449b-a135-a3320c62dc51)

### Conclusión

Desarrollar este proyecto con Selenium ha sido una experiencia muy enriquecedora para mi proceso de formación en pruebas de software. Durante el desarrollo de cada una de las pruebas automatizadas, pude entender de manera más clara la importancia de validar el comportamiento de una aplicación web desde diferentes ángulos, como la interacción con formularios, la carga y descarga de archivos, el manejo de alertas y el uso del modo headless.

En lo personal, este proyecto no solo me permitió aplicar lo aprendido en clase, sino también descubrir que el área de pruebas es fundamental para garantizar la calidad del software. Sin duda, este trabajo me motivó a seguir profundizando en este campo, ya que me demostró que con práctica y dedicación es posible automatizar procesos complejos de forma eficiente.
