# ═══════════════════════════════════════════════════════════
# DATASAI — Jour 6 : Prédire le churn client avec Random Forest
# Dataset : IBM Telco Customer Churn — 7 043 clients réels
# Source  : github.com/IBM/telco-customer-churn-on-icp4d
# datasai.fr
# ═══════════════════════════════════════════════════════════

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.preprocessing import LabelEncoder

# ── Chargement ────────────────────────────────────────────
url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
df  = pd.read_csv(url)
print(f"Dataset : {len(df)} clients | Churn : {(df['Churn']=='Yes').mean()*100:.1f}%\n")

# ── Nettoyage ─────────────────────────────────────────────
# TotalCharges contient des espaces → conversion en float
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df = df.dropna().drop('customerID', axis=1)
print(f"Après nettoyage : {len(df)} clients\n")

# ── Encodage ──────────────────────────────────────────────
features_cat = ['gender','Partner','Dependents','PhoneService','MultipleLines',
                'InternetService','OnlineSecurity','OnlineBackup','DeviceProtection',
                'TechSupport','StreamingTV','StreamingMovies','Contract',
                'PaperlessBilling','PaymentMethod']
features_num = ['SeniorCitizen','tenure','MonthlyCharges','TotalCharges']

le = LabelEncoder()
for col in features_cat:
    df[col] = le.fit_transform(df[col].astype(str))
df['Churn'] = (df['Churn'] == 'Yes').astype(int)

features = features_num + features_cat
X = df[features]
y = df['Churn']

# ── Train / Test Split ────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
print(f"Entraînement : {len(X_train)} | Test : {len(X_test)}\n")

# ── Entraînement ──────────────────────────────────────────
# class_weight='balanced' crucial sur données déséquilibrées
# 73.5% fidèles vs 26.5% churners
rf = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight='balanced'
)
rf.fit(X_train, y_train)

# ── Évaluation ────────────────────────────────────────────
y_pred  = rf.predict(X_test)
y_proba = rf.predict_proba(X_test)[:,1]
print("Résultats :")
print(classification_report(y_test, y_pred, target_names=['Fidèle','Churner']))
print(f"AUC-ROC : {roc_auc_score(y_test, y_proba):.3f}\n")

# ── Feature Importance ────────────────────────────────────
importances = pd.Series(
    rf.feature_importances_, index=features
).sort_values(ascending=False)
print("Top 8 features :")
for feat, imp in importances.head(8).items():
    print(f"  {feat:<20} {imp:.3f}  {'█'*int(imp*50)}")

# ── Prédictions ───────────────────────────────────────────
print("\nExemples de prédictions :")

# Client à risque : contrat mensuel, peu ancienneté, facture élevée
risque = pd.DataFrame([{
    'SeniorCitizen':0,'tenure':2,'MonthlyCharges':99.65,'TotalCharges':199.3,
    'gender':1,'Partner':0,'Dependents':0,'PhoneService':1,'MultipleLines':1,
    'InternetService':1,'OnlineSecurity':0,'OnlineBackup':0,'DeviceProtection':0,
    'TechSupport':0,'StreamingTV':1,'StreamingMovies':1,
    'Contract':0,'PaperlessBilling':1,'PaymentMethod':2
}])
prob1 = rf.predict_proba(risque)[0][1]
print(f"  Contrat mensuel | 2 mois | 99€/mois → churn : {prob1:.1%} ⚠️")

# Client fidèle : contrat 2 ans, ancienneté élevée, facture raisonnable
fidele = pd.DataFrame([{
    'SeniorCitizen':0,'tenure':60,'MonthlyCharges':45.50,'TotalCharges':2730.0,
    'gender':0,'Partner':1,'Dependents':1,'PhoneService':1,'MultipleLines':0,
    'InternetService':1,'OnlineSecurity':1,'OnlineBackup':1,'DeviceProtection':1,
    'TechSupport':1,'StreamingTV':0,'StreamingMovies':0,
    'Contract':2,'PaperlessBilling':0,'PaymentMethod':0
}])
prob2 = rf.predict_proba(fidele)[0][1]
print(f"  Contrat 2 ans  | 60 mois | 45€/mois → churn : {prob2:.1%} ✅")

print(f"\nLEÇON : La valeur est dans l'interprétation et les actions business.")