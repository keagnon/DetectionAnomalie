import streamlit as st
import pandas as pd
import mlflow
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split, GridSearchCV

df = pd.read_csv('fusion_courbe_mouvement.csv', delimiter=';', encoding='utf-8')
df.columns = df.columns.str.strip()

df['mois'] = pd.to_datetime(df['date'], format='%d/%m/%Y').dt.month
df['jour_semaine'] = pd.to_datetime(df['date'], format='%d/%m/%Y').dt.dayofweek
df['moyenne_conso_horaire'] = df[['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00',
                                  '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00',
                                  '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']].mean(axis=1)

df_clean = df.dropna(subset=['Consommation_journaliere'])

features = df_clean[["région", "movement_social", "mois", "jour_semaine", "moyenne_conso_horaire"]]
target = df_clean['Consommation_journaliere']

st.title("Prédiction de la Consommation Journalière")

date = st.date_input("Sélectionnez une date", value=pd.to_datetime("2024-09-22"))
region = st.selectbox("Sélectionnez une région", df['région'].unique())

movement_social = st.checkbox("Y a-t-il un mouvement social ?")

moyenne_conso_horaire = st.number_input("Entrez la moyenne de consommation horaire", min_value=0.0)

if st.button("Prédire"):
    input_data = pd.DataFrame({
        'région': [region],
        'movement_social': [movement_social],
        'mois': [date.month],
        'jour_semaine': [date.weekday()],
        'moyenne_conso_horaire': [moyenne_conso_horaire]
    })

    categorical_cols = ["région"]
    numerical_cols = ['movement_social', 'mois', 'jour_semaine', 'moyenne_conso_horaire']

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_cols),
            ('cat', OneHotEncoder(), categorical_cols)
        ]
    )

    ridge_model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', Ridge())
    ])
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.3, random_state=42)
    param_grid = {'model__alpha': [0.1, 1.0, 10.0, 100.0]}
    grid_search = GridSearchCV(ridge_model, param_grid, cv=5)
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    predictions = best_model.predict(input_data)
    st.write(f"La prédiction de la consommation journalière est : {predictions[0]:.2f} MW")
