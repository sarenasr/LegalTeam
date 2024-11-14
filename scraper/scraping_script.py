from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import logging
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


from datetime import datetime

logging.getLogger('selenium').setLevel(logging.ERROR)
os.environ['PYTHONWARNINGS'] = 'ignore'

def webscrape(num) -> None:
    chrome_options = Options()
    # chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--no-sandbox") # linux only
    #chrome_options.add_argument("--headless=new") # for Chrome >= 109
    # chrome_options.add_argument("--headless")
    chrome_options.headless = True # also works
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--log-level=3')  # Fatal only
    chrome_options.add_argument('--silent')
    driver = webdriver.Chrome(options=chrome_options)
    # Initialize ChromeDriver
    #driver = webdriver.Chrome()

    # Open the website
    driver.get('https://consultaprocesos.ramajudicial.gov.co/Procesos/NumeroRadicacion')
    driver.maximize_window()

    data = {"status": "success", "message": "", "actuaciones": []}

    try:
        # Wait for the radio button by targeting the label text
        todos_los_procesos_radio = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'Todos los Procesos')]"))
        )
        todos_los_procesos_radio.click()

        # Wait for the input field to appear and enter the case number
        search_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Ingrese los 23 dígitos del número de Radicación']"))
        )
        case_number = num ##### CHANGE FOR ANY OTHER RADICADO  #####
        search_box.send_keys(case_number)

        # Wait for the "Consultar" button and click it
        consultar_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Consultar Número de radicación']"))
        )
        consultar_button.click()

        # Try to handle the popup if it appears
        try:
            # Wait for the popup to appear
            popup = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'v-dialog--active')]"))
            )
            print("Popup detected")
            
            # Wait for the "Volver" button using a more specific selector based on class and span content
            volver_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@align='center']//button//span[contains(text(), 'Volver')]"))
            )
            
            # Log the detection of the "Volver" button
            print("Volver button detected")

            # Click the "Volver" button to dismiss the popup
            volver_button.click()

            # Log the successful click
            print("Popup dismissed by clicking 'Volver'.")

        except Exception as e:
            print("No popup detected or error handling popup:", str(e))

        # Continue with handling the page and extracting the most recent case
        # (You can add here the part for processing the results, like in previous code)

            # After dismissing the popup (if applicable), find the table rows
        rows = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, "//tbody/tr"))
        )

        most_recent_date = None
        selected_row = None

        # Iterate through each row to extract the dates and compare
        for row in rows:
            # Locate the date within the third column (Fecha de Radicación y última actuación)
            date_button = row.find_element(By.XPATH, ".//td[3]//button//span")
            date_text = date_button.text.strip()  # Example: '2024-09-30'
            
            # Convert the extracted date text to a datetime object for comparison
            current_date = datetime.strptime(date_text, '%Y-%m-%d')
            print(current_date)
            
            # Check if this date is the most recent
            if most_recent_date is None or current_date > most_recent_date:
                most_recent_date = current_date
                selected_row = row

        # After identifying the row with the most recent date
        if selected_row:
            # Click the associated button in that row to select the most recent case
            case_button = selected_row.find_element(By.XPATH, ".//td[2]//button")
            time.sleep(0.2)
            case_button.click()
            
            print(f"Clicked case with the most recent date: {most_recent_date}")

        else:
            print("No rows found or no recent date could be determined.")

        # Extract the "Despacho" information from the table
        try:
            despacho = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//th[contains(text(), 'Despacho:')]/following-sibling::td"))
            ).text

            print(f"Despacho: {despacho}")
        except Exception as e:
            print("Unable to locate Despacho:", str(e))

        # Click the "Actuaciones" button
        try:
            actuaciones_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@role='tab' and contains(text(), 'Actuaciones')]"))
            )
            #time.sleep(2)
            actuaciones_button.click()
            print("Navigated to Actuaciones tab.")
        except Exception as e:
            print("Unable to click Actuaciones button:", str(e))


        # First, print the table's HTML to check its structure
        try:
            table_html = driver.find_element(By.XPATH, "//table").get_attribute("outerHTML")
            print("Table HTML:\n", table_html)
        except Exception as e:
            print("Unable to locate the table element:", str(e))

        # Initialize an empty list to hold the actuaciones data
        actuaciones_data = []

        try:
            # Confirm that the "Actuaciones" tab is active
            active_tab = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'v-tab--active') and text()='Actuaciones']"))
            )
            time.sleep(0.2)
            # Locate the table by header or unique identifier
            actuaciones_table = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//table//th[@aria-label='Fecha de Actuación']/ancestor::table"))
            )

            # Extract all rows from the table
            rows = WebDriverWait(actuaciones_table, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, ".//tbody/tr"))
            )

            for i, row in enumerate(rows[:5]):
                try:
                    fecha_actuacion = row.find_element(By.XPATH, "./td[1]").text.strip()
                    actuacion = row.find_element(By.XPATH, "./td[2]").text.strip()
                    anotacion = row.find_element(By.XPATH, "./td[3]").text.strip()
                    
                    data["actuaciones"].append({
                        "fecha_actuacion": fecha_actuacion,
                        "actuacion": actuacion,
                        "anotacion": anotacion
                    })
                except Exception as e:
                    print(f"Skipping row {i+1} due to error: {str(e)}")
                    continue

            return data

        except Exception as e:
            data["status"] = "error"
            data["message"] = str(e)
            return data

    finally:
        driver.quit()

#webscrape(11001311000620220034300)
