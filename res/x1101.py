import os
import subprocess
import time
import torch
from colablib.colored_print import cprint, print_line

if 'content' in os.listdir('/'):
    ui = "/content"
    env = 'Colab'
elif 'kaggle' in os.listdir('/'):
    ui = "/kaggle/working"
    env = 'Kaggle'
else:
     cprint('Error. Enviroment not detected', color="flat_red")
    
branch = "master"
ui_path = os.path.join(ui, "x1101")
git_path = os.path.join(ui_path, "extensions")

torch_ver = torch.__version__
cuda_ver = torch.version.cuda
is_gpu = "Yes." if torch.cuda.is_available() else "GPU not detected."

def kontolondon(oppai, asu, si_kontol, kntl, debug=True):   
    start_time = time.time() 
    cprint(f"    > {asu}", color="flat_cyan")
    try:
        #subprocess.run(oppai, check=True, shell=True, text=True)  # for debug
        subprocess.run(oppai, check=True, shell=True, text=True,  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        si_kontol += 1
    except subprocess.CalledProcessError as e:
        print(f"Error at [{asu}]: {e}")
        kntl += 1
    end_time = time.time()
    return si_kontol, kntl, end_time - start_time

if __name__ == "__main__":   
    cprint(f"[+] PyTorch Version :", torch_ver, "| Cuda :", cuda_ver, "| GPU Access :", is_gpu, color="flat_green")
    print_line(0)
    
    rudi = [
        ("apt-get update && apt -y install aria2", "aria2"),
        ("apt-get install lz4", "lz4"),
        ("pip install colorama", "colorama"),
        ("npm install -g localtunnel", "localtunnel"),
        ("curl -s -OL https://github.com/DEX-1101/sd-webui-notebook/raw/main/res/new_tunnel", "new_tunnel"),
        ("curl -s -Lo /usr/bin/cl https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 && chmod +x /usr/bin/cl", "cloudflared"),
        (f"curl -sLO https://github.com/openziti/zrok/releases/download/v0.4.23/zrok_0.4.23_linux_amd64.tar.gz && tar -xzf zrok_0.4.23_linux_amd64.tar.gz && rm -rf zrok_0.4.23_linux_amd64.tar.gz && mv {ui}/zrok /usr/bin", "zrok"),
        (f"wget https://github.com/gutris1/segsmaker/raw/main/kaggle/script/pantat88.py -O {ui}/semvak_zeus.py", "semvak_zeus.py")
    ]

    yanto = [
        (f"wget https://raw.githubusercontent.com/DEX-1101/SecretNAI/main/template.txt -O {ui}/download_list.txt", "download_list.txt"),
        (f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/x1101/UI/resolve/main/ui.tar.lz4 -o ui.tar.lz4 && tar -xI lz4 -f ui.tar.lz4 && mv {ui}/kaggle/working/x1101 {ui} && rm {ui}/ui.tar.lz4 && rm -rf {ui}/kaggle", "Installing UI..."),
        (f"cd {ui_path} && git reset --hard && git pull && git switch {branch} && git pull && git reset --hard", "Updating UI..."),
        (f"rm -rf {git_path}/* && cd {git_path} && git clone https://github.com/BlafKing/sd-civitai-browser-plus && git clone https://github.com/Mikubill/sd-webui-controlnet && git clone https://github.com/DominikDoom/a1111-sd-webui-tagcomplete && git clone https://github.com/DEX-1101/sd-encrypt-image && git clone https://github.com/DEX-1101/timer && git clone https://github.com/gutris1/sd-hub && git clone https://github.com/Bing-su/adetailer.git && git clone https://github.com/zanllp/sd-webui-infinite-image-browsing && git clone https://github.com/thomasasfk/sd-webui-aspect-ratio-helper && git clone https://github.com/hako-mikan/sd-webui-regional-prompter && git clone https://github.com/picobyte/stable-diffusion-webui-wd14-tagger && git clone https://github.com/Coyote-A/ultimate-upscale-for-automatic1111 && git clone https://github.com/Haoming02/sd-webui-tabs-extension", "Installing Extensions..."),
        
    ]

    agus = []
    
    if 'content' in os.listdir('/'):
        agus.append(("pip install xformers==0.0.25 --no-deps", "Installing xformers..."))
    elif 'kaggle' in os.listdir('/'):
        agus.append(("pip install torch==2.1.2+cu121 torchvision==0.16.2+cu121 torchaudio==2.1.2 --extra-index-url https://download.pytorch.org/whl/cu121", "Installing torch..."))
        agus.append(("pip install xformers==0.0.23.post1 triton==2.1.0", "Installing xformers..."))
    else:
        agus.append((""))
            
    si_kontol = 0
    kntl = 0
    total_time = 0
    
    cprint(f"[+] Installing [{env}] Requirements", color="flat_yellow")
    for oppai, asu in rudi + yanto + agus:
        si_kontol, kntl, command_time = kontolondon(oppai, asu, si_kontol, kntl)
        total_time += command_time
        
    print_line(0)
    cprint(f"[+] {kntl} of {si_kontol} error found. All completed within: {total_time:.2f} secs", color="flat_yellow")
