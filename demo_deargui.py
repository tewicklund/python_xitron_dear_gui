import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
from functions import *

dpg.create_context()

auto_width, auto_height = compute_window_size()
dpg.create_viewport(title='Custom Title', width=auto_width, height=auto_height)

demo.show_demo()

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
