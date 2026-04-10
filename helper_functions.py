from screeninfo import get_monitors


# function for sizing UI window (viewport) based on primary monitor width and height
def compute_window_size(width=None, height=None):

    all_monitors=get_monitors()

    main_monitor=max(all_monitors,key=lambda monitor: monitor.width * monitor.height)
    main_width=main_monitor.width
    main_height=main_monitor.height

    # defaults to 75% of biggest monitor's width and height
    viewport_width=int(main_width*0.75)
    viewport_height=int(main_height*0.75)

    # OVERRIDE: User can enter their own custom viewport size
    if width is not None and height is not None:
        viewport_width=width
        viewport_height=height

    return viewport_width,viewport_height

def build_query_string_list(ch1_query_no_harms_path, num_harms):

    # make a list of query strings to send to analyzer, limit of 480 char response
    with open(ch1_query_no_harms_path,'r') as f:
        ch1_query_with_harms=f.readline().rstrip('\r\n')

    # add harmonics, voltage and current
    for x in range(num_harms):
        ch1_query_with_harms+=f',V:CH1:H{x+1},A:CH1:H{x+1}'
    ch1_query_with_harms+='\n'

    # make 4 element list, each with a channel specific query
    q_list=[ch1_query_with_harms]
    for x in range(3):
        q_list.append(ch1_query_with_harms.replace('CH1',f'CH{str(x+2)}'))
    #print(f"Source query string: {ch1_query_no_harms}")
    #print(f"Output query string list: {q_list}")

    # return list of queries
    return q_list

#test_q_list=build_query_string_list("ch1_q_string.txt",13)