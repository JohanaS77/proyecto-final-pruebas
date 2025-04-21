from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from datetime import datetime
import json

download_path = os.path.join(os.getcwd(), "downloads")
os.makedirs(download_path, exist_ok=True)

screenshot_dir = r"C:\Users\elgej\selenium-tests\headless"
os.makedirs(screenshot_dir, exist_ok=True)

def take_screenshot(driver, name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{name}_{timestamp}.png"
    file_path = os.path.join(screenshot_dir, file_name)
    driver.save_screenshot(file_path)
    print(f"Pantallazo guardado en: {file_path}")

def test_descarga_headless():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  
    chrome_options.add_argument("--window-size=1920,1080") 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    prefs = {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,  
        "plugins.always_open_pdf_externally": True  
    }
    chrome_options.add_experimental_option("prefs", prefs)

    try:
        driver = webdriver.Chrome(options=chrome_options)

        # Habilitar descargas en modo headless (Chrome 86+)
        driver.command_executor._commands["send_command"] = (
            "POST", "/session/$sessionId/chromium/send_command"
        )
        params = {
            "cmd": "Page.setDownloadBehavior",
            "params": {
                "behavior": "allow",
                "downloadPath": download_path
            }
        }
        driver.execute("send_command", params)

        wait = WebDriverWait(driver, 10)

        print("Iniciando prueba de descarga en modo headless...")
        driver.get("https://demoqa.com/upload-download")

        take_screenshot(driver, "pagina_inicial_headless")

        download_button = wait.until(EC.element_to_be_clickable((By.ID, "downloadButton")))

        take_screenshot(driver, "antes_descarga_headless")

        download_button.click()
        print("Botón de descarga presionado")

        archivo_descargado = os.path.join(download_path, "sampleFile.jpeg")
        tiempo_maximo = 15
        tiempo_espera = 0
        while not os.path.exists(archivo_descargado) and tiempo_espera < tiempo_maximo:
            time.sleep(1)
            tiempo_espera += 1
            print(f"Esperando descarga... {tiempo_espera}s")

        take_screenshot(driver, "despues_descarga_headless")

        assert os.path.exists(archivo_descargado), f"El archivo no se descargó correctamente a: {archivo_descargado}"

        file_size = os.path.getsize(archivo_descargado)
        print(f"¡PRUEBA EXITOSA! El archivo fue descargado a: {archivo_descargado}")
        print(f"Tamaño del archivo: {file_size} bytes")

        # Mostrar mensaje de éxito en la página
        mensaje = f"¡Descarga exitosa! Archivo guardado en: {archivo_descargado}"
        driver.execute_script(
            f"""
            const mensaje = {json.dumps(mensaje)};
            const div = document.createElement('div');
            div.style = "color:green;font-size:20px;position:fixed;top:10px;left:10px;background:white;padding:10px;z-index:9999;";
            div.textContent = mensaje;
            document.body.appendChild(div);
            """
        )
        take_screenshot(driver, "descarga_exitosa_headless")

    except Exception as e:
        print(f"Error durante la prueba: {e}")
        if 'driver' in locals():
            mensaje_error = f"Error: {str(e)}"
            driver.execute_script(
                f"""
                const mensaje = {json.dumps(mensaje_error)};
                const div = document.createElement('div');
                div.style = "color:red;font-size:20px;position:fixed;top:10px;left:10px;background:white;padding:10px;z-index:9999;";
                div.textContent = mensaje;
                document.body.appendChild(div);
                """
            )
            take_screenshot(driver, "error_en_prueba_headless")
        raise

    finally:
        if 'driver' in locals():
            driver.quit()
        print("Prueba finalizada.")
