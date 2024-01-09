import dearpygui.dearpygui as dpg
import sys
import glob
import docklaunch3 as dckl

import asyncio
import concurrent.futures
from multiprocessing import Manager

import logging
import psutil
import re
import os
import threading
import yaml
import numpy as np
from subprocess import Popen, PIPE


dpg.create_context()
dpg.create_viewport(title="Conan", width=800, height=800)

"""
softwares = {
    "Autodock-gpu": {"version": "gpu", "path": "/path/to/autodock-gpu"},
    "Autodock-vina": {"version": "vina", "path": "/path/to/autodock-vina"},
    "Gnina": {"version": "gnina", "path": "/path/to/gnina"},
    "Smina": {"version": "smina", "path": "/path/to/smina"},
    "Qvina-w": {"version": "qvina-w", "path": "/path/to/qvina"},
    "Qvina2.1": {"version": "qvina2.1", "path": "/path/to/qvina"},
    "Autodock4": {"version": "AD4", "path": "/path/to/autodock4"}
}
"""
#software parameters

async def monitor_docking_status(status_dict):
    while True:
        logging.info("MONITORING")
        logging.info(str(dict(status_dict)))  # Convert manager dict to regular dict for logging
        if dpg.does_item_exist("docking_todo"):
            pending_count = sum(1 for value in status_dict.values() if value == 'Pending')
            dpg.set_value("docking_todo", f"Number of ligands not docked yet: {pending_count}")
        if dpg.does_item_exist("docking_text"):
            docking_count = sum(1 for value in status_dict.values() if value == 'Processing')
            dpg.set_value("docking_text", f"Number of ligands being docked {docking_count}")
        if dpg.does_item_exist("docked_text"):
            docked_count = sum(1 for value in status_dict.values() if value == 'Completed')
            dpg.set_value("docked_text", f"Number of ligands docked: {docked_count}")
        await asyncio.sleep(5)  # Check status every 5 seconds

def start_async_monitoring(status_dict):
    asyncio.run(monitor_docking_status(status_dict))


with open('../parameters/parameters_software/softwares.yaml', 'r') as file:
    softwares = yaml.safe_load(file)

def boutonsave(sender, data):
    # dpg.get_value(Sender)
    print(dpg.get_value("nptsx"))
    print(dpg.get_value("Softdock"))


def delete_second_window(sender):
    dpg.delete_item(sender)

def create_subfolders(results_folder):
    subfolders = ["DOCKED", "PARAMETERS", "FILES", "RESULTS","MAPS","RECEPTORS"]
    for subfolder in subfolders:
        os.makedirs(os.path.join(results_folder, subfolder), exist_ok=True)

def save_parameters_to_yaml(results_folder, parameters):
    params_file = os.path.join(results_folder, "PARAMETERS", "docking_parameters.yaml")
    with open(params_file, 'w') as file:
        yaml.dump(parameters, file)


def monitor_file_count(directory, update_interval, stop_event):
    while not stop_event.is_set():
        file_count = len(os.listdir(directory))
        dpg.set_value("file_count", f"Number of files found: {file_count}")
        time.sleep(update_interval)

def save_file():
    path = dpg.get_value("pathconfig")
    f = open(path, "w+")
    software = dpg.get_value("Softdock")
    soft2 = softwares.get(software, "")
    f.write("#SOFTWARE# " + soft2 + " \n")
    # f.write("#DEBUG# "+dpg.get_value("debug")+" \n")

    debug = dpg.get_value("debug")
    if debug == "True":
        f.write("#DEBUG# " + "yes" + " \n")
    else:
        f.write("#DEBUG# " + "no" + " \n")

    f.write("#THREADS# " + dpg.get_value("threads") + " \n")
    f.write("#NRUNS# " + dpg.get_value("nruns") + " \n")
    f.write("#PATHDB# " + dpg.get_value("db") + " \n")
    f.write("#PATHRESULTS# " + dpg.get_value("results_folder") + " \n")
    f.write("#SPACING# " + dpg.get_value("spacing") + " \n")
    f.write("#CENTERX# " + dpg.get_value("centerx") + " \n")
    f.write("#CENTERY# " + dpg.get_value("centery") + " \n")
    f.write("#CENTERZ# " + dpg.get_value("centerz") + " \n")
    f.write("#NPTSX# " + dpg.get_value("nptsx") + " \n")
    f.write("#NPTSY# " + dpg.get_value("nptsy") + " \n")
    f.write("#NPTSZ# " + dpg.get_value("nptsz") + " \n")
    f.close()
    return


def load_file(sender, app_data, user_data):
    print(f"user_data = {user_data}")
    with open(user_data) as f:
        lines = f.readlines()

    for line in lines:
        # Extract key and value from each line
        parts = line.split("#")
        if len(parts) < 3:
            continue
        key, value = parts[1], parts[2].strip()

        # Handle different keys
        if key == "SOFTWARE":
            # Find the software name matching the version
            for name, details in softwares.items():
                if details["short_name"] == value:
                    dpg.set_value("Softdock", name)
                    break
        elif key == "PATHRESULTS":
            dpg.set_value("results_folder", value)
        elif key == "PATHCONFIGFILE":
            dpg.set_value("config_file", value)
        elif key in ["DEBUG", "THREADS", "NRUNS", "PATHDB", "SPACING", "CENTERX", "CENTERY", "CENTERZ", "NPTSX", "NPTSY", "NPTSZ"]:
            # Update the corresponding GUI element
            gui_key = key.lower() if key != "PATHDB" else "db"
            print(gui_key,value)
            dpg.set_value(gui_key, value)

    print(dpg.get_value("Softdock"))

def display_settings():
    with dpg.window(
        label="Compute",
        width=400,
        height=400,
        pos=(100, 100),
        tag="computeinformationdb",
        on_close=delete_second_window,
    ):
        dpg.add_text("Edit settings")
        dpg.add_input_text("Edit settings")


def display_config(software_key):
    print(software_key)
    version = softwares[software_key]["version"]
    print(version)
    file_name = f"{version}.yaml"
    directory = "../parameters/parameters_software"
    file_path = os.path.join(directory, file_name)
    print(file_path)

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
            # Clear existing GUI elements in the dynamic config window
            if dpg.does_item_exist("dynamic_config_window"):
                dpg.delete_item("dynamic_config_window")
            # Rebuild the GUI with the loaded configuration
            build_dynamic_gui(config)
    else:
        print(f"Configuration file for {software_key} not found.")

def build_dynamic_gui(config):
    # Clear existing GUI elements if any
    if dpg.does_item_exist("dynamic_config_window"):
        dpg.delete_item("dynamic_config_window")

    # Create a new window
    with dpg.window(label="Dynamic Configuration Editor", tag="dynamic_config_window"):
        print(config.items())
        for section, settings in config.items():
            with dpg.group(label=f"{section} Settings"):
                # Handle dictionary values
                if isinstance(settings, dict):
                    for key, value in settings.items():
                        create_gui_element(section, key, value)
                else:
                    # Handle non-dictionary values
                    create_gui_element(section, section, settings)

        dpg.add_button(label="Save Configuration", callback=save_current_config)
        dpg.add_button(label="Load Configuration", callback=load_current_config)

def create_gui_element(section, key, value):
    # Function to create GUI elements based on value type
    if isinstance(value, bool):
        dpg.add_checkbox(tag=f"{section}_{key}", label=key, default_value=value)
    elif isinstance(value, int):
        dpg.add_input_int(tag=f"{section}_{key}", label=key, default_value=value)
    elif isinstance(value, float):
        dpg.add_input_float(tag=f"{section}_{key}", label=key, default_value=value)
    else:  # Handle as string
        dpg.add_input_text(tag=f"{section}_{key}", label=key, default_value=str(value))


def get_info_db(sender, app_data, user_data):
    import rdkit
    from rdkit.Chem import rdMolDescriptors
    from rdkit import Chem
    from rdkit.Chem import GraphDescriptors
    from rdkit.Chem import Descriptors
    import numpy as np

    descriptor_names = list(rdMolDescriptors.Properties.GetAvailableProperties())
    descriptor_names.remove("NumAtomStereoCenters")
    descriptor_names.remove("NumUnspecifiedAtomStereoCenters")
    print(descriptor_names)
    listofpdbqt = glob.glob(f"{user_data}/**/*.pdbqt", recursive=True)
    print(listofpdbqt)

    def compute_descript(blockdata, descriptors_to_compute):
        # transformation du bloc texte en molecule rdkit
        m = Chem.rdmolfiles.MolFromPDBBlock(blockdata)
        # get_descriptors = rdMolDescriptors.Properties(descriptors_to_compute)
        descriptors = []

        if m:
            descriptors = np.array(descriptors_to_compute.ComputeProperties(m))

        return descriptors

    with dpg.window(
        label="Compute",
        width=400,
        height=400,
        pos=(100, 100),
        tag="computeinformationdb",
        on_close=delete_second_window,
    ):
        descriptor_names = list(dict.fromkeys(descriptor_names))
        print(descriptor_names)

        # Add a callback function to handle check/uncheck all checkboxes
        def check_uncheck_all(sender, app_data, user_data):
            check_all = dpg.get_value("check_all")
            for descriptor in descriptor_names:
                dpg.set_value(descriptor, check_all)

        def check_checked():
            good = []
            print("GOOD")
            for descriptor in descriptor_names:
                if dpg.get_value(descriptor):
                    good.append(descriptor)
            print(good)
            return good

        # Do the calculations on the selected descriptors
        def iteration_pdbqt(sender, data, user_data):
            descriptor_names_entry = check_checked()
            print(f"desc names: {descriptor_names_entry}")
            get_descriptors = rdMolDescriptors.Properties(descriptor_names_entry)

            import pandas as pd

            pandas_df = pd.DataFrame(columns=descriptor_names_entry)
            import time

            print(len(listofpdbqt))
            # time.sleep(10)
            for file in listofpdbqt:
                with open(file, "r+") as pdbqt:  # read a list of lines into data
                    pdbqtcontenu = pdbqt.readlines()
                    # print(pdbqtcontenu)
                blockdata = ""

                # Tiny pdbqt parser
                for x in range(len(pdbqtcontenu)):
                    if pdbqtcontenu[x][:4] == "ATOM" or pdbqtcontenu[x][:6] == "HETATM":
                        templine = pdbqtcontenu[x].split()
                        pdbqtcontenu[x] = pdbqtcontenu[x][:-3]
                        pdbqtcontenu[x] = pdbqtcontenu[x] + templine[2][:1] + "\n"
                        blockdata = blockdata + pdbqtcontenu[x]
                        # print(x)
                    if pdbqtcontenu[x][:6] == "ENDMDL":
                        print("break")
                        break

                print(compute_descript(blockdata, get_descriptors))
                # Compute the descriptors for the current blockdata
                descriptors = compute_descript(blockdata, get_descriptors)

                # Append the computed descriptors to the pandas_df dataframe
                if len(descriptors) > 0:
                    pandas_df = pandas_df.append(
                        pd.Series(descriptors, index=descriptor_names_entry),
                        ignore_index=True,
                    )

            print(pandas_df)
            """
            data = pandas_df['exactmw']
            import matplotlib.pyplot as plt
# Plotting the histogram
            plt.hist(data, bins=10)  # Adjust the number of bins as needed

            # Adding labels and title
            plt.xlabel('Values')
            plt.ylabel('Frequency')
            plt.title('Histogram of First Column')

            # Displaying the histogram
            plt.show()
    
            """
            with dpg.window(
                label="Descriptors Histogram",
                width=700,
                height=400,
                pos=(100, 100),
                tag="descriptors_histogram",
                on_close=delete_second_window,
            ):
                dpg.add_text("Select the number of bins:")
                dpg.add_input_int(
                    label="Number of bins", tag="num_bins", default_value=15
                )

                # def plot_histograms(sender, app_data, user_data):
                num_bins = dpg.get_value("num_bins")
                datap = pandas_df["exactmw"].values.tolist()
                amin, amax = min(datap), max(datap)
                newdata = []
                for i, val in enumerate(datap):
                    newdata.append((val - amin) / (amax - amin))
                print(newdata)

                # Create a histogram plot
                with dpg.plot(label="Histogram"):
                    dpg.add_plot_axis(1, label="y", tag="y_axis")
                    dpg.add_histogram_series(newdata, bins=10, parent="y_axis")  # A
                """
                with dpg.plot(label="Histograms", width=700, height=400,parent="descriptors_histogram"):
                    
                    dpg.add_plot_axis(dpg.mvXAxis, label="x")
                    dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis")
                    #for descriptor in descriptor_names_entry:
                    print([int(item) for item in list(pandas_df["exactmw"])])
                    hist_series = dpg.add_histogram_series([int(item) for item in list(pandas_df["exactmw"])], bins=int(num_bins), label="exactmw", parent="y_axis")
                    
                    dpg.add_plot_legend(location="upper right")
                    
                    dpg.set_item_color(hist_series, [255, 0, 0, 255])

                    #dpg.add_histogram_series(list(pandas_df['exactmw']), bins=num_bins, label='descriptor', parent="y_axis")
                    #dpg.add_plot_legend(location="upper right")
                    #dpg.add_plot_axis(dpg.mvXAxis, label="x")
                    #dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis")
                    """

                # series belong to a y axis

                # dpg.add_button(label="Plot Histograms", tag="plot_histograms", callback=plot_histograms)

        dpg.add_text(
            "Which descriptor do you want to compute on the database ? \n Rdkit calculations are used for this."
        )
        with dpg.group(horizontal=True):
            dpg.add_checkbox(
                label="Check/Uncheck All", callback=check_uncheck_all, tag="check_all"
            )

            dpg.add_button(label="Run", tag="loadconf", callback=iteration_pdbqt)

        for descriptor in descriptor_names:
            checkbox = dpg.add_checkbox(label=descriptor, tag=descriptor)

        # Add the check/uncheck all checkbox

        # dpg.add_button(label=descriptor, callback=lambda: dpg.set_value(descriptor, not dpg.get_value(descriptor)), user_data=descriptor, tag=descriptor)


def detect_config_files(path):
    print(path)
    filestoscan = glob.glob(f"{path}/*.txt")
    print(filestoscan)
    config_files = []
    import datetime

    def convert_date(file_date):
        return datetime.datetime.fromtimestamp(file_date).strftime("%Y/%m/%d %H:%M:%S")

    for file in filestoscan:
        with open(file) as f:
            first_line = f.readline()
            if "#SOFTWARE#" in first_line:
                file_name = os.path.basename(file)
                file_path = os.path.abspath(file)
                file_date = os.path.getctime(file)
                file_date = convert_date(file_date)

                config_files.append(
                    (file_name, file_path, first_line.split()[1], file_date)
                )

    print(config_files)
    return config_files



def save_config(sender):
    with dpg.window(
        label="Save",
        width=200,
        height=200,
        pos=(100, 100),
        tag="saveconfig",
        on_close=delete_second_window,
    ):
        dpg.add_input_text(tag="pathconfig", width=150)
        dpg.add_button(label="Save File", tag="saveconf", callback=save_file)
        # dpg.add_text(f"CPU usage:{psutil.cpu_percent()}%, Memory usage: {psutil.virtual_memory().percent}%", tag="usage")


def load_config(sender):
    with dpg.window(
        label="Load",
        width=700,
        height=400,
        pos=(100, 100),
        tag="loadconfig",
        on_close=delete_second_window,
    ):
        dpg.add_input_text(tag="pathconfig2", width=150)
        dpg.add_button(
            label="Load File",
            tag="loadconf",
            callback=load_file,
            user_data=lambda: str(dpg.get_value("pathconfig2")),
        )
        dpg.add_text("Theses are detected files in the current directory:")
        config_files = detect_config_files(os.getcwd())
        

        print(config_files)
        headers_conf = ["Filename", "Path", "Software", "Date of Creation", "Open"]
        with dpg.table(
            header_row=True,
            resizable=True,
            borders_outerH=True,
            borders_innerV=True,
            borders_innerH=True,
            borders_outerV=True,
        ):
            print(len(config_files))

            for x in range(len(headers_conf)):
                print(headers_conf[x])
                dpg.add_table_column(label=headers_conf[x])

            for i in range(len(config_files)):
                with dpg.table_row():
                    for j in range(len(config_files[i])):
                        dpg.add_text(config_files[i][j])
                    dpg.add_button(
                        label="Load this file",
                        callback=load_file,
                        user_data=config_files[i][1],
                    )


# dckl.dockingtot("VINA","90","75","85","55","-21","-20","0.375","1","100","/home/louis/Téléchargements/dbtest/",True)
def run(sender, data):
    # Retrieve software and parameters from GUI
    software = dpg.get_value("Softdock")
    soft = softwares.get(software, "")['short_name']
    print(soft)

    # Set up the results folder
    results_folder = dpg.get_value("results_folder")
    if not results_folder: 
        results_folder = os.path.join(f"results_{soft}")
    create_subfolders(results_folder)

    # Collect parameters from the GUI
    nptsx, nptsy, nptsz = dpg.get_value("nptsx"), dpg.get_value("nptsy"), dpg.get_value("nptsz")
    gridcenterx, gridcentery, gridcenterz = dpg.get_value("centerx"), dpg.get_value("centery"), dpg.get_value("centerz")
    spacing, threads, nruns = dpg.get_value("spacing"), dpg.get_value("threads"), dpg.get_value("nruns")
    pathdb2, debug = dpg.get_value("db"), dpg.get_value("debug") == "True"

    parameters = {
        "Software": software,
        "Number of Points": {"X": nptsx, "Y": nptsy, "Z": nptsz},
        "Grid Center": {"X": gridcenterx, "Y": gridcentery, "Z": gridcenterz},
        "Spacing": spacing,
        "Threads": threads,
        "Runs": nruns,
        "Database Path": pathdb2,
        "Debug": debug
        # Add more parameters here if needed
    }
    save_parameters_to_yaml(results_folder, parameters)

    # Run docking process
    with dpg.window(label="Example Window"):
        dpg.add_text("Display current results")
        dpg.add_text("0", tag="docking_todo")
        dpg.add_text("0", tag="docking_text")
        dpg.add_text("0", tag="docked_text")
        
        


    print(f"dckl.dockingtot({software}, {nptsx}, {nptsy}, {nptsz}, {gridcenterx}, {gridcentery}, {gridcenterz}, {spacing}, {threads}, {nruns}, {pathdb2}, {results_folder}, {debug})")
    """
    dckl.dockingtot(
        software, nptsx, nptsy, nptsz, gridcenterx, gridcentery, gridcenterz, 
        spacing, threads, nruns, pathdb2,results_folder, debug,
    )
    """

    manager = Manager()
    status_dict = manager.dict()
    file_ligands = glob.glob(f'{pathdb2}/**/*.pdbqt', recursive=True)

    status_dict.update({ligand_info: 'Pending' for ligand_info in np.arange(1, len(file_ligands)+1, 1)})

    # Start the docking process in a separate thread
    threading.Thread(target=dckl.dockingtot, args=(
        software, nptsx, nptsy, nptsz, gridcenterx, gridcentery, gridcenterz, 
        spacing, threads, nruns, pathdb2, results_folder, debug, status_dict
    ), daemon=True).start()

    # Start monitoring in a separate thread
    threading.Thread(target=start_async_monitoring, args=(status_dict,), daemon=True).start()

    

def windowsettingsopen(path):
    with open(path, "r+") as configfile:
        # read a list of lines into data
        config_data = configfile.readlines()

    with dpg.window(label="Parameters", width=800, height=500):
        block_config = ''.join(config_data)
        dpg.add_input_text(tag="", label="test2", multiline=True, height=500, width=800, default_value=block_config)

def settingseditor(sender, data):
    soft = dpg.get_value("Softdock")
    display_config(soft)


def view_grid(sender, data):
    nptsx = dpg.get_value("nptsx")
    nptsy = dpg.get_value("nptsy")
    nptsz = dpg.get_value("nptsz")
    gridcenterx = dpg.get_value("centerx")
    gridcentery = dpg.get_value("centery")
    gridcenterz = dpg.get_value("centerz")
    spacing = dpg.get_value("spacing")
    nptsx = float(nptsx) * float(spacing)
    nptsy = float(nptsy) * float(spacing)
    nptsz = float(nptsz) * float(spacing)
    pathrecs = glob.glob("../receptors/*.pdbqt")
    txtrec = ""
    pathfilerec = "../parameters/temp_files/pathreceptors.txt"
    if os.path.isfile(pathfilerec):
        os.remove(pathfilerec)

    for x in pathrecs:
        txtrec = txtrec + x + "\n"
    file = open(pathfilerec, "w")  # append mode
    file.write(txtrec)
    file.close()
    print(
        f"python3 ../parameters/viewreceptor.py {nptsx} {nptsy} {nptsz} {gridcenterx} {gridcentery} {gridcenterz}"
    )
    process = Popen(
        [
            "python3",
            "../parameters/viewreceptor.py",
            str(nptsx),
            str(nptsy),
            str(nptsz),
            str(gridcenterx),
            str(gridcentery),
            str(gridcenterz),
        ],
        stdout=PIPE,
        stderr=PIPE,
    )
    # viewer.viewreceptor(pathrecs,nptsx,nptsy,nptsz,gridcenterx,gridcentery,gridcenterz)


def print_me(sender, data):
    print(f"Menu Item: {sender}{data}")


def setdb(sender, data):
    pathdb = dpg.get_value("db")
    listofpdbqt = glob.glob(f"{pathdb}/**/*.pdbqt", recursive=True)
    print(len(listofpdbqt))
    if len(listofpdbqt) == 0:
        dpg.set_value("textdb", "No pdbqt detected on this path")
    else:
        dpg.set_value("textdb", f"Found {len(listofpdbqt)} ligands on this path")


def close(sender, data):
    sys.exit()


def validation(sender, app_data):
    print("App Data: ", app_data)
    print(app_data["file_path_name"])
    dpg.set_value("db", app_data["file_path_name"])

def validation2(sender, app_data):
    print("App Data: ", app_data)
    print(app_data["file_path_name"])
    dpg.set_value("results_folder", app_data["file_path_name"])

def cancel_callback(sender, app_data):
    print("Cancel was clicked.")
    print("Sender: ", sender)
    print("App Data: ", app_data)


"""
def on_render(sender, data):
    #dpgc.get_total_time()
    dpg.set_value("usage",f"CPU usage: {psutil.cpu_percent()}%, Memory usage: {psutil.virtual_memory().percent}%", tag="usage")
    print("test")
"""


def update():
    dpg.set_value(
        "usage",
        f"CPU usage:{psutil.cpu_percent()}%, Memory usage: {psutil.virtual_memory().percent}%",
    )

#softwares_list = ["Autodock-gpu", "Autodock-vina", "Autodock4", "Gnina", "Smina", "Qvina"]
softwares_list = list(softwares.keys())

with dpg.window(label="Parameters", width=500, height=500,tag="Parameters"):
    # dpg.set_main_window_size(500,500)
    with dpg.group(horizontal=True):
        dpg.add_text("Conan")
        # ... other elements on the same line ...
        dpg.add_spacer(width=400)  # Add a spacer to push the button to the end
    
        dpg.add_button(label="Settings")

    dpg.add_button(label="Load Configuration", callback=load_config)
    dpg.add_listbox(tag="Softdock", items=softwares_list)
    dpg.add_text("Number of points in the grid")
    dpg.add_text("  X  --- Y ---  Z")
    with dpg.group(horizontal=True):
        dpg.add_input_text(tag="nptsx", width=40)
        # dpg.add_same_line()
        dpg.add_input_text(tag="nptsy", width=40)
        # dpg.add_same_line()
        dpg.add_input_text(tag="nptsz", width=40)

    dpg.add_text("Center of the grid")
    dpg.add_text("  X  --- Y ---  Z")
    with dpg.group(horizontal=True):
        dpg.add_input_text(tag="centerx", width=40)
        # dpg.add_same_line()
        dpg.add_input_text(tag="centery", width=40)
        # dpg.add_same_line()
        dpg.add_input_text(tag="centerz", width=40)
    # dpg.add_text("Spacing (Angstrom)")
    dpg.add_input_text(tag="spacing", width=40, label="Spacing (Angstrom)")
    dpg.add_button(label="View grid in Pymol", callback=view_grid)
    # dpg.add_text("Number of Runs             Number of Threads")

    dpg.add_input_text(tag="nruns", width=40, label="Number of Genetic Runs")
    dpg.add_input_text(tag="threads", width=40, label="Number of Threads")
    dpg.add_button(label="Edit all settings", callback=settingseditor)
    dpg.add_text("Path of Database:")
    with dpg.group(horizontal=True):
        dpg.add_input_text(tag="db", width=150)
        dpg.add_file_dialog(
            directory_selector=True,
            show=False,
            callback=validation,
            tag="file_dialog_id",
            cancel_callback=cancel_callback,
        )
        dpg.add_button(
            label="Directory Selector", callback=lambda: dpg.show_item("file_dialog_id")
        )
        dpg.add_button(
            label="Get informations",
            callback=get_info_db,
            user_data="/home/louis/Téléchargements/PROJETISDD/ligands",
        )
    dpg.add_button(label="Set", callback=setdb)
    dpg.add_text("No database selected yet", tag="textdb")
    dpg.add_text("Result folder:")
    with dpg.group(horizontal=True):
        dpg.add_input_text(tag="results_folder", width=150)
        dpg.add_button(label="Select Results Folder", callback=lambda: dpg.show_item("results_folder_dialog_id"))
        dpg.add_file_dialog(
            directory_selector=True,
            show=False,
            callback=validation2,
            tag="results_folder_dialog_id",
            cancel_callback=cancel_callback,
        )
        dpg.add_button(
            label="Directory Selector", callback=lambda: dpg.show_item("results_folder_dialog_id")
        )

    dpg.add_text("Enable Debugging:")
    dpg.add_radio_button(tag="debug", items=["True", "False"], horizontal=True)
    with dpg.group(horizontal=True):
        dpg.add_button(label="Save", callback=boutonsave)
        dpg.add_button(label="Run", callback=run)
    dpg.add_button(label="Close", callback=close)
    dpg.add_button(label="Save Configuration", callback=save_config)
    # dpg.add_text(f"CPU usage:{psutil.cpu_percent()}%, Memory usage: {psutil.virtual_memory().percent}%", tag="usage")


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Parameters", True)
dpg.start_dearpygui()
dpg.destroy_context()
