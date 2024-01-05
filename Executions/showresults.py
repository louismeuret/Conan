import dearpygui.dearpygui as dpg
import glob
import postprocess2 as pp
import os
import os.path
from prolif.plotting.network import LigNetwork

# import MDAnalysis as mda
import prolif
from rdkit import Chem
import pathlib
import webbrowser
from subprocess import Popen, PIPE
from multiprocessing import Process

# import pymol_clust
import numpy as np
import pickle
import dbscan_cluster
import pandas as pd

dpg.create_context()
dpg.create_viewport(title="Conan", width=1500, height=500)
softwares = ["Autodock-gpu", "Autodock-vina", "Autodock4", "Gnina", "Smina", "Qvina"]
headersall = [
    "Ligand Name",
    "Energy",
    "LogP",
    "MolWt",
    "Complexity",
    "Center of mass",
    "Show Interactions",
    "Open in Pymol",
]
headersgnina = [
    "Ligand Name",
    "Energy",
    "CNNscore",
    "CNNactivity",
    "LogP",
    "MolWt",
    "Complexity",
    "Center of mass",
    "Show Interactions",
    "Open in Pymol",
]


def pymolcluster(sender, app_data, user_data):
    pathlist = "../parameters/temp_files/list_results.pkl"
    print("clustering")
    with open(pathlist, "wb") as f:
        pickle.dump(user_data, f)

    process = Popen(["python3", "pymol_clust.py"], stdout=PIPE, stderr=PIPE)


def dbscancluster(sender, app_data, user_data):
    clustered = dbscan_cluster.dbscan_clust(user_data)
    df = pd.DataFrame(user_data)
    print(df)
    df = df.iloc[:, :2]
    df[2] = clustered["Cluster"]

    print(df)

    header_clust = ["Ligand Name", "Energy", "Cluster"]
    with dpg.window(label="Cluster", width=1500, height=500):
        with dpg.table(
            header_row=True,
            resizable=True,
            borders_outerH=True,
            borders_innerV=True,
            borders_innerH=True,
            borders_outerV=True,
        ):
            for x in range(len(header_clust)):
                print(header_clust[x])
                dpg.add_table_column(label=header_clust[x])

            for i in range(len(df)):
                with dpg.table_row():
                    dpg.add_text(str(df.iloc[i, 0]))
                    dpg.add_text(str(df.iloc[i, 1]))
                    dpg.add_text(str(df.iloc[i, 2]))

            """
            print(linestoadd)
            for i in range(len(linestoadd)):
                with dpg.table_row():
                    for j in range(len(linestoadd)):
                        dpg.add_text(linestoadd[i][j])  
            """

    print(clustered)


def csvsave(sender, app_data, user_data):
    import time

    if len(user_data[0][0]) == 6:
        df = pd.DataFrame(user_data[0], columns=headersall[:-2])
    else:
        df = pd.DataFrame(user_data[0], columns=headersgnina[:-2])
    t = time.localtime()
    current_time = time.strftime("%H_%M_%S", t)
    df.to_csv(f"{user_data[1]}_{current_time}.csv")

    print(df)


def get_res(pathres, soft2):
    sortabc, sortnrj = pp.process_results(pathres, soft2)
    print(pathres, soft2)
    print(sortnrj)
    with dpg.window(label=soft2, width=600, height=500):
        with dpg.group(horizontal=True):
            dpg.add_button(
                label="View all results in Pymol",
                callback=pymolcluster,
                user_data=sortnrj,
            )
            dpg.add_button(
                label="Cluster positions", callback=dbscancluster, user_data=sortnrj
            )
            dpg.add_button(
                label="Save as CSV", callback=csvsave, user_data=[sortnrj, soft2]
            )

        with dpg.table(
            header_row=True,
            resizable=True,
            borders_outerH=True,
            borders_innerV=True,
            borders_innerH=True,
            borders_outerV=True,
        ):
            print(len(sortnrj[0]))
            if len(sortnrj[0]) == 6:
                for x in range(len(sortnrj[0]) + 2):
                    print(headersall[x])
                    dpg.add_table_column(label=headersall[x])
            else:
                for x in range(len(sortnrj[0]) + 2):
                    dpg.add_table_column(label=headersgnina[x])

            for i in range(len(sortnrj)):
                with dpg.table_row():
                    for j in range(len(sortnrj[i])):
                        dpg.add_text(sortnrj[i][j])
                    dpg.add_button(
                        label="Show interactions",
                        callback=show_interactions,
                        user_data=[sortnrj[i], pathres],
                    )
                    dpg.add_button(
                        label="Open in Pymol",
                        callback=pymol_open,
                        user_data=[sortnrj[i], pathres],
                    )


# Define a function to open the results directory and get the results for each software
def openres():
    tosearch = os.path.dirname(os.getcwd())
    #toopen = glob.glob(f"{tosearch}/results*")
    toopen = [path for path in glob.glob(f"{tosearch}/result*") if os.path.isdir(path)]
    for path in toopen:
        soft = path.split("_")[-1]
        print(f"SOFTWARE USED = {soft}")
        get_res(path, soft)


# Define a function to find files with a given name in a directory
def findfiles(name, dir):
    newdir = pathlib.Path(dir)
    listfile = list(newdir.rglob(name))
    liststr = [str(i) for i in listfile]
    print(liststr)
    return liststr


def openconsensus(sender, app_data, user_data):
    tosearch = os.path.dirname(os.getcwd())
    #toopen = glob.glob(f"{tosearch}/results*")
    toopen = [path for path in glob.glob(f"{tosearch}/result*") if os.path.isdir(path)]
    print(toopen)

    def compute_values():
        good = []
        for path in toopen:
            if dpg.get_value(path.split("_")[-1]):
                print(path.split("_")[-1])
                good.append([path, path.split("_")[-1]])

            print(good)
        dataframe_list = []
        for x in good:
            sortabc, sortnrj = pp.process_results(x[0], x[1])
            sortnrj = pd.DataFrame(sortnrj)
            dataframe_list.append(sortnrj)

        print(dataframe_list)
        # Find lines with the first values of the rows in common between all the dataframes

        # Merge all the dataframes in the dataframe list, according to their first column, and do the sum of the second element of the row
        df = (
            pd.concat(dataframe_list)
            .groupby(0, as_index=False)
            .agg({1: "sum", 2: "first"})
        )

        # Split each string of the first column by _, and remove the last element of the list, then reconstruct with join with _
        df[0] = df[0].apply(lambda x: "_".join(x.split("_")[:-1]))

        unique_values = df[0].unique()

        # Get the values in the second column for each element in unique_values
        print(unique_values)

        list_results_class = []
        for val in unique_values:
            values = df.loc[df[0] == val, 1].values
            list_results_class.append(
                [val, sum(values) / len(values), sum(values), len(values)]
            )

        # Sort new_col by second element of each list
        list_results_class.sort(key=lambda x: x[1])
        headers_class = [
            "Names Ligand",
            "Average of Energies",
            "Sum of Energies",
            "Number of value found",
        ]
        with dpg.window(label="Classified", width=1500, height=500):
            dpg.add_text("Results are sorted by Average of Energies")
            with dpg.table(
                header_row=True,
                resizable=True,
                borders_outerH=True,
                borders_innerV=True,
                borders_innerH=True,
                borders_outerV=True,
            ):
                for x in range(len(headers_class)):
                    print(headers_class[x])
                    dpg.add_table_column(label=headers_class[x])
                for i in range(len(list_results_class)):
                    with dpg.table_row():
                        for j in range(len(list_results_class[i])):
                            dpg.add_text(list_results_class[i][j])

    with dpg.window(label="Select results to process", width=500, height=500):
        dpg.add_text(
            "Conan has detected theses results, please select the one that you want to compair"
        )
        def check_uncheck_all_2(sender, app_data, user_data):
            check_all_2 = dpg.get_value("check_all_2")
            for path in toopen:
                dpg.set_value(path.split("_")[-1], check_all_2)
        dpg.add_checkbox(label="Check/Uncheck All", callback=check_uncheck_all_2, tag="check_all_2")

        for path in toopen:
            dpg.add_checkbox(
                label=path.split("_")[-1], default_value=False, tag=path.split("_")[-1]
            )
        dpg.add_button(label="Process", callback=compute_values)

        

    # sortabc,sortnrj = pp.process_results(pathres,soft2)


# Define a function to open a ligand and receptor in PyMOL
def pymol_open(sender, app_data, user_data):
    import pymol

    pathres = user_data[1]
    ligand = user_data[0][0]
    pathlig = findfiles(ligand, pathres)[0] + "/best.pdbqt"
    receptor = ligand.split("_")[0] + ".pdbqt"
    rec = f"{os.path.dirname(os.getcwd())}/receptors/{receptor}"
    print(f"ligand : {pathlig}, rec: {rec}")
    process = Popen(
        ["python3", "launchpymol.py", rec, pathlig], stdout=PIPE, stderr=PIPE
    )
    # data = process.communicate()
    # os.call(f"python launchpymol.py -pathrec {rec} -pathlig {pathlig}",shell=True)


def show_interactions(sender, app_data, user_data):
    pathres = user_data[1]
    ligand = user_data[0][0]
    print(pathres, ligand)
    pathlig = findfiles(ligand, pathres)[0] + "/best.pdbqt"

    def pdbqtreader(path):
        blockdata = ""
        with open(path, "r+") as pdbqt:
            # read a list of lines into data
            pdbqtcontenu = pdbqt.readlines()

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
        # print(blockdata)
        mol = Chem.rdmolfiles.MolFromPDBBlock(blockdata, sanitize=False, removeHs=False)
        return mol

    lig = pdbqtreader(pathlig)
    receptor = ligand.split("_")[0] + ".pdbqt"
    rec = pdbqtreader(f"{os.path.dirname(os.getcwd())}/receptors/{receptor}")

    ligtemp = prolif.Molecule(lig)
    rectemp = prolif.Molecule(rec)
    print(ligtemp)
    print(rectemp)

    ligpro = prolif.molecule.pdbqt_supplier(pathlig, lig)

    fp = prolif.Fingerprint(count = True)
    fp.run_from_iterable([ligtemp],rectemp)
    #ifp = fp.generate(ligtemp, rectemp,metadata=True)
    #df = prolif.to_dataframe({0: ifp}, fp.interactions)
    #print(df)
    #print(ifp)
    #ifp["Frame"] = 0
    #df = prolif.to_dataframe([ifp], fp.interactions.keys())
    net = LigNetwork.from_fingerprint(
        fp,
        ligtemp,
        # replace with `kind="frame", frame=0` for the other depiction
        kind="aggregate",
        threshold=0.3,
        rotation=270,
    )
    net.save(f"../parameters/temp_html/{ligand}.html")
    webbrowser.open(f"../parameters/temp_html/{ligand}.html", new=2)



def load():
    software = dpg.get_value("Softdock")
    if software == "Autodock-gpu":
        soft2 = "GPU"
    if software == "Autodock-vina":
        soft2 = "VINA"
    if software == "Gnina":
        soft2 = "GNINA"
    if software == "Smina":
        soft2 = "SMINA"
    if software == "Qvina":
        soft2 = "QVINA"
    if software == "Autodock4":
        soft2 = "AD4"
    pathres = dpg.get_value("pathresults")
    get_res(pathres, soft2)
    return


with dpg.window(label="Parameters", width=1200, height=1000):
    # dpg.set_main_window_size(500,500)
    dpg.add_text("Select the software used")
    dpg.add_listbox(tag="Softdock", items=softwares)
    dpg.add_text("Enter Path")

    dpg.add_input_text(tag="pathresults", width=200, label="Path for the results")
    dpg.add_button(label="Load Configuration", callback=load)
    dpg.add_button(label="Open all results found", callback=openres)
    dpg.add_button(label="Consensus Docking", callback=openconsensus)

dpg.create_viewport(title="Show results", width=600, height=600)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
