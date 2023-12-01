#from dearpygui_ext import logger
#logger.mvLogger()
import dearpygui.dearpygui as dpg
from dearpygui_ext import logger
import sys
import glob
import docklaunch as dckl
import psutil

def delete_second_window(sender):
    dpg.delete_item("secondwindow")

def launch_window():
    with dpg.window(label="Running", width=200, height=200, pos=(100, 100),tag="secondwindow"):
        dpg.add_button(label="Delete second",small=True,callback=delete_second_window)
        dpg.add_text(f"CPU usage:{psutil.cpu_percent()}%, Memory usage: {psutil.virtual_memory().percent}%", tag="usage")
        
dpg.create_context()


dpg.create_viewport(title='Conan', width=800, height=500)   
    
with dpg.window(label="Parameters",width=500,height=500):
    #dpg.set_main_window_size(500,500)
    dpg.add_text("Conan")
    dpg.add_button(label="Launch Window",callback=launch_window)
    #dpg.add_text(f"CPU usage:{psutil.cpu_percent()}%, Memory usage: {psutil.virtual_memory().percent}%", tag="usage")
    


    
dpg.setup_dearpygui()
dpg.show_viewport()

while dpg.is_dearpygui_running():
    # insert here any code you would like to run in the render loop
    # you can manually stop by using stop_dearpygui()

    dpg.set_value("usage",f"CPU usage:{psutil.cpu_percent()}%, Memory usage: {psutil.virtual_memory().percent}%")
    dpg.render_dearpygui_frame()

dpg.start_dearpygui()
dpg.destroy_context()  
