from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import random
import requests
from pathlib import Path
from datetime import datetime


# 2 min a 1 ora
# random_sleep = random.uniform(120,3600)
#da 2 minuti a 10 minuti
random_sleep_fumetto = random.uniform(30,35)
random_sleep_cambio_pagina =random.uniform(2, 6)

random_sleep_cambio_pagina =random.uniform(40, 100)
random_sleep_fumetto = random.uniform(1200,1800)

ID = 17
url="https://www.bonellidigitalclassic.com/detail/TEX_WILLER/BN/TEX_W_"
folder_name="Tex Willer"
max_pagine=68

ID = 0
url="https://www.bonellidigitalclassic.com/detail/DRAGONERO_MONDO_OSCURO/BN/DRAGONERO_MONDO_OSCURO_"
folder_name="Dragonero Mondo Oscuro"
max_pagine=100


# Apri Chrome
driver = webdriver.Chrome()

while True:
    ID += 1
    print(f"Processing ID: {ID}")
    ID_TEXT = ("000"+str(ID))[-3:]
    
    driver.get(f"{url}{ID_TEXT}")
    time.sleep(5)
    try:
        login_link = driver.find_element("xpath", "//a[contains(text(), 'Accedi')] | //button[contains(text(), 'Accedi')]")
        login_link.click()
        print("Click sul pulsante 'Accedi' eseguito")
        time.sleep(3)

        # Compila il campo input email
        email_input = driver.find_element("css selector", "input[type='email']")
        email_input.send_keys("andreabongiorno@gmail.com")


        # Compila il campo input email
        email_input = driver.find_element("css selector", "input[type='password']")
        email_input.send_keys("Tex2026!")

        login_button = driver.find_element("css selector", "button[type='submit']")
        login_button.click()

    except NoSuchElementException:
        print("Pulsante 'Accedi' non trovato, procedo comunque")


    # Cartella dove salvare le immagini
    output_dir = Path(f"{ID_TEXT} {folder_name}")
    output_dir.mkdir(parents=True, exist_ok=True)

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
                    filename = output_dir / f"{folder_name}_{counter}.gif"
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

        if (counter > max_pagine):
            print(f"Limite di {max_pagine} pagine raggiunto, ciclo terminato")
            print(f"Attesa di {random_sleep_fumetto} secondi prima di procedere al prossimo ID.")
            print(f"Data e ora attuale: {datetime.now()}")
            future_time = datetime.now() + __import__('datetime').timedelta(seconds=random_sleep_fumetto)
            print(f"Ripresa prevista alle: {future_time}")
            time.sleep(random_sleep_fumetto)
            break
        # Aspetta il caricamento della pagina seguente
        
        print(f"Attesa di {random_sleep_cambio_pagina} secondi prima di procedere al cambio pagina successiva.")
        print(f"Data e ora attuale: {datetime.now()}")
        future_time = datetime.now() + __import__('datetime').timedelta(seconds=random_sleep_cambio_pagina)
        print(f"Ripresa prevista alle: {future_time}")
        
        time.sleep(random_sleep_cambio_pagina)

    


