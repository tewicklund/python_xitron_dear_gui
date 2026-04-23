import dearpygui.dearpygui as dpg
from pathlib import Path
import time
import socket
import threading
from helper_functions import *
import json

# threading event to make stop button work
stop_event=threading.Event()

#-------------------------------------------------- MISC SECTION --------------------------------------------------#

def load_from_json():
    with open('test_parameter_config.json') as f:
        parameters_from_json=json.load(f)
    
    dpg.set_value('test_name_text',parameters_from_json['test_name'])
    parent_path=parameters_from_json['log_file_path']
    if parent_path != '':
        dpg.set_value('folder_path_text',parameters_from_json['log_file_path'])
    dpg.set_value('num_harmonics_int',parameters_from_json['num_harmonics'])
    dpg.set_value('log_period_text',parameters_from_json['logging_period'])
    dpg.set_value('test_duration_text',parameters_from_json['test_duration'])
    dpg.set_value('extra_data_text',parameters_from_json['extra_data'])


def open_pa_sockets():
    PA_sockets=[]
    for x in range(len(PA_names)):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        pa_ip=dpg.get_value(f'PA_IP{x+1}')
        pa_port=dpg.get_value(f'PA_port{x+1}')
        if pa_ip != "" and pa_port != "":
            s.connect((pa_ip,int(pa_port)))
            s.settimeout(1)
            PA_sockets.append(s)
    return PA_sockets

def close_pa_sockets(pa_sockets):
    for socket in pa_sockets:
        try:
            socket.close()
        except:
            pass

def get_xitron_IPs(tcp_port):
    # get base of IP, ex "192.168.99.""
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip=s.getsockname()[0]
    finally:
        s.close()
    ip_parts=ip.split('.')
    subnet_base_string=''
    for x in range(3):
        subnet_base_string+=ip_parts[x]+'.'
    print(f'On subnet {subnet_base_string}')

    #try every IP on subnet for xitron presence
    xitron_ip_list=[]
    for x in range(2,255):
        dpg.set_value(loading_bar_id,float(x)/float(255))
        resp=""
        test_ip=subnet_base_string+str(x)
        print(f"trying ip {test_ip}")
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.03)
            s.connect((test_ip,tcp_port))
            s.sendall(b"*IDN?\n")
            resp = s.recv(1024).decode()
        except:
            print(f'Nothing at {test_ip}')
        finally:
            s.close()
        if "XT2640" in resp:
            print(f'Success! IP {test_ip} is an XT2640')
            xitron_ip_list.append(test_ip)
        else:
            print(f'No XT2640 at {test_ip}')
    dpg.set_value(loading_bar_id,0)
    return xitron_ip_list

#-------------------------------------------------- MISC SECTION --------------------------------------------------#


#-------------------------------------------------- CALLBACK SECTION --------------------------------------------------#

def save_to_json_callback():
    test_parameter_dict={
        'test_name':dpg.get_value('test_name_text'),
        'log_file_path':dpg.get_value('folder_path_text'),
        'num_harmonics':dpg.get_value('num_harmonics_int'),
        'logging_period':dpg.get_value('log_period_text'),
        'test_duration':dpg.get_value('test_duration_text'),
        'extra_data':dpg.get_value('extra_data_text')
        }
    with open('test_parameter_config.json','w') as f:
        json.dump(test_parameter_dict,f)

def get_pa_addresses_callback():
    dpg.set_value("get_ip_status_text","Please Wait, getting IPs...")
    pa_address_list=get_xitron_IPs(10733)
    for x in range(len(PA_names)):
        ip_value=pa_address_list[x] if len(pa_address_list) > x else ""
        port_value=10733 if len(pa_address_list) > x else ""
        dpg.set_value(f'PA_IP{x+1}',ip_value)
        dpg.set_value(f'PA_port{x+1}',port_value)
    dpg.set_value("get_ip_status_text","Got IP Addresses and Ports")


# right arrow callback function
def right_arrow_callback():
    max_page_num=len(PA_names)-1
    current_page_num=PA_names.index(dpg.get_value('PA_ID'))
    if current_page_num+1<=max_page_num:
        current_page_num += 1
        dpg.set_value('PA_ID',PA_names[current_page_num])

# left arrow callback function
def left_arrow_callback():
    min_page_num=0
    current_page_num=PA_names.index(dpg.get_value('PA_ID'))
    if current_page_num>min_page_num:
        current_page_num -= 1
        dpg.set_value('PA_ID',PA_names[current_page_num])

# START button callback function
def start_test():

    # clear the stop event in case the last session was stopped 
    stop_event.clear()

    # start main test script in another thread, allowing GUI updates and button presses while main script runs
    threading.Thread(target=worker, daemon=True).start()


# main test worker function
def worker():

    # set indicator bool test_running to True
    global test_running
    test_running=True
    indefinite_logging=False

    # collect input parameters from GUI
    log_file_full_path=dpg.get_value("folder_path_text")+'/'+dpg.get_value("test_name_text")+'.csv'

    num_harmonics=dpg.get_value("num_harmonics_int")

    logging_period_seconds_float=float(dpg.get_value("log_period_text"))
    if logging_period_seconds_float<=0.2:
        print("FAST SAMPLING MODE: logging period <= 200ms, no terminal or GUI feedback, wait for Done!")    
    fast_mode=(logging_period_seconds_float<0.200)

    if dpg.get_value("test_duration_text") == "":
        indefinite_logging=True
        num_samples=10
    else:
        test_duration_seconds_float=float(dpg.get_value("test_duration_text"))
        # compute number of samples
        num_samples=int(test_duration_seconds_float/logging_period_seconds_float)

    extra_data_string=dpg.get_value("extra_data_text")

    
    
    # make a list of query strings to send to analyzer, limit of 480 char response
    query_string_list=build_query_string_list("ch1_q_string.txt",num_harmonics,extra_data_string)

    # make a list of zeros to render if no analyzer connected
    zeros_resp_string=""
    for x in range(44):
        zeros_resp_string+="0.0000,"
    

    # open sockets for power analyzers
    PA_sockets=open_pa_sockets()
    

    # main test loop
    with open(log_file_full_path,'w') as f:

        
        # add column headers to first row
        f.write("Timestamp Epoch ms,")
        for socket_num in range(len(PA_sockets)):
            for subquery in query_string_list:
                column_headers_per_analyzer=subquery.removeprefix('READ?,').removesuffix('\n')+','
                column_headers_per_analyzer=column_headers_per_analyzer.replace(',',f':PA{socket_num+1},')
                f.write(column_headers_per_analyzer)
        f.write('\n')

        # add column headers to backup file
        if not fast_mode:
            backup_f=open(log_file_full_path+'.bak','w')
            # add column headers to first row
            backup_f.write("Timestamp Epoch ms,")
            for socket_num in range(len(PA_sockets)):
                for subquery in query_string_list:
                    column_headers_per_analyzer=subquery.removeprefix('READ?,').removesuffix('\n')+','
                    column_headers_per_analyzer=column_headers_per_analyzer.replace(',',f':PA{socket_num+1},')
                    backup_f.write(column_headers_per_analyzer)
                backup_f.write(',')
            backup_f.write('\n')
            backup_f.close()

        # log and display each sample till end of test
        sample_num=0
        while sample_num < num_samples or indefinite_logging:
        #for sample_num in range(num_samples):

            # stop when STOP pressed
            if stop_event.is_set():
                print("Stopped!", flush=True)
                dpg.set_value(loading_bar_id,0)
                render_feedback(zeros_resp_string,0)
                return
            
            reading_time=time.time()
            f.write(str(int(reading_time*1000))+',')
            big_response_string=""
            reattempt_flag=False

            # query each power analyzer for test data
            try:
                for socket_num in range(len(PA_sockets)):
                    for subquery in query_string_list:
                        #print(f'sending string {repr(subquery)}',flush=True)
                        PA_sockets[socket_num].sendall(subquery.encode())
                        response_string=PA_sockets[socket_num].recv(4096).decode()
                        #print(f'Got response {response_string}', flush=True)
                        #time.sleep(0.01)
                        big_response_string+=response_string.rstrip('\r\n')+','
                    current_page_num=PA_names.index(dpg.get_value('PA_ID'))
                    #print(f'big response string: {repr(big_response_string)}',flush=True)
                    
                    # if sample period longer than 0.2 seconds, give feedback and write to backup file
                    if (not fast_mode):
                        print(f"Got sample {sample_num+1} of {num_samples if not indefinite_logging else 'many'}", flush=True)
                        dpg.set_value(loading_bar_id,float(sample_num)/float(num_samples))
                        if current_page_num == socket_num:
                            render_feedback(big_response_string,num_harmonics)
                        elif current_page_num>=len(PA_sockets):
                            render_feedback(zeros_resp_string,0)

                        backup_f=open(log_file_full_path+'.bak','a')
                        backup_f.write(big_response_string)
                        backup_f.close()
                    
                    # write responses from all xitron channels to log
                    f.write(big_response_string)

                    # reset big response string
                    big_response_string=""
                f.write('\n')

            # try rebuilding list of sockets if the above loop fails
            except:
                print("starting reconnection attempts")
                reattempt_flag=True
                max_attempts=20
                attempt=0
                
                while attempt<max_attempts:
                    try:
                        close_pa_sockets(PA_sockets)
                        PA_sockets=open_pa_sockets()
                        print("recovered!")
                        attempt=max_attempts
                    except:
                        attempt+=1
                        f.write(f"Connection error, retry {attempt} of {max_attempts}\n")
                        print(f'failed attempt {attempt} of {max_attempts}')
                        if attempt == max_attempts:
                            print('RECOVERY ATTEMPT FAILED, STOPPING TEST')
                            stop_event.set()

            # print a warning if the reading takes longer than the logging period
            if reattempt_flag:
                reattempt_flag=False
            else:
                if time.time()>reading_time+logging_period_seconds_float:
                    print("WARNING: sampling period too short!",flush=True)

                # wait till a full logging period has passed
                while(time.time()<reading_time+logging_period_seconds_float):
                    pass

            sample_num+=1

    # close sockets after test is done
    dpg.set_value(loading_bar_id,0)
    render_feedback(zeros_resp_string,0)
    print("Done!")
    for socket_num in range(len(PA_sockets)):
        PA_sockets[socket_num].close()


# stop test callback function
def stop_test():
    stop_event.set()


#-------------------------------------------------- CALLBACK SECTION --------------------------------------------------#


# dearpygui setup
dpg.create_context()

# feedback columns parameters
num_cols_feedback=5
channel_names=["CH1","CH2","CH3","CH4"]

# names for the power analyzers
PA_names=["XT2640 1","XT2640 2","XT2640 3","XT2640 4"]


# size GUI window based on the size of the largest display
viewport_width,viewport_height=compute_window_size()
print(f"viewport width {viewport_width}")
print(f"viewport_height {viewport_height}")


#set sizes of all major UI elements based on viewport width
ctrl_width=0.5*viewport_width
print(f"ctrl width {ctrl_width}")
fb_width=viewport_width-ctrl_width
print(f"fb_width {fb_width}")
button_window_height=int(viewport_height*0.17)
if button_window_height<100:
    button_window_height=100
print(f"button window height {button_window_height}")
loading_window_height=int(viewport_height*0.1)
if loading_window_height<100:
    loading_window_height=100
print(f"loading window height {loading_window_height}")
fb_height=viewport_height-button_window_height-loading_window_height
print(f"feedback height {fb_height}")
ctrl_height=fb_height
print(f"ctrl height {ctrl_height}")

# set spacer height
spacer_height=int(viewport_height*0.005)


# add a font registry, needed for having next of different sizes
with dpg.font_registry():
    #first argument ids the path to the .ttf or .otf file
    title_font = dpg.add_font("DejaVuSans.ttf", int(viewport_width*0.02))
    normal_font = dpg.add_font("DejaVuSans.ttf", int(viewport_width*0.013))
    tiny_font = dpg.add_font("DejaVuSans.ttf", int(viewport_width*0.008))
    button_font=dpg.add_font("DejaVuSans.ttf", int(viewport_width*0.04))
    feedback_font=dpg.add_font("FiraMono-Regular.ttf",int(viewport_width*0.013))

with dpg.theme() as compact_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, 0)
        dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 0, 0)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, 0)
# text defaults to normal font
dpg.bind_font(normal_font)


#-------------------------------------------------- CONTROL SECTION --------------------------------------------------#
with dpg.window( pos=(0,0),width=ctrl_width,height=ctrl_height,no_move=True,no_resize=True,no_title_bar=True,tag="ctrl_window"):

    # Control section title
    dpg.add_text("CONTROL",tag="ctrl_title")
    dpg.bind_item_font("ctrl_title",title_font)
    dpg.add_spacer(height=spacer_height)

    


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
            default_path=str(Path(__file__).resolve().parent)
            full_path_text=dpg.add_input_text(width=-1,default_value=default_path,tag="folder_path_text")
            dpg.bind_item_font(full_path_text,tiny_font)


        # Number of harmonics to log
        with dpg.table_row():
            dpg.add_text("Num Harmonics to Log:")
            dpg.add_input_int(tag='num_harmonics_int',default_value=13)

        # time between readings
        with dpg.table_row():
            dpg.add_text("Logging Period (s):")
            dpg.add_input_text(width=-1,hint="Enter integer between 100 and 10,000",tag="log_period_text",default_value='0.25')

        
        # total test duration, leaving blank will set the test time to 1 week
        with dpg.table_row():
            dpg.add_text("Test Duration (s)")
            dpg.add_input_text(width=-1,hint="Leave blank for indefinite logging",tag="test_duration_text")

        
        # put other desired parameters to log here
        with dpg.table_row():
            dpg.add_text("Extra Data to Log")
            dpg.add_input_text(width=-1,hint="ex. V:CH1:CF,A:CH1:CF,V:CH2:CF,A:CH2:CF",tag="extra_data_text")

        with dpg.table_row():
            dpg.add_text("")
            dpg.add_button(label="SAVE TO JSON",callback=save_to_json_callback)

        # add spacer row
        with dpg.table_row():
            dpg.add_text(" ")
            dpg.add_text(" ")

        # Xitron network details
        prev_options_index=6
        for x in range(len(PA_names)):
            with dpg.table_row():
                dpg.add_text(f"Xitron {x+1} IP Address:")
                dpg.add_input_text(width=-1,tag=f'PA_IP{x+1}')
                prev_options_index+=1

            with dpg.table_row():
                dpg.add_text(f"Xitron {x+1} Port:")
                dpg.add_input_text(width=-1,tag=f'PA_port{x+1}')
                prev_options_index+=1

            if x != len(PA_names)-1:
                with dpg.table_row():
                    dpg.add_text(" ")
                    dpg.add_text(" ")

        with dpg.table_row():
            dpg.add_text("")
            dpg.add_button(label="GET PA ADDRESSES",callback=get_pa_addresses_callback)
        
        with dpg.table_row():
            dpg.add_text("")
            dpg.add_text(label="",tag="get_ip_status_text")

        

# seperate window at bottom for start and stop buttons
with dpg.window( pos=(0,ctrl_height+loading_window_height),width=ctrl_width,height=button_window_height,no_move=True,no_resize=True,no_title_bar=True):
    with dpg.table(header_row=False,borders_innerH=True):
        dpg.add_table_column()
        dpg.add_table_column()

        with dpg.table_row():
            decrement_button=dpg.add_button(label="     START    ",callback=start_test)
            increment_button=dpg.add_button(label="     STOP     ",callback=stop_test)
            dpg.bind_item_font(decrement_button,button_font)
            dpg.bind_item_font(increment_button,button_font)


load_from_json()

#-------------------------------------------------- CONTROL SECTION --------------------------------------------------#




#------------------------------------------------- FEEDBACK SECTION --------------------------------------------------#

# function for displaying response from xitron
def render_feedback(response_string_raw,num_harms):
    response_list=response_string_raw.split(',')
    #print(response_list,flush=True)
    response_index=0
    for chan in channel_names:
        dpg.set_value(f'V_RMS_{chan}',(response_list[response_index]))
        response_index+=1
        dpg.set_value(f'V_AC_{chan}',(response_list[response_index]))
        response_index+=1
        dpg.set_value(f'V_DC_{chan}',(response_list[response_index]))
        response_index+=1
        dpg.set_value(f'A_RMS_{chan}',(response_list[response_index]))
        response_index+=1
        dpg.set_value(f'A_AC_{chan}',(response_list[response_index]))
        response_index+=1
        dpg.set_value(f'A_DC_{chan}',(response_list[response_index]))
        response_index+=1
        dpg.set_value(f'W_RMS_{chan}',(response_list[response_index]))
        response_index+=1
        dpg.set_value(f'W_AC_{chan}',(response_list[response_index]))
        response_index+=1
        dpg.set_value(f'W_DC_{chan}',(response_list[response_index]))
        response_index+=1
        dpg.set_value(f'PF_{chan}',(response_list[response_index]))
        response_index+=1
        dpg.set_value(f'FREQ_{chan}',(response_list[response_index]))
        response_index+=1+num_harms*2

with dpg.window( pos=(ctrl_width,0),width=fb_width,height=fb_height,no_move=True,no_resize=True,no_title_bar=True):


    feedback_title=dpg.add_text("FEEDBACK")
    dpg.bind_item_font(feedback_title,title_font)
    dpg.add_spacer(height=spacer_height)

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

        with dpg.table_row():
            dpg.add_text("FREQUENCY")
            for chan in channel_names:
                tag_string=f"FREQ_{chan}"
                dpg.add_text("0.000000",tag=tag_string)
                dpg.bind_item_font(tag_string,feedback_font)

# seperate window at bottom for right and left arrow buttons
with dpg.window( pos=(ctrl_width,fb_height+loading_window_height),width=fb_width,height=button_window_height,no_move=True,no_resize=True,no_title_bar=True):
    with dpg.table(header_row=False,borders_innerH=True):
        dpg.add_table_column()
        dpg.add_table_column()

        with dpg.table_row():
            decrement_button=dpg.add_button(label="      <<      ",callback=left_arrow_callback)
            increment_button=dpg.add_button(label="      >>     ",callback=right_arrow_callback)
            dpg.bind_item_font(decrement_button,button_font)
            dpg.bind_item_font(increment_button,button_font)


# add window for displaying progress bar
with dpg.window( pos=(0,fb_height),width=viewport_width,height=loading_window_height,no_move=True,no_resize=True,no_title_bar=True) as loading_window:

    dpg.add_text("Progress:")
    loading_bar_id = dpg.add_progress_bar(default_value=0.0, width=viewport_width,height=int(loading_window_height*0.6))
    
dpg.bind_item_theme(loading_window,compact_theme)



#------------------------------------------------- FEEDBACK SECTION --------------------------------------------------#

# start GUI and destroy when closed
dpg.create_viewport(title='Xitron GUI', width=viewport_width, height=viewport_height,resizable=False)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()