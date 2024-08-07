## My Notebook Collection

## Notes
  - Notebook works on both Colab (pro) and Kaggle. Although i don't use colab, so let me know if there is a issue.
## How to Start
 1. In the Kaggle, select `File` > `Import Notebook` > `GitHub` > type `DEX-1101/sd-webui-notebook` and choose the Notebook you want to use (*.ipynb extension)
 2. For Colab :
    
    [![](https://img.shields.io/static/v1?message=Open%20in%20Colab&logo=googlecolab&labelColor=5c5c5c&color=0f80c1&label=%20&style=for-the-badge)](https://colab.research.google.com/github/DEX-1101/sd-webui-notebook/blob/main/kaggle-colab-notebook-(one-click).ipynb) 
## One-click Notebook
 Usage : `x1101.py` `--args1` `--args2`
List of all available args :
```
--debug        : print all output.
--req          : A file required for notebook to run.
--config       : URL for WebUI config file if you want to import your config.
--pastebin     : Pastebin URL if you want to download model/lora/extensions/embeddings. Currently supported Huggingface's url only.
--hf_token     : HuggingFace's Token if you download it from private repo for Pastebin download.
--ngrok_token  : Token for tunneling with Ngrok (optional).
--zrok_token   : Token for tunneling with Zrok (optional).
--hub_token    : URL tha contains token for HUB extension for easily downloading stuff inside WebUI.
--branch       : Switch different branch for a111-webui. Default is 'master'
```
**Note** : To download model/lora or extension use ``--pastebin`` option, use [these](https://pastebin.com/XahpVjuT) format. Or you can use [HUB extensions](https://github.com/gutris1/sd-hub) inside webui.

## How to use/register zrok tunnel (optional)
  - Register [Here](https://colab.research.google.com/github/DEX-1101/sd-webui-notebook/blob/main/zrok_sign_up.ipynb). Just follow the instruction on it.

![sss](https://raw.githubusercontent.com/DEX-1101/sd-webui-notebook/main/img/Screenshot_13.png)
![markdown](https://raw.githubusercontent.com/DEX-1101/sd-webui-notebook/main/img/Screenshot_27.png)
![ss](https://raw.githubusercontent.com/DEX-1101/sd-webui-notebook/main/img/Screenshot_706.png)

 



