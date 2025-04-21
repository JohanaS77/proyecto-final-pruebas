from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from datetime import datetime

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)  

driver = webdriver.Chrome(options=options)
driver.maximize_window()

screenshot_dir = r"C:\Users\elgej\selenium-tests\alertas"
os.makedirs(screenshot_dir, exist_ok=True)

def take_screenshot(name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{name}_{timestamp}.png"
    file_path = os.path.join(screenshot_dir, file_name)
    driver.save_screenshot(file_path)
    print(f"Pantallazo guardado en: {file_path}")

try:
    print("Iniciando prueba de alertas...")
    driver.get("https://demoqa.com/alerts")
    wait = WebDriverWait(driver, 10)
    
    take_screenshot("pagina_inicial")
    
    # ---------- ALERTA DE CONFIRMACIÓN ----------
    print("Probando alerta de confirmación...")
    confirm_button = driver.find_element(By.ID, "confirmButton")
    
    driver.execute_script("arguments[0].scrollIntoView(true);", confirm_button)
    time.sleep(1) 
    
    take_screenshot("antes_alerta_confirmacion")
    
    wait.until(EC.element_to_be_clickable((By.ID, "confirmButton")))
    confirm_button.click()
    
    alert = wait.until(EC.alert_is_present())
    print("Texto de la alerta:", alert.text)
    
    time.sleep(3)
    
    alert.accept()
    
    take_screenshot("despues_alerta_confirmacion")
    
    result = driver.find_element(By.ID, "confirmResult").text
    print("Resultado en la página:", result)
    if "You selected Ok" in result:
        print("Confirmación aceptada correctamente")
    else:
        print("Algo salió mal al aceptar la alerta")
    
    # ---------- ALERTA DE PROMPT ----------
    print("Probando alerta de prompt...")
    prompt_button = driver.find_element(By.ID, "promtButton")
    driver.execute_script("arguments[0].scrollIntoView(true);", prompt_button)
    time.sleep(1)
    
    take_screenshot("antes_alerta_prompt")
    
    wait.until(EC.element_to_be_clickable((By.ID, "promtButton")))
    prompt_button.click()
    
    alert = wait.until(EC.alert_is_present())
    print("Texto de la alerta:", alert.text)
    
    time.sleep(3)
    
    nombre = "JulianBot"
    alert.send_keys(nombre)
    alert.accept()
    
    take_screenshot("despues_alerta_prompt")
    
    result = driver.find_element(By.ID, "promptResult").text
    print("Resultado en la página:", result)
    if nombre in result:
        print("Texto del prompt capturado y validado correctamente")
        take_screenshot("resultado_final")
    else:
        print("Algo salió mal al escribir en el prompt")

except Exception as e:
    print("Error durante la prueba:", str(e))
    take_screenshot("error")

finally:
    print("Cerrando navegador...")
    driver.quit()
    print("Prueba finalizada.")