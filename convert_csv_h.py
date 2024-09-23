import csv

# Liste des colonnes à supprimer par numéro (index basé sur 1, comme indiqué)
COLUMNS_TO_EXCLUDE = [1, 5, 7, 8, 9, 10, 12, 13, 14, 16, 17, 18, 19, 22, 23, 24, 25, 29, 30, 32, 34, 35, 36, 37, 41, 44, 46, 48, 49, 52, 54, 58, 60, 63, 64, 65, 67]

def process_lines_to_csv_with_headers(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile, delimiter=';')  # Fichier avec des points-virgules
        writer = None

        for i, row in enumerate(reader):
            if i == 0:
                # Première ligne contient les en-têtes, on supprime les colonnes non voulues
                headers = [header for idx, header in enumerate(row) if (idx + 1) not in COLUMNS_TO_EXCLUDE]
                writer = csv.writer(outfile)
                writer.writerow(headers)
            else:
                # Pour les autres lignes, on supprime les colonnes comme dans les en-têtes
                row = [value for idx, value in enumerate(row) if (idx + 1) not in COLUMNS_TO_EXCLUDE]
                writer.writerow(row)

# Fichiers d'entrée et de sortie
input_file = 'apol_AudioVision.txt'
output_file = 'output_filtered.csv'

# Lancement du traitement
process_lines_to_csv_with_headers(input_file, output_file)
