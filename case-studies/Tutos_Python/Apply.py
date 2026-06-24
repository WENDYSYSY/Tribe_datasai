# ═══════════════════════════════════════════════════════════
# DATASAI — Jour 3 : apply() vs vectorisation — benchmark réel
# Dataset : 500 000 lignes + Titanic (seaborn)
# datasai.fr
# ═══════════════════════════════════════════════════════════

import pandas as pd
import numpy as np
import seaborn as sns
import time

# ── Datasets ──────────────────────────────────────────────
np.random.seed(42)
n = 500_000
df = pd.DataFrame({
    'age':       np.random.randint(18, 80, n),
    'salaire':   np.random.uniform(20000, 120000, n),
    'score':     np.random.uniform(0, 100, n),
    'categorie': np.random.choice(['A', 'B', 'C'], n),
})
titanic = sns.load_dataset('titanic')

def bench(label, func):
    t0 = time.time()
    result = func()
    ms = (time.time() - t0) * 1000
    print(f"  {label:<40} {ms:>8.1f} ms")
    return result, ms

print(f"Dataset : {n:,} lignes\n")


# ── CAS 1 : Catégoriser l'âge ─────────────────────────────
print("CAS 1 — Catégoriser l'âge en tranches")

# AVANT
r1, t1 = bench("apply() + lambda",
    lambda: df['age'].apply(
        lambda x: 'Jeune' if x < 30 else 'Adulte' if x < 60 else 'Senior'))

# APRÈS — np.select() évalue toutes les lignes d'un coup
r2, t2 = bench("np.select()",
    lambda: np.select(
        [df['age'] < 30, df['age'] < 60],
        ['Jeune', 'Adulte'],
        default='Senior'))

print(f"  → {t1/t2:.0f}x plus rapide | Identiques : {(r1==r2).all()}")


# ── CAS 2 : Bonus conditionnel ────────────────────────────
print("\nCAS 2 — Bonus conditionnel selon catégorie")

# AVANT — apply() axis=1 : le plus lent de tous
r3, t3 = bench("apply() row-wise (axis=1)",
    lambda: df.apply(
        lambda row: row['salaire'] * 0.15 if row['categorie'] == 'A'
        else row['salaire'] * 0.10 if row['categorie'] == 'B'
        else row['salaire'] * 0.05, axis=1))

# APRÈS — np.where() chaîné
r4, t4 = bench("np.where() chaîné",
    lambda: np.where(df['categorie'] == 'A', df['salaire'] * 0.15,
             np.where(df['categorie'] == 'B', df['salaire'] * 0.10,
                      df['salaire'] * 0.05)))

print(f"  → {t3/t4:.0f}x plus rapide | {t3/1000:.1f}s → {t4/1000:.2f}s")


# ── CAS 3 : Normalisation ─────────────────────────────────
print("\nCAS 3 — Normaliser un score entre 0 et 1")

mn, mx = df['score'].min(), df['score'].max()

# AVANT
r5, t5 = bench("apply() + lambda",
    lambda: df['score'].apply(lambda x: (x - mn) / (mx - mn)))

# APRÈS — vectorisation pure
r6, t6 = bench("Vectorisation pure",
    lambda: (df['score'] - mn) / (mx - mn))

print(f"  → {t5/t6:.0f}x plus rapide")


# ── CAS 4 : Titanic — map() ───────────────────────────────
print("\nCAS 4 — Titanic : map() pour les valeurs fixes")

# AVANT
titanic['survie_apply'] = titanic['survived'].apply(
    lambda x: 'Survivant' if x == 1 else 'Décédé')

# APRÈS — map() est fait pour ça
titanic['survie_map'] = titanic['survived'].map({1: 'Survivant', 0: 'Décédé'})

print(titanic[['pclass', 'sex', 'age', 'survived', 'survie_map']].head(8).to_string())
print(f"\nDistribution :\n{titanic['survie_map'].value_counts().to_string()}")


# ── Résumé ────────────────────────────────────────────────
print(f"""
RÉSUMÉ — Tableau de décision :

  Conditions multiples        → np.select()
  Condition simple (si/sinon) → np.where()
  Calcul numérique            → Vectorisation directe
  Mapper des valeurs fixes    → .map()
  Remplacer des valeurs       → .replace()
  Logique très complexe       → apply() — dernier recours

LEÇON : apply() est pratique mais coûteux.
Sur 500K lignes, np.where() est {t3/t4:.0f}x plus rapide.
Vectorisez toujours. apply() en dernier recours.
""")