# Swarm-to-A1111-Metadata

Scripts for SwarmUI metadata conversion to A1111 metadata (mostly used for Civitai to automatically detect the resources). If you find a bug, you have some problem or you want to request a feature please open an Issue.

## Table of Content
- [Installation](#installation)
  - [Windows](#windows)
  - [Linux](#linux)
- [Usage](#usage)
- [Changelog](#changelog)

## Installation
### Windows
Before proceeding with the installation make sure you have python and git installed. If you don't i'll leave the download links here:
- Python 3.10.9 (Make sure to check "Add python.exe to the PATH" during the installation): https://www.python.org/downloads/release/python-3109/
- Git (Just click "Next" in all the installation process): https://git-scm.com/download/win

Open a cmd and run this commands one by one and in order:
```
git clone https://github.com/Jelosus2/swarm-to-a1111-metadata
cd swarm-to-a1111-metadata
setup.bat
```
**Note:** All the paths you input in the setup must be [absolute paths](https://www.computerhope.com/issues/ch001708.htm#windows)
You can setup everything again anytime running the same file.

After that let all install and fill the inputs, then you can run it by executing the file `run.bat`

### Linux
Before proceeding with the installation make sure you have python and git installed. If you don't i'll leave the commands here:
- Python 3.10 with venv: `sudo apt install python3.10-venv`
- Git: `sudo apt install git`

Open a terminal and run this commands one by one and in order:
```
git clone https://github.com/Jelosus2/swarm-to-a1111-metadata
cd swarm-to-a1111-metadata
./setup.sh
```
**Note:** All the paths you input in the setup must be [absolute paths](https://www.computerhope.com/issues/ch001708.htm#linux)
You can setup everything again anytime running the same file.

After that let all install and fill the inputs, then you can run it by executing the file `run.sh`

## Usage
Once all the setup is complete you can run the respective run file (`run.bat` for Windows and `run.sh` for Linux) and a file explorer dialog will open. Select the directory where you store the images you want to convert and let the script do it's magic.

## Changelog
- July 28, 2024:
  - Script uploaded.