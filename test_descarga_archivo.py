from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
from datetime import datetime

# Directorios
screenshot_dir = r"C:\Users\elgej\selenium-tests"
os.makedirs(screenshot_dir, exist_ok=True)

download_dir = os.path.join(screenshot_dir, "downloads")
os.makedirs(download_dir, exist_ok=True)

def take_screenshot(driver, name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{name}_{timestamp}.png"
    file_path = os.path.join(screenshot_dir, file_name)
    driver.save_screenshot(file_path)
    print(f"Pantallazo guardado en: {file_path}")

def test_descarga_archivo():
    # Opciones de Chrome
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.maximize_window()
        wait = WebDriverWait(driver, 10)

        print("Iniciando prueba de descarga...")
        driver.get("https://demoqa.com/upload-download")

        take_screenshot(driver, "pagina_descarga_inicial")
        download_button = wait.until(EC.element_to_be_clickable((By.ID, "downloadButton")))
        take_screenshot(driver, "antes_descarga")
        download_button.click()
        print("Botón de descarga presionado")

        # Esperar que el archivo se descargue
        archivo_descargado = os.path.join(download_dir, "sampleFile.jpeg")
        tiempo_maximo = 15
        tiempo_espera = 0
        while not os.path.exists(archivo_descargado) and tiempo_espera < tiempo_maximo:
            time.sleep(1)
            tiempo_espera += 1
            print(f"Esperando descarga... {tiempo_espera}s")

        take_screenshot(driver, "despues_descarga")

        # Verificar existencia del archivo
        assert os.path.exists(archivo_descargado), f"El archivo no se descargó correctamente a: {archivo_descargado}"

        file_size = os.path.getsize(archivo_descargado)
        print(f"¡PRUEBA EXITOSA! El archivo fue descargado a: {archivo_descargado}")
        print(f"Tamaño del archivo: {file_size} bytes")

        driver.execute_script("document.body.innerHTML += '<div id=\"success-message\" style=\"color:green;font-size:20px;position:fixed;top:10px;left:10px;background:white;padding:10px;z-index:9999;\">¡Descarga exitosa!</div>'")
        take_screenshot(driver, "descarga_exitosa")

        print("\nArchivos en el directorio de descarga:")
        for archivo in os.listdir(download_dir):
            print(f" - {archivo}")

        time.sleep(2)

    except Exception as e:
        print(f"Error durante la prueba: {e}")
        if 'driver' in locals():
            driver.execute_script("document.body.innerHTML += '<div id=\"error-message\" style=\"color:red;font-size:20px;position:fixed;top:10px;left:10px;background:white;padding:10px;z-index:9999;\">Error: " + str(e).replace("'", "\\'") + "</div>'")
            take_screenshot(driver, "error_en_prueba")
        raise e

    finally:
        if 'driver' in locals():
            driver.quit()
        print("Prueba finalizada.")
