import dearpygui.dearpygui as dpg
from helper_functions import *
from pathlib import Path


#-------------------------------------------------- CALLBACK SECTION --------------------------------------------------#


# right arrow callback function
def increment_page():
    max_page_num=len(PA_names)-1
    current_page_num=PA_names.index(dpg.get_value('PA_ID'))
    if current_page_num+1<=max_page_num:
        current_page_num += 1
        dpg.set_value('PA_ID',PA_names[current_page_num])

# left arrow callback function
def decrement_page():
    min_page_num=0
    current_page_num=PA_names.index(dpg.get_value('PA_ID'))
    if current_page_num>min_page_num:
        current_page_num -= 1
        dpg.set_value('PA_ID',PA_names[current_page_num])



# start test callback function
def start_test():
    # collect input parameters from GUI
    log_file_full_path=dpg.get_value("folder_path_text")+'/'+dpg.get_value("test_name_text")+'.csv'
    print(log_file_full_path)
    num_harmonics=dpg.get_value("num_harmonics_int")
    logging_period_seconds_float=float(dpg.get_value("log_period_ms_text"))/1000.0
    extra_data_string=dpg.get_value("extra_data_text")



    # f=open("sample_response.txt",'r')
    # sample_response_string=f.readline()
    # f.close()
    # render_feedback(sample_response_string)
    pass

# stop test callback function
def stop_test():
    pass


#-------------------------------------------------- CALLBACK SECTION --------------------------------------------------#


# function for converting response string to display
def render_feedback(response_string_raw):
    response_list=response_string_raw.split(',')
    response_index=0
    for chan in channel_names:
        dpg.set_value(f'V_RMS_{chan}',prep_float_for_disp(response_list[response_index]))
        response_index+=1
        dpg.set_value(f'V_AC_{chan}',prep_float_for_disp(response_list[response_index]))
        response_index+=1
        dpg.set_value(f'V_DC_{chan}',prep_float_for_disp(response_list[response_index]))
        response_index+=1
        dpg.set_value(f'A_RMS_{chan}',prep_float_for_disp(response_list[response_index]))
        response_index+=1
        dpg.set_value(f'A_AC_{chan}',prep_float_for_disp(response_list[response_index]))
        response_index+=1
        dpg.set_value(f'A_DC_{chan}',prep_float_for_disp(response_list[response_index]))
        response_index+=1
        dpg.set_value(f'W_RMS_{chan}',prep_float_for_disp(response_list[response_index]))
        response_index+=1
        dpg.set_value(f'W_AC_{chan}',prep_float_for_disp(response_list[response_index]))
        response_index+=1
        dpg.set_value(f'W_DC_{chan}',prep_float_for_disp(response_list[response_index]))
        response_index+=1
        dpg.set_value(f'PF_{chan}',prep_float_for_disp(response_list[response_index]))
        response_index+=1






# dearpygui setup
dpg.create_context()

# feedback columns parameters
num_cols_feedback=5
channel_names=["CH1","CH2","CH3","CH4"]

# names for the power analyzers
PA_names=["XT2640 1","XT2640 2","XT2640 3","XT2640 4"]


# size GUI window based on the size of the largest display
viewport_width,viewport_height=compute_window_size()


#set sizes of all major UI elements
ctrl_width=0.5*viewport_width
fb_width=viewport_width-ctrl_width
button_window_height=int(viewport_height*0.14)
fb_height=viewport_height-button_window_height
ctrl_height=fb_height


# add a font registry, needed for having next of different sizes
with dpg.font_registry():
    #first argument ids the path to the .ttf or .otf file
    title_font = dpg.add_font("DejaVuSans.ttf", int(viewport_width*0.02))
    normal_font = dpg.add_font("DejaVuSans.ttf", int(viewport_width*0.013))
    tiny_font = dpg.add_font("DejaVuSans.ttf", int(viewport_width*0.008))
    button_font=dpg.add_font("DejaVuSans.ttf", int(viewport_width*0.05))
    feedback_font=dpg.add_font("FiraMono-Regular.ttf",int(viewport_width*0.013))

# text defaults to normal font
dpg.bind_font(normal_font)


#-------------------------------------------------- CONTROL SECTION --------------------------------------------------#
with dpg.window( pos=(0,0),width=ctrl_width,height=ctrl_height,no_move=True,no_resize=True,no_title_bar=True,tag="ctrl_window"):

    # Control section title
    dpg.add_text("CONTROL",tag="ctrl_title")
    dpg.bind_item_font("ctrl_title",title_font)
    dpg.add_spacer(height=int(viewport_height*0.05))


    with dpg.table(header_row=False):

        # set divider within control section
        dpg.add_table_column(width_fixed=True, init_width_or_weight=ctrl_width*0.3)
        dpg.add_table_column()


        # Test Name field
        with dpg.table_row():
            dpg.add_text("Test Name:")
            dpg.add_input_text(width=-1, hint=".csv appended automatically",tag="test_name_text")

        
        # Log file path field
        with dpg.table_row():
            dpg.add_text("Log File Path:")
            full_path_text=dpg.add_input_text(width=-1,default_value=Path(__file__).resolve().parent,tag="folder_path_text")
            dpg.bind_item_font(full_path_text,tiny_font)


        
        with dpg.table_row():
            dpg.add_text("Num Harmonics to Log:")
            dpg.add_input_int(tag='num_harmonics_int')

        
        with dpg.table_row():
            dpg.add_text("Logging Period (ms):")
            dpg.add_input_text(width=-1,hint="Enter integer between 100 and 10,000",tag="log_period_ms_text")

        

        with dpg.table_row():
            dpg.add_text("Test Duration (s)")
            dpg.add_input_text(width=-1,hint="Leave 0 for indefinite logging")

        

        with dpg.table_row():
            dpg.add_text("Extra Data to Log")
            dpg.add_input_text(width=-1,hint="ex. V:CH1:CF,A:CH1:CF,V:CH2:CF,A:CH2:CF",tag="extra_data_text")

       


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


with dpg.window( pos=(0,ctrl_height),width=ctrl_width,height=button_window_height,no_move=True,no_resize=True,no_title_bar=True):
    with dpg.table(header_row=False,borders_innerH=True):
        dpg.add_table_column()
        dpg.add_table_column()

        with dpg.table_row():
            decrement_button=dpg.add_button(label="     START    ",callback=start_test)
            increment_button=dpg.add_button(label="     STOP     ",callback=stop_test)
            dpg.bind_item_font(decrement_button,button_font)
            dpg.bind_item_font(increment_button,button_font)

#-------------------------------------------------- CONTROL SECTION --------------------------------------------------#




#------------------------------------------------- FEEDBACK SECTION --------------------------------------------------#

with dpg.window( pos=(ctrl_width,0),width=fb_width,height=fb_height,no_move=True,no_resize=True,no_title_bar=True):


    feedback_title=dpg.add_text("FEEDBACK")
    dpg.bind_item_font(feedback_title,title_font)
    dpg.add_spacer(height=int(viewport_height*0.05))

    with dpg.table(header_row=False,borders_innerH=True,borders_innerV=True):
        
        for x in range(num_cols_feedback):
            dpg.add_table_column()

        with dpg.table_row():
            
            dpg.add_text(PA_names[0],tag="PA_ID")
            for chan in channel_names:
                dpg.add_text(chan)


        with dpg.table_row():
            dpg.add_text("VOLTS RMS")
            for chan in channel_names:
                tag_string=f"V_RMS_{chan}"
                dpg.add_text("0.000000",tag=tag_string)
                dpg.bind_item_font(tag_string,feedback_font)


        with dpg.table_row():
            dpg.add_text("VOLTS AC")
            for chan in channel_names:
                tag_string=f"V_AC_{chan}"
                dpg.add_text("0.000000",tag=tag_string)
                dpg.bind_item_font(tag_string,feedback_font)

        with dpg.table_row():
            dpg.add_text("VOLTS DC")
            for chan in channel_names:
                tag_string=f"V_DC_{chan}"
                dpg.add_text("0.000000",tag=tag_string)
                dpg.bind_item_font(tag_string,feedback_font)

        with dpg.table_row():
            dpg.add_text("")
            for chan in channel_names:
                dpg.add_text("")

        with dpg.table_row():
            dpg.add_text("AMPS RMS")
            for chan in channel_names:
                tag_string=f"A_RMS_{chan}"
                dpg.add_text("0.000000",tag=tag_string)
                dpg.bind_item_font(tag_string,feedback_font)

        with dpg.table_row():
            dpg.add_text("AMPS AC")
            for chan in channel_names:
                tag_string=f"A_AC_{chan}"
                dpg.add_text("0.000000",tag=tag_string)
                dpg.bind_item_font(tag_string,feedback_font)

        with dpg.table_row():
            dpg.add_text("AMPS DC")
            for chan in channel_names:
                tag_string=f"A_DC_{chan}"
                dpg.add_text("0.000000",tag=tag_string)
                dpg.bind_item_font(tag_string,feedback_font)

        with dpg.table_row():
            dpg.add_text("")
            for chan in channel_names:
                dpg.add_text("")

        with dpg.table_row():
            dpg.add_text("WATTS RMS")
            for chan in channel_names:
                tag_string=f"W_RMS_{chan}"
                dpg.add_text("0.000000",tag=tag_string)
                dpg.bind_item_font(tag_string,feedback_font)

        with dpg.table_row():
            dpg.add_text("WATTS AC")
            for chan in channel_names:
                tag_string=f"W_AC_{chan}"
                dpg.add_text("0.000000",tag=tag_string)
                dpg.bind_item_font(tag_string,feedback_font)

        with dpg.table_row():
            dpg.add_text("WATTS DC")
            for chan in channel_names:
                tag_string=f"W_DC_{chan}"
                dpg.add_text("0.000000",tag=tag_string)
                dpg.bind_item_font(tag_string,feedback_font)

        with dpg.table_row():
            dpg.add_text("")
            for chan in channel_names:
                dpg.add_text("")

        with dpg.table_row():
            dpg.add_text("POWER FACTOR")
            for chan in channel_names:
                tag_string=f"PF_{chan}"
                dpg.add_text("0.000000",tag=tag_string)
                dpg.bind_item_font(tag_string,feedback_font)


with dpg.window( pos=(ctrl_width,fb_height),width=fb_width,height=button_window_height,no_move=True,no_resize=True,no_title_bar=True):
    with dpg.table(header_row=False,borders_innerH=True):
        dpg.add_table_column()
        dpg.add_table_column()

        with dpg.table_row():
            decrement_button=dpg.add_button(label="      <<      ",callback=decrement_page)
            increment_button=dpg.add_button(label="      >>     ",callback=increment_page)
            dpg.bind_item_font(decrement_button,button_font)
            dpg.bind_item_font(increment_button,button_font)



#------------------------------------------------- FEEDBACK SECTION --------------------------------------------------#


dpg.create_viewport(title='Xitron GUI', width=viewport_width, height=viewport_height,resizable=False)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
