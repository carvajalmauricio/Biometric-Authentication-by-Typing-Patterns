import json
import numpy as np
import difflib
from flask import Flask, Blueprint, jsonify, request, redirect, url_for, session
import joblib
bp = Blueprint('m_preprocess', __name__, url_prefix="/")
model = joblib.load('best_model.pkl')

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 
            deletions = current_row[j] + 1       
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

# Función para reconstruir la frase tecleada en una sesión
def reconstruct_typed_phrase(entries):
    phrase = ""

    return phrase

# Función para encontrar la frase objetivo más similar
def find_most_similar_phrase(typed_phrase, recognize_phrases):
    best_match = ""
    highest_ratio = 0
    for phrase_id, target_phrase in recognize_phrases.items():
        ratio = difflib.SequenceMatcher(None, typed_phrase, target_phrase).ratio()
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = target_phrase
    return best_match

def calculate_features(data, recognize_phrases):
    features = []
    for username, sessions in data.items():
        for session_key, entries in sessions.items():
            if session_key == "session_summaries":
                continue  # Ignora el resumen de sesión si está presente

            use_shift = use_caps = include_period = 0
            special_keys_time = []
            all_times_since_last_key = []

            for entry in entries:
                key = entry["key"]
                time_since_last_key = entry.get("timeSinceLastKey", 0)
                
                if key.isprintable() and key not in ["Control", "Tab", "ArrowRight", "Dead"]:
                    all_times_since_last_key.append(time_since_last_key)
                if key == ".":
                    include_period = 1
                if key == "Shift":
                    use_shift += 1
                if key == "CapsLock":
                    use_caps += 1
                if key in ["Backspace", "Delete", "ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown"]:
                    special_keys_time.append(time_since_last_key)

            avg_time_special_keys = np.mean(special_keys_time) if special_keys_time else 0
            avg_time_per_session = np.mean(all_times_since_last_key) if all_times_since_last_key else 0

            typed_phrase = reconstruct_typed_phrase(entries)
            most_similar_phrase = find_most_similar_phrase(typed_phrase, recognize_phrases)
            distance = levenshtein_distance(typed_phrase, most_similar_phrase)

            session_features = [
                avg_time_special_keys,
                use_shift,
                use_caps,
                include_period,
                avg_time_per_session,
                distance
            ]
            features.append(session_features)

    return np.array(features)


with open('phrases.json', 'r') as f:
    recognize_phrases = json.load(f)["recognize-phrases"]

label_to_username = {0: 'alejius12405', 1: 'JhonC19', 2:'maurolrs1', 3:'Elian_Misse', 4: 'andrea', 5: 'camis08', 6:'zazaale'}

@bp.route('/authorized', methods=['POST'])
def authorized():
    username = session.get('username')

    if request.method == 'POST':
        data_load = request.get_json()
        print(data_load)
        data = data_load['data']
        with open('phrases.json', 'r', encoding='utf-8') as file:
            phrases_data = json.load(file)
            recognize_phrases = phrases_data["recognize-phrases"]
        # Calcular las características adicionales
        features = calculate_features(data, recognize_phrases)

        max_length = max(len(x) for x in features)
        features_padded = np.array([list(f) + [0] * (max_length - len(f)) for f in features])

        # Realizar la predicción con el modelo
        prediction_indices = model.predict(features_padded)
            # Convertir índices de predicción a nombres de usuario usando el mapeo label_to_username
        predicted_users = [label_to_username[index] for index in prediction_indices]
    
        print(predicted_users)
            # Determinar si el usuario fue reconocido y preparar la respuesta
    recognized = username == predicted_users[0]
    message = f"Bienvenido al Portal {username}" if recognized else f"Verifica tu cuenta {username}. El sistema no ha podido verificar tu identidad"
    redirect_url = url_for('verificate_blueprint.verificate') if not recognized else None
    
    # Preparar la respuesta
    response_data = {
        'message': message,
        'redirect': not recognized,
        'redirectURL': redirect_url
    }
    
    return jsonify(response_data)
