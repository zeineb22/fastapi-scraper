from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import logging
import re
from datetime import datetime
import time

def scrape_annonces():
    logging.basicConfig(filename='scraping_errors.log', level=logging.ERROR, format='%(asctime)s - %(message)s')
    
    # ==================== Configuration du WebDriver ====================
    service = Service("C:/Windows/chromedriver.exe")  
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  
    driver = webdriver.Chrome(service=service, options=options)

    url = "http://www.tunisie-annonce.com/AnnoncesAuto.asp"
    driver.get(url)

    data = []
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, '//tr[contains(@bgcolor, "#294a73")]')))
        annonces = driver.find_elements(By.XPATH, '//tr[contains(@bgcolor, "#294a73")]/following-sibling::tr')

        for annonce in annonces:
            try:
                colonnes = annonce.find_elements(By.TAG_NAME, "td")
                if len(colonnes) >= 13:
                    region = colonnes[1].text.strip() or "N/A"
                    marque = colonnes[3].text.strip() or "N/A"
                    modele = colonnes[5].text.strip() or "N/A"
                    texte = colonnes[7].text.strip() or "N/A"
                    annee = colonnes[9].text.strip() or "N/A"
                    
                    # Extraction du prix
                    prix = "N/A"
                    if "onmouseover" in colonnes[11].get_attribute("outerHTML"):
                        prix_html = colonnes[11].get_attribute("onmouseover")
                        prix_match = re.search(r"(\d{1,3}(?:\s?\d{3})+)\s*Dinar", prix_html)
                        if prix_match:
                            prix = prix_match.group(1).replace(" ", "")
                    
                    # Extraction de la date de modification
                    date_modif = "N/A"
                    if "onmouseover" in colonnes[13].get_attribute("outerHTML"):
                        date_html = colonnes[13].get_attribute("onmouseover")
                        date_match = re.search(r"(\d{2}/\d{2}/\d{4})", date_html)
                        if date_match:
                            date_modif = date_match.group(1)

                    # Filtre sur janvier et février 2025
                    if date_modif != "N/A":
                        try:
                            date_obj = datetime.strptime(date_modif, "%d/%m/%Y")
                            if date_obj.year == 2025 and date_obj.month in [1, 2]:
                                # Extraction du lien
                                lien = colonnes[7].find_element(By.TAG_NAME, "a").get_attribute("href") if colonnes[7].find_elements(By.TAG_NAME, "a") else "N/A"
                                
                                data.append([region, marque, modele, texte, annee, prix, date_modif, lien])
                        except Exception as e:
                            logging.error(f"Erreur parsing date : {e}")
            except Exception as e:
                logging.error(f"Erreur extraction annonce : {e}")
        
        #============= Sauvegarde CSV ============
        if data:
            df = pd.DataFrame(data, columns=["Région", "Marque", "Modèle", "Texte", "Année", "Prix", "Modifié", "Lien"])
            df.to_csv("annonces_vehicules.csv", index=False, encoding="utf-8")
            return f"{len(data)} annonces filtrées (Janvier et Février 2025) enregistrées."
        else:
            return "Aucune donnée extraite pour janvier et février 2025."

    finally:
        driver.quit()

# ============= TEST DIRECT ============
if __name__ == "__main__":
    # Lancer le scraping
    resultat = scrape_annonces()
    print(resultat)
    
    # Lire le CSV pour vérifier
    try:
        df = pd.read_csv("annonces_vehicules.csv")
        print("\nVoici un aperçu du fichier CSV :\n")
        print(df.head())
    except Exception as e:
        print(f"Erreur lecture CSV : {e}")
