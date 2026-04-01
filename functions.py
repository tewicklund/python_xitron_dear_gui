from screeninfo import get_monitors


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
