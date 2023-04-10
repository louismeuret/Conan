import dearpygui.dearpygui as dpg
import glob
import postprocess as pp
import os
import os.path
from prolif.plotting.network import LigNetwork
#import MDAnalysis as mda
import prolif
from rdkit import Chem
import pathlib
import webbrowser
from subprocess import Popen, PIPE
from multiprocessing import Process

dpg.create_context()
dpg.create_viewport(title='Conan', width=1200, height=500)
softwares = ["Autodock-gpu","Autodock-vina","Autodock4","Gnina","Smina","Qvina"]
headersall = ["Nom ligand","Energy","LogP","MolWt","Complexity"]
headersgnina = ["Nom ligand","Energy","CNNscore","CNNactivity","LogP","MolWt","Complexity"]
def get_res(pathres,soft2):
    sortabc,sortnrj = pp.process_results(pathres,soft2)
    with dpg.window(label=soft2,width=1200,height=500):
        with dpg.table(header_row=False,resizable=True,borders_outerH=True, borders_innerV=True, borders_innerH=True, borders_outerV=True):
            if len(sortabc[0]) == 6:
                for x in range(len(sortabc[0])+2):
                    dpg.add_table_column()
            else:
                for x in range(len(sortabc[0])+2):
                    dpg.add_table_column()

            for i in range(len(sortabc)):
                with dpg.table_row():
                    for j in range(len(sortabc[i])):
                        dpg.add_text(sortabc[i][j])
                    dpg.add_button(label="Show interactions",callback=show_interactions,user_data=[sortabc[i],pathres])
                    dpg.add_button(label="Open in Pymol", callback=pymol_open,user_data=[sortabc[i],pathres])

def openres():
    tosearch = os.path.dirname(os.getcwd())
    toopen = glob.glob(f'{tosearch}/results*')
    for path in toopen:
        soft = path.split("_")[1]
        get_res(path,soft)

def findfiles(name,dir):
    newdir = pathlib.Path(dir)
    listfile = list(newdir.rglob(name))
    liststr = [str(i) for i in listfile]
    print(liststr)
    return liststr

def pymol_open(sender, app_data, user_data):
    import pymol
    pathres = user_data[1]
    ligand = user_data[0][0]
    pathlig = findfiles(ligand,pathres)[0] + "/best.pdbqt"
    receptor = ligand.split("_")[0]+".pdbqt"
    rec = f"{os.path.dirname(os.getcwd())}/receptors/{receptor}"
    print(f"ligand : {pathlig}, rec: {rec}")
    process = Popen(["python","launchpymol.py",rec,pathlig],stdout=PIPE,stderr=PIPE)
    #data = process.communicate()
    #os.call(f"python launchpymol.py -pathrec {rec} -pathlig {pathlig}",shell=True)

def show_interactions(sender, app_data, user_data):
    pathres = user_data[1]
    ligand = user_data[0][0]
    print(pathres,ligand)
    pathlig = findfiles(ligand,pathres)[0] + "/best.pdbqt"
    def pdbqtreader(path):
        blockdata = ""
        with open(path, "r+") as pdbqt:
            # read a list of lines into data
            pdbqtcontenu = pdbqt.readlines()

        for x in range(len(pdbqtcontenu)):
            if pdbqtcontenu[x][:4] == "ATOM" or pdbqtcontenu[x][:6] == "HETATM":
                templine = pdbqtcontenu[x].split()
                pdbqtcontenu[x] = pdbqtcontenu[x][:-3]
                pdbqtcontenu[x] = pdbqtcontenu[x]+templine[2][:1]+"\n"
                blockdata = blockdata + pdbqtcontenu[x]
                #print(x)
            if pdbqtcontenu[x][:6] == "ENDMDL":
                print("break")
                break
        #print(blockdata)
        mol = Chem.rdmolfiles.MolFromPDBBlock(blockdata,sanitize=False,removeHs=False)
        return mol

    lig = pdbqtreader(pathlig)
    receptor = ligand.split("_")[0]+".pdbqt"
    rec = pdbqtreader(f"{os.path.dirname(os.getcwd())}/receptors/{receptor}")

    ligtemp = prolif.Molecule(lig)
    rectemp = prolif.Molecule(rec)

    ligpro = prolif.molecule.pdbqt_supplier(pathlig,lig)

    fp = prolif.Fingerprint()
    ifp = fp.generate(ligtemp, rectemp, return_atoms=True)
    ifp["Frame"] = 0
    df = prolif.to_dataframe([ifp],fp.interactions.keys(),return_atoms=True)
    net = LigNetwork.from_ifp(
        df,
        ligtemp,
        # replace with `kind="frame", frame=0` for the other depiction
        kind="aggregate",
        threshold=0.3,
        rotation=270,
    )
    net.save(f"../parametres/temp_html/{ligand}.html")
    webbrowser.open(f"../parametres/temp_html/{ligand}.html", new=2)

            

def load():
    software = dpg.get_value("Softdock")
    if software == "Autodock-gpu" : soft2 = "GPU"
    if software == "Autodock-vina" : soft2 = "VINA"
    if software == "Gnina" : soft2 = "GNINA"
    if software == "Smina" : soft2 = "SMINA"
    if software == "Qvina" : soft2 = "QVINA"
    if software == "Autodock4": soft2 = "AD4"
    pathres = dpg.get_value("pathresults")
    get_res(pathres,soft2)
    return

with dpg.window(label="Parameters",width=1200,height=1000):
    #dpg.set_main_window_size(500,500)
    dpg.add_text("Select the software used")
    dpg.add_listbox(tag="Softdock",items=softwares)
    dpg.add_text("Enter Path")

    dpg.add_input_text(tag="pathresults",width=200,label="Path for the results")
    dpg.add_button(label="Load Configuration",callback=load)
    dpg.add_button(label="Open all results found",callback=openres)

dpg.create_viewport(title='Show results', width=1200, height=600)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

