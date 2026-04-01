import dearpygui.dearpygui as dpg
from screeninfo import get_monitors
from functions import *

# dearpygui setup
dpg.create_context()

# temp placeholder
num_channels=12
channel_names=["Parameter","CH1","CH2","CH3","CH4"]
num_channels=len(channel_names)



viewport_width,viewport_height=compute_window_size()

ctrl_width=0.4*viewport_width
feedback_width=viewport_width-ctrl_width



# add a font registry
with dpg.font_registry():
    #first argument ids the path to the .ttf or .otf file
    title_font = dpg.add_font("DejaVuSans.ttf", int(viewport_width*0.02))
    normal_font = dpg.add_font("DejaVuSans.ttf", int(viewport_width*0.01))

dpg.bind_font(normal_font)

with dpg.window( pos=(0,0),width=ctrl_width,height=viewport_height,no_move=True,no_resize=True,no_title_bar=True):
    with dpg.table(header_row=False):
        dpg.add_table_column(width_fixed=True, init_width_or_weight=ctrl_width*0.3)
        dpg.add_table_column()

        with dpg.table_row():
            ctrl_title=dpg.add_text("Control")
        dpg.bind_item_font(ctrl_title,title_font)


        with dpg.table_row():
            dpg.add_text("Test Name:")
            dpg.add_input_text(width=-1)



        with dpg.table_row():
            dpg.add_text("Number of Harmonics:")
            dpg.add_input_int()


with dpg.window( pos=(ctrl_width,0),width=feedback_width,height=viewport_height,no_move=True,no_resize=True,no_title_bar=True):
    with dpg.table(header_row=False):
        for chan in channel_names:
            dpg.add_table_column(label=chan)


        with dpg.table_row():
            for chan in channel_names:
                dpg.add_text(chan)

        with dpg.table_row():
            dpg.add_text("VOLTS RMS")
            for chan in channel_names:
                dpg.add_text("0.0000")


        with dpg.table_row():
            dpg.add_text("VOLTS AC")
            for chan in channel_names:
                dpg.add_text("0.0000")

        with dpg.table_row():
            dpg.add_text("VOLTS DC")
            for chan in channel_names:
                dpg.add_text("0.0000")

        with dpg.table_row():
            dpg.add_text("")
            for chan in channel_names:
                dpg.add_text("")

        with dpg.table_row():
            dpg.add_text("AMPS RMS")
            for chan in channel_names:
                dpg.add_text("0.0000")

        with dpg.table_row():
            dpg.add_text("AMPS AC")
            for chan in channel_names:
                dpg.add_text("0.0000")

        with dpg.table_row():
            dpg.add_text("AMPS DC")
            for chan in channel_names:
                dpg.add_text("0.0000")

        with dpg.table_row():
            dpg.add_text("")
            for chan in channel_names:
                dpg.add_text("")

        with dpg.table_row():
            dpg.add_text("WATTS RMS")
            for chan in channel_names:
                dpg.add_text("0.0000")

        with dpg.table_row():
            dpg.add_text("WATTS AC")
            for chan in channel_names:
                dpg.add_text("0.0000")

        with dpg.table_row():
            dpg.add_text("WATTS DC")
            for chan in channel_names:
                dpg.add_text("0.0000")

        with dpg.table_row():
            dpg.add_text("")
            for chan in channel_names:
                dpg.add_text("")

        with dpg.table_row():
            dpg.add_text("POWER FACTOR")
            for chan in channel_names:
                dpg.add_text("0.0000")


# with dpg.group(horizontal=True):
#     dpg.add_text("Number of Harmonics:")
#     dpg.add_slider_int(default_value=0,max_value=100,min_value=0,width=viewport_width*0.2)
#
#
# with dpg.window(label="Control", pos=(0,0),width=viewport_width/2,height=viewport_height,no_move=True):
#     with dpg.group(horizontal=True):
#         dpg.add_text("Number of Harmonics:")
#         dpg.add_slider_int(default_value=0,max_value=100,min_value=0,width=viewport_width*0.2)
#     test_name_input_text=dpg.add_input_text(label="Test Name", default_value="test1")
#     dpg.add_slider_int(label="Number of Harmonics",default_value=0,max_value=100,min_value=0,width=viewport_width*0.2)
#     dpg.bind_item_font(test_name_input_text,normal_font)
#     pass
#
# with dpg.window(label="Feedback", pos=(viewport_width/2,0),width=viewport_width/2,height=viewport_height,no_move=True):
#     pass

dpg.create_viewport(title='Xitron GUI', width=viewport_width, height=viewport_height,resizable=False)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
