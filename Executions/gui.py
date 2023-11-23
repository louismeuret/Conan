import dearpygui.dearpygui as dpg
import sys
import glob
import docklaunch as dckl
import psutil
import re
import os
from subprocess import Popen, PIPE


dpg.create_context()
dpg.create_viewport(title="Conan", width=800, height=500)

#dpg.show_metrics()


def boutonsave(sender, data):
    # dpg.get_value(Sender)
    print(dpg.get_value("nptsx"))
    print(dpg.get_value("Softdock"))


def delete_second_window(sender):
    dpg.delete_item(sender)


def save_file():
    path = dpg.get_value("pathconfig")
    f = open(path, "w+")
    software = dpg.get_value("Softdock")
    if software == "Autodock-gpu":
        soft2 = "gpu"
    if software == "Autodock-vina":
        soft2 = "vina"
    if software == "Gnina":
        soft2 = "gnina"
    if software == "Smina":
        soft2 = "smina"
    if software == "Qvina":
        soft2 = "qvina"
    if software == "Autodock4":
        soft2 = "AD4"
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
    f.write("#SPACING# " + dpg.get_value("spacing") + " \n")
    f.write("#CENTERX# " + dpg.get_value("gridcenterx") + " \n")
    f.write("#CENTERY# " + dpg.get_value("gridcentery") + " \n")
    f.write("#CENTERZ# " + dpg.get_value("gridcenterz") + " \n")
    f.write("#SIZEX# " + dpg.get_value("nptsx") + " \n")
    f.write("#SIZEY# " + dpg.get_value("nptsy") + " \n")
    f.write("#SIZEZ# " + dpg.get_value("nptsz") + " \n")
    f.close()
    return


def load_file(sender, app_data, user_data):
    print(f"user_data = {user_data}")
    with open(user_data) as f:
        lines = f.readlines()
    for x in range(len(lines)):
        if re.findall(r"\S+", lines[x])[0] == "#SOFTWARE#":
            # /home/louis/Téléchargements/Conansuite/Executions/test.txt
            if re.findall(r"\S+", lines[x])[1].strip() == "vina":
                print("test")
                dpg.set_value("Softdock", softwares[1])
                print("found vina")
            if re.findall(r"\S+", lines[x])[1].strip() == "gpu":
                dpg.set_value("Softdock", softwares[0])
            if re.findall(r"\S+", lines[x])[1].strip() == "gnina":
                dpg.set_value("Softdock", softwares[2])
            if re.findall(r"\S+", lines[x])[1].strip() == "smina":
                dpg.set_value("Softdock", softwares[3])
            if re.findall(r"\S+", lines[x])[1].strip() == "qvina":
                dpg.set_value("Softdock", softwares[4])
            if re.findall(r"\S+", lines[x])[1].strip() == "autodock4":
                dpg.set_value("Softdock", softwares[4])

        if re.findall(r"\S+", lines[x])[0] == "#DEBUG#":
            if re.findall(r"\S+", lines[x])[1].strip() == "yes":
                dpg.set_value("debug", "True")
            if re.findall(r"\S+", lines[x])[1].strip() == "no":
                dpg.set_value("debug", "False")

        if re.findall(r"\S+", lines[x])[0] == "#THREADS#":
            dpg.set_value("threads", re.findall(r"\S+", lines[x])[1].strip())

        if re.findall(r"\S+", lines[x])[0] == "#NRUNS#":
            dpg.set_value("nruns", re.findall(r"\S+", lines[x])[1].strip())

        if re.findall(r"\S+", lines[x])[0] == "#PATHDB#":
            dpg.set_value("db", re.findall(r"\S+", lines[x])[1].strip())

        if re.findall(r"\S+", lines[x])[0] == "#SPACING#":
            dpg.set_value("spacing", re.findall(r"\S+", lines[x])[1].strip())
        if re.findall(r"\S+", lines[x])[0] == "#CENTERX#":
            dpg.set_value("gridcenterx", re.findall(r"\S+", lines[x])[1].strip())
        if re.findall(r"\S+", lines[x])[0] == "#CENTERY#":
            dpg.set_value("gridcentery", re.findall(r"\S+", lines[x])[1].strip())
        if re.findall(r"\S+", lines[x])[0] == "#CENTERZ#":
            dpg.set_value("gridcenterz", re.findall(r"\S+", lines[x])[1].strip())
        if re.findall(r"\S+", lines[x])[0] == "#SIZEX#":
            dpg.set_value("nptsx", re.findall(r"\S+", lines[x])[1].strip())
        if re.findall(r"\S+", lines[x])[0] == "#SIZEY#":
            dpg.set_value("nptsy", re.findall(r"\S+", lines[x])[1].strip())
        if re.findall(r"\S+", lines[x])[0] == "#SIZEZ#":
            dpg.set_value("nptsz", re.findall(r"\S+", lines[x])[1].strip())

    print(dpg.get_value("Softdock"))
3

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
    software = dpg.get_value("Softdock")
    if software == "Autodock-gpu":
        soft = "GPU"
    if software == "Autodock-vina":
        soft = "VINA"
    if software == "Gnina":
        soft = "GNINA"
    if software == "Smina":
        soft = "SMINA"
    if software == "Qvina":
        soft = "QVINA"
    if software == "Autodock4":
        soft = "AD4"

    nptsx = dpg.get_value("nptsx")
    nptsy = dpg.get_value("nptsy")
    nptsz = dpg.get_value("nptsz")
    gridcenterx = dpg.get_value("gridcenterx")
    gridcentery = dpg.get_value("gridcentery")
    gridcenterz = dpg.get_value("gridcenterz")
    spacing = dpg.get_value("spacing")
    threads = dpg.get_value("threads")
    nruns = dpg.get_value("nruns")
    pathdb2 = dpg.get_value("db")
    if dpg.get_value("debug") == "True":
        debug = True
    else:
        debug = False
    import asyncio

    async def count_files():
        while True:
            listoffiles = glob.glob("results_VINA/*.pdbqt")
            print(listoffiles)
            dpg.set_value("file_count", f"Number of files found: {len(listoffiles)}")
            await asyncio.sleep(1)

    async def start_count_files():
        asyncio.create_task(count_files())

    with dpg.window(label="Parameters", width=500, height=500):
        dpg.add_text(tag="file_count")
        asyncio.run(start_count_files())

    dckl.dockingtot(
        soft,
        nptsx,
        nptsy,
        nptsz,
        gridcenterx,
        gridcentery,
        gridcenterz,
        spacing,
        threads,
        nruns,
        pathdb2,
        debug,
    )

def windowsettingsopen(path):
    with open(path, "r+") as configfile:
        # read a list of lines into data
        config_data = configfile.readlines()

    with dpg.window(label="Parameters", width=800, height=500):
        block_config = ''.join(config_data)
        dpg.add_input_text(tag="", label="test2", multiline=True, height=500, width=800, default_value=block_config)

def settingseditor(sender, data):
    soft = dpg.get_value("Softdock")
    # need to 
    if soft == "Autodock-vina" or "Smina" or "Qvina":
        windowsettingsopen("/home/louis/Conan/parametres/DOCKING.dpf")


def view_grid(sender, data):
    nptsx = dpg.get_value("nptsx")
    nptsy = dpg.get_value("nptsy")
    nptsz = dpg.get_value("nptsz")
    gridcenterx = dpg.get_value("gridcenterx")
    gridcentery = dpg.get_value("gridcentery")
    gridcenterz = dpg.get_value("gridcenterz")
    spacing = dpg.get_value("spacing")
    nptsx = float(nptsx) * float(spacing)
    nptsy = float(nptsy) * float(spacing)
    nptsz = float(nptsz) * float(spacing)
    pathrecs = glob.glob("../receptors/*.pdbqt")
    txtrec = ""
    pathfilerec = "../parametres/temp_files/pathreceptors.txt"
    if os.path.isfile(pathfilerec):
        os.remove(pathfilerec)

    for x in pathrecs:
        txtrec = txtrec + x + "\n"
    file = open(pathfilerec, "w")  # append mode
    file.write(txtrec)
    file.close()
    print(
        f"python ../parametres/viewreceptor.py {nptsx} {nptsy} {nptsz} {gridcenterx} {gridcentery} {gridcenterz}"
    )
    process = Popen(
        [
            "python",
            "../parametres/viewreceptor.py",
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


softwares = ["Autodock-gpu", "Autodock-vina", "Autodock4", "Gnina", "Smina", "Qvina"]
with dpg.window(label="Parameters", width=500, height=500):
    # dpg.set_main_window_size(500,500)
    dpg.add_text("Conan")
    dpg.add_button(label="Load Configuration", callback=load_config)
    dpg.add_listbox(tag="Softdock", items=softwares)
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
        dpg.add_input_text(tag="gridcenterx", width=40)
        # dpg.add_same_line()
        dpg.add_input_text(tag="gridcentery", width=40)
        # dpg.add_same_line()
        dpg.add_input_text(tag="gridcenterz", width=40)
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
dpg.start_dearpygui()
dpg.destroy_context()
