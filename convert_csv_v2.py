import csv
import json

# Liste des colonnes à supprimer (1, 4, 5, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 21, 26, 27, 33, 35, 36, 37, 39, 46, 50, 51, 52, 53, 54, 55, 56, 58, 65, 66, 69 à la fin)
COLUMNS_TO_EXCLUDE = [1, 4, 5, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 21, 26, 27, 33, 35, 36, 37, 39, 46, 50, 51, 52, 53, 54, 55, 56, 58, 65, 66] + list(range(69, 1000))

def parse_json_columns(row):
    parsed_row = []
    for item in row:
        try:
            # Tente de charger les données sous forme de JSON
            parsed_item = json.loads(item)
            # Si c'est un dict ou une liste, on le transforme en string pour le CSV
            if isinstance(parsed_item, (dict, list)):
                parsed_row.append(json.dumps(parsed_item))
            else:
                parsed_row.append(str(parsed_item))
        except json.JSONDecodeError:
            # Si ce n'est pas du JSON, on garde l'élément tel quel
            parsed_row.append(item)
    return parsed_row

def process_lines_to_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile, delimiter=';')
        writer = None
        max_columns = 0

        for row in reader:
            # Parse chaque colonne pour vérifier si elle contient du JSON
            row = parse_json_columns(row)
            
            # Mettre à jour max_columns en fonction de la ligne actuelle
            if len(row) > max_columns:
                max_columns = len(row)

            # Supprimer les colonnes spécifiées
            row = [value for i, value in enumerate(row) if i + 1 not in COLUMNS_TO_EXCLUDE]

            if writer is None:
                # Créer les entêtes en fonction du nombre maximum de colonnes
                fieldnames = [f"column_{i}" for i in range(len(row))]
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()

            # Ajouter des colonnes si la ligne actuelle a plus de colonnes que prévu
            if len(row) > len(fieldnames):
                fieldnames.extend([f"column_{i}" for i in range(len(fieldnames), len(row))])
                writer.fieldnames = fieldnames

            # Écrire la ligne dans le fichier CSV
            writer.writerow({f"column_{i}": value for i, value in enumerate(row)})

# Fichiers d'entrée et de sortie
input_file = 'data_link.txt'
output_file = 'output.csv'

# Lancement du traitement
process_lines_to_csv(input_file, output_file)
