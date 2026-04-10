from screeninfo import get_monitors


# function for sizing UI window (viewport) based on primary monitor width and height
def compute_window_size(width=None, height=None):
    all_monitors=get_monitors()

    main_monitor=max(all_monitors,key=lambda monitor: monitor.width * monitor.height)
    main_width=main_monitor.width
    main_height=main_monitor.height

    viewport_width=int(main_width*0.75)
    viewport_height=int(main_height*0.75)

    # OVERRIDE: User can enter their own custom viewport size
    if width is not None and height is not None:
        viewport_width=width
        viewport_height=height

    return viewport_width,viewport_height

def prep_float_for_disp(input_float_string,num_chars=8):
    return(input_float_string)

    input_float_length=len(input_float_string)

    if input_float_length == num_chars:
        return input_float_string

    elif input_float_length > num_chars:
        return input_float_string[0:num_chars]

    else:
        output_float_string=input_float_string
        output_float_length=len(output_float_string)
        while output_float_length < num_chars:
            output_float_string=output_float_string+'0'
            output_float_length=len(output_float_string)
        return output_float_string

def build_query_string_list(ch1_query_no_harms, num_harms):
    # make a list of query strings to send to analyzer, limit of 480 char response
    with open(ch1_query_no_harms,'r') as f:
        ch1_query_with_harms=f.readline().rstrip('\r\n')
    for x in range(num_harms):
        ch1_query_with_harms+=f',V:CH1:H{x+1},A:CH1:H{x+1}'
    ch1_query_with_harms+='\n'
    q_list=[ch1_query_with_harms]
    for x in range(3):
        q_list.append(ch1_query_with_harms.replace('CH1',f'CH{str(x+2)}'))
    #print(f"Source query string: {ch1_query_no_harms}")
    #print(f"Output query string list: {q_list}")
    return q_list

test_q_list=build_query_string_list("ch1_q_string.txt",13)