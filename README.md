# eTriops   
## Virtual Pet project centered around raising a Triops.


**HOW TO RUN:**

For Windows:   
1. Just open eTriops-Win.exe

For Linux (or anyone else wanting to run the native Python script):   
1. Make sure you have the following dependencies installed:
   - Python 3.7 or greater
   - Tkinter (might already be included in your Python install)
2. Navigate to the etriops directory and run:   
    `python etriops.py`


**HOW TO BUILD A NEW EXE:**
1. Make sure you have the necessary dependencies as described above
2. Make sure you have PyInstaller installed and that it's added to your system PATH.   
    - NOTE: It is HIGHLY recommended you build using PyInstaller v.3.3. Newer versions tend to generate false positives with many antiviruses!
3. Navigate to the etriops directory and run:   
    `pyinstaller etriops.py -w --onefile --add-data "assets;assets" --icon="assets/favicon.ico"`
4. The new EXE will be located in the dist/ directory. It is recommended you copy it to a more convenient location.
5. The \_pycache\_/, build/, and empty dist/ directories, as well as etriops.spec, can be safely deleted once the EXE is built.
