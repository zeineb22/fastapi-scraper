from fastapi import FastAPI, HTTPException
import pandas as pd
from scraper import scrape_annonces
import os

app = FastAPI()

# Endpoint pour récupérer toutes les annonces
from fastapi import FastAPI, HTTPException
import pandas as pd
from scraper import scrape_annonces
import os

app = FastAPI()

# Endpoint pour récupérer toutes les annonces
@app.get("/annonces")
def get_annonces():
    try:
        # Vérifiez si le fichier existe
        if not os.path.exists("annonces_vehicules.csv"):
            raise HTTPException(status_code=404, detail="Aucune donnée disponible. Veuillez lancer le scraping d'abord.")

        # Lire les annonces depuis le fichier CSV
        df = pd.read_csv("annonces_vehicules.csv")

        # Vérifiez si le fichier est vide
        if df.empty:
            raise HTTPException(status_code=404, detail="Aucune donnée disponible. Veuillez lancer le scraping d'abord.")

        # Convertir le DataFrame en JSON
        return df.to_dict(orient="records")
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=500, detail="Le fichier CSV est vide ou mal formaté.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la lecture du fichier CSV : {str(e)}")


# Endpoint pour lancer une nouvelle session de scraping
@app.post("/scrape")
def scrape():
    try:
        # Lancer le scraping
        data = scrape_annonces()
        return {"message": "Scraping terminé avec succès", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
