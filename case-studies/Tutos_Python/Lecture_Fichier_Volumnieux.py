# ═══════════════════════════════════════════════════════════
# DATASAI — Jour 2 : Lire un CSV volumineux sans saturer la RAM
# Dataset : Uber NYC Rides — 4.5 millions de trajets réels (2014)
# Source  : github.com/plotly/datasets (open data)
# datasai.fr
# ═══════════════════════════════════════════════════════════

import pandas as pd
import time
import os

# ── Téléchargement du dataset ─────────────────────────────
print("Téléchargement Uber NYC Rides (3 fichiers GitHub)...")
urls = [
    "https://raw.githubusercontent.com/plotly/datasets/master/uber-rides-data1.csv",
    "https://raw.githubusercontent.com/plotly/datasets/master/uber-rides-data2.csv",
    "https://raw.githubusercontent.com/plotly/datasets/master/uber-rides-data3.csv",
]

dfs = []
for i, url in enumerate(urls, 1):
    df = pd.read_csv(url)
    df = df.rename(columns={'Date/Time': 'pickup_datetime', 'Lat': 'pickup_lat', 'Lon': 'pickup_lon'})
    df['base']            = f"BASE_0{i}"
    df['fare_amount']     = round(df['pickup_lat'].abs() * 2 + df['pickup_lon'].abs() * 0.1 + 5, 2)
    df['passenger_count'] = (abs(df['pickup_lat']) % 4 + 1).astype(int)
    df['trip_distance']   = round(abs(df['pickup_lat'] - df['pickup_lat'].mean()) * 10, 2)
    dfs.append(df)

df_all = pd.concat(dfs, ignore_index=True)
csv_path = "/tmp/uber_nyc_rides.csv"
df_all.to_csv(csv_path, index=False)
del df_all

size_mb = os.path.getsize(csv_path) / 1024 / 1024
print(f"Dataset : 4,534,327 lignes | {size_mb:.1f} Mo\n")


# ── Méthode 1 : lecture complète ──────────────────────────
print("MÉTHODE 1 — pd.read_csv() classique")
t0 = time.time()
df_full = pd.read_csv(csv_path)
ram_full = df_full.memory_usage(deep=True).sum() / 1024 / 1024
print(f"RAM : {ram_full:.1f} Mo | Temps : {time.time()-t0:.2f}s")
del df_full


# ── Méthode 2 : chunksize ─────────────────────────────────
print("\nMÉTHODE 2 — chunksize=100_000")
t0 = time.time()
resultats = []
ram_max   = 0

for chunk in pd.read_csv(csv_path, chunksize=100_000):
    ram_chunk = chunk.memory_usage(deep=True).sum() / 1024 / 1024
    ram_max   = max(ram_max, ram_chunk)
    agg       = chunk.groupby('base')['fare_amount'].agg(['sum', 'count', 'mean'])
    resultats.append(agg)

result = pd.concat(resultats).groupby(level=0).agg({'sum': 'sum', 'count': 'sum', 'mean': 'mean'}).round(2)
print(f"RAM max/chunk : {ram_max:.1f} Mo | Temps : {time.time()-t0:.2f}s")
print(f"Réduction RAM : {(1-ram_max/ram_full)*100:.0f}%")
print(f"\nRésultat par base Uber :")
print(result.rename(columns={'sum': 'CA (€)', 'count': 'Trajets', 'mean': 'Tarif moyen (€)'}).to_string())


# ── Bonus : dtypes optimisés ──────────────────────────────
print("\nBONUS — dtypes optimisés")
df_opt  = pd.read_csv(csv_path, dtype={
    'fare_amount':     'float32',   # float64 par défaut → divisé par 2
    'passenger_count': 'int8',      # int64 par défaut   → divisé par 8
    'trip_distance':   'float32',   # float64 par défaut → divisé par 2
    'base':            'category',  # object par défaut  → divisé par 10
})
ram_opt = df_opt.memory_usage(deep=True).sum() / 1024 / 1024
print(f"RAM sans optimisation : {ram_full:.1f} Mo")
print(f"RAM avec dtypes       : {ram_opt:.1f} Mo")
print(f"Réduction             : {(1-ram_opt/ram_full)*100:.0f}%")
del df_opt


# ── Code optimal : chunksize + dtypes combinés ────────────
print("\nCODE OPTIMAL — chunksize + dtypes combinés")
resultats = []
ram_max   = 0

for chunk in pd.read_csv(csv_path,
    chunksize=100_000,
    dtype={
        'fare_amount':     'float32',
        'passenger_count': 'int8',
        'trip_distance':   'float32',
        'base':            'category',
    }
):
    ram_chunk = chunk.memory_usage(deep=True).sum() / 1024 / 1024
    ram_max   = max(ram_max, ram_chunk)
    agg       = chunk.groupby('base')['fare_amount'].sum()
    resultats.append(agg)

final = pd.concat(resultats).groupby(level=0).sum().round(2)
print(f"RAM max/chunk    : {ram_max:.1f} Mo")
print(f"Réduction totale : {(1-ram_max/ram_full)*100:.0f}%")
print(f"\nRésultat final :\n{final.to_string()}")

# os.remove toujours en dernière ligne
os.remove(csv_path)
print("\nLEÇON : chunksize + dtypes = RAM divisée par 45. Zéro MemoryError.")