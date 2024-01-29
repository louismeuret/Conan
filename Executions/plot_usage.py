import dearpygui.dearpygui as dpg
import time
import collections
import threading
import psutil

nsamples = 50

# Data queues for CPU and RAM usage
cpu_data_y = collections.deque([0.0] * nsamples, maxlen=nsamples)
ram_data_y = collections.deque([0.0] * nsamples, maxlen=nsamples)
data_x = collections.deque([0.0] * nsamples, maxlen=nsamples)

def fetch_system_usage():
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    return cpu_usage, ram_usage

def update_data():
    t0 = time.time()
    while True:
        # Get new data sample
        t = time.time() - t0
        cpu_usage, ram_usage = fetch_system_usage()

        # Update data queues
        data_x.append(t)
        cpu_data_y.append(cpu_usage)
        ram_data_y.append(ram_usage)
        
        # Update the series with new data
        dpg.set_value('cpu_series_tag', [list(data_x), list(cpu_data_y)])
        dpg.set_value('ram_series_tag', [list(data_x), list(ram_data_y)])
        dpg.fit_axis_data('x_axis')
        dpg.set_axis_limits("y_axis", 0, 100)
        #dpg.fit_axis_data('y_axis')
        
        time.sleep(1)  # Adjust the sleep time as needed

dpg.create_context()
with dpg.window(label='System Monitor', tag='win', width=800, height=600):
    with dpg.plot(label='System Usage', height=400, width=400):
        dpg.add_plot_legend()
        x_axis = dpg.add_plot_axis(dpg.mvXAxis, label='Time (s)', tag='x_axis',time=True,)
        y_axis = dpg.add_plot_axis(dpg.mvYAxis, label='Usage (%)', tag='y_axis')

        # CPU and RAM usage series
        dpg.add_line_series(x=list(data_x), y=list(cpu_data_y), label='CPU Usage (%)', parent='y_axis', tag='cpu_series_tag')
        dpg.add_line_series(x=list(data_x), y=list(ram_data_y), label='RAM Usage (%)', parent='y_axis', tag='ram_series_tag')
            
dpg.create_viewport(title='System Monitor', width=850, height=640)
dpg.setup_dearpygui()
dpg.show_viewport()

thread = threading.Thread(target=update_data)
thread.start()
dpg.start_dearpygui()

dpg.destroy_context()
