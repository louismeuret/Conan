import subprocess

def dock_ligand(rec_file, lig_file, output_file):
    # Create the command string
    cmd = f"gnina -r {rec_file} -l {lig_file} -o {output_file}"
    # Use the subprocess module to execute the command
    subprocess.run(cmd, shell=True)

