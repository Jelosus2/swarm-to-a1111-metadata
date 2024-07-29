from pathlib import Path
from lib import hash
import subprocess
import main
import sys

def setup_config():
  if not Path("venv").exists():
    print("Creating venv and installing requirements...")
    subprocess.check_call("python -m venv venv", shell=sys.platform == "linux")
    
    venv_pip = Path("venv/bin/pip") if sys.platform == "linux" else Path("venv/Scripts/pip.exe")
    subprocess.check_call(f"{venv_pip} install pillow")

  if Path("config.json").exists():
    regenerate_config = None
    while regenerate_config not in ("y", "n"):
      regenerate_config = input("Do you want to setup the config again?(y/n): ").lower()
    if regenerate_config == "n":
      return

  config_obj = {
    "LoraFolder": "",
    "CheckpointFolder": "",
    "Cache": True
  }

  lora_dir = None
  while not lora_dir:
    lora_dir = input("Specify the directory where your LoRAs are: ")
  config_obj["LoraFolder"] = Path(lora_dir).as_posix()
  
  checkpoint_dir = None
  while not checkpoint_dir:
    checkpoint_dir = input("Specify the path of the directory where your Checkpoints are: ")
  config_obj["CheckpointFolder"] = Path(checkpoint_dir).as_posix()

  cache = None
  while cache not in ("y", "n"):
    cache = input("Do you want to enable the cache system to speedup the hashing process?(y/n): ").lower()
  config_obj["Cache"] = True if cache == "y" else False
  if Path("cache.json").exists():
    regenerate_cache = None
    while regenerate_cache not in ("y", "n"):
      regenerate_cache = input("Do you wish to regenerate the cache file? Note: By doing this old resources will need to be rehashed.(y/n): ").lower()
    if regenerate_cache == "y":
      hash.generate_cache_file()
  else:
    hash.generate_cache_file()

  main.generate_config_file(config_obj)

setup_config()