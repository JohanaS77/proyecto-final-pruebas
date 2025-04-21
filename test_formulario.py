from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import os
from datetime import datetime

# Configuración de directorios
screenshot_dir = r"C:\Users\elgej\selenium-tests\registro_usuarios"
os.makedirs(screenshot_dir, exist_ok=True)

def take_screenshot(driver, name):
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(screenshot_dir, f"{name}_{timestamp}.png")
        driver.save_screenshot(file_path)
        print(f"Pantallazo guardado en: {file_path}")
    except Exception as e:
        print(f"Error al guardar pantallazo {name}: {e}")

def test_formulario():
    # Configuración del navegador
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    try:
        # Iniciar navegador
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        driver.set_page_load_timeout(30)
        wait = WebDriverWait(driver, 10)

        print("Iniciando prueba de formulario...")
        driver.get("https://demoqa.com/automation-practice-form")
        take_screenshot(driver, "01_pagina_inicial")

        # Completar datos personales
        wait.until(EC.presence_of_element_located((By.ID, "firstName"))).send_keys("Julián")
        driver.find_element(By.ID, "lastName").send_keys("Rodríguez")
        driver.find_element(By.ID, "userEmail").send_keys("julian.rodriguez@mail.com")
        take_screenshot(driver, "02_datos_personales")

        # Seleccionar género
        gender = driver.find_element(By.CSS_SELECTOR, "label[for='gender-radio-1']")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", gender)
        driver.execute_script("arguments[0].click();", gender)
        take_screenshot(driver, "03_genero_seleccionado")

        # Completar teléfono
        driver.find_element(By.ID, "userNumber").send_keys("3112442060")

        # Seleccionar fecha de nacimiento
        date_input = driver.find_element(By.ID, "dateOfBirthInput")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", date_input)
        date_input.click()
        take_screenshot(driver, "04_calendario_abierto")

        day = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".react-datepicker__day--001:not(.react-datepicker__day--outside-month)")
        ))
        day.click()
        take_screenshot(driver, "05_fecha_seleccionada")

        # Seleccionar hobby
        hobby = driver.find_element(By.CSS_SELECTOR, "label[for='hobbies-checkbox-1']")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", hobby)
        driver.execute_script("arguments[0].click();", hobby)
        take_screenshot(driver, "06_hobby_seleccionado")

        # Completar dirección
        address = driver.find_element(By.ID, "currentAddress")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", address)
        address.send_keys("Calle Ejemplo 123, Ciudad Ejemplo")
        take_screenshot(driver, "07_direccion_completada")

        # Enviar formulario
        submit = driver.find_element(By.ID, "submit")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit)
        take_screenshot(driver, "08_antes_submit")
        driver.execute_script("arguments[0].click();", submit)
        take_screenshot(driver, "09_despues_submit")

        # Verificar resultado
        try:
            modal = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "modal-content")))
            take_screenshot(driver, "10_modal_encontrado")

            modal_text = modal.text
            if "Thanks for submitting the form" in modal_text:
                print("¡PRUEBA EXITOSA! Se encontró el mensaje de éxito en el modal.")
                driver.execute_script("""
                    var modal = document.querySelector('.modal-content');
                    var successText = Array.from(modal.querySelectorAll('*')).find(el => el.textContent.includes('Thanks for submitting the form'));
                    if(successText) {
                        successText.style.border = '3px solid green';
                        successText.style.backgroundColor = 'rgba(0, 255, 0, 0.2)';
                    }
                """)
                take_screenshot(driver, "11_registro_exitoso_resaltado")
            else:
                print("El mensaje de éxito no se encontró en el modal")
        except TimeoutException:
            print("No se encontró el modal")
            if "Thanks for submitting the form" in driver.page_source:
                print("Se encontró el mensaje en la página.")
                take_screenshot(driver, "11_mensaje_en_pagina")

    except Exception as e:
        print(f"Error: {e}")
        if 'driver' in locals():
            take_screenshot(driver, "error_general")

    finally:
        if 'driver' in locals():
            driver.quit()
        print("Prueba finalizada")
