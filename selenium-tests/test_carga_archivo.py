from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import os

# Configuración de directorios
screenshots_dir = r"C:\Users\elgej\selenium-tests\carga_archivos"
os.makedirs(screenshots_dir, exist_ok=True)

# Crear archivo de prueba si no existe
archivo_prueba = "archivo_prueba.txt"
if not os.path.exists(archivo_prueba):
    with open(archivo_prueba, "w") as f:
        f.write("Este es un archivo de prueba para subir.")
file_path = os.path.abspath(archivo_prueba)

def test_carga_archivo():
    # Configuración del navegador
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.maximize_window()

    try:
        print("Iniciando prueba de carga de archivo...")
        driver.get("https://demoqa.com/upload-download")
        time.sleep(2)

        # Subir archivo
        upload_input = driver.find_element(By.ID, "uploadFile")
        upload_input.send_keys(file_path)
        print("Archivo subido")

        # Verificar resultado
        uploaded_path = driver.find_element(By.ID, "uploadedFilePath").text
        print(f"Texto de resultado: {uploaded_path}")

        assert "archivo_prueba.txt" in uploaded_path, "El nombre del archivo no coincide o no se muestra."

        # Captura de pantalla
        time.sleep(2)
        screenshot_path = os.path.join(screenshots_dir, "archivo_subido.png")
        driver.save_screenshot(screenshot_path)
        print(f"Captura guardada en: {screenshot_path}")

    except Exception as e:
        print(f"Error en la carga de archivos: {e}")
        raise e  # importante para que pytest lo marque como falla

    finally:
        driver.quit()
        print("Prueba finalizada.")
