import dearpygui.dearpygui as dpg
from screeninfo import get_monitors
from functions import *
from pathlib import Path

# dearpygui setup
dpg.create_context()

# temp placeholder
num_channels=12
channel_names=["Parameter","CH1","CH2","CH3","CH4"]
num_channels=len(channel_names)


# size GUI window based on the size of the largest display
viewport_width,viewport_height=compute_window_size()

#set the divider between control section and feedback section of GUI
ctrl_width=0.5*viewport_width
feedback_width=viewport_width-ctrl_width


# add a font registry, needed for having next of different sizes
with dpg.font_registry():
    #first argument ids the path to the .ttf or .otf file
    title_font = dpg.add_font("DejaVuSans.ttf", int(viewport_width*0.02))
    normal_font = dpg.add_font("DejaVuSans.ttf", int(viewport_width*0.013))
    tiny_font = dpg.add_font("DejaVuSans.ttf", int(viewport_width*0.008))

# text defaults to normal font
dpg.bind_font(normal_font)


#-------------------------------------------------- CONTROL SECTION --------------------------------------------------#

with dpg.window( pos=(0,0),width=ctrl_width,height=viewport_height,no_move=True,no_resize=True,no_title_bar=True):

    # Control section title
    ctrl_title=dpg.add_text("CONTROL",pos=[ctrl_width/2-100,0])
    dpg.bind_item_font(ctrl_title,title_font)


    with dpg.table(header_row=False):

        # set divider within control section
        dpg.add_table_column(width_fixed=True, init_width_or_weight=ctrl_width*0.3)
        dpg.add_table_column()


        with dpg.table_row():
            dpg.add_text(" ")
            dpg.add_text(" ")

        # Test Name field
        with dpg.table_row():
            dpg.add_text("Test Name:")
            dpg.add_input_text(width=-1, hint=".csv appended automatically")

        with dpg.table_row():
            dpg.add_text(" ")
            dpg.add_text(" ")

        # Log file path field
        with dpg.table_row():
            dpg.add_text("Log File Path:")
            full_path_text=dpg.add_input_text(width=-1,default_value=Path(__file__).resolve().parent)
            dpg.bind_item_font(full_path_text,tiny_font)


        with dpg.table_row():
            dpg.add_text(" ")
            dpg.add_text(" ")

        with dpg.table_row():
            dpg.add_text("Num Harmonics to Log:")
            dpg.add_input_int()

        with dpg.table_row():
            dpg.add_text(" ")
            dpg.add_text(" ")

        with dpg.table_row():
            dpg.add_text("Logging Period (ms):")
            dpg.add_input_text(width=-1,hint="Enter integer between 100 and 10,000")

        with dpg.table_row():
            dpg.add_text(" ")
            dpg.add_text(" ")

        with dpg.table_row():
            dpg.add_text("Test Duration (s)")
            dpg.add_input_text(width=-1,hint="Leave 0 for indefinite logging")

        with dpg.table_row():
            dpg.add_text(" ")
            dpg.add_text(" ")

        with dpg.table_row():
            dpg.add_text("Extra Data to Log")
            dpg.add_input_text(width=-1,hint="ex. V:CH1:CF,A:CH1:CF,V:CH2:CF,A:CH2:CF")

        with dpg.table_row():
            dpg.add_text(" ")
            dpg.add_text(" ")


        with dpg.table_row():
            dpg.add_text(" ")
            dpg.add_text(" ")

        # Xitron network details
        for x in range(4):
            print(f"creating xitron ip section {x+1}")
            with dpg.table_row():
                dpg.add_text(f"Xitron {x+1} IP Address:")
                dpg.add_input_text(width=-1)

            with dpg.table_row():
                dpg.add_text(f"Xitron {x+1} Port:")
                dpg.add_input_text(width=-1)

            with dpg.table_row():
                dpg.add_text(" ")
                dpg.add_text(" ")




#-------------------------------------------------- CONTROL SECTION --------------------------------------------------#




#------------------------------------------------- FEEDBACK SECTION --------------------------------------------------#

with dpg.window( pos=(ctrl_width,0),width=feedback_width,height=viewport_height,no_move=True,no_resize=True,no_title_bar=True):


    feedback_title=dpg.add_text("FEEDBACK",pos=[feedback_width/2-100,0])
    dpg.bind_item_font(feedback_title,title_font)

    with dpg.table(header_row=False):
        with dpg.table_row():
            dpg.add_text(" ")
            dpg.add_text(" ")
        with dpg.table_row():
            dpg.add_text(" ")
            dpg.add_text(" ")
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

#------------------------------------------------- FEEDBACK SECTION --------------------------------------------------#


dpg.create_viewport(title='Xitron GUI', width=viewport_width, height=viewport_height,resizable=False)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
