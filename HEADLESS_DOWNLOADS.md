# Manejo de Descargas y Modo Headless

Este documento explica detalladamente cómo se implementaron las descargas automáticas y el modo headless en el proyecto de pruebas con Selenium.

## Manejo de Descargas Automáticas

### Configuración

Para manejar las descargas automáticas, se configurói las opciones del navegador Chrome para:
1. Especificar la carpeta `downloads` como ruta de descarga predeterminada
2. Desactivar la ventana de diálogo de descarga
3. Permitir que las descargas se completen en segundo plano

#### Implementación para Chrome:

```python
import os
from selenium import webdriver

# Definir la ruta de descarga relativa al proyecto
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
download_path = os.path.join(project_root, "downloads")

# Crear la carpeta si no existe
os.makedirs(download_path, exist_ok=True)

# Configurar opciones de Chrome
chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": download_path,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", prefs)

# Inicializar el driver
chromedriver_path = os.path.join(project_root, "chromedriver-win64", "chromedriver.exe")
driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
```

### Verificación de Descargas

Para verificar que los archivos se descargaron correctamente, se implementa un mecanismo de espera:

```python
import os
import time

def wait_for_download(file_path, timeout=30):
    """Espera a que un archivo se descargue completamente."""
    start_time = time.time()
    while not os.path.exists(file_path):
        if time.time() - start_time > timeout:
            raise Exception(f"Timeout esperando que {file_path} se descargue")
        time.sleep(0.5)
    
    # Verificar que el archivo no esté en uso (descarga completa)
    file_size = -1
    while file_size != os.path.getsize(file_path):
        file_size = os.path.getsize(file_path)
        time.sleep(0.5)
        if time.time() - start_time > timeout:
            break
    
    return os.path.exists(file_path)
```

## Modo Headless

El modo headless permite ejecutar pruebas sin abrir una ventana visible del navegador, lo que es útil para:
- Entornos de integración continua (CI/CD)
- Servidores sin interfaz gráfica
- Pruebas rápidas en segundo plano

### Implementación para Chrome:

```python
import os
from selenium import webdriver

# Configurar rutas
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
download_path = os.path.join(project_root, "downloads")
chromedriver_path = os.path.join(project_root, "chromedriver-win64", "chromedriver.exe")

# Crear carpeta de descargas si no existe
os.makedirs(download_path, exist_ok=True)

# Configurar modo headless
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")  # Necesario en algunos sistemas
chrome_options.add_argument("--window-size=1920,1080")  # Establecer tamaño de ventana
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Añadir configuración de descargas en modo headless
prefs = {
    "download.default_directory": download_path,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", prefs)

# Inicializar el driver en modo headless
driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
```

### Desafíos del Modo Headless

Algunos desafíos específicos del modo headless y cómo los solucioné:

1. **Interacciones con alertas**:
   - En modo headless, las alertas se manejan de manera diferente
   - Solución: Usamos el manejador de alertas de Selenium para interactuar con ellas

2. **Capturas de pantalla para depuración**:
   - A pesar de no tener interfaz gráfica visible, Selenium puede capturar pantallas:
   ```python
   driver.save_screenshot("headless_screenshot.png")
   ```

3. **Problemas de renderizado**:
   - Algunas páginas detectan el modo headless y cambian su comportamiento
   - Solución: Añadimos headers y configuraciones para simular un navegador normal:
   ```python
   chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
   ```

## Combinación de Modo Headless y Descargas

El principal desafío fue asegurar que las descargas funcionaran correctamente en modo headless. La solución:

1. Configurar correctamente el directorio de descargas antes de iniciar el navegador
2. Usar esperas para verificar que los archivos se descarguen completamente
3. Implementar manejo de errores para detectar problemas de descarga

## Conclusión

La implementación exitosa del modo headless y el manejo de descargas permitió:
- Ejecutar pruebas en entornos sin interfaz gráfica
- Automatizar completamente el proceso de descarga y verificación
- Reducir el tiempo de ejecución de las pruebas
