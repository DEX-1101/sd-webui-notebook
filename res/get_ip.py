import re
import requests
from colorama import init, Fore, Back, Style
from colablib.colored_print import cprint, print_line
import time
import cloudpickle as pickle
try:
    start_colab
except:
    start_colab = int(time.time())-5
    
def get_public_ip(version='ipv4'):
    try:
        url = f'https://api64.ipify.org?format=json&{version}=true'
        response = requests.get(url)
        data = response.json()
        public_ip = data['ip']
        return public_ip
    except Exception as e:
        print(f"Error getting public {version} address:", e)

public_ipv4 = get_public_ip(version='ipv4')

tunnel_class = pickle.load(open("new_tunnel", "rb"), encoding="utf-8")
tunnel_port= 1101
tunnel = tunnel_class(tunnel_port)
