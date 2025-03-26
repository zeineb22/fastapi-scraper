from fastapi import FastAPI, HTTPException
import pandas as pd
from scraper import scrape_annonces
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Autoriser CORS pour tests frontend éventuels
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== GET ====================
@app.get("/annonces")
def get_annonces():
    try:
        if not os.path.exists("annonces_vehicules.csv"):
            raise HTTPException(status_code=404, detail="Aucune donnée disponible. Lancez d'abord le scraping.")

        df = pd.read_csv("annonces_vehicules.csv")

        if df.empty:
            raise HTTPException(status_code=404, detail="Fichier vide.")

        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la lecture du CSV : {str(e)}")

# ==================== POST ====================
@app.post("/scrape")
def scrape():
    try:
        data = scrape_annonces()
        return {"message": "Scraping terminé avec succès", "details": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== Lancer le serveur ====================
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
