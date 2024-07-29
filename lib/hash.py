from datetime import datetime
from pathlib import Path
import hashlib
import json

cache_path = Path(Path(__file__).parent.parent, "cache.json")

def generate_cache_file():
  with open(cache_path, "w") as cache_file:
    json.dump({}, cache_file, indent=2)

def generate_hash(file_path, cache) -> str:
  filename = Path(file_path)

  if cache and not cache_path.exists():
    generate_cache_file()

  if cache:
    try:
      with open(cache_path, "r", encoding="utf-8") as cache_file:
        cache_obj = json.load(cache_file)

      if cache_obj.get(filename.stem):
        return cache_obj.get(filename.stem)
    except json.JSONDecodeError:
      print("Failed to decode the cache file, renaming it and generating a new one...")
      cache_path.rename(Path(Path(__file__).parent.parent, f"cache_old_{int(datetime.now().timestamp() * 1000)}.json"))
      generate_cache_file()
      cache_obj = {}

  hash_sha256 = hashlib.sha256()
  blksize = 1024 * 1024

  with open(filename, "rb") as file:
    for chunk in iter(lambda: file.read(blksize), b""):
      hash_sha256.update(chunk)

  digested_hash = hash_sha256.hexdigest()[:10]

  if cache:
    cache_obj[filename.stem] = digested_hash
    with open(cache_path, "w") as cache_file:
      json.dump(cache_obj, cache_file, indent=2)

  return digested_hash

def lora_hash_generation(lora_list, lora_folder, cache) -> str:
  if len(lora_list) == 0:
    return ""
  
  if not lora_folder:
    print("LoRAs were detected in the metadata but you didn't setup the LoRA search directory in the config.json.")
    return "no-lora"

  lora_dir = Path(lora_folder)
  lora_hashes = ' Lora hashes: "'

  for index, lora in enumerate(lora_list):
    lora_name = lora.split("/")[-1]
    matching_loras = [file for ext in (f"{lora_name}.safetensors", f"{lora_name}.ckpt") for file in lora_dir.rglob(ext)]

    if len(matching_loras) > 0:
      if index == len(lora_list) - 1:
        lora_hashes += f'{matching_loras[0].stem}: {generate_hash(matching_loras[0], cache)}",'
      else:
        lora_hashes += f"{matching_loras[0].stem}: {generate_hash(matching_loras[0], cache)}, "
    else:
      print("No LoRA in the specified LoraFolder path matched the metadata, please check again.")
      return "no-lora"

  return lora_hashes

def model_hash_generation(model, model_folder, cache) -> str:
  if not model_folder:
    print("A Checkpoint was detected in the metadata but you didn't setup the Checkpoint search directory in the config.json.")
    return "no-checkpoint"
  
  model_name = model.split("/")[-1]
  model_dir = Path(model_folder)

  matching_checkpoint = [file for ext in (f"{model_name}.safetensors", f"{model_name}.ckpt") for file in model_dir.rglob(ext)]

  if len(matching_checkpoint) == 0:
    print("No Checkpoint in the specified CheckpointFolder path matched the metadata, please check again.")
    return "no-checkpoint"
  
  return generate_hash(matching_checkpoint[0], cache)