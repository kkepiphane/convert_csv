import csv
import json
from datetime import datetime
import os
import glob as g

def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            if len(v) > 0 and isinstance(v[0], dict):
                for idx, item in enumerate(v):
                    items.extend(flatten_dict(item, f"{new_key}{sep}{idx}", sep=sep).items())
            else:
                items.append((new_key, ','.join(map(str, v))))  # Convert list of simple values to a comma-separated string
        elif isinstance(v, str) and ";" in v:
            # Handle string values containing semicolons
            items.append((new_key, v.replace(';', ' ')))  # Replace semicolons with commas
        else:
            items.append((new_key, v))
    return dict(items)

def json_to_csv(json_file_path, csv_file_path):
    with open(json_file_path, 'r') as json_file, open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        # Obtenir les en-têtes du CSV
        headers_written = False
        headers = set()
        
        # Première passe pour déterminer tous les en-têtes possibles
        for line in json_file:
            try:
                obj = json.loads(line)
                flattened_record = flatten_dict(obj)
                headers.update(flattened_record.keys())
            except json.JSONDecodeError as e:
                print(f"Erreur de décodage JSON sur la ligne : {line}. Erreur : {e}")
        
        headers = list(headers)
        
        # Écrire les en-têtes dans le fichier CSV
        csv_writer.writerow(headers)
        
        # Se repositionner au début du fichier JSON pour la seconde passe
        json_file.seek(0)
        
        # Seconde passe pour écrire les données
        for line in json_file:
            try:
                obj = json.loads(line)
                flattened_record = flatten_dict(obj)
                csv_writer.writerow(flattened_record.get(h, '') for h in headers)
            except json.JSONDecodeError as e:
                print(f"Erreur de décodage JSON sur la ligne : {line}. Erreur : {e}")

# Fonction principale pour traiter tous les fichiers JSON du répertoire
def process_all_json_files(directory):
    current_date_time = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    for json_file in g.glob(os.path.join(directory, "*.csv")):
        csv_file = os.path.join(directory, f"output_{os.path.basename(json_file).replace('.json', '')}_{current_date_time}.csv")
        json_to_csv(json_file, csv_file)

# Utilisation de la fonction
process_all_json_files('.')
