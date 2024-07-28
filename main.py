from PIL import Image, PngImagePlugin
from tkinter import filedialog
from pathlib import Path
from lib import hash
import tkinter as tk
import json

def select_folder_dialog() -> str:
  root = tk.Tk()
  root.withdraw()

  folder_path = filedialog.askdirectory(
    title="Select a folder",
    mustexist=True
  )

  return folder_path

def change_image_metadata(image_dir, config):
  path = Path(image_dir)
  png_files = list(path.glob("*.png"))

  if len(png_files) == 0:
    print("No file matches the criteria")
    return
  
  for file in png_files:
    image = Image.open(file)
    generation_metadata = image.info["parameters"]

    if "sui_image_params" in generation_metadata:
      print(f"Converting {file.name}...")
      metadata_object = json.loads(generation_metadata)

      image_params = metadata_object["sui_image_params"]

      prompt = image_params.get("original_prompt", image_params["prompt"])
      negative_prompt = image_params.get("negativeprompt", "")
      cfg = image_params["cfgscale"]
      steps = image_params["steps"]
      sampler = image_params["sampler"] if image_params.get("sampler") else "euler"
      scheduler = image_params["scheduler"] if image_params.get("scheduler") else "normal"
      seed = image_params["seed"]
      size = f'{image_params["width"]}x{image_params["height"]}'
      model = image_params["model"]
      version = image_params["swarm_version"]

      model_hash = hash.model_hash_generation(image_params["model"], config.get("CheckpointFolder", ""), config.get("Cache", False))
      lora_hashes = hash.lora_hash_generation(image_params.get("loras", []), config.get("LoraFolder", ""), config.get("Cache", False))

      if model_hash == "no-checkpoint" or lora_hashes == "no-lora":
        print("Stopping conversion...")
        return

      new_metadata_string = f"{prompt}\nNegative prompt: {negative_prompt}\nSteps: {steps}, Sampler: {sampler}, Schedule type: {scheduler}, CFG scale: {cfg}, Seed: {seed}, Size: {size}, Model hash: {model_hash}, Model: {model},{lora_hashes} Version: {version}"

      metadata = PngImagePlugin.PngInfo()
      metadata.add_text("parameters", new_metadata_string)

      image.save(file, pnginfo=metadata)
      print(f"{file.name} has been converted successfully!")
    else:
      print(f"{file.name} doesn't contain SwarmUI metadata, skipping...")

def main():
  image_dir = select_folder_dialog()

  if not Path("config.json").exists():
    config_defaults = {
      "LoraFolder": "",
      "CheckpointFolder": "",
      "Cache": True
    }

    with open("config.json", "w") as config_file:
      json.dump(config_defaults, config_file, indent=2)

  with open("config.json", encoding="utf-8") as config_file:
    config = json.load(config_file)

  change_image_metadata(image_dir, config)

main()