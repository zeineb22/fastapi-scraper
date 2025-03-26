import pandas as pd
import dash
from dash import html, dcc
import plotly.express as px

# ==================== Charger les données ====================

# Lire les données depuis le CSV
df = pd.read_csv('annonces_vehicules.csv')

# Convertir les prix en numériques
df['Prix'] = pd.to_numeric(df['Prix'], errors='coerce')

# Convertir la date
df['Date'] = pd.to_datetime(df['Modifié'], format='%d/%m/%Y', errors='coerce')

# Ajouter le mois pour analyse
df['Mois'] = df['Date'].dt.month_name()

# ==================== Créer l'application Dash ====================

app = dash.Dash(__name__)
app.title = "Tableau de Bord Annonces"

# ==================== Graphiques ====================

# 1. Répartition des annonces par région
fig_region = px.pie(df, names='Région', title='Répartition des annonces par région')

# 2. Répartition des annonces par marque
df_marque = df['Marque'].value_counts().reset_index()
df_marque.columns = ['Marque', 'Nombre']

fig_marque = px.bar(df_marque,
                    x='Marque', y='Nombre',
                    labels={'Marque': 'Marque', 'Nombre': 'Nombre d\'annonces'},
                    title='Nombre d\'annonces par marque')

# 3. Histogramme des prix
fig_prix = px.histogram(df, x='Prix', nbins=10, title='Distribution des prix')

# 4. Nombre d'annonces par mois
df_mois = df['Mois'].value_counts().reset_index()
df_mois.columns = ['Mois', 'Nombre']

fig_mois = px.bar(df_mois,
                  x='Mois', y='Nombre',
                  labels={'Mois': 'Mois', 'Nombre': 'Nombre d\'annonces'},
                  title='Nombre d\'annonces par mois')

# ==================== Layout ====================

app.layout = html.Div(children=[
    html.H1(children='Tableau de Bord des Annonces de Véhicules', style={'textAlign': 'center'}),

    html.Div(children=[
        dcc.Graph(figure=fig_region),
        dcc.Graph(figure=fig_marque),
        dcc.Graph(figure=fig_prix),
        dcc.Graph(figure=fig_mois),
    ])
])

# ==================== Lancer le serveur ====================

if __name__ == '__main__':
    app.run(debug=True)
