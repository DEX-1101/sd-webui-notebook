pastebin_url = ""
hf_token = ""

#Code by Bang Furqanil
import os
import time
from colablib.utils import py_utils
from pydantic import BaseModel
from colablib.utils.py_utils import get_filename
from colablib.sd_models.downloader import aria2_download, download
from colablib.colored_print import cprint, print_line
from colablib.utils.config_utils import read_config
from colablib.utils.git_utils import clone_repo

root_path = "/kaggle/working"
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
user_header = f"Authorization: Bearer {hf_token}"
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
        headers['Authorization'] = f'Bearer {hf_token}'
       
def custom_download(custom_dirs):
    for key, value in custom_dirs.items():
        urls     = value.url.split(",")  # Split the comma-separated URLs
        dst      = value.dst

        if value.url:
            print_line(0, color="green")
            cprint(f" [+] Downloading {key}.", color="flat_yellow")

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

def main():
    start_time    = time.time()
    textfile_path = download_list
    if pastebin_url:
        textfile_path = custom_download_list(pastebin_url)
    download_from_textfile(textfile_path)
    custom_download(custom_dirs)

    elapsed_time  = py_utils.calculate_elapsed_time(start_time)
    print_line(0, color="green")
    cprint(f"[+] Download completed within {elapsed_time}.", color="flat_yellow")
main()
