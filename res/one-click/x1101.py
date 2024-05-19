import time
import sys
import os
import subprocess
from threading import Thread

def progress_bar():
    sys.stdout.write('Loading \033[31mx1101.py\033[0m [')
    sys.stdout.flush()
    while not progress_done:
        sys.stdout.write('\033[92m' + '■' + '\033[0m')
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write('][ok]')
    sys.stdout.flush()
    print() 

def run_subprocesses():
    global progress_done
    if not os.path.exists("x1101"):
        subprocess.run("pip install -q git+https://github.com/DEX-1101/colablib", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run("apt -y install -qq aria2", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run("pip install colorama", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if 'content' in os.listdir('/') and not os.path.exists("x1101"):
        subprocess.run("pip install xformers==0.0.25 --no-deps", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif 'kaggle' in os.listdir('/') and not os.path.exists("x1101"):
        #subprocess.run("pip install torch==2.1.2+cu121 torchvision==0.16.2+cu121 torchaudio==2.1.2 --extra-index-url https://download.pytorch.org/whl/cu121", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run("pip install xformers==0.0.26.post1", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    progress_done = True

# Flag to indicate when the subprocesses are done
progress_done = False
progress_thread = Thread(target=progress_bar)
subprocess_thread = Thread(target=run_subprocesses)

progress_thread.start()
subprocess_thread.start()

# Wait for both threads to complete
subprocess_thread.join()
progress_thread.join()

import argparse
import torch
import re
import requests
from colablib.utils import py_utils
from pydantic import BaseModel
from colablib.utils.py_utils import get_filename
from colablib.sd_models.downloader import aria2_download, download
from colablib.colored_print import cprint, print_line
from colablib.utils.config_utils import read_config
from colablib.utils.git_utils import clone_repo
from colorama import init, Fore, Back, Style

torch_ver = torch.__version__
cuda_ver = torch.version.cuda
gpu_status = f"{torch.cuda.get_device_name(torch.cuda.current_device())}" if torch.cuda.is_available() else "No GPU detected."

if 'content' in os.listdir('/'):
    root_path = "/content"
    ui = "/content"
    env = 'Colab'
elif 'kaggle' in os.listdir('/'):
    root_path = "/kaggle/working"
    ui = "/kaggle/working"
    env = 'Kaggle'
else:
     cprint('Error. Enviroment not detected', color="flat_red")

print_line(0)
cprint(f"[+] PyTorch Version :", torch_ver, "| Cuda :", cuda_ver, "| GPU :", gpu_status, "| Env :", env, "|", color="flat_green")
print_line(0)
cprint("[+] Preparing Notebook", color="flat_yellow")

################# UI #################
branch = "master"
ui_path = os.path.join(ui, "x1101")
git_path = os.path.join(ui_path, "extensions")

ui = "/kaggle/working"

def run_subprocesses(commands, show_output=False):
    processes = []
    for i, (command, message) in enumerate(commands):
        cprint(f"    > {message}", color="flat_cyan")
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        processes.append((i, process))
        process.wait()  # Wait for the process to complete
        stdout, stderr = process.communicate()
        output = stdout.decode() + stderr.decode()
        if args.debug:
            show_output = True
            print(output)  # Show all output for each process
        if process.returncode != 0:
            print(f"Subprocess {i+1} failed with error: {stderr.decode().strip()}")

commands = [
    ("apt-get install -y aria2", "aria2"),
    ("npm install -g localtunnel", "localtunnel"),
    ("apt-get install lz4", "lz4"),
    ("curl -s -Lo /usr/bin/cl https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 && chmod +x /usr/bin/cl", "cloudflared"),
    (f"curl -sLO https://github.com/openziti/zrok/releases/download/v0.4.23/zrok_0.4.23_linux_amd64.tar.gz && tar -xzf zrok_0.4.23_linux_amd64.tar.gz && rm -rf zrok_0.4.23_linux_amd64.tar.gz && mv {ui}/zrok /usr/bin", "zrok"),
    (f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/x1101/UI/resolve/main/ui.tar.lz4 -o ui.tar.lz4 && tar -xI lz4 -f ui.tar.lz4 && mv -f {ui}/kaggle/working/x1101 {ui} && rm {ui}/ui.tar.lz4 && rm -rf {ui}/kaggle", "Installing UI..."),
    (f"cd {ui_path} && git reset --hard && git pull && git switch {branch} && git pull && git reset --hard", "Updating UI..."),
    (f"rm -rf {git_path}/* && cd {git_path} && git clone https://github.com/BlafKing/sd-civitai-browser-plus && git clone https://github.com/Mikubill/sd-webui-controlnet && git clone https://github.com/DominikDoom/a1111-sd-webui-tagcomplete && git clone https://github.com/DEX-1101/sd-encrypt-image && git clone https://github.com/DEX-1101/timer && git clone https://github.com/gutris1/sd-hub && git clone https://github.com/Bing-su/adetailer.git && git clone https://github.com/zanllp/sd-webui-infinite-image-browsing && git clone https://github.com/thomasasfk/sd-webui-aspect-ratio-helper && git clone https://github.com/hako-mikan/sd-webui-regional-prompter && git clone https://github.com/picobyte/stable-diffusion-webui-wd14-tagger && git clone https://github.com/Coyote-A/ultimate-upscale-for-automatic1111 && git clone https://github.com/Haoming02/sd-webui-tabs-extension", "Cloning Extensions..."),
    ("", "Done")
]

################# UI ##################

################# PASTEBIN DL #################
webui_path = os.path.join(root_path, "x1101")

custom_model_url        = ""
custom_vae_url          = ""
custom_embedding_url    = ""
custom_LoRA_url         = ""
custom_extensions_url   = ""
models_dir          = os.path.join(webui_path, "models", "Stable-diffusion")
vaes_dir            = os.path.join(webui_path, "models", "VAE")
lora_dir            = os.path.join(webui_path, "models", "Lora")
embeddings_dir      = os.path.join(webui_path, "embeddings")
extensions_dir      = os.path.join(webui_path, "extensions")
download_list       = os.path.join(root_path, "download_list.txt")

class CustomDirs(BaseModel):
    url: str
    dst: str

custom_dirs = {
    "model"       : CustomDirs(url=custom_model_url, dst=models_dir),
    "vae"         : CustomDirs(url=custom_vae_url, dst=vaes_dir),
    "embedding"   : CustomDirs(url=custom_embedding_url, dst=embeddings_dir),
    "lora"        : CustomDirs(url=custom_LoRA_url, dst=lora_dir),
    "extensions"  : CustomDirs(url=custom_extensions_url, dst=extensions_dir),
}

def parse_urls(filename):
    content = read_config(filename)
    lines   = content.strip().split('\n')
    result  = {}
    key     = ''
    for line in lines:
        if not line.strip():
            continue
        if line.startswith('//'):
            continue
        if line.startswith('#'):
            key = line[1:].lower()
            result[key] = []
        else:
            urls = [url.strip() for url in line.split(',') if url.strip() != '']
            result[key].extend(urls)
    return result

def get_filename(url, token=None):
    headers = {}
    if token:
        headers['Authorization'] = 'Bearer hf_token'
       
def custom_download(custom_dirs):
    for key, value in custom_dirs.items():
        urls     = value.url.split(",")  # Split the comma-separated URLs
        dst      = value.dst

        if value.url:
            print_line(0)
            cprint(f"[+] Downloading {key}.", color="flat_yellow")

        for url in urls:
            url = url.strip()  # Remove leading/trailing whitespaces from each URL
            if url != "":
                print_line(0, color="green")
                if "|" in url:
                    url, filename = map(str.strip, url.split("|"))
                    if not filename.endswith((".safetensors", ".ckpt", ".pt", "pth")):
                        filename = filename + os.path.splitext(get_filename(url))[1]
                else:
                    if not url.startswith("fuse:"):
                        filename = get_filename(url)

                if url.startswith("fuse:"):
                    fuse(url, key, dst)
                elif key == "extensions":
                    clone_repo(url, cwd=dst)
                else:
                   download(url=url, filename=filename, user_header=user_header, dst=dst, quiet=False)

def download_from_textfile(filename):
    for key, urls in parse_urls(filename).items():
        for url in urls:
            if "civitai.com" in url:
                url += "&ApiKey={civitai_api_key}" if "?" in url else "?ApiKey={civitai_api_key}"
        key_lower = key.lower()
        if key_lower in custom_dirs:
            if custom_dirs[key_lower].url:
                custom_dirs[key_lower].url += ',' + ','.join(urls)
            else:
                custom_dirs[key_lower].url = ','.join(urls)
        else:
            cprint(f"Warning: Category '{key}' from the file is not found in custom_dirs.", color="flat_yellow")
            
def custom_download_list(url):
    filename = "custom_download_list.txt"
    filepath = os.path.join(root_path, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    if 'pastebin.com' in url:
        if 'raw' not in url:
            url = url.replace('pastebin.com', 'pastebin.com/raw')
    download(url=url, filename=filename, user_header=user_header, dst=root_path, quiet=True)
    return filepath
    
########## PASTEBIN DL #################

def download_file_with_aria2(url, save_dir='.'):
    local_filename = os.path.join(save_dir, url.split('/')[-1])

    # aria2c command
    command = [
        'aria2c',
        '--dir', save_dir,
        '--out', local_filename,
        '--console-log-level=error',
        '--summary-interval=0',
        url
    ]
    
    # Start the aria2c process
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cprint(f"    Downloading {url}", color="flat_cyan")
    process.wait()  # Ensure the process has completed
    
    if process.returncode == 0:
        cprint(f"    File saved as {local_filename}", color="flat_cyan")
    else:
        cprint(f"    Download failed for: {url}", color="flat_red")

def download_from_link_file(link_file_path):
    with open(link_file_path, 'r') as file:
        urls = file.readlines()
    
    for url in urls:
        url = url.strip()
        if url:  # Skip any blank lines
            download_file_with_aria2(url)

############# TUNNELS #######################
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
############# TUNNELS #######################

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ada indo coy !!!.")
    parser.add_argument("--req", type=str, help="Required file for notebook to run.")
    parser.add_argument("--config", type=str, help="The URL of your WebUI's config file if you want to import it.")
    parser.add_argument("--pastebin", type=str, help="Pastebin URL if you want to download model/lora/extensions.")
    parser.add_argument("--hf_token", type=str, help="HuggingFace's Token if you download it from private repo for Pastebin download.")
    parser.add_argument("--zrok_token", type=str, help="Token for tunneling with Zrok. This is optional.")
    parser.add_argument("--ngrok_token", required=True, type=str, help="Token for tunneling with ngrok. This is REQUIRED even you're don't planning to use it.")
    parser.add_argument("--hub_token", type=str, help="Token for HUB extension for easily downloading stuff inside WebUI, do NOT put your token here but instead link file contains the token.")
    parser.add_argument("--debug", action='store_true', help="Enable debug mode.")
    
    args = parser.parse_args()

    # variable
    args.req = "https://github.com/DEX-1101/sd-webui-notebook/raw/main/res/req.txt"
    pastebin_url     = args.pastebin
    hf_token         = args.hf_token
    zrok_token       = args.zrok_token
    ngrok_token      = args.ngrok_token
    import_config    = args.config
    secret           = args.hub_token

    if args.debug:
        cprint("    Debug mode enabled", color="flat_red")
        show_output = True
    
    # Download the link file
    download_file_with_aria2(args.req)
    link_file_path = os.path.join('.', args.req.split('/')[-1])
    # Download files listed in the link file
    download_from_link_file(link_file_path)

    ############### UI ####################  

    print_line(0)
    cprint(f"[+] Installing Requirements", color="flat_yellow")
    if not os.path.exists("x1101"):
        run_subprocesses(commands)
    
    if args.config:
        subprocess.run(f"wget -q {import_config} -O {ui}/config.json", shell=True)
    
    if args.hub_token:
        subprocess.run(f"mkdir -p {ui}/x1101 && wget -q {secret} -O {ui}/x1101/sd-hub-token.json", shell=True)
    
    if args.pastebin:
        start_time    = time.time()
        textfile_path = download_list
        if pastebin_url:
            user_header = f"Authorization: Bearer {hf_token}"
            textfile_path = custom_download_list(pastebin_url)
        download_from_textfile(textfile_path)
        custom_download(custom_dirs)
        elapsed_time  = py_utils.calculate_elapsed_time(start_time)
        
    print_line(0)
    cprint(f"[+] Starting WebUI...", color="flat_yellow")
    tunnel_class = pickle.load(open("new_tunnel", "rb"), encoding="utf-8")
    tunnel_port= 1101
    tunnel = tunnel_class(tunnel_port)
    tunnel.add_tunnel(command="cl tunnel --url localhost:{port}", name="cl", pattern=re.compile(r"[\w-]+\.trycloudflare\.com"))
    tunnel.add_tunnel(command="lt --port {port}", name="lt", pattern=re.compile(r"[\w-]+\.loca\.lt"), note="Password : " + Fore.GREEN + public_ipv4 + Style.RESET_ALL + " rerun cell if 404 error.")
    if args.zrok_token:
        subprocess.run(f"zrok enable {zrok_token}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        tunnel.add_tunnel(command="zrok share public http://localhost:{port}/ --headless", name="zrok", pattern=re.compile(r"[\w-]+\.share\.zrok\.io"))
    
    with tunnel:
        #subprocess.run("python -m http.server 1101", shell=True)
        #os.chdir(ui)
        subprocess.run(f"echo -n {start_colab} >{ui}/x1101/static/colabTimer.txt", shell=True)
        lol = f"sed -i -e \"s/\\[\\\"sd_model_checkpoint\\\"\\]/\\[\\\"sd_model_checkpoint\\\",\\\"sd_vae\\\",\\\"CLIP_stop_at_last_layers\\\"\\]/g\" {ui}/x1101/modules/shared_options.py"
        subprocess.run(lol, shell=True)       
        subprocess.run(f"cd {ui}/x1101 && python launch.py --port=1101 --ngrok {ngrok_token} --api --encrypt-pass=x1101 --xformers --theme dark --enable-insecure-extension-access --disable-console-progressbars --disable-safe-unpickle --no-half-vae", shell=True)
        
