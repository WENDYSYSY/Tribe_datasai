# ═══════════════════════════════════════════════════════════
# DATASAI — Jour 5 : Segmentation client avec K-means de A à Z
# Dataset : Titanic réel (seaborn) — 714 passagers
# datasai.fr
# ═══════════════════════════════════════════════════════════

import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

# ── Dataset ───────────────────────────────────────────────
df = sns.load_dataset('titanic')[['age', 'fare', 'pclass', 'survived']].dropna()
print(f"Dataset : {len(df)} passagers\n")

features = ['age', 'fare', 'pclass']
X        = df[features]


# ── Étape 1 : Standardisation ─────────────────────────────
# Obligatoire avec K-means — met toutes les variables
# sur la même échelle (moyenne=0, écart-type=1)
scaler   = StandardScaler()
X_scaled = scaler.fit_transform(X)
print("Standardisation effectuée")
print(f"Avant : fare de {X['fare'].min():.0f}€ à {X['fare'].max():.0f}€")
print(f"Après : moyenne ≈ 0, écart-type ≈ 1\n")


# ── Étape 2 : Choisir le bon k ────────────────────────────
# Méthode du coude + score silhouette
inertias    = []
silhouettes = []
K_range     = range(2, 9)

for k in K_range:
    km  = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    inertias.append(km.inertia_)
    sil = silhouette_score(X_scaled, km.labels_)
    silhouettes.append(sil)
    print(f"k={k} | Inertie={km.inertia_:>8.1f} | Silhouette={sil:.3f}")

best_k = list(K_range)[silhouettes.index(max(silhouettes))]
print(f"\nMeilleur k : {best_k} (silhouette={max(silhouettes):.3f})\n")


# ── Étape 3 : Entraînement final ──────────────────────────
km_final      = KMeans(n_clusters=best_k, random_state=42, n_init=10)
df['segment'] = km_final.fit_predict(X_scaled)

print(f"Distribution des {best_k} segments :")
for seg, count in df['segment'].value_counts().sort_index().items():
    print(f"  Segment {seg} : {count} passagers ({count/len(df)*100:.1f}%)")


# ── Étape 4 : Analyse des segments ────────────────────────
print(f"\nProfil des segments :")
profil = df.groupby('segment')[features + ['survived']].mean().round(2)
print(profil.to_string())

print(f"\nTaux de survie par segment :")
print(df.groupby('segment')['survived'].mean().round(3).to_string())

print(f"""
Interprétation :
  Segment 0 → Passagers âgés, riches, 1ère classe → 60.8% de survie
  Segment 1 → Passagers jeunes, économiques, 3ème classe → 31.8% de survie

LEÇON : K-means segmente automatiquement selon les patterns dans les données.
Mais c'est vous qui donnez du sens aux clusters.
""")