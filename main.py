from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import requests
from pathlib import Path
from datetime import datetime

# Apri Chrome
driver = webdriver.Chrome()
driver.get("https://www.bonellidigitalclassic.com/detail/TEX_WILLER/BN/TEX_W_006")

# Cartella dove salvare le immagini
output_dir = Path("downloads")
if output_dir.exists():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(f"downloads_{timestamp}")
output_dir.mkdir(parents=True, exist_ok=True)

# Compila il campo input email
email_input = driver.find_element("css selector", "input[type='email']")
email_input.send_keys("andreabongiorno@gmail.com")


# Compila il campo input email
email_input = driver.find_element("css selector", "input[type='password']")
email_input.send_keys("Tex2026!")

login_button = driver.find_element("css selector", "button[type='submit']")
login_button.click()

# Contatore per i file scaricati
counter = 1
time.sleep(5)
# Attendi e clicca sul link "Leggi"
try:
    read_link = driver.find_element("xpath", "//a[contains(text(), 'Leggi')]")
    read_link.click()
    print("Click sul link 'Leggi' eseguito")
except NoSuchElementException:
    print("Link 'Leggi' non trovato")

# Aspetta qualche secondo per caricare la pagina
time.sleep(3)

while True:

    # Cerca il div con classe mercuryBox
    try:
        mercury = driver.find_element("css selector", "div.mercuryBox")
    except NoSuchElementException:
        print("Elemento div.mercuryBox non trovato, ciclo terminato")
        break

    # Salva screenshot del div mercuryBox
    # screenshot_path = output_dir / f"mercury_screenshot_{counter}.png"
    # mercury.screenshot(str(screenshot_path))
    # print(f"Screenshot del div mercuryBox salvato: {screenshot_path}")

    # Cerca un'immagine all'interno del div e scaricala se presente
    try:
        img = mercury.find_element("css selector", "img")
        src = img.get_attribute('src')
        print(f"Img src trovata: {src}")
        if src:
            response = requests.get(src)
            if response.status_code == 200:
                filename = output_dir / f"image_downloaded_{counter}.gif"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"Immagine scaricata: {filename}")
            else:
                print(f"Errore nel download: {response.status_code}")
    except NoSuchElementException:
        print("Nessuna <img> trovata dentro il div mercuryBox")

    # Incrementa il contatore
    counter += 1

    # Clicca sul pulsante navigatorNext, se presente; altrimenti termina
    try:
        next_button = driver.find_element("id", "navigatorNext")
        next_button.click()
        print("Click su navigatorNext eseguito")
    except NoSuchElementException:
        print("Elemento navigatorNext non trovato, ciclo terminato")
        break

    if (counter > 70):
        print("Limite di 70 pagine raggiunto, ciclo terminato")
        break
    # Aspetta il caricamento della pagina seguente
    time.sleep(30)

# Chiudi il browser
driver.quit()


