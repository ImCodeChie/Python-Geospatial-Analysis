import os
import shutil

source_folders = [
    r"\\pp-prc-01-scus\DDL\FieldBoundaries_not_delivered\Europe",
    r"\\pp-prc-01-scus\DDL\FieldBoundaries\2023\Europe"
]
destination_folder = r"C:\Users\lyi\Desktop\Clip_validation\Western Europe\ml"
keywords = [
    "Kokpektinskiy", "Koksuskiy", "Taldyqorghan", "Terenozekskiy", "Zhaksynskiy",
    "Agsu", "Samaxı", "Enotaevskiy rayon", "Dubovskiy rayon", "Gorodishchenskiy rayon",
    "Beloglinskiy rayon", "Novopokrovskiy rayon", "Ichnianskyi", "Eregli", "Dykans",
    "Shyshats'kyi", "Zin'kivs'kyi", "Alapaevskiy rayon", "Rezhevskiy rayon", "Balcauti",
    "Calafindesti", "Dornesti", "Fratautii Noi", "Fratautii Vechi", "Granicesti", "Radauti",
    "Satu Mare", "Imbabah", "Unorganized in Al Jizah", "Ashmun", "Puy-de-Dôme", "Ancona",
    "Macerata", "Vendee", "Linköping", "Mjolby", "Motala", "Lund", "Malmo", "Svedala",
    "Trelleborg", "Vellinge", "Lidkoping", "Vara", "Gers", "Lincolnshire", "Cuenca", "Kenitra",
    "Sidi Kacem", "Aljustrel", "Beja", "Cuba", "Ferreira do Alentejo", "Bordj Ben Azzouz",
    "Bouchakroune", "Daoussen", "El Ghrous", "Foughala", "Lichana", "Lioua", "Mekhadma",
    "Tolga", "Eidsberg", "Rakkestad", "Ceylanpınar", "Viransehir", "Yaranskiy rayon",
    "Pestovskiy rayon", "Ustyuzhenskiy rayon", "Thessaly"
]

tasks_completed = 0

for source_folder in source_folders:
    for root, _, files in os.walk(source_folder):
        for file in files:
            if file.endswith(".gpkg") and any(keyword.lower() in file.lower() for keyword in keywords):
                source_path = os.path.join(root, file)
                destination_path = os.path.join(destination_folder, file)
                print(f"Copying {source_path} to {destination_folder}")
                shutil.copy(source_path, destination_path)
                tasks_completed += 1

print(f"All {tasks_completed} tasks are fully done!")
