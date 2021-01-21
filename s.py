import socket
import subprocess

val = socket.getaddrinfo(socket.gethostname(), 8000, family=socket.AF_INET)
ip_addr = None
for i in val:
    mem = i[-1][0]
    if mem.split('.')[-1] != '1':
        ip_addr = mem
        break

subprocess.call("venv\\Scripts\\activate")
subprocess.call(f"python manage.py {ip_addr}:8000")

