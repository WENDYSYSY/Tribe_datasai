# ═══════════════════════════════════════════════════════════
# DATASAI — Semaine 2, Jour 4
# BigQuery — Requêter des données sur le Cloud
# Dataset : NYC Citi Bike Trips — 58+ millions de trajets réels
# Source  : cloud.google.com/bigquery/docs
# datasai.fr
# ═══════════════════════════════════════════════════════════

# ── Installation (dans le terminal PowerShell) ────────────
# pip install google-cloud-bigquery pandas

# ── Authentification (dans le terminal PowerShell) ────────
# gcloud auth application-default login --no-browser
# → Suivre les instructions dans le terminal
# → Se connecter avec le compte Google Cloud

# ── Imports ───────────────────────────────────────────────
from google.cloud import bigquery  # librairie BigQuery officielle Google
import pandas as pd                # pour afficher les résultats en tableau
import time                        # pour mesurer la durée de chaque requête

# ── Connexion à BigQuery ──────────────────────────────────
# bigquery.Client() crée une connexion à BigQuery
# project = ton ID de projet Google Cloud
# Les credentials viennent de gcloud auth application-default login
client = bigquery.Client(project="gen-lang-client-0080670010")

print("=" * 55)
print("  DATASAI — BigQuery : NYC Citi Bike Trips")
print("  58+ millions de trajets réels depuis 2013")
print("=" * 55)


# ═══════════════════════════════════════════════════════════
# REQUÊTE 1 — Aperçu des données
# ═══════════════════════════════════════════════════════════
# SELECT * = sélectionner toutes les colonnes
# LIMIT 100 = afficher seulement 100 lignes
# Sans LIMIT → BigQuery scanne toute la table → coût élevé
# Les backticks `` sont obligatoires autour du nom de table
# Syntaxe BigQuery : `projet.dataset.table`

print("\n" + "─" * 55)
print("REQUÊTE 1 — Aperçu des données")
print("─" * 55)

t0 = time.time()

q1 = """
SELECT *
FROM `bigquery-public-data.new_york_citibike.citibike_trips`
LIMIT 100
"""

# client.query() envoie la requête à BigQuery
# .to_dataframe() convertit les résultats en DataFrame Pandas
df1 = client.query(q1).to_dataframe()

print(f"⏱ Durée : {time.time()-t0:.2f}s | {len(df1)} lignes retournées")
print(f"Colonnes disponibles : {list(df1.columns)}")
print(df1.head(5).to_string(index=False))


# ═══════════════════════════════════════════════════════════
# REQUÊTE 2 — Filtrer les valeurs NULL
# ═══════════════════════════════════════════════════════════
# WHERE tripduration IS NOT NULL
# → exclure les lignes où tripduration est vide
# En data réelle, les valeurs manquantes sont très fréquentes
# Il faut toujours les gérer avant l'analyse

print("\n" + "─" * 55)
print("REQUÊTE 2 — Sans valeurs NULL sur tripduration")
print("─" * 55)

t0 = time.time()

q2 = """
SELECT *
FROM `bigquery-public-data.new_york_citibike.citibike_trips`
WHERE tripduration IS NOT NULL
LIMIT 100
"""

df2 = client.query(q2).to_dataframe()

print(f"⏱ Durée : {time.time()-t0:.2f}s | {len(df2)} lignes retournées")
print(df2.head(5).to_string(index=False))


# ═══════════════════════════════════════════════════════════
# REQUÊTE 3 — Sélectionner uniquement les colonnes utiles
# ═══════════════════════════════════════════════════════════
# Bonne pratique BigQuery : ne jamais faire SELECT * en production
# BigQuery facture par données scannées
# Sélectionner seulement les colonnes nécessaires = moins cher + plus rapide
# Ici on sélectionne 5 colonnes au lieu de toutes

print("\n" + "─" * 55)
print("REQUÊTE 3 — Colonnes utiles uniquement")
print("─" * 55)

t0 = time.time()

q3 = """
SELECT
  tripduration,          -- durée du trajet en secondes
  starttime,             -- heure de départ
  start_station_name,    -- station de départ
  end_station_name,      -- station d'arrivée
  usertype               -- type : Subscriber ou Customer
FROM `bigquery-public-data.new_york_citibike.citibike_trips`
WHERE tripduration IS NOT NULL
AND   start_station_name IS NOT NULL
AND   starttime IS NOT NULL
LIMIT 100
"""

df3 = client.query(q3).to_dataframe()

print(f"⏱ Durée : {time.time()-t0:.2f}s | {len(df3)} lignes retournées")
print(df3.head(10).to_string(index=False))


# ═══════════════════════════════════════════════════════════
# REQUÊTE 4 — Compter le nombre total de trajets
# ═══════════════════════════════════════════════════════════
# COUNT(*) = compter toutes les lignes de la table
# AS total_trajets = donner un nom lisible à la colonne résultat
# Cette requête scanne toute la table
# Mais BigQuery ne lit qu'une seule colonne → rapide et peu coûteux

print("\n" + "─" * 55)
print("REQUÊTE 4 — Nombre total de trajets")
print("─" * 55)

t0 = time.time()

q4 = """
SELECT
  COUNT(*) AS total_trajets
FROM `bigquery-public-data.new_york_citibike.citibike_trips`
"""

df4 = client.query(q4).to_dataframe()

print(f"⏱ Durée : {time.time()-t0:.2f}s")
print(f"Total trajets : {df4['total_trajets'][0]:,}")
# :, = format avec séparateurs de milliers pour lisibilité


# ═══════════════════════════════════════════════════════════
# REQUÊTE 5 — Top 100 stations les plus populaires
# ═══════════════════════════════════════════════════════════
# GROUP BY = regrouper les lignes par valeur unique de la colonne
# COUNT(*) = compter les trajets dans chaque groupe
# ORDER BY ... DESC = trier du plus grand au plus petit
# DESC = descendant (du plus grand au plus petit)
# ASC  = ascendant  (du plus petit au plus grand)

print("\n" + "─" * 55)
print("REQUÊTE 5 — Top 100 stations les plus populaires")
print("─" * 55)

t0 = time.time()

q5 = """
SELECT
  start_station_name,
  COUNT(*) AS nombre_trajets
FROM `bigquery-public-data.new_york_citibike.citibike_trips`
WHERE start_station_name IS NOT NULL
GROUP BY start_station_name
ORDER BY nombre_trajets DESC
LIMIT 100
"""

df5 = client.query(q5).to_dataframe()

print(f"⏱ Durée : {time.time()-t0:.2f}s | {len(df5)} stations")
print(f"\nTop 10 stations :")
print(df5.head(10).to_string(index=False))
print(f"\nStation #1 : {df5.iloc[0]['start_station_name']}")
print(f"Trajets    : {df5.iloc[0]['nombre_trajets']:,}")


# ═══════════════════════════════════════════════════════════
# REQUÊTE 6 — Durée moyenne par type d'utilisateur
# ═══════════════════════════════════════════════════════════
# AVG() = calcule la moyenne d'une colonne numérique
# tripduration est en secondes → on divise par 60 pour avoir des minutes
# ROUND(valeur, 1) = arrondir à 1 décimale
# Subscriber = abonné annuel (utilise le vélo pour commuter)
# Customer   = client ponctuel (touriste, utilisation occasionnelle)

print("\n" + "─" * 55)
print("REQUÊTE 6 — Durée moyenne par type d'utilisateur")
print("─" * 55)

t0 = time.time()

q6 = """
SELECT
  usertype,
  ROUND(AVG(tripduration)/60, 1) AS duree_moy_minutes,
  COUNT(*) AS nombre_trajets
FROM `bigquery-public-data.new_york_citibike.citibike_trips`
WHERE tripduration > 0
AND   usertype IS NOT NULL
GROUP BY usertype
ORDER BY duree_moy_minutes DESC
"""

df6 = client.query(q6).to_dataframe()

print(f"⏱ Durée : {time.time()-t0:.2f}s")
print(df6.to_string(index=False))
print(f"\n→ Interprétation :")
print(f"  Subscriber = abonnés annuels → trajets courts (commute)")
print(f"  Customer   = clients ponctuels → trajets plus longs (touristes)")


# ═══════════════════════════════════════════════════════════
# REQUÊTE 7 — Évolution mensuelle des trajets
# ═══════════════════════════════════════════════════════════
# EXTRACT() = extraire une partie d'une date
# YEAR  = extraire l'année
# MONTH = extraire le mois (1 à 12)
# GROUP BY annee, month = regrouper par année ET mois
# ORDER BY annee, month DESC = trier par année puis mois décroissant
# Cette requête révèle la saisonnalité : plus de trajets en été

print("\n" + "─" * 55)
print("REQUÊTE 7 — Évolution mensuelle des trajets")
print("─" * 55)

t0 = time.time()

q7 = """
SELECT
  EXTRACT(YEAR FROM starttime)  AS annee,
  EXTRACT(MONTH FROM starttime) AS month,
  COUNT(*) AS nombre_trajets
FROM `bigquery-public-data.new_york_citibike.citibike_trips`
WHERE starttime IS NOT NULL
GROUP BY annee, month
ORDER BY annee, month DESC
"""

df7 = client.query(q7).to_dataframe()

print(f"⏱ Durée : {time.time()-t0:.2f}s | {len(df7)} mois de données")
print(f"\n10 dernières périodes :")
print(df7.head(10).to_string(index=False))
print(f"\n→ La saisonnalité est visible :")
print(f"  Été (juin-août) → pic d'utilisation")
print(f"  Hiver (jan-fév) → creux d'utilisation")


# ═══════════════════════════════════════════════════════════
# RÉSUMÉ FINAL
# ═══════════════════════════════════════════════════════════

print("\n" + "=" * 55)
print("  RÉSUMÉ — 7 requêtes BigQuery sur NYC Citi Bike")
print("=" * 55)
print("""
  R1 → SELECT * LIMIT 100          : aperçu des données
  R2 → WHERE IS NOT NULL            : filtrer les valeurs manquantes
  R3 → SELECT colonnes spécifiques  : optimiser les coûts
  R4 → COUNT(*)                     : compter les lignes
  R5 → GROUP BY + ORDER BY          : top stations populaires
  R6 → AVG() + GROUP BY             : moyenne par catégorie
  R7 → EXTRACT() + GROUP BY         : analyse temporelle

  LEÇON : BigQuery = SQL sur le Cloud.
  58 millions de lignes interrogées en quelques secondes.
  Premier 1 To par mois gratuit.
  datasai.fr
""")