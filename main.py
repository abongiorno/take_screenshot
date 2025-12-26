from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import random
import requests
from pathlib import Path
from datetime import datetime

root_dir = "C:\\Users\\andre\\OneDrive\\01_ANDREA\\Fumetti"
slow_read = True  # Imposta su True per lettura lenta, False per rapida

#TEX WILLER
# ID = 75
# url="https://www.bonellidigitalclassic.com/detail/TEX_WILLER/BN/TEX_W_"
# folder_name="Tex Willer"
# max_fumetto=80

#TEX
# ID = 7
# url="https://www.bonellidigitalclassic.com/detail/TEX/BN/TEX_"
# folder_name="Tex"
# max_fumetto=9

# #TEX PRESENTA
# ID=8
# url="https://www.bonellidigitalclassic.com/detail/TEX_PRESENTA/BN/TEX_PRES_"
# folder_name="Tex Presenta"
# max_fumetto=80

# # SUPERTEX SPECIALE
# ID=0
# url="https://www.bonellidigitalclassic.com/detail/SUPERTEX_SPECIALE/BN/SUPERTEX_SPECIALE_"
# folder_name="SuperTex Speciale"
# max_fumetto=80

# TEX SPECIALE
ID=5
url="https://www.bonellidigitalclassic.com/detail/TEX_SPECIALE/BN/TEX_SPECIALE_"
folder_name="Tex Speciale"
max_fumetto=80

# #DRAGONERO
# ID=42
# url="https://www.bonellidigitalclassic.com/detail/DRAGONERO/BN/DGN_"
# folder_name="Dragonero"
# max_fumetto=80

# #DRAGONERO MONDO OSCURO
# ID = 6
# url="https://www.bonellidigitalclassic.com/detail/DRAGONERO_MONDO_OSCURO/BN/DRAGONERO_MONDO_OSCURO_"
# folder_name="Dragonero Mondo Oscuro"
# max_fumetto=80

#DRAGONERO_IL_RIBELLE
# ID = 0
# url="https://www.bonellidigitalclassic.com/detail/DRAGONERO_IL_RIBELLE/BN/DRAGONERO_IL_RIBELLE_"
# folder_name="Dragonero Il Ribelle"
# max_fumetto=80




# Apri Chrome
driver = webdriver.Chrome()

while ID <= max_fumetto:
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
    output_dir = Path(root_dir) / folder_name / f"{ID_TEXT} {folder_name}"
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

    first = True

    try:
            page_index = driver.find_element("id", "pageIndex")
            page_text = page_index.text
            max_pagine = int(page_text.split("/ ")[1])+1
            print(f"Numero totale di pagine: {max_pagine}")
    except (NoSuchElementException, IndexError, ValueError):
        print("Non è stato possibile recuperare il numero di pagine")

    while True:
        if slow_read == True:
            #REALE
            random_sleep_cambio_pagina_master =random.uniform(35, 45)
            random_sleep_fumetto = random.uniform(120,240)
        else:
            #RAPIDO
            random_sleep_cambio_pagina_master =random.uniform(2,10)
            random_sleep_fumetto = random.uniform(5,15)

        # Cerca il div con classe mercuryBox
        try:
            time.sleep(1)
            mercury = driver.find_elements("css selector", "div.mercuryBox")
            if first:
                mercury= mercury[0]
                first= False
            else:
                mercury= mercury[1]
        except NoSuchElementException:
            print("Elemento div.mercuryBox non trovato, ciclo terminato")
            break

        # Salva screenshot del div mercuryBox
        # screenshot_path = output_dir / f"mercury_screenshot_{counter}.png"
        # mercury.screenshot(str(screenshot_path))
        # print(f"Screenshot del div mercuryBox salvato: {screenshot_path}")

        #Verifico se l'immagine non è già stata scaricata
        filename = output_dir / f"{ID_TEXT}_{folder_name}_{counter}.gif"
        if not filename.exists():
            random_sleep_cambio_pagina = random_sleep_cambio_pagina_master
            print(f"File {filename} non esistente, procedo con il download.")
        
            # Cerca un'immagine all'interno del div e scaricala se presente
            try:
                img = mercury.find_element("css selector", "img")
                src = img.get_attribute('src')
                print(f"Img src trovata: {src}")
                if src:
                    response = requests.get(src)
                    if response.status_code == 200:
                        
                        with open(filename, 'wb') as f:
                            f.write(response.content)
                        print(f"Immagine scaricata: {filename}")
                    else:
                        print(f"Errore nel download: {response.status_code}")
            except NoSuchElementException:
                print("Nessuna <img> trovata dentro il div mercuryBox")
        else:
            random_sleep_cambio_pagina = 2
            print(f"File {filename} già esistente, salto il download.")

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

    


