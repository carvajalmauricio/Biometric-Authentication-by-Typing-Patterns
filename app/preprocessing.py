import json
import numpy as np
import nltk
import difflib

# Suponiendo que recognize_phrases contiene tus frases objetivo
with open('phrases.json') as f:
    recognize_phrases = json.load(f)["recognize-phrases"]
# Función para calcular la distancia de Levenshtein (puedes usar una librería específica o esta aproximación)
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
    for entry in entries:
        if entry["key"] == "Backspace":
            phrase = phrase[:-1]  # Eliminar el último caracter
        elif entry["key"].isprintable() and entry["key"] not in ["Control", "Tab", "ArrowRight", "Dead"]:
            phrase += entry["key"]
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

# Función para calcular las características adicionales
def calculate_additional_features(data):
    for user_data in data:
        for username, sessions in user_data.items():
            for session_id, session in sessions.items():

                # Crear un resumen de las características para la sesión
                session_summary = {
                    "session_id": session_id,  # Opcional, si necesitas referenciar la sesión específica
                    "avgTimeSpecialKeys": avg_time_special_keys,
                    "useShift": use_shift,
                    "useCaps": use_cap,
                    "includePeriod": include_period,
                    "avgTimePerSession": avg_time_per_session
                }
                # Crear una copia del diccionario user_data[username] para evitar el error
                user_data_copy = user_data[username].copy()
                if "session_summaries" not in user_data_copy:
                    user_data_copy["session_summaries"] = []
                user_data_copy["session_summaries"].append(session_summary)
                # Actualizar el diccionario original con la copia modificada
                user_data[username] = user_data_copy
    
    # Procesar cada usuario y sesión
    for user_sessions in data:
        for username, sessions in user_sessions.items():
            if "session_summaries" not in sessions:
                sessions["session_summaries"] = []

            for session_id, entries in sessions.items():
                if session_id == "session_summaries":
                    continue  # Saltar el procesamiento para el resumen de la sesión
                
                # Reconstruir la frase tecleada en la sesión
                typed_phrase = ''.join([entry["key"] for entry in entries if entry["key"].isprintable() and entry["key"] not in ["Control", "Tab", "ArrowRight", "Dead", "Backspace"]])

                # Encontrar la frase objetivo más similar
                most_similar_phrase = find_most_similar_phrase(typed_phrase, recognize_phrases)

                # Calcular la distancia de Levenshtein
                distance = levenshtein_distance(typed_phrase, most_similar_phrase)

                # Agregar la información al resumen de la sesión
                sessions["session_summaries"].append({
                    "session_id": session_id,
                    "typed_phrase": typed_phrase,
                    "most_similar_phrase": most_similar_phrase,
                    "distanceF": distance
                })

# Cargar los datos desde el archivo JSON
with open('data.json', 'r') as file:
    data = json.load(file)["data"]

# Calcular las características adicionales
calculate_additional_features(data)

# Opcional: guardar los datos modificados de nuevo en un archivo, si es necesario
with open('data_with_features.json', 'w') as file:
    json.dump({"data": data}, file, indent=4)

