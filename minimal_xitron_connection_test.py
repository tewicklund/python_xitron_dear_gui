import time
import socket

ip="192.168.99.184"
port=10733

# import query string that is sent to power analyzers
f=open("minimal_query_string.txt",'r')
minimal_query_string=f.readline().rstrip("\r\n")
f.close()
print(f"got q string {minimal_query_string}")

minimal_query_string+="\n"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f'attempting connection to {ip} port {port}', flush=True)
s.connect((ip,port))
s.settimeout(10)

print(f"sending q string {repr(minimal_query_string)}")
s.sendall(minimal_query_string.encode())
response_string=s.recv(4096).decode()
print(f'Got response {response_string}', flush=True)

s.shutdown(socket.SHUT_RDWR)