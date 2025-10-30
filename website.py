from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import sys
import time

def setup_driver():
    load_dotenv()
    try:
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")

        driver_path = os.getenv("DRIVER_PATH")
        if not os.path.exists(driver_path):
            sys.exit(1)
        service = Service(driver_path)
        driver = webdriver.Edge(service=service, options=options)
        return driver
    except Exception as e:
        print(f"Failed to open Edge: {e}")
        sys.exit(1)
def start_game(driver, url):
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    try:
        play_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Jogar agora')]")))
        play_button.click()
    except:
        pass
    try:
        start_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Iniciar')]")))
        start_button.click()
    except Exception as e:
        print(f"Start button not found: {e}")
        sys.exit(1)
    try:
        close_instructions = wait.until(EC.element_to_be_clickable((By.ID, "close")))
        close_instructions.click()
    except:
        pass
def find_useful_letters(driver):
    letters = []
    letters_html = driver.find_elements(By.CSS_SELECTOR, ".cell-letter.svelte-1vt3j7k")
    for letter in letters_html:
        letters.append(letter.text)
    return letters
def send_answers(driver, filtered_words):
    input_box = driver.find_element(By.ID, "input")
    words_tried = 0
    for word in filtered_words:
        try:
            if possible_word(driver, word):
                print(f'Attempting word: {word}')
                input_box.send_keys(word)
                input_box.send_keys(Keys.ENTER)
                time.sleep(.2)
                input_box.send_keys(Keys.CONTROL + 'a')
                input_box.send_keys(Keys.DELETE)
                words_tried += 1
        except:
            break
    return words_tried
def possible_word(driver, word):
    selector = f"//span[contains(., '{len(word)} letras')]"
    if len(driver.find_elements(By.XPATH, selector)) > 0:
        return True
    else:
        return False
def check_success(driver):
    total_points = driver.find_element(By.CSS_SELECTOR, ".points.svelte-9jj3fa")
    total_points = total_points.text
    total_points = total_points.split('/')
    return total_points
def get_words_from_today(driver):
    words = []
    words_html = driver.find_elements(By.CSS_SELECTOR, ".word-box.svelte-9jj3fa.found")
    for word in words_html:
        words.append(word.text)
    return words