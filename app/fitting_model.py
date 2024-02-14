import json
import joblib
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Cargar datos
with open('data_with_features.json', 'r', encoding='utf-8') as file:
    data = json.load(file)["data"]

with open('phrases.json', 'r', encoding='utf-8') as file:
    phrases_data = json.load(file)
    recognize_phrases = phrases_data["recognize-phrases"]

# Cargar datos
with open('data_with_features.json', 'r', encoding='utf-8') as file:
    data = json.load(file)["data"]

features = []
labels = []
username_to_index = {}  # Mapa de nombres de usuario a índices
index = 0

# Preparar para normalizar 'distanceF'
distanceF_values = []

for user_data in data:
    for username, sessions in user_data.items():
        # Asignar índice a cada usuario
        if username not in username_to_index:
            username_to_index[username] = index
            index += 1
        
        for summary in sessions.get("session_summaries", []):
            if "distanceF" in summary:
                distanceF_values.append(summary["distanceF"])

# Calcular la media y la desviación estándar de 'distanceF'
mean_distanceF = np.mean(distanceF_values)
std_distanceF = np.std(distanceF_values)

for user_data in data:
    for username, sessions in user_data.items():
        user_index = username_to_index[username]

        for session_key, session_entries in sessions.items():
            if session_key != "session_summaries":
                for entry in session_entries:
                    features.append([entry.get("timeSinceLastKey", 0), entry.get("timeStamp", 0)])
                    labels.append(user_index)

        for summary in sessions.get("session_summaries", []):
            feature_vector = [summary.get(key, 0) for key in ["avgTimeSpecialKeys", "useShift", "useCaps", "includePeriod", "avgTimePerSession"]]
            if "distanceF" in summary:
                # Normalizar 'distanceF'
                normalized_distanceF = (summary["distanceF"] - mean_distanceF) / std_distanceF
                feature_vector.append(normalized_distanceF)
            features.append(feature_vector)
            labels.append(user_index)

# Verificar que las características y etiquetas tienen la misma longitud antes de continuar
assert len(features) == len(labels), "La cantidad de características y etiquetas debe ser la misma."

# Asegurarse de que todas las secuencias tengan la misma longitud
max_length = max(len(x) for x in features)
features = np.array([x + [0] * (max_length - len(x)) for x in features])

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

model = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', RandomForestClassifier(random_state=42))
])

param_dist = {
    'clf__n_estimators': [10, 50, 100, 200],
    'clf__max_depth': [30, 10, 20, 30],
    'clf__min_samples_split': [2, 5, 40],
    'clf__min_samples_leaf': [1, 4, 4]
}

random_search = RandomizedSearchCV(model, param_distributions=param_dist, n_iter=50, cv=5, scoring='accuracy', random_state=42)
random_search.fit(X_train, y_train)

best_model = random_search.best_estimator_

y_pred = best_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

best_params = random_search.best_params_
print(f"Best parameters: {best_params}")

joblib.dump(best_model, 'best_model.pkl')
