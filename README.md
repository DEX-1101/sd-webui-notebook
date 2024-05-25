## My Notebook Collection

## Notes
  - Notebook works on both Colab (pro) and Kaggle. Although i don't use colab, so let me know if the is issue.
## How to Start
 1. In the Kaggle, select `File` > `Import Notebook` > `GitHub` > type `DEX-1101/sd-webui-notebook` and choose the Notebook you want to use (*.ipynb extension)
 2. You need a `ngrok token`, get it from [here](https://dashboard.ngrok.com/get-started/your-authtoken). You need register it first.
## One-click Notebook
 Usage : `x1101.py` `--args1` `--args2`
List of all available args :
```
--debug        : Enable debug mode, useful for diagnosing.
--req          : A file required for notebook to run.
--config       : URL for WebUI config file if you want to import your config.
--pastebin     : Pastebin URL if you want to download model/lora/extensions/embeddings. Currently supported HF only.
--hf_token     : HuggingFace's Token if you download it from private repo for Pastebin download.
--ngrok_token  : Token for tunneling with ngrok. This is REQUIRED even you're don't planning to use it.
--zrok_token   : Token for tunneling with Zrok. This is optional.
--hub_token    : URL tha contains token for HUB extension for easily downloading stuff inside WebUI.
```
**Note** : To download model/lora or extension use ``--pastebin`` option, use [these](https://pastebin.com/XahpVjuT) format.

## How to use/register zrok tunnel
  - Register [Here](https://colab.research.google.com/github/DEX-1101/sd-webui-notebook/blob/main/zrok_sign_up.ipynb). Just follow the instruction on it.

![sss](https://raw.githubusercontent.com/DEX-1101/sd-webui-notebook/main/img/Screenshot_13.png)
![markdown](https://raw.githubusercontent.com/DEX-1101/sd-webui-notebook/main/img/Screenshot_27.png)
![ss](https://raw.githubusercontent.com/DEX-1101/sd-webui-notebook/main/img/Screenshot_706.png)

 



