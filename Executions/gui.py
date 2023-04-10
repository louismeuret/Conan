import dearpygui.dearpygui as dpg
import sys
import glob
import docklaunch as dckl
import psutil
import re
import os
from subprocess import Popen, PIPE
dpg.create_context()
dpg.create_viewport(title='Conan', width=800, height=500)

dpg.show_metrics()

def boutonsave(sender, data):
    #dpg.get_value(Sender)
    print(dpg.get_value("nptsx"))
    print(dpg.get_value("Softdock"))

def delete_second_window(sender):
    dpg.delete_item(sender)

def save_file():
    path = dpg.get_value("pathconfig")
    f = open(path,"w+")
    software = dpg.get_value("Softdock")
    if software == "Autodock-gpu" : soft2 = "gpu"
    if software == "Autodock-vina" : soft2 = "vina"
    if software == "Gnina" : soft2 = "gnina"
    if software == "Smina" : soft2 = "smina"
    if software == "Qvina" : soft2 = "qvina"
    if software == "Autodock4": soft2 = "AD4"
    f.write("#SOFTWARE# "+soft2+" \n")
    f.write("#DEBUG# "+dpg.get_value("debug")+" \n")
    f.write("#THREADS# "+dpg.get_value("threads")+" \n")
    f.write("#NRUNS# "+dpg.get_value("nruns")+" \n")
    f.write("#PATHDB# "+dpg.get_value("db")+" \n")
    f.write("#SPACING# "+dpg.get_value("spacing")+" \n")
    f.write("#CENTERX# "+dpg.get_value("gridcenterx")+" \n")
    f.write("#CENTERY# "+dpg.get_value("gridcentery")+" \n")
    f.write("#CENTERZ# "+dpg.get_value("gridcenterz")+" \n")
    f.write("#SIZEX# "+dpg.get_value("nptsx")+" \n")
    f.write("#SIZEY# "+dpg.get_value("nptsy")+" \n")
    f.write("#SIZEZ# "+dpg.get_value("nptsz")+" \n")
    f.close()
    return
 
def load_file():
    with open(dpg.get_value("pathconfig2")) as f:
        lines = f.readlines()
    for x in range(len(lines)):

        if (re.findall(r'\S+', lines[x])[0] == "#SOFTWARE#"):
            # /home/louis/Téléchargements/Conansuite/Executions/test.txt
            if re.findall(r'\S+', lines[x])[1].strip() == "vina":
                print("test")
                dpg.set_value("Softdock",softwares[1])
                print("found vina")
            if re.findall(r'\S+', lines[x])[1].strip() == "gpu":
                dpg.set_value("Softdock",softwares[0])
            if re.findall(r'\S+', lines[x])[1].strip() == "gnina":
                dpg.set_value("Softdock",softwares[2])
            if re.findall(r'\S+', lines[x])[1].strip() == "smina":
                dpg.set_value("Softdock",softwares[3])
            if re.findall(r'\S+', lines[x])[1].strip() == "qvina":
                dpg.set_value("Softdock",softwares[4])
            if re.findall(r'\S+', lines[x])[1].strip() == "autodock4":
                dpg.set_value("Softdock",softwares[4])


        if re.findall(r'\S+', lines[x])[0] == "#DEBUG#":
            if re.findall(r'\S+', lines[x])[1].strip() == "yes":
                dpg.set_value("debug","True")
            if re.findall(r'\S+', lines[x])[1].strip() == "no":
                dpg.set_value("debug","False")
                
        if re.findall(r'\S+', lines[x])[0] == "#THREADS#":
            dpg.set_value("threads",re.findall(r'\S+', lines[x])[1].strip())

        if re.findall(r'\S+', lines[x])[0] == "#NRUNS#":
            dpg.set_value("nruns",re.findall(r'\S+', lines[x])[1].strip())
            
        if re.findall(r'\S+', lines[x])[0] == "#PATHDB#":
            dpg.set_value("db",re.findall(r'\S+', lines[x])[1].strip())
            
        if re.findall(r'\S+', lines[x])[0] == "#SPACING#":
            dpg.set_value("spacing",re.findall(r'\S+', lines[x])[1].strip())
        if re.findall(r'\S+', lines[x])[0] == "#CENTERX#":
            dpg.set_value("gridcenterx",re.findall(r'\S+', lines[x])[1].strip())
        if re.findall(r'\S+', lines[x])[0] == "#CENTERY#":
            dpg.set_value("gridcentery",re.findall(r'\S+', lines[x])[1].strip())
        if re.findall(r'\S+', lines[x])[0] == "#CENTERZ#":
            dpg.set_value("gridcenterz",re.findall(r'\S+', lines[x])[1].strip())
        if re.findall(r'\S+', lines[x])[0] == "#SIZEX#":
            dpg.set_value("nptsx",re.findall(r'\S+', lines[x])[1].strip())
        if re.findall(r'\S+', lines[x])[0] == "#SIZEY#":
            dpg.set_value("nptsy",re.findall(r'\S+', lines[x])[1].strip())
        if re.findall(r'\S+', lines[x])[0] == "#SIZEZ#":
            dpg.set_value("nptsz",re.findall(r'\S+', lines[x])[1].strip())
            
    print(dpg.get_value("Softdock"))
    
    
    
def save_config(sender):
    with dpg.window(label="Save", width=200, height=200, pos=(100, 100), tag="saveconfig",on_close=delete_second_window):
        dpg.add_input_text(tag="pathconfig",width=150) 
        dpg.add_button(label="Save File",tag="saveconf",callback=save_file)
        #dpg.add_text(f"CPU usage:{psutil.cpu_percent()}%, Memory usage: {psutil.virtual_memory().percent}%", tag="usage")

def load_config(sender):
    with dpg.window(label="Load", width=200, height=200, pos=(100, 100), tag="loadconfig",on_close=delete_second_window):
        dpg.add_input_text(tag="pathconfig2",width=150) 
        dpg.add_button(label="Load File",tag="loadconf",callback=load_file)
        
#dckl.dockingtot("VINA","90","75","85","55","-21","-20","0.375","1","100","/home/louis/Téléchargements/dbtest/",True)
def run(sender,data):
    software = dpg.get_value("Softdock")
    if software == "Autodock-gpu" : soft = "GPU"
    if software == "Autodock-vina" : soft = "VINA"
    if software == "Gnina" : soft = "GNINA"
    if software == "Smina" : soft = "SMINA"
    if software == "Qvina" : soft = "QVINA"
    if software == "Autodock4" : soft = "AD4"

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
    if dpg.get_value("debug")=="True":
        debug = True
    else:
        debug = False
    dckl.dockingtot(soft,nptsx,nptsy,nptsz,gridcenterx,gridcentery,gridcenterz,spacing,threads,nruns,pathdb2,debug)
    
def view_grid(sender,data):
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
        txtrec = txtrec + x+"\n"
    file = open(pathfilerec,"w")#append mode
    file.write(txtrec)
    file.close()
    print(f"python ../parametres/viewreceptor.py {nptsx} {nptsy} {nptsz} {gridcenterx} {gridcentery} {gridcenterz}")
    process = Popen(["python","../parametres/viewreceptor.py",str(nptsx),str(nptsy),str(nptsz),str(gridcenterx),str(gridcentery),str(gridcenterz)],stdout=PIPE,stderr=PIPE)
    #viewer.viewreceptor(pathrecs,nptsx,nptsy,nptsz,gridcenterx,gridcentery,gridcenterz)

    
    
def print_me(sender,data):
    print(f"Menu Item: {sender}{data}")
    
def setdb(sender,data):
    pathdb = dpg.get_value("db")
    listofpdbqt = glob.glob(f'{pathdb}/**/*.pdbqt', recursive=True)
    print(len(listofpdbqt))
    if len(listofpdbqt)==0:
        dpg.set_value("textdb","No pdbqt detected on this path")
    else:
        dpg.set_value("textdb",f"Found {len(listofpdbqt)} ligands on this path")

def close(sender,data):
    sys.exit() 

def validation(sender, app_data):
    print("App Data: ", app_data)
    print(app_data["file_path_name"])
    dpg.set_value("db",app_data["file_path_name"])

def cancel_callback(sender, app_data):
    print('Cancel was clicked.')
    print("Sender: ", sender)
    print("App Data: ", app_data)
"""
def on_render(sender, data):
    #dpgc.get_total_time()
    dpg.set_value("usage",f"CPU usage: {psutil.cpu_percent()}%, Memory usage: {psutil.virtual_memory().percent}%", tag="usage")
    print("test")
""" 

def update():
    dpg.set_value("usage",f"CPU usage:{psutil.cpu_percent()}%, Memory usage: {psutil.virtual_memory().percent}%")
    
softwares = ["Autodock-gpu","Autodock-vina","Autodock4","Gnina","Smina","Qvina"]
with dpg.window(label="Parameters",width=500,height=500):
    #dpg.set_main_window_size(500,500)
    dpg.add_text("Conan")
    dpg.add_button(label="Load Configuration",callback=load_config)
    dpg.add_listbox(tag="Softdock",items=softwares)
    dpg.add_text("Number of points in the grid")
    dpg.add_text("  X  --- Y ---  Z")
    with dpg.group(horizontal=True):
        dpg.add_input_text(tag="nptsx",width=40)
        #dpg.add_same_line()
        dpg.add_input_text(tag="nptsy",width=40)
        #dpg.add_same_line()
        dpg.add_input_text(tag="nptsz",width=40)
        
    dpg.add_text("Center of the grid")
    dpg.add_text("  X  --- Y ---  Z")
    with dpg.group(horizontal=True):
        dpg.add_input_text(tag="gridcenterx",width=40)
        #dpg.add_same_line()
        dpg.add_input_text(tag="gridcentery",width=40)
        #dpg.add_same_line()
        dpg.add_input_text(tag="gridcenterz",width=40)
    #dpg.add_text("Spacing (Angstrom)")   
    dpg.add_input_text(tag="spacing",width=40,label="Spacing (Angstrom)")
    dpg.add_button(label="View grid in Pymol",callback=view_grid) 
    #dpg.add_text("Number of Runs             Number of Threads")  

    dpg.add_input_text(tag="nruns",width=40,label="Number of Genetic Runs")  
    dpg.add_input_text(tag="threads",width=40,label="Number of Threads")
    dpg.add_text("Path of Database:")  
    with dpg.group(horizontal=True):
        dpg.add_input_text(tag="db",width=150) 
        dpg.add_file_dialog(directory_selector=True, show=False, callback=validation, tag="file_dialog_id",cancel_callback=cancel_callback)
        dpg.add_button(label="Directory Selector", callback=lambda: dpg.show_item("file_dialog_id"))
    dpg.add_button(label="Set",callback=setdb)
    dpg.add_text("No database selected yet", tag="textdb")
    dpg.add_text("Enable Debugging:")
    dpg.add_radio_button(tag="debug",items = ["True","False"],horizontal=True)
    with dpg.group(horizontal=True):
        dpg.add_button(label="Save",callback=boutonsave)
        dpg.add_button(label="Run",callback=run)
    dpg.add_button(label="Close",callback=close)
    dpg.add_button(label="Save Configuration",callback=save_config)
    #dpg.add_text(f"CPU usage:{psutil.cpu_percent()}%, Memory usage: {psutil.virtual_memory().percent}%", tag="usage")
    


    
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
