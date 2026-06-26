# ═══════════════════════════════════════════════════════════
# DATASAI — Jour 4 : Détecter les valeurs aberrantes
#           4 méthodes comparées sur le dataset Titanic
# Dataset : Titanic réel (seaborn) + outliers injectés
# datasai.fr
# ═══════════════════════════════════════════════════════════

import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.ensemble import IsolationForest
from scipy import stats

# ── Dataset ───────────────────────────────────────────────
df = sns.load_dataset('titanic')[['fare', 'age', 'pclass']].dropna()

# Injection de 5 outliers contrôlés
np.random.seed(42)
outliers_injectes = pd.DataFrame({
    'fare':   [800.0, 950.0, 1200.0, -50.0, 2500.0],
    'age':    [35.0,  42.0,  28.0,   55.0,  30.0],
    'pclass': [1,     1,     1,      3,     1]
})
df = pd.concat([df, outliers_injectes], ignore_index=True)
print(f"Dataset : {len(df)} passagers | fare : {df['fare'].min():.2f}€ → {df['fare'].max():.2f}€\n")


# ── Méthode 1 : IQR ───────────────────────────────────────
Q1    = df['fare'].quantile(0.25)
Q3    = df['fare'].quantile(0.75)
IQR   = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
outliers_iqr = df[(df['fare'] < lower) | (df['fare'] > upper)]
print(f"IQR         : {len(outliers_iqr):>3} outliers | [{lower:.2f}€ ; {upper:.2f}€]")


# ── Méthode 2 : Z-score ───────────────────────────────────
z_scores   = np.abs(stats.zscore(df['fare']))
outliers_z = df[z_scores > 3]
print(f"Z-score     : {len(outliers_z):>3} outliers (Z > 3)")


# ── Méthode 3 : Percentiles ───────────────────────────────
p01        = df['fare'].quantile(0.01)
p99        = df['fare'].quantile(0.99)
outliers_p = df[(df['fare'] < p01) | (df['fare'] > p99)]
print(f"Percentiles : {len(outliers_p):>3} outliers ([{p01:.2f}€ ; {p99:.2f}€])")


# ── Méthode 4 : Isolation Forest ──────────────────────────
iso          = IsolationForest(contamination=0.05, random_state=42)
df['anomalie'] = iso.fit_predict(df[['fare', 'age']])
outliers_iso = df[df['anomalie'] == -1]
print(f"Iso Forest  : {len(outliers_iso):>3} outliers (multi-dim : fare + age)")


# ── Comparaison ───────────────────────────────────────────
print(f"""
┌─────────────────────┬──────────┬───────────────────────────────┐
│ Méthode             │ Outliers │ Quand l'utiliser              │
├─────────────────────┼──────────┼───────────────────────────────┤
│ IQR                 │  {len(outliers_iqr):>5}   │ Distribution asymétrique      │
│ Z-score             │  {len(outliers_z):>5}   │ Distribution normale          │
│ Percentiles         │  {len(outliers_p):>5}   │ Seuils métier ajustables      │
│ Isolation Forest    │  {len(outliers_iso):>5}   │ Données multi-dimensionnelles │
└─────────────────────┴──────────┴───────────────────────────────┘

LEÇON : Commence par visualiser. Puis confirme avec une méthode statistique.
""")