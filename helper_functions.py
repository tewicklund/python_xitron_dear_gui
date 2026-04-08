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

