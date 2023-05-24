# Conan: Virtual Screening and Docking Program

Conan is a program that allows virtual screening through docking on multiple receptors simultaneously, using large ligand libraries.

## Program Files

The main part of the program is contained in two Python files located in the `Executions` folder:

- `docklaunch.py`: Facilitates docking operations and launching dockings from the command line or via a Python script.
- `docking.py`: Can be used as a library to launch docking with the requested software on the specified ligands.

## Preparing for Docking

1. Copy the receptor files in PDBQT format with calculated loads to the `receptors` folder. Use the script `prepare_receptor4.py` from the `parametres` folder. Note that the receptors must be aligned since only one set of coordinates is used.

2. Fill the folder where the ligands are present. The ligands can be organized in multiple nested folders, and all PDBQT files in the database will be used. Ligand files should be in PDBQT format with calculated loads.

## Launching Conan with a Graphical Interface

To launch the program with a graphical interface, you need to install the necessary packages:

1. Go to the `parameters` folder and execute the following command: `pip install -r requirements.txt`.

2. Move to the `Executions` folder and run the program with the command: `python gui.py`. This will open the graphical interface where you can interact with the program.

Note: The graphical interface allows saving configurations for easier parameter modification.

## Launching Conan from the Command Line

To launch the program from the command line:

1. Navigate to the `Executions` folder.

2. Run the command: `python clilaunch.py -h`. This command displays all the necessary arguments for executing the program.

Here's an example command for docking with Autodock-GPU:
```python
python clilaunch.py -software GPU -nptsx 50 -nptsy 76 -nptsz 74 -gridcenterx 11.356 -gridcentery 0 -gridcenterz 8.729 -spacing 1 -threads 4 -nruns 100 -pathdb /home/louis/Downloads/PROJETISDD/ligands/
```
The different software options are: GPU (Autodock-GPU), VINA (Autodock-Vina), AD4 (Autodock4), and Gnina (Gnina).

A docking progress bar is displayed in the terminal, showing the number of ligands fully docked to each receptor.

## Analyzing Results

After the execution of Conan, you can analyze the results using the provided scripts in the `Analysis` folder:

- `postprocessdict.py` for Autodock-GPU.
- `postprocessvina.py` for Autodock-Vina.
- `postprocessAD4.py` for Autodock4.
- `postprocessgnina.py` for Gnina.

There's also a global script available, `show_results.py`, which opens a graphical window to automatically view the results and perform primary analysis. These scripts retrieve the energies and display the ligands with the best scores in a ranked output. The results can be found in the `results_name_of_the_software` folders. The postprocess scripts generate a PDB file for the best pose of each dock when possible.
