# eTriops   
## Virtual Pet project centered around raising a Triops.


**HOW TO RUN:**

For Windows:   
1. Follow the steps for "How to Build a New EXE", below.
2. Double-click on the resulting etriops.exe

For Linux (or anyone else wanting to run the native Python script):   
1. Make sure you have the following dependencies installed:
   - Python 3.7 or greater
   - Tkinter (might already be included in your Python install)
2. Navigate to the etriops directory and run:   
    `python etriops.py`


**HOW TO BUILD A NEW EXE:**
1. Make sure you have the necessary dependencies as described above
2. Make sure you have PyInstaller installed and that it's added to your system PATH.   
3. Navigate to the etriops directory and run:   
    `pyinstaller etriops.py -w --add-data "assets;assets" --icon="assets/favicon.ico"`
4. Inside the dist/ directory will be a directory named 'etriops', which contains the EXE along with all of its support files. It is recommended you copy this directory to a more convenient location.
5. The \_pycache\_/, build/, and empty dist/ directories, as well as etriops.spec, can be safely deleted once the EXE is built.
