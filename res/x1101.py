import os
import subprocess
import time
from colablib.colored_print import cprint, print_line
cprint("[+] Installing Requirments", color="flat_yellow")

is_colab = False
branch = "master"
root_path = "/kaggle/working"
ui_path = os.path.join(root_path, "x1101")
git_path = os.path.join(ui_path, "extensions")

def kontolondon(command, message, success_count, failure_count):
    """
    Function to execute a shell command silently.
    """
    start_time = time.time() 
    cprint(f"    > {message}", color="flat_cyan")
    try:
        # Run the command in the subprocess silently
        #subprocess.run(command, check=True, shell=True, text=True)
        subprocess.run(command, check=True, shell=True, text=True,  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        #cprint(f"{message}", color="flat_cyan")
        success_count += 1
    except subprocess.CalledProcessError as e:
        print(f"Error at [{message}]: {e}")
        failure_count += 1
    end_time = time.time()
    return success_count, failure_count, end_time - start_time

if __name__ == "__main__":
    # List of commands with custom messages
    commands = [
        
        ("apt -y install -qq aria2", "aria2"),
        ("apt-get install lz4", "lz4"),
        ("pip install -q colorama", "colorama"),
        ("npm install -g localtunnel", "localtunnel"),
        ("curl -s -OL https://github.com/DEX-1101/sd-webui-notebook/raw/main/res/new_tunnel", "new_tunnel"),
        ("curl -s -Lo /usr/bin/cl https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 && chmod +x /usr/bin/cl", "cloudflared tunnel"),
        (f"curl -sLO https://github.com/openziti/zrok/releases/download/v0.4.23/zrok_0.4.23_linux_amd64.tar.gz && tar -xzf zrok_0.4.23_linux_amd64.tar.gz && rm -rf zrok_0.4.23_linux_amd64.tar.gz && mv {root_path}/zrok /usr/bin", "zrok"),
        (f"wget -q https://github.com/gutris1/segsmaker/raw/main/kaggle/script/pantat88.py -O {root_path}/semvak_zeus.py", "semvak_zeus.py")
    ]

    commands2 = [
        (f"wget -q https://raw.githubusercontent.com/DEX-1101/SecretNAI/main/template.txt -O {root_path}/download_list.txt", "download_list.txt"),
        (f"aria2c --console-log-level=error -q -c -x 16 -s 16 -k 1M https://huggingface.co/x1101/UI/resolve/main/ui.tar.lz4 -o ui.tar.lz4 && tar -xI lz4 -f ui.tar.lz4 && mv {root_path}/kaggle/working/x1101 {root_path} && rm {root_path}/ui.tar.lz4 && rm -rf {root_path}/kaggle", "Installing UI"),
        (f"cd {ui_path} && git pull && git switch {branch} && git pull && git reset --hard", "Updating UI"),
        (f"find {git_path} -mindepth 1 -maxdepth 1 -type d -print -exec git -C {{}} reset --hard \;", "Updating Extensions")
        
    ]

    commands3 = []
    
    if is_colab:
        commands3.append(("pip install -q xformers==0.0.22.post7", "xformers"))
    else:
        #commands3.append(("pip install -q torch==2.0.1+cu118 torchvision==0.15.2+cu118 torchaudio==2.0.2+cu118 torchtext==0.15.2 torchdata==0.6.1 --extra-index-url https://download.pytorch.org/whl/cu118", "torch"))
        commands3.append(("pip install -q xformers==0.0.20 triton==2.0.0", "xformers"))
        
    # Initialize counters and total time
    success_count = 0
    failure_count = 0
    total_time = 0
    
    # Execute each command silently with custom messages
    for command, message in commands + commands2 + commands3:  # Combine all commands
        success_count, failure_count, command_time = kontolondon(command, message, success_count, failure_count)
        total_time += command_time
    
    # Print summary
    cprint(f"[+] {failure_count} of {success_count} error found. All completed within: {total_time:.2f} secs", color="flat_yellow")
