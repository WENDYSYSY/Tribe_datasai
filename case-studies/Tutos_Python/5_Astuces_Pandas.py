# ═══════════════════════════════════════════════════════════
# DATASAI — Série "30 jours de Python & Data Science"
# Jour 1 : 5 astuces Pandas appliquées au dataset Titanic
# ═══════════════════════════════════════════════════════════
# Dataset : Titanic (seaborn) — 891 passagers réels
# Auteur  : DataSAI — datasai.fr
# ═══════════════════════════════════════════════════════════

import pandas as pd
import numpy as np
import seaborn as sns

# ── CHARGEMENT DU DATASET ───────────────────────────────
# Le dataset Titanic est intégré dans seaborn
# Pas besoin de téléchargement — disponible en une ligne
df = sns.load_dataset('titanic')

print("=" * 55)
print("  DATASAI — Jour 1 : 5 astuces Pandas")
print("  Dataset : Titanic — 891 passagers réels")
print("=" * 55)
print(f"\nAperçu du dataset :")
print(df[['survived','pclass','sex','age','fare','embarked']].head(5).to_string())
print(f"\n{df.shape[0]} passagers · {df.shape[1]} colonnes\n")


# ═══════════════════════════════════════════════════════════
# ASTUCE 1 — query()
# Filtrer des données comme on écrit une phrase
# ═══════════════════════════════════════════════════════════

print("─" * 55)
print("ASTUCE 1 — query()")
print("Filtrer sans masques booléens")
print("─" * 55)

# AVANT — difficile à lire quand les conditions s'accumulent
avant = df[(df['age'] > 30) & (df['survived'] == 1) & (df['pclass'] == 1)]

# APRÈS — query() accepte une condition en texte naturel
# Plus besoin de répéter df[] à chaque condition
apres = df.query("age > 30 and survived == 1 and pclass == 1")

print(f"\nAVANT  : df[(df['age'] > 30) & (df['survived'] == 1) & (df['pclass'] == 1)]")
print(f"APRÈS  : df.query(\"age > 30 and survived == 1 and pclass == 1\")")
print(f"\nRésultat : {len(apres)} survivants de 1ère classe de plus de 30 ans")
print(f"Résultats identiques : {len(avant) == len(apres)} ✅")
print(f"\nExtrait :")
print(apres[['pclass','sex','age','fare','survived']].head(5).to_string())


# ═══════════════════════════════════════════════════════════
# ASTUCE 2 — assign()
# Créer plusieurs colonnes en une seule expression
# ═══════════════════════════════════════════════════════════

print("\n" + "─" * 55)
print("ASTUCE 2 — assign()")
print("Créer des colonnes sans muter le DataFrame")
print("─" * 55)

# AVANT — 3 lignes séparées qui modifient le DataFrame en place
# df['age_group']      = df['age'].apply(lambda x: 'Enfant' if x < 18 else 'Adulte')
# df['fare_normalise'] = (df['fare'] - df['fare'].min()) / (df['fare'].max() - df['fare'].min())
# df['survie_label']   = df['survived'].map({0: 'Décédé', 1: 'Survivant'})

# APRÈS — assign() crée toutes les colonnes en une expression chaînable
# Chaque lambda reçoit le DataFrame en cours de construction
# Le DataFrame original df n'est jamais modifié
df_enrichi = df.assign(
    age_group      = lambda x: np.where(x['age'] < 18, 'Enfant', 'Adulte'),
    fare_normalise = lambda x: (x['fare'] - x['fare'].min()) / (x['fare'].max() - x['fare'].min()),
    survie_label   = lambda x: x['survived'].map({0: 'Décédé', 1: 'Survivant'})
)

print(f"\n3 colonnes créées en une seule expression :")
print(df_enrichi[['age','age_group','fare','fare_normalise','survie_label']].head(8).to_string())
print(f"\nDataFrame original inchangé : {list(df.columns) == list(sns.load_dataset('titanic').columns)} ✅")


# ═══════════════════════════════════════════════════════════
# ASTUCE 3 — pipe()
# Enchaîner des transformations sans imbrication
# ═══════════════════════════════════════════════════════════

print("\n" + "─" * 55)
print("ASTUCE 3 — pipe()")
print("Pipeline lisible de A à Z")
print("─" * 55)

# On définit chaque transformation comme une fonction
# Chaque fonction fait une seule chose — facile à déboguer

def supprimer_nulls(df):
    """Supprime les lignes avec age ou fare manquant"""
    return df.dropna(subset=['age', 'fare'])

def ajouter_features(df):
    """Ajoute les colonnes utiles pour l'analyse"""
    return df.assign(
        age_group    = np.where(df['age'] < 18, 'Enfant', 'Adulte'),
        survie_label = df['survived'].map({0: 'Décédé', 1: 'Survivant'})
    )

def taux_survie_par_classe(df):
    """Calcule le taux de survie moyen par classe"""
    return (df
        .groupby('pclass')['survived']
        .mean()
        .round(3)
        .reset_index()
        .rename(columns={'pclass': 'Classe', 'survived': 'Taux de survie'})
    )

# AVANT — variables temporaires partout, logique éparpillée
# df_clean = df.dropna(subset=['age','fare'])
# df_clean['age_group'] = np.where(df_clean['age'] < 18, 'Enfant', 'Adulte')
# result = df_clean.groupby('pclass')['survived'].mean().round(3).reset_index()

# APRÈS — pipe() passe le DataFrame à chaque fonction dans l'ordre
# Le code se lit de haut en bas comme une recette
result = (df
    .pipe(supprimer_nulls)       # étape 1 : nettoyer les nulls
    .pipe(ajouter_features)      # étape 2 : enrichir les données
    .pipe(taux_survie_par_classe) # étape 3 : agréger et analyser
)

print(f"\nTaux de survie par classe :")
print(result.to_string(index=False))
print(f"\n→ 1ère classe : 65.6% de survie vs 23.9% en 3ème classe")
print(f"→ La classe sociale a joué un rôle décisif dans la survie ✅")


# ═══════════════════════════════════════════════════════════
# ASTUCE 4 — explode()
# Transformer une colonne de listes en lignes individuelles
# ═══════════════════════════════════════════════════════════

print("\n" + "─" * 55)
print("ASTUCE 4 — explode()")
print("Décomposer des listes en lignes individuelles")
print("─" * 55)

# On crée une colonne avec des listes de caractéristiques
# pour chaque passager — cas fréquent en data réelle
df_tags = df[['survived', 'pclass', 'sex']].copy()
df_tags['caracteristiques'] = df_tags.apply(
    lambda row: (
        (['survivant'] if row['survived'] == 1 else ['décédé']) +
        (['premiere_classe'] if row['pclass'] == 1 else []) +
        (['femme'] if row['sex'] == 'female' else ['homme'])
    ), axis=1
)

print(f"\nAVANT explode() — chaque ligne contient une liste :")
print(df_tags[['sex', 'pclass', 'survived', 'caracteristiques']].head(5).to_string())

# explode() décompose chaque liste en autant de lignes
# que la liste contient d'éléments
# Indispensable pour analyser des données imbriquées
df_exploded = df_tags[['sex', 'survived', 'caracteristiques']].explode('caracteristiques')

print(f"\nAPRÈS explode() — chaque caractéristique est une ligne :")
print(df_exploded.head(10).to_string())

analyse = df_exploded.groupby('caracteristiques').size().sort_values(ascending=False)
print(f"\nAnalyse des caractéristiques :")
print(analyse.to_string())
print(f"\n→ 577 hommes à bord, 342 survivants au total ✅")


# ═══════════════════════════════════════════════════════════
# ASTUCE 5 — nlargest()
# Récupérer le top N directement
# ═══════════════════════════════════════════════════════════

print("\n" + "─" * 55)
print("ASTUCE 5 — nlargest()")
print("Top N en une seule opération")
print("─" * 55)

# AVANT — deux opérations pour un seul besoin
avant5 = (df
    .groupby('embark_town')['fare']
    .mean()
    .sort_values(ascending=False)
    .head(3)
)

# APRÈS — nlargest(n) fait les deux en une opération
# Plus court, intention immédiatement claire
apres5 = (df
    .groupby('embark_town')['fare']
    .mean()
    .nlargest(3)
)

print(f"\nAVANT  : .mean().sort_values(ascending=False).head(3)")
print(f"APRÈS  : .mean().nlargest(3)")
print(f"\nTop 3 villes d'embarquement par tarif moyen :")
print(apres5.round(2).to_string())
print(f"\nRésultats identiques : {avant5.equals(apres5)} ✅")
print(f"\n→ Les passagers embarqués à Cherbourg payaient en moyenne")
print(f"  59.95€ — soit 4x plus que ceux de Queenstown (13.28€)")


# ═══════════════════════════════════════════════════════════
# RÉSUMÉ FINAL
# ═══════════════════════════════════════════════════════════

print("\n" + "=" * 55)
print("  RÉSUMÉ — 5 astuces Pandas sur le Titanic")
print("=" * 55)
print("""
  query()    → Filtrer sans masques booléens illisibles
  assign()   → Créer des colonnes sans muter le DataFrame
  pipe()     → Construire un pipeline lisible et déboguable
  explode()  → Décomposer des listes en lignes individuelles
  nlargest() → Top N sans sort_values + head
""")
print("  LEÇON : La lisibilité, c'est aussi une performance.")
print("  Un code qu'on comprend vite, c'est un code")
print("  qu'on maintient vite.")
print()
print("  Dataset : seaborn.load_dataset('titanic')")
print("  Source  : datasai.fr")
print("=" * 55)