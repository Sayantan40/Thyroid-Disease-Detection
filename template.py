import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO,format="[%(asctime)s]:%(message)s: ")

package_name = "Thyroid"

## List of files that we wish to create 
list_of_files = [
          
          "github/workflows/.gitkeep",                        ## .gitkeep is an place holder file

          f"src/{package_name}/__init__.py" ,                 ## this will help to understand its a package

          f"src/{package_name}/components/__init__.py",        ## src is a script folder

          f"src/{package_name}/utils/__init__.py",
          
          f"src/{package_name}/config/__init__.py",
          
          f"src/{package_name}/pipeline/__init__.py",
          
          f"src/{package_name}/entity/__init__.py",
          
          f"src/{package_name}/constants/__init__.py",
          
          f"src/{package_name}/logger/__init__.py",

          "tests/__init__.py",
          
          "tests/unit/__init__.py",
          
          "tests/integration/__init__.py",

          "configs/config.yaml",

          "dvc.yaml" ,                                         ## for data version control (dvc) pipeline

          "init_setup.sh" ,                                   ## A shell script file that will help to create the environment
          
          "requirements.txt",
          
          "requirements_dev.txt",                         ## this help to create development requirements
          
          "setup.py",

          "setup.cfg",

          "pyproject.toml",

          "tox.ini" ,                                   ## this is done for testing of project

          "research/trials.ipynb",

          "Dockerfile",

          "app.py",

          
          
          ]



for filepath in list_of_files:
    
    filepath = Path(filepath)
    
    file_dir , filename = os.path.split(filepath)

    if file_dir != "":
        
        os.makedirs(file_dir,exist_ok=True)
        
        logging.info(f"Creating directory : {file_dir} for file : {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0): ## this is to prevent overiding of files
        
        with open(filepath,"w") as f:
            pass                            ## create an empty file

        logging.info(f"Creating empty file : {filepath}")

    else:

        logging.info(f" {filename} already exists ")
