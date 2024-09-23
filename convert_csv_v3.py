import csv
import json

# Liste des colonnes à supprimer (mise à jour avec les indices donnés)
COLUMNS_TO_EXCLUDE = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 71, 72, 73, 74, 75, 76, 77, 78, 80, 81, 82, 84, 85, 86, 87, 89, 90, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 108, 110, 111, 112, 113, 115, 116, 119, 120, 121, 122, 123, 124, 125, 126, 127, 129] + list(range(130, 153)) + [153, 154]

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
        reader = csv.reader(infile, delimiter=',')  # Utiliser une virgule comme séparateur
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
input_file = 'dmc_Auteur_Anglaisv2.txt'
output_file = 'output1.csv'

# Lancement du traitement
process_lines_to_csv(input_file, output_file)
