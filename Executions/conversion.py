import os
import subprocess

def prepare_ligand4(input_pdb, output_pdbqt):
    command = f"./prepare_ligand4.py -l {input_pdb} -o {output_pdbqt}"
    subprocess.run(command, shell=True)

def process_all_pdb_files(folder_path, output_folder):
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdb"):
            input_pdb_path = os.path.join(folder_path, filename)
            output_pdbqt_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.pdbqt")
            
            prepare_ligand4(input_pdb_path, output_pdbqt_path)
            print(f"Conversion complete for {filename}. Output file: {output_pdbqt_path}")

# Example usage:
pdb_folder = "/home/sdv/m2isdd/lmeuret/Téléchargements/Conan-main2/Conan-main/db"
output_folder = "/home/sdv/m2isdd/lmeuret/Téléchargements/Conan-main2/Conan-main/db"

process_all_pdb_files(pdb_folder, output_folder)

