from screeninfo import get_monitors
import socket


# function for sizing UI window (viewport) based on primary monitor width and height
def compute_window_size(width=None, height=None):

    all_monitors=get_monitors()

    main_monitor=max(all_monitors,key=lambda monitor: monitor.width * monitor.height)
    main_width=main_monitor.width
    main_height=main_monitor.height

    # defaults to 75% of biggest monitor's width and height
    viewport_width=int(main_width*0.9)
    viewport_height=int(main_height*0.9)

    # OVERRIDE: User can enter their own custom viewport size
    if width is not None and height is not None:
        viewport_width=width
        viewport_height=height

    return viewport_width,viewport_height

def build_query_string_list(ch1_query_no_harms_path, num_harms,extra_data):

    # make a list of query strings to send to analyzer, limit of 480 char response
    with open(ch1_query_no_harms_path,'r') as f:
        ch1_query_with_harms=f.readline().rstrip('\r\n')

    # add harmonics, voltage and current
    for x in range(num_harms):
        ch1_query_with_harms+=f',V:CH1:H{x+1},A:CH1:H{x+1}'
    ch1_query_with_harms+='\n'

    # make 5 element list, 4 channels followed by extra data
    q_list=[ch1_query_with_harms]
    for x in range(3):
        q_list.append(ch1_query_with_harms.replace('CH1',f'CH{str(x+2)}'))
    if extra_data != '':
        q_list.append('READ?,'+extra_data+'\n')
    #print(f"Source query string: {ch1_query_no_harms}")
    #print(f"Output query string list: {q_list}")

    # return list of queries
    return q_list

#test_q_list=build_query_string_list("ch1_q_string.txt",13,'V:CH2:CF')
#print(test_q_list)

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
    return xitron_ip_list

#test_xitron_IP_list=get_xitron_IPs(10733)
#print(test_xitron_IP_list)