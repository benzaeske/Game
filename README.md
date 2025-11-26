Working repository for a pixel art game a la "[Vampire Survivors](https://store.steampowered.com/app/1794680/Vampire_Survivors/)"

### Setup Instructions:
1. Make sure you have installed the latest version of Python: https://www.python.org/downloads/ 

2. Clone the repository and set up a python virtual environment (I develop using venv): `python -m venv venv`

3. Install the necessary dependencies from the requirements.txt in the project:
   - First you must activate the virtual envionment: `venv\Scripts\activate` (if using the command line from an IDE like Pycharm, it will automatically do this for you)
   - Install the requirements into your virtual environment: `pip install -r requirements.txt`
   - Pygame may require you to install certain sdl dependencies in order for it to work... I'm not exactly sure but when I tried setting this up on my mac it had issues. `pip install pygame` in your repository might also fix this.
  
4. The current state of the game can be run by launching main.py
