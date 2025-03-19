from fastapi import FastAPI, HTTPException, BackgroundTasks
from typing import List
import asyncio
import logging

# Configuration de base du logging pour obtenir plus de détails en cas d'erreurs
logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

# Liste d'annonces simulée
annonces = []

# Fonction de scraping simulée
async def scraping_data():
    try:
        logging.debug("Début du scraping...")
        await asyncio.sleep(3)  # Simule un délai de scraping
        # Ajout d'une annonce simulée après le délai
        annonces.append({
            "region": "Tunis",
            "marque": "Peugeot",
            "modele": "308",
            "prix": "50000",
            "annee": "2020"
        })
        logging.debug("Scraping terminé avec succès.")
        return "✅ Scraping terminé avec succès."
    except Exception as e:
        logging.error(f"Erreur lors du scraping: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors du scraping: {str(e)}")

# Route POST pour démarrer le scraping
@app.post("/scrape")
async def scrape_data(background_tasks: BackgroundTasks):
    """
    Cette route démarre le scraping en arrière-plan.
    """
    try:
        # Ajout de la tâche de scraping en arrière-plan
        background_tasks.add_task(scraping_data)
        logging.debug("Scraping lancé en arrière-plan.")
        return {"message": "Scraping démarré en arrière-plan."}
    except Exception as e:
        logging.error(f"Erreur dans la route de scraping: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur dans la route de scraping: {str(e)}")

# Route GET pour récupérer les annonces
@app.get("/annonces")
async def get_annonces():
    """
    Cette route permet de récupérer les annonces après un scraping.
    """
    try:
        if annonces:
            return {"annonces": annonces}
        else:
            raise HTTPException(status_code=404, detail="Aucune annonce trouvée")
    except Exception as e:
        logging.error(f"Erreur dans la récupération des annonces: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur dans la récupération des annonces: {str(e)}")

# Route d'état pour vérifier si l'application fonctionne correctement
@app.get("/a")
async def read_root():
    try:
        return {"message": "L'application fonctionne correctement!"}
    except Exception as e:
        logging.error(f"Erreur dans la route de vérification: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur dans la route de vérification: {str(e)}")

